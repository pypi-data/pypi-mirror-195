"""
Author: "Keitaro Yamashita, Garib N. Murshudov"
MRC Laboratory of Molecular Biology

This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""
from __future__ import absolute_import, division, print_function, generators
import gemmi
import numpy
import json
import scipy.sparse
from servalcat.utils import logger
from servalcat.xtal.sigmaa import determine_mlf_params, determine_mlf_params_from_cc, mlf, calc_DFc
from servalcat import utils
b_to_u = utils.model.b_to_u
u_to_b = utils.model.u_to_b

class LL_Xtal:
    def __init__(self, hkldata, centric_and_selections, free, st, monlib, source="xray", mott_bethe=True, use_solvent=False):
        assert source in ("electron", "xray") # neutron?
        self.source = source
        self.mott_bethe = False if source != "electron" else mott_bethe
        self.hkldata = hkldata
        self.centric_and_selections = centric_and_selections
        self.free = free
        self.st = st
        self.monlib = monlib
        self.d_min = hkldata.d_min_max()[0]
        self.fc_labs = ["FC0"]
        self.use_solvent = use_solvent
        if use_solvent:
            self.fc_labs.append("FCbulk")
            self.hkldata.df["FCbulk"] = 0j
        self.D_labs = ["D{}".format(i) for i in range(len(self.fc_labs))]
        self.k_overall = numpy.ones(len(self.hkldata.df.index))
        self.hkldata.df["k_aniso"] = 1.
        self.hkldata.df["FP_org"] = self.hkldata.df["FP"]
        self.hkldata.df["SIGFP_org"] = self.hkldata.df["SIGFP"]

        self.use_in_est = "test" if "FREE" in hkldata.df else "all"
        self.use_in_target = "work" if "FREE" in hkldata.df else "all"
        logger.writeln("will use {} reflections for parameter estimation".format(self.use_in_est))
        logger.writeln("will use {} reflections for refinement".format(self.use_in_target))

    def update_ml_params(self):
        # FIXME make sure D > 0
        determine_mlf_params(self.hkldata, self.fc_labs, self.D_labs,
                             self.centric_and_selections, use=self.use_in_est)#, D_as_exp=True, S_as_exp=True)
        for lab in self.D_labs + ["S"]:
            self.hkldata.binned_df[lab].where(self.hkldata.binned_df[lab] > 0, 0.01, inplace=True)
            self.hkldata.binned_df[lab].where(self.hkldata.binned_df[lab] < numpy.inf, 1, inplace=True)
        #determine_mlf_params_from_cc(self.hkldata, self.fc_labs, self.D_labs,
        #                             self.centric_and_selections)


    def update_fc(self):
        if self.st.ncs:
            st = self.st.clone()
            st.expand_ncs(gemmi.HowToNameCopiedChain.Dup)
        else:
            st = self.st

        self.hkldata.df[self.fc_labs[0]] = utils.model.calc_fc_fft(st, self.d_min - 1e-6,
                                                                   monlib=self.monlib,
                                                                   source=self.source,
                                                                   mott_bethe=self.mott_bethe,
                                                                   miller_array=self.hkldata.miller_array())
        self.hkldata.df["FC"] = self.hkldata.df[self.fc_labs].sum(axis=1)
        
    def overall_scale(self, min_b=0.1):
        scaling = gemmi.Scaling(self.hkldata.cell, self.hkldata.sg)
        scaling.use_solvent = self.use_solvent
        scaleto = self.hkldata.as_asu_data(label="FP_org", label_sigma="SIGFP_org")
        scaleto.value_array["sigma"] = 1.
        fc_asu = self.hkldata.as_asu_data(self.fc_labs[0])
        if not self.use_solvent:
            logger.writeln("Scaling Fc with no bulk solvent contribution")
            scaling.prepare_points(fc_asu, scaleto)
        else:
            logger.writeln("Calculating solvent contribution..")
            grid = gemmi.FloatGrid()
            grid.setup_from(self.st, spacing=min(0.4, (self.d_min-1e-6)/2))
            masker = gemmi.SolventMasker(gemmi.AtomicRadiiSet.Cctbx)
            masker.put_mask_on_float_grid(grid, self.st[0])
            fmask_gr = gemmi.transform_map_to_f_phi(grid)
            self.hkldata.df[self.fc_labs[-1]] = fmask_gr.get_value_by_hkl(self.hkldata.miller_array())
            fmask_asu = self.hkldata.as_asu_data(self.fc_labs[-1])
            scaling.prepare_points(fc_asu, scaleto, fmask_asu)

        scaling.fit_isotropic_b_approximately()
        logger.writeln(" initial k,b = {:.2e} {:.2e}".format(scaling.k_overall, scaling.b_overall.u11))
        scaling.fit_parameters()
        b_aniso = scaling.b_overall
        b = b_aniso.trace() / 3
        b_aniso = b_aniso.added_kI(-b) # subtract isotropic contribution
        logger.writeln(" k_ov= {:.2e} B_iso= {:.2e} B_aniso= {}".format(scaling.k_overall, b, b_aniso))
        
        min_b_iso = utils.model.minimum_b(self.st[0]) # actually min of aniso too
        tmp = min_b_iso + b
        if tmp < min_b: # perhaps better only adjust b_iso that went too small, but we need to recalculate Fc
            logger.writeln(" Adjusting overall B to avoid too small value")
            b += min_b - tmp
        logger.writeln(" Applying overall B to model: {:.2f}".format(b))
        utils.model.shift_b(self.st[0], b)
        k_iso = self.hkldata.debye_waller_factors(b_iso=b)
        k_aniso = self.hkldata.debye_waller_factors(b_cart=b_aniso)
        self.hkldata.df["k_aniso"] = scaling.k_overall * k_aniso

        if self.use_solvent:
            logger.writeln(" k_sol= {:.2e} B_sol= {:.2e}".format(scaling.k_sol, scaling.b_sol))
            solvent_scale = scaling.get_solvent_scale(0.25 / self.hkldata.d_spacings()**2)
            self.hkldata.df[self.fc_labs[-1]] *= solvent_scale

        self.hkldata.df["FP"] = self.hkldata.df["FP_org"] / self.hkldata.df.k_aniso
        self.hkldata.df["SIGFP"] = self.hkldata.df["SIGFP_org"] /self.hkldata.df.k_aniso

        for lab in self.fc_labs: self.hkldata.df[lab] *= k_iso
        self.hkldata.df["FC"] = self.hkldata.df[self.fc_labs].sum(axis=1)
    # overall_scale()

    def calc_target(self): # -LL target for MLF
        ret = 0
        for i_bin, idxes in self.hkldata.binned():
            ret += mlf(self.hkldata.df,
                       self.fc_labs,
                       [self.hkldata.binned_df.loc[i_bin, lab] for lab in self.D_labs],
                       self.hkldata.binned_df.S[i_bin],
                       self.centric_and_selections[i_bin],
                       use=self.use_in_target)

        return ret * 2 # friedel mates
    # calc_target()

    def calc_stats(self):
        calc_r = lambda sel: utils.hkl.r_factor(self.hkldata.df.FP_org[sel],
                                                numpy.abs(self.hkldata.df.FC[sel] * self.hkldata.df.k_aniso[sel]))
        ret = {"summary": {"-LL": self.calc_target()}}
        if "FREE" in self.hkldata.df:
            test_sel = (self.hkldata.df.FREE == self.free).fillna(False)
            r_free = calc_r(test_sel)
            r_work = calc_r(~test_sel)
            logger.writeln("R_work = {:.4f} R_free = {:.4f}".format(r_work, r_free))
            ret["summary"]["Rfree"] = r_free
            ret["summary"]["Rwork"] = r_work
        else:
            r = utils.hkl.r_factor(self.hkldata.df.FP_org,
                                   numpy.abs(self.hkldata.df.FC * self.hkldata.df.k_aniso))
            logger.writeln("R = {:.4f}".format(r))
            ret["summary"]["R"] = r
        return ret

    def calc_grad(self, refine_xyz, adp_mode, refine_h, specs):
        dll_dab = numpy.zeros(len(self.hkldata.df.FC), dtype=numpy.complex128)
        d2ll_dab2 = numpy.empty(len(self.hkldata.df.index))
        d2ll_dab2[:] = numpy.nan
        blur = utils.model.determine_blur_for_dencalc(self.st, self.d_min / 3) # TODO need more work
        logger.writeln("blur for deriv= {:.2f}".format(blur))
        for i_bin, _ in self.hkldata.binned():
            idxes = numpy.concatenate([sel[1] for sel in self.centric_and_selections[i_bin]]) # w/o missing reflections
            bin_d_min = self.hkldata.binned_df.d_min[i_bin]
            bin_d_max = self.hkldata.binned_df.d_max[i_bin]
            Ds = [max(0., self.hkldata.binned_df[lab][i_bin]) for lab in self.D_labs] # negative D is replaced with zero here
            S = self.hkldata.binned_df.S[i_bin]
            for c, work, test in self.centric_and_selections[i_bin]:
                if self.use_in_target == "all":
                    cidxes = numpy.concatenate([work, test])
                else:
                    cidxes = work if self.use_in_target == "work" else test
                Fcs = [self.hkldata.df[lab].to_numpy()[cidxes] for lab in self.fc_labs]
                Fc = calc_DFc(Ds, Fcs) # sum(D * Fc)
                expip = numpy.exp(1j * numpy.angle(Fc))
                Fo = self.hkldata.df.FP.to_numpy()[cidxes]
                SigFo = self.hkldata.df.SIGFP.to_numpy()[cidxes]
                epsilon = self.hkldata.df.epsilon.to_numpy()[cidxes]
                Fc_abs = numpy.abs(Fc)

                if c == 0: # acentric
                    Sigma = 2 * SigFo**2 + epsilon * S
                    X = 2 * Fo * Fc_abs / Sigma
                    m = gemmi.bessel_i1_over_i0(X)
                    g = (2 * Fc_abs / Sigma - m * 2 * Fo / Sigma) * Ds[0]  # XXX assuming 0 is atomic structure
                    dll_dab[cidxes] = g * expip
                    d2ll_dab2[cidxes] = (2 / Sigma - (1 - m / X - m**2) * (2 * Fo / Sigma)**2) * Ds[0]**2
                else:
                    Sigma = SigFo**2 + epsilon * S
                    X = Fo * Fc_abs / Sigma
                    #X = X.astype(numpy.float64)
                    m = numpy.tanh(X)
                    g = (Fc_abs / Sigma - m * Fo / Sigma) * Ds[0]
                    dll_dab[cidxes] = g * expip
                    d2ll_dab2[cidxes] = (1 / Sigma - (Fo / (Sigma * numpy.cosh(X)))**2) * Ds[0]**2

        if self.mott_bethe:
            dll_dab *= self.hkldata.d_spacings()**2 * gemmi.mott_bethe_const()
            d2ll_dab2 *= gemmi.mott_bethe_const()**2

        # strangely, we need V for Hessian and V**2/n for gradient.
        d2ll_dab2 *= self.hkldata.cell.volume
        dll_dab_den = self.hkldata.fft_map(data=dll_dab * self.hkldata.debye_waller_factors(b_iso=-blur))
        dll_dab_den.array[:] *= self.hkldata.cell.volume**2 / dll_dab_den.point_count
        #asu = dll_dab_den.masked_asu()
        #dll_dab_den.array[:] *= 1 - asu.mask_array # 0 to use
        #atoms = [x.atom for x in self.st[0].all()]
        atoms = [None for _ in range(self.st[0].count_atom_sites())]
        for cra in self.st[0].all(): atoms[cra.atom.serial-1] = cra.atom
        
        # correction for special positions
        cs_count = len(self.hkldata.sg.operations())
        occ_backup = {}
        for atom, images, _ in specs:
            # use only crystallographic multiplicity just in case
            n_sym = len([x for x in images if x < cs_count]) + 1
            logger.writeln("spec_corr: images= {} {} n={}".format(images, len(images), n_sym))
            occ_backup[atom] = atom.occ
            atom.occ *= n_sym

        ll = gemmi.LLX(self.st.cell, self.hkldata.sg, atoms, self.mott_bethe, refine_xyz, adp_mode, refine_h)
        ll.set_ncs([x.tr for x in self.st.ncs if not x.given])
        vn = numpy.array(ll.calc_grad(dll_dab_den, blur))

        # second derivative
        d2dfw_table = gemmi.TableS3(*self.hkldata.d_min_max())
        valid_sel = numpy.isfinite(d2ll_dab2)
        d2dfw_table.make_table(1./self.hkldata.d_spacings().to_numpy()[valid_sel], d2ll_dab2[valid_sel])
        b_iso_all = [cra.atom.aniso.trace() / 3 * u_to_b if cra.atom.aniso.nonzero() else cra.atom.b_iso
                     for cra in self.st[0].all()]
        b_iso_min = min(b_iso_all)
        b_iso_max = max(b_iso_all)
        elems = set(cra.atom.element for cra in self.st[0].all())
        b_sf_min = 0 #min(min(e.it92.b) for e in elems) # because there is constants
        b_sf_max = max(max(e.it92.b) for e in elems)
        fisher_b_min = b_iso_min + b_sf_min
        fisher_b_max = 2 * (b_iso_max + b_sf_max)
        logger.writeln("preparing fast Fisher table for B= {:.2f} - {:.2f}".format(fisher_b_min, fisher_b_max))
        ll.make_fisher_table_diag_fast(fisher_b_min, fisher_b_max, d2dfw_table)
        #json.dump(dict(b=ll.table_bs, pp1=ll.pp1, bb=ll.bb),
        #          open("ll_fisher.json", "w"), indent=True)
        #a, (b,c) = ll.fisher_for_coo()
        #json.dump(([float(x) for x in a], ([int(x) for x in b], [int(x) for x in c])), open("fisher.json", "w"))
        coo = scipy.sparse.coo_matrix(ll.fisher_for_coo())
        lil = coo.tolil()
        rows, cols = lil.nonzero()
        lil[cols,rows] = lil[rows,cols]

        for atom in occ_backup:
            atom.occ = occ_backup[atom]
            
        return vn, lil
