#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

"""
Simple and stupid implementation of vhdl formater, no parser based on regular expressions
"""

indentIncr = ["^entity", "^port\s*\(", "^port\s*map\s*\(", "^generic\s*map\s*\(", "^generic\s*\(",
              "^architecture", "^if", "^case", "^port\s+map\s*\(", "^process", "^while", "^component",
              "\S+\s*:\s*process"]
indentDecr = ["^end", "^\)"]
indentPeak = ["^begin", "^elsif", "^else", "^when",]

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

    for l in vhdlString.split("\n"):
        l = l.strip()
        if any([x.match(l) for x in indentDecr]):
            indent -= 1
            lines.append(getIndent(indent) + l)
        elif any([x.match(l) for x in indentIncr]):
            lines.append(getIndent(indent) + l)
            indent += 1
        elif any([x.match(l) for x in indentPeak]):
            lines.append(getIndent(indent - 1) + l)
        else:
            lines.append(getIndent(indent) + l)
    return "\n".join(lines)
