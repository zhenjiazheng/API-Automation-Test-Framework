#!/usr/bin/env python

__author__ = 'zhengandy'
import sys, os


sys.path.extend(os.path.dirname(os.path.abspath(__file__)))
# print os.path.dirname(os.path.abspath(__file__))

from argparse import ArgumentParser

ap = ArgumentParser(
    #prog = __file__,
    description = 'xiaowang api unittest',
)

ap.add_argument('number', action="store",type=int, nargs='?', default=0)
ap.add_argument('case_folder', action="store",type=str, nargs='?', default="M0")
ap.add_argument('sleep_time', action="store",type=float, nargs='?', default=0)
args = ap.parse_args()


os.environ.setdefault('UT_ITEM', str(args.number-1))
os.environ.setdefault('CASE_FOLDER', args.case_folder)
os.environ.setdefault('SLEEP_TIME', str(args.sleep_time))

import testRunner
# import jsonRPCTest
testRunner.main()