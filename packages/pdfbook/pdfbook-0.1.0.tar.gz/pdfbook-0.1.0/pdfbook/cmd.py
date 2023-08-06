#!/usr/bin/env python
"""
pdfbook.cmd - rearrange pages in PDF file into signatures.
"""
#
# Copyright 2010-2023 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This file is part of pdfbook.
#
# pdfbook is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# pdfbook is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pdfbook. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later
()
__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2010-2023 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU Affero General Public License v3 or later (AGPLv3+)"

from . import main, __version__, DecryptionError
from .i18n import _

import PyPDF2.errors


def run():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__,
                        help=_("show program's version number and exit"))
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        dest='verbosity',
                        help=_("Be verbose. Indicates how the pages will be "
                               "rearranged. Can be used more than once to "
                               "increase verbosity."))
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help=_("Show what would have been done, "
                               "but do not generate files."))

    group = parser.add_argument_group('Define Target')
    group.add_argument('-s', '--signature', type=int, default=4,
                       help=_("Specify the size of the signature (number "
                              "of sides which will be folded and bound "
                              "together). Default: %(default)s"))
    parser.add_argument('infilename', metavar=_("InputFile"),
                        help=_("name of pdf file to convert"))
    parser.add_argument('outfilename', metavar=_("OutputFile"),
                        help=_("filename of bookified pdf document to write"))

    args = parser.parse_args()

    if args.signature % 4 != 0 or args.signature < 0:
        parser.error('-s/--signature <signature> must be positive and divisible by 4.')

    try:
        main(**vars(args))
    except (IOError, DecryptionError) as e:
        raise SystemExit(str(e))
    except PyPDF2.errors.PdfReadError as e:
        parser.error(_("The input-file is either corrupt or no PDF at all: %s")
                     % e)


if __name__ == '__main__':
    run()
