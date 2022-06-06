# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import re
import sys

import inkex
import pyembroidery

from ..i18n import _
from ..threads import ThreadCatalog
from .base import InkstitchExtension


class ApplyThreadlist(InkstitchExtension):
    '''
    Applies colors of a thread list to elements
    Count of colors and elements should fit together
    Use case: reapply colors to e.g. a dst file
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-f", "--filepath", type=str, default="", dest="filepath")
        self.arg_parser.add_argument("-m", "--method", type=int, default=1, dest="method")
        self.arg_parser.add_argument("-t", "--palette", type=str, default=None, dest="palette")

    def effect(self):
        # Remove selection, we want all the elements in the document
        self.svg.selection.clear()

        if not self.get_elements():
            return

        path = self.options.filepath
        if not os.path.exists(path):
            inkex.errormsg(_("File not found."))
            sys.exit(1)
        if os.path.isdir(path):
            inkex.errormsg(_("The filepath specified is not a file but a dictionary.\nPlease choose a threadlist file to import."))
            sys.exit(1)

        method = self.options.method
        if method == 1:
            colors = self.parse_inkstitch_threadlist(path)
        else:
            colors = self.parse_threadlist_by_catalog_number(path)

        if all(c is None for c in colors):
            inkex.errormsg(_("Couldn't find any matching colors in the file."))
            if method == 1:
                inkex.errormsg(_('Please try to import as "other threadlist" and specify a color palette below.'))
            else:
                inkex.errormsg(_("Please chose an other color palette for your design."))
            sys.exit(1)

        # Iterate through the color blocks to apply colors
        element_color = ""
        i = -1
        for element in self.elements:
            if element.color != element_color:
                element_color = element.color
                i += 1

            # No more colors in the list, stop here
            if i == len(colors):
                break

            style = element.node.get('style').replace("%s" % element_color, "%s" % colors[i])
            element.node.set('style', style)

    def parse_inkstitch_threadlist(self, path):
        colors = []
        if path.endswith('txt'):
            with open(path) as threadlist:
                for line in threadlist:
                    if line[0].isdigit():
                        m = re.search(r"\((#[0-9A-Fa-f]{6})\)", line)
                        if m:
                            colors.append(m.group(1))
                        else:
                            # Color not found
                            colors.append(None)
        else:
            threads = pyembroidery.read(path).threadlist
            for color in threads:
                colors.append(color.hex_color())
        return colors

    def parse_threadlist_by_catalog_number(self, path):
        palette_name = self.options.palette
        palette = ThreadCatalog().get_palette_by_name(palette_name)

        colors = []
        palette_numbers = []
        palette_colors = []

        for color in palette:
            palette_numbers.append(color.number)
            palette_colors.append('#%s' % color.hex_digits.lower())
        with open(path) as threadlist:
            for line in threadlist:
                if line[0].isdigit():
                    # some threadlists may add a # in front of the catalof number
                    # let's remove it from the entire string before splitting it up
                    thread = line.replace('#', '').split()
                    catalog_number = set(thread[1:]).intersection(palette_numbers)
                    if catalog_number:
                        color_index = palette_numbers.index(next(iter(catalog_number)))
                        colors.append(palette_colors[color_index])
                    else:
                        # No color found
                        colors.append(None)
        return colors

    def find_elements(self, xpath):
        svg = self.document.getroot()
        elements = svg.xpath(xpath, namespaces=inkex.NSS)
        return elements
