from dataclasses import dataclass
from typing import Optional

from .group import Group
from .text import Text
from .svg_element import INF_CON
from .alignment import HorizontalAlignment, VerticalAlignment


@dataclass
class TextLine:
    text: str
    fill: Optional[str] = None
    font_size: float = 16.0
    font_family: str = "arial"
    font_weight: str = 'normal'
    horizontal_alignment: str = HorizontalAlignment.CENTER


class MultiLineText(Group):
    def __init__(
        self,
        x,
        y,
        text_lines,
        line_gap_px=2,
        horizontal_alignment=HorizontalAlignment.CENTER,
        vertical_alignment=VerticalAlignment.CENTER,
    ) -> None:
        super().__init__()

        self.x = x
        self.y = y
        self.text_lines = text_lines
        self.line_gap_px = line_gap_px
        self.horizontal_alignment = horizontal_alignment
        self.vertical_alignment = vertical_alignment

    @property
    def bounds(self):
        self._layout(-INF_CON, INF_CON, -INF_CON, INF_CON)
        return super().bounds

    def _layout(self, x_con_min, x_con_max, y_con_min, y_con_max):
        height = 0
        self.children = []

        for line in self.text_lines:
            self.children.append(Text(
                self.x, self.y+height + line.font_size/2, line.text,
                horizontal_alignment=line.horizontal_alignment,
                vertical_alignment=VerticalAlignment.CENTER,
                font_family=line.font_family,
                font_size=line.font_size,
                font_weight=line.font_weight,
                fill=line.fill,
            ))
            height += line.font_size + self.line_gap_px

        height -= self.line_gap_px

        bounds = super()._layout(x_con_min, x_con_max, y_con_min, y_con_max)

        max_width = max(map(lambda x: x.width, self.children))

        for line in self.children:
            if line.horizontal_alignment == HorizontalAlignment.LEFT:
                line.x = line.x - max_width / 2.0
            elif line.horizontal_alignment == HorizontalAlignment.RIGHT:
                line.x = line.x + max_width / 2.0

            if self.horizontal_alignment == HorizontalAlignment.LEFT:
                line.x = line.x + max_width / 2.0
            elif self.horizontal_alignment == HorizontalAlignment.RIGHT:
                line.x = line.x - max_width / 2.0

            if self.vertical_alignment == VerticalAlignment.CENTER:
                line.y -= height / 2.0
            elif self.vertical_alignment == VerticalAlignment.BOTTOM:
                line.y -= height

        return bounds

    @classmethod
    def from_text(
        cls,
        x,
        y,
        text,
        line_gap_px=2,
        font_size=TextLine.font_size,
        font_family=TextLine.font_family,
        font_weight=TextLine.font_weight,
        text_horizontal_alignment=TextLine.horizontal_alignment,
        horizontal_alignment=HorizontalAlignment.CENTER,
        vertical_alignment=VerticalAlignment.CENTER,
        fill=None,
    ):
        lines = list(map(lambda x: TextLine(
            text=x,
            fill=fill,
            font_size=font_size,
            font_family=font_family,
            font_weight=font_weight,
            horizontal_alignment=text_horizontal_alignment,
        ), text.split('\n')))
        return MultiLineText(
            x=x,
            y=y,
            text_lines=lines,
            line_gap_px=line_gap_px,
            horizontal_alignment=horizontal_alignment,
            vertical_alignment=vertical_alignment,
        )
