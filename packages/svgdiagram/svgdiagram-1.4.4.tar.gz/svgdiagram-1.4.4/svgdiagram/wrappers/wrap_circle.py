import math

from svgdiagram.elements.group import Group
from svgdiagram.elements.circle import Circle
from svgdiagram.elements.svg_element import INF_CON


class WrapCircle(Group):
    def __init__(self, child, padding_px=10,
                 stroke="black", stroke_width_px=1,
                 fill="white",) -> None:
        super().__init__()
        self.child = child
        self.padding_px = padding_px
        self.stroke = stroke
        self.stroke_width_px = stroke_width_px
        self.fill = fill

    @property
    def bounds(self):
        self._layout(x_con_min=-INF_CON, x_con_max=INF_CON,
                     y_con_min=-INF_CON, y_con_max=INF_CON)
        return super().bounds

    def _layout(self,
                x_con_min=-INF_CON, x_con_max=INF_CON,
                y_con_min=-INF_CON, y_con_max=INF_CON):
        c_xmin, c_xmax, c_ymin, c_ymax = self.child.bounds

        self.children = []

        center_x = (c_xmin + c_xmax) / 2.0
        center_y = (c_ymin + c_ymax) / 2.0
        width = c_xmax - c_xmin
        height = c_ymax - c_ymin

        radius = math.sqrt(width**2 + height**2) / 2.0 + self.padding_px

        self.append_child(Circle(
            center_x,
            center_y,
            radius,
            stroke=self.stroke,
            stroke_width_px=self.stroke_width_px,
            fill=self.fill,
        ))

        self.append_child(self.child)

        return super()._layout(x_con_min, x_con_max, y_con_min, y_con_max)
