#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from vhdl_toolkit.hierarchyExtractor import DesignFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check syntax of vhdl files.')
    parser.add_argument('files', metavar='FILE', nargs='+', help='files to add copy in ipcore')
    parser.add_argument('--parallel', default=True, help='process in parallel')
    args = parser.parse_args()
    dfs = DesignFile.loadFiles(args.files, parallel=args.parallel)
