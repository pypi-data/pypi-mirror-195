from svgdiagram.elements.group import Group
from svgdiagram.elements.text import Text
from svgdiagram.elements.path import Path

from svgdiagram.derived_elements.milestone import Milestone as UIMilestone
from svgdiagram.derived_elements.task import Task as UITask

from svgdiagram.shapes.diamond_shape import DiamondShape
from svgdiagram.elements.multi_line_text import MultiLineText
from svgdiagram.elements.alignment import HorizontalAlignment


def render_swimlane(y_offset, swimlane, xmin, xmax, date_to_column_x_pos):
    group = Group()
    id_shape_map = {}

    milestone_size = 30.0
    swimlane_y = y_offset+milestone_size+10

    # draw line
    group.append_child(
        Text(
            xmin-8, swimlane_y,
            swimlane.name,
            horizontal_alignment=HorizontalAlignment.RIGHT,
        )
    )

    group.append_child(Path(
        points=[(xmin, swimlane_y), (xmax, swimlane_y)]
    ))

    # render tasks
    for task in swimlane.tasks:
        group.append_child(UITask(
            x_start=date_to_column_x_pos(task.start_date),
            x_end=date_to_column_x_pos(task.end_date),
            y=swimlane_y,
            height=20,
            radius=5,
            text=task.name,
            progess=task.progress,
        ))

    # render milestones
    for milestone in swimlane.milestones:
        milestone_x = date_to_column_x_pos(milestone.due_date)
        milestone_element = UIMilestone(
            milestone_x,
            swimlane_y,
        )
        if milestone.id:
            id_shape_map[milestone.id] = DiamondShape(
                milestone_element)

        group.append_child(
            milestone_element
        )
        group.append_child(
            MultiLineText.from_text(
                milestone_x,
                swimlane_y+25,
                milestone.name,
                font_size=10,
            )
        )

    return swimlane_y+40, group, id_shape_map
