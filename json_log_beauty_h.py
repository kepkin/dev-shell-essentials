#!/usr/bin/env python

__author__ = 'Alexander.Nevskiy'

import argparse
import json
import sys

# todo: write unit test
# data = {}
# data['a'] = {}
# data['a']['b'] = 3
# data['a']['c'] = 45
# data['a']['d'] = 4
#
# r = {}
# set_value("a.b", data, r)
# set_value("a.c", data, r)
# print(r)

def set_value(k, data, result):
    keys = k.split(".")

    a = result
    d = data
    for nk in keys[:-1]:
        if nk not in a:
            a[nk] = {}
        a = a[nk]
        d = data[nk]

    a[keys[-1]] = d[keys[-1]]


def main(cmd):
    infile = sys.stdin
    outfile = sys.stdout
    indent = 4
    if cmd.collapse:
        indent = None

    for l in infile.readlines():
        try:
            obj = json.loads(l)
            if cmd.show is not None:
                obj2 = {}
                for k in cmd.show:
                    set_value(k, obj, obj2)
                obj = obj2
            json.dump(obj, outfile, sort_keys=True, indent=indent)
            print('')
        except ValueError as e:
            print("Failed decode json for: {}\n error: {}".format(l, e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--show', required=False, type=str, nargs='+',
                        help='What fields to show. You can use complex keys like Object.SubObject.field')
    parser.add_argument('-c', '--collapse', action='store_true', required=False, default=False,
                        help='Useful when you don\'t want to prettify but get subset of json with --show')

    cmd = parser.parse_args()
    main(cmd)
