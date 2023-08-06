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
import os
import shutil
import argparse
from servalcat.utils import logger
from servalcat import utils
from servalcat.xtal.sigmaa import process_input, calculate_maps
from servalcat.refine.xtal import LL_Xtal
from servalcat.refine.refine import Geom, Refine
b_to_u = utils.model.b_to_u

def add_arguments(parser):
    parser.description = "EXPERIMENTAL program to refine crystallographic structures"
    parser.add_argument("--hklin", required=True)
    parser.add_argument("-d", '--d_min', type=float)
    parser.add_argument('--nbins', type=int, default=20,
                        help="Number of bins (default: %(default)d)")
    parser.add_argument("--labin", nargs="+", help="F SIGF FREE input")
    parser.add_argument('--free', type=int, default=0,
                        help='flag number for test set')
    parser.add_argument('--model', required=True,
                        help='Input atomic model file')
    parser.add_argument("--monlib",
                        help="Monomer library path. Default: $CLIBD_MON")
    parser.add_argument('--ligand', nargs="*", action="append",
                        help="restraint dictionary cif file(s)")
    parser.add_argument('--hydrogen', default="all", choices=["all", "yes", "no"],
                        help="all: add riding hydrogen atoms, yes: use hydrogen atoms if present, no: remove hydrogen atoms in input. "
                        "Default: %(default)s")
    parser.add_argument('--jellybody', action='store_true',
                        help="Use jelly body restraints")
    parser.add_argument('--jellybody_params', nargs=2, type=float,
                        metavar=("sigma", "dmax"), default=[0.01, 4.2],
                        help="Jelly body sigma and dmax (default: %(default)s)")
    parser.add_argument('--keywords', nargs='+', action="append",
                        help="refmac keyword(s)")
    parser.add_argument('--keyword_file', nargs='+', action="append",
                        help="refmac keyword file(s)")
    parser.add_argument('--randomize', type=float, default=0,
                        help='Shake coordinates with specified rmsd')
    parser.add_argument('--ncycle', type=int, default=10,
                        help="number of CG cycles (default: %(default)d)")
    parser.add_argument('--weight', type=float, default=1,
                        help="refinement weight")
    parser.add_argument('--sigma_b', type=float, default=30,
                        help="refinement ADP sigma in B (default: %(default)f)")
    parser.add_argument('--bfactor', type=float,
                        help="reset all atomic B values to specified value")
    parser.add_argument('--fix_xyz', action="store_true")
    parser.add_argument('--adp',  choices=["fix", "iso", "aniso"], default="iso")
    parser.add_argument('--max_dist_for_adp_restraint', type=float, default=4.)
    parser.add_argument('--unrestrained',  action='store_true', help="No positional restraints")
    parser.add_argument('--refine_h', action="store_true", help="Refine hydrogen (default: restraints only)")
    parser.add_argument("--source", choices=["electron", "xray", "neutron"], default="electron")
    parser.add_argument('--no_solvent',  action='store_true',
                        help="Do not consider bulk solvent contribution")
    parser.add_argument('-o','--output_prefix')
# add_arguments()

def parse_args(arg_list):
    parser = argparse.ArgumentParser()
    add_arguments(parser)
    return parser.parse_args(arg_list)
# parse_args()

def main(args):
    if not args.output_prefix:
        args.output_prefix = utils.fileio.splitext(os.path.basename(args.model))[0] + "_refined"

    keywords = []
    if args.keywords or args.keyword_file:
        if args.keywords: keywords = sum(args.keywords, [])
        if args.keyword_file: keywords.extend(l for f in sum(args.keyword_file, []) for l in open(f))

    hkldata, sts, fc_labs, centric_and_selections = process_input(hklin=args.hklin,
                                                                  labin=args.labin,
                                                                  n_bins=args.nbins,
                                                                  free=args.free,
                                                                  xyzins=[args.model],
                                                                  source=args.source,
                                                                  d_min=args.d_min)
    st = sts[0]
    monlib = utils.restraints.load_monomer_library(st, monomer_dir=args.monlib, cif_files=args.ligand,
                                                   stop_for_unknowns=False)
    h_change = {"all":gemmi.HydrogenChange.ReAddButWater,
                "yes":gemmi.HydrogenChange.NoChange,
                "no":gemmi.HydrogenChange.Remove}[args.hydrogen]
    try:
        topo = utils.restraints.prepare_topology(st, monlib, h_change=h_change,
                                                 check_hydrogen=(args.hydrogen=="yes"))
    except RuntimeError as e:
        raise SystemExit("Error: {}".format(e))

    # initialize ADP
    if args.adp != "fix":
        utils.model.reset_adp(st[0], args.bfactor, args.adp == "aniso")
    
    geom = Geom(st, topo, monlib, shake_rms=args.randomize, sigma_b=args.sigma_b, refmac_keywords=keywords)
    geom.geom.adpr_max_dist = args.max_dist_for_adp_restraint
    if args.jellybody:
        geom.geom.ridge_sigma, geom.geom.ridge_dmax = args.jellybody_params

    ll = LL_Xtal(hkldata, centric_and_selections, args.free, st, monlib, source=args.source, use_solvent=not args.no_solvent)
    refiner = Refine(st, geom, ll=ll,
                     refine_xyz=not args.fix_xyz,
                     adp_mode=dict(fix=0, iso=1, aniso=2)[args.adp],
                     refine_h=args.refine_h,
                     unrestrained=args.unrestrained)

    refiner.run_cycles(args.ncycle, weight=args.weight)
    utils.fileio.write_model(refiner.st, args.output_prefix, pdb=True, cif=True)

    calculate_maps(ll.hkldata, centric_and_selections, ll.fc_labs, ll.D_labs, args.output_prefix + "_stats.log")

    # Write mtz file
    labs = ["FP", "SIGFP", "FOM", "FWT", "DELFWT", "FC"]
    if not args.no_solvent:
        labs.append("FCbulk")
    mtz_out = args.output_prefix+".mtz"
    hkldata.write_mtz(mtz_out, labs=labs, types={"FOM": "W", "FP":"F", "SIGFP":"Q"})
    logger.writeln("output mtz: {}".format(mtz_out))

# main()

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    main(args)
