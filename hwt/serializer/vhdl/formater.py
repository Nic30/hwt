#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple and stupid implementation of vhdl formater, no parser based
on regular expressions
"""

import re


indentIncr = ["^entity", "^port\s*\(",
              "^port\s*map\s*\(", "^generic\s*map\s*\(", "^generic\s*\(",
              "^architecture", "^if", "^case", "^port\s+map\s*\(", "^process",
              "^while", "^component",
              "\S+\s*:\s*process"]
indentDecr = ["^end[^\w\d_]", "^\)"]
indentPeak = ["^begin", "^elsif", "^else", "^when"]

indentIncr = list(map(lambda x: re.compile(x, re.IGNORECASE), indentIncr))
indentDecr = list(map(lambda x: re.compile(x, re.IGNORECASE), indentDecr))
indentPeak = list(map(lambda x: re.compile(x, re.IGNORECASE), indentPeak))


def get_indent(i):
    return "".join([" " for _ in range(i)])


def formatVhdl(vhdlString):
    indent = 0
    lines = []

    def getIndent(i):
        return get_indent(i * 4)

    for line in vhdlString.split("\n"):
        line = line.strip()
        if any([x.match(line) for x in indentDecr]):
            indent -= 1
            lines.append(getIndent(indent) + line)
        elif any([x.match(line) for x in indentIncr]):
            lines.append(getIndent(indent) + line)
            indent += 1
        elif any([x.match(line) for x in indentPeak]):
            lines.append(getIndent(indent - 1) + line)
        else:
            lines.append(getIndent(indent) + line)
    return "\n".join(lines)
