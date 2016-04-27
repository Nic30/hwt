#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from hdl_toolkit.hierarchyExtractor import DesignFile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check syntax of vhdl files.')
    parser.add_argument('files', metavar='FILE', nargs='+', help='files to add copy in ipcore')
    parser.add_argument('--parallel', default=True, help='process in parallel')
    args = parser.parse_args()
    dfs = DesignFile.loadFiles(args.files, parallel=args.parallel)
    for df in dfs:
        for e in df.hdlCtx.entities:
            print("%s (%s)" % (e, df.fileName))
