from svgdiagram.elements.group import Group
from svgdiagram.elements.rect import Rect
from svgdiagram.elements.svg_element import INF_CON


class WrapRect(Group):
    def __init__(self, child, padding_px=10,
                 rx=None, ry=None,
                 stroke="black", stroke_width_px=1,
                 fill="white",) -> None:
        super().__init__()
        self.child = child
        self.padding_px = padding_px
        self.rx = rx
        self.ry = ry
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

        self.append_child(Rect(
            c_xmin-self.padding_px,
            c_ymin-self.padding_px,
            c_xmax-c_xmin+2*self.padding_px,
            c_ymax-c_ymin+2*self.padding_px,
            rx=self.rx,
            ry=self.ry,
            stroke=self.stroke,
            stroke_width_px=self.stroke_width_px,
            fill=self.fill,
        ))

        self.append_child(self.child)

        return super()._layout(x_con_min, x_con_max, y_con_min, y_con_max)
