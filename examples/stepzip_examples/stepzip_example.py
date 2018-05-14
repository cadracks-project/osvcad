# coding=utf-8

r"""Example use for the stepzip module"""

from __future__ import print_function

import shutil
from osvcad.cadzip import create_cadzip, extract_cadzip
from osvcad.nodes import Part

from osvcad.view import view_part

create_cadzip("models/spacer.stp", "models/spacer.anchors")

shutil.copy("models/spacer.zip", "models/spacer_copy.zip")

s, a = extract_cadzip("models/spacer_copy.zip")

n = Part.from_stepzip("models/spacer.zip")

print(s)
print(a)
print(n)

view_part(n)
