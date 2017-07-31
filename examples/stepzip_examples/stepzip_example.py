# coding=utf-8

r"""Example use for the stepzip module"""

from __future__ import print_function

import shutil
from osvcad.stepzip import create_stepzip, extract_stepzip
from osvcad.nodes import GeometryNode

create_stepzip("models/spacer.stp", "models/spacer.anchors")

shutil.copy("models/spacer.zip", "models/spacer_copy.zip")

s, a = extract_stepzip("models/spacer_copy.zip")

n = GeometryNode.from_stepzip("models/spacer.zip")

print(s)
print(a)
print(n)
