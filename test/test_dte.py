#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 by Jiuguang Wang (www.robo.guru)
# All rights reserved.
# This file is part of DTE Calculator and is released under the  MIT License.
# Please see the LICENSE file that should have been included as part of
# this package.

import os
import sys
import dte


def test_dte():
    # Plot
    dte.dte_calculator('data/dte.csv')

    # Get the file size of the output PDF
    file_size = os.path.getsize('DTE.pdf')

    # Check the size is greater than 40 KB
    assert file_size > 20 * 1024, "Test failed"
