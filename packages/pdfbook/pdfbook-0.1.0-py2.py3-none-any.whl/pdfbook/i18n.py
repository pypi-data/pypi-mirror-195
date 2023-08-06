# -*- coding: utf-8 -*-
#
# Copyright 2022-2023 by Hartmut Goebel <h.goebel@crazy-compilers.com>
#
# This file is part of pdfdecrypt.
#
# pdfdecrypt is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# pdfdecrypt is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public
# License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with pdfdecrypt. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

__all__ = ["_"]

import gettext
import os
import sys

_domain = 'pdfbook'
if getattr(sys, 'frozen', None):
    localedir = os.path.join(sys._MEIPASS, 'locale')
else:
    localedir = os.path.join(os.path.dirname(__file__), 'locale')
translate = gettext.translation(_domain,
                                localedir, fallback=True)
_ = translate.gettext

# required to make translations work in argparse
gettext.textdomain(_domain)
gettext.bindtextdomain(_domain, localedir)
