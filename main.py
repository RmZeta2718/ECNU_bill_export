#!/usr/bin/env python
from get_bill import GetYearBill
from convert import ParseConfig, Convert
from export import Export

from objprint import op
import argparse

op.config(color=True, line_number=True, arg_name=True)
op.install()

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--out-path', default='out/dump.csv', type=str, help='output path')
parser.add_argument('-y', '--year', type=int, help='year of exported bill', required=True)
parser.add_argument('--config', default='config.yaml', type=str, help='path to your config.yaml')
args = parser.parse_args()

data = GetYearBill(args.year)
meta = ParseConfig(args.config)
data, notfound = Convert(data, meta)
if len(notfound):
    print('Warning: shops not found in config')
    print(notfound)
Export(data, args.out_path)
