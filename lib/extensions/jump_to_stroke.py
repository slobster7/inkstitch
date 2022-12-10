# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import DirectedLineSegment, errormsg, PathElement

from ..i18n import _
from ..svg import PIXELS_PER_MM, get_correction_transform
from .base import InkstitchExtension


class JumpToStroke(InkstitchExtension):
    """Convert a satin column into a running stitch."""

    def effect(self):
        if not self.svg.selection or not self.get_elements() or len(self.elements) < 2:
            errormsg(_("Please select at least two elements to convert the jump stitch to a running stitch."))
            return

        last_stitch_group = None
        for element in self.elements:
            stitch_group = element.to_stitch_groups(last_stitch_group)
            end = stitch_group[-1].stitches[-1]
            if last_stitch_group is not None:
                start = last_stitch_group.stitches[-1]
                self.generate_stroke(element, start, end)

            last_stitch_group = stitch_group[-1]

    def generate_stroke(self, element, start, end):
        node = element.node
        parent = node.getparent()
        index = parent.index(node)

        # do not add a running stitch if the distance is smaller than the collapse setting
        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm'] or 3.0
        collapse_len *= PIXELS_PER_MM
        line = DirectedLineSegment((start.x, start.y), (end.x, end.y))
        if collapse_len > line.length:
            return

        path = f'M {start.x}, {start.y} L {end.x}, {end.y}'
        color = element.color
        style = f'stroke:{color};stroke-width:1px;stroke-dasharray:3, 1;fill:none;'

        line = PathElement(d=path, style=style, transform=get_correction_transform(node))
        parent.insert(index, line)


if __name__ == '__main__':
    JumpToStroke().run()
