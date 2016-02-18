#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource
from vivado_toolkit.ip_packager.packager import Packager
from vhdl_toolkit.hierarchyExtractor import DesignFile, findFileWhereNameIsDefined


class TopUnitTemplate(UnitWithSource):  # name and entity name does not have to be same
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Package vhld files as ipcore, and create gui.')
    parser.add_argument('files', metavar='FILE', nargs='+', help='files to add copy in ipcore')
    parser.add_argument('--top', required=True, help='name of top entity')
    parser.add_argument('--repo', help='directory where ipcore will be stored')
    parser.add_argument('--parallel', default=True, help='process in parallel')
    args = parser.parse_args()

    dfs = DesignFile.loadFiles(args.files, parallel=args.parallel)
    mainDf = findFileWhereNameIsDefined(dfs, args.top)  # [TODO] construct dependencies from top entity
    
    assert('.' not in args.top)
    TopUnitTemplate.__name__ = args.top
    TopUnitTemplate._origin = mainDf.fileName
    u = TopUnitTemplate()  # there are properties on this instance representing real interfaces and generics

    p = Packager(u, extraVhdlFiles=args.files)  # packager is class used for packing ipcores
    p.createPackage(args.repo)  # you can modify anything before this step, every path is relative in this ipcore
    print(u.__class__.__name__ + ' packaged')
