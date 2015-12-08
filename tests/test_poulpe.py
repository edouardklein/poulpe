#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_poulpe
----------------------------------

Tests for `poulpe` module.
"""

import unittest

from poulpe import poulpe


class TestPoulpe(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

# One day I'll do real tests :
# cd ..; rm -rf test; mkdir test; cd test; poulpe init; cp /Volumes/KINGSTON/edouard/src/poulpe/tests/artefacts.txt ./ ;touch .gitignore; git add .gitignore ; git commit -m "Initial commit" ; git add artefacts.txt ; git commit -m "first file"


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
