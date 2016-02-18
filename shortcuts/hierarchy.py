#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from vhdl_toolkit.hierarchyExtractor import DesignFile, findFileWhereNameIsDefined 
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate dictionary of dependencies between files.')
    parser.add_argument('files', metavar='N', nargs='+', help='files to parse')
    parser.add_argument('--top', required=True, help='name of top entity')
    parser.add_argument('--parallel', default=True, help='process in parallel')
    args = parser.parse_args()
    dfs = DesignFile.loadFiles(args.files, parallel=args.parallel)
    depDict = DesignFile.fileDependencyDict(designFiles=dfs)
    mainDf = findFileWhereNameIsDefined(dfs, args.top)  # [TODO] construct dependencies from top entity
    print(depDict)
    
    
