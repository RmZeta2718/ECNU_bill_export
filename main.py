#!/usr/bin/env python
import argparse

from objprint import op

from convert import Convert, ParseConfig
from export import Export
from get_bill import GetYearBill

op.config(color=True, line_number=True, arg_name=True)
op.install()

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--out-path", default="out/dump.csv", type=str, help="output path")
parser.add_argument("-y", "--year", type=int, help="year of exported bill", required=True)
parser.add_argument("-s", "--month_start", type=int, help="start month of exported bill", default=1)
parser.add_argument("-e", "--month_end", type=int, help="end month of exported bill", default=12)
parser.add_argument("--config", default="config.yaml", type=str, help="path to your config.yaml")
args = parser.parse_args()

data = GetYearBill(args.year, args.month_start, args.month_end)
meta = ParseConfig(args.config)
data, notfound = Convert(data, meta)
if len(notfound):
    print("Warning: shops not found in config")
    print(notfound)
Export(data, args.out_path)
