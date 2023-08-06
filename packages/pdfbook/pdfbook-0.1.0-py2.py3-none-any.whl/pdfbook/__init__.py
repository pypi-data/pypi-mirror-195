#!/usr/bin/env python
"""
pdfbook - rearrange pages in PDF file into signatures.
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

__author__ = "Hartmut Goebel <h.goebel@crazy-compilers.com>"
__copyright__ = "Copyright 2010-2023 by Hartmut Goebel <h.goebel@crazy-compilers.com>"
__licence__ = "GNU Affero General Public License v3 or later (AGPLv3+)"
__version__ = "0.1.0"

from PyPDF2 import PdfFileWriter, PdfFileReader, PageObject
from PyPDF2.types import NameObject
from PyPDF2.generic import RectangleObject, NullObject, DictionaryObject

import logging
from logging import log
from .i18n import _


class DecryptionError(ValueError):
    pass


PAGE_BOXES = ("/MediaBox", "/CropBox")


class _EmptyPage(PageObject):

    def __init__(self, pdf):
        PageObject.__init__(self, pdf)
        self.__setitem__(NameObject('/Type'), NameObject('/Page'))
        self.__setitem__(NameObject('/Parent'), NullObject())
        self.__setitem__(NameObject('/Resources'), DictionaryObject())
        firstpage = pdf.getPage(0)
        for attr in PAGE_BOXES:
            if attr in firstpage:
                self[NameObject(attr)] = RectangleObject(list(firstpage[attr]))


def bookify(inpdf, outpdf, signature):

    def sort_pages(numPages, signature):
        maxPage = numPages + (signature - numPages % signature) % signature
        for currentpg in range(maxPage):
            actualpg = currentpg - (currentpg % signature)
            if currentpg % 4 in (0, 3):
                actualpg += signature - 1 - (currentpg % signature) // 2
            else:
                actualpg += (currentpg % signature) // 2
            if actualpg >= numPages:
                yield '*', emptyPage
            else:
                yield actualpg + 1, inpdf.getPage(actualpg)

    emptyPage = _EmptyPage(inpdf)
    pagelist = []
    for num, page in sort_pages(inpdf.numPages, signature):
        pagelist.append(num)
        outpdf.addPage(page)
    log(19, ' '.join('[%s]' % p for p in pagelist))


def password_hook():
    import getpass
    return getpass.getpass()


def main(infilename, outfilename, signature=4,
         verbosity=0, dry_run=False, password_hook=password_hook):
    logging.basicConfig(level=20 - verbosity, format="%(message)s")
    outpdf = PdfFileWriter()
    inpdf = PdfFileReader(open(infilename, 'rb'))

    if inpdf.isEncrypted:
        log(16, 'File is encrypted')
        # try empty password first
        if not inpdf.decrypt(''):
            if not inpdf.decrypt(password_hook()):
                raise DecryptionError(_("Can't decrypt PDF. Wrong Password?"))

    log(17, 'Signature: %s', signature)
    log(18, 'Number of input pages: %s', inpdf.numPages)

    bookify(inpdf, outpdf, signature)
    if not dry_run:
        outpdf.write(open(outfilename, 'wb'))
