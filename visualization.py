import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.transforms import Bbox
import matplotlib.patches as patches
from alignment import Move, Alignment, DefinedModelMove, SynchronousMove, LogMove
from typing import List, Set, Dict, Tuple, Optional
import re
from functools import reduce

MOVE_WIDTH = 6
ACTIVITY_HIGHT = 2
OBJECT_HEIGHT = 1
BUFFER_HEIGHT = 0.5
BUFFER_WIDTH = 0.5
SPACE_BETWEEN_COLUMNS = 1
TEXT_BUFFER_TOP = 0.1
TEXT_BUFFER_LEFT = 0.3
TEXT_BUFFER_RIGHT = 0.1

SYNC_COLOR = "green"
MODEL_MOVE_COLOR = "orange"
LOG_MOVE_COLOR = "red"
DEFAULT_COLOR = "gray"


def use_fontsize_that_fits(text, width, height, fig=None, ax=None):
    '''Automatically decrease the fontsize until it fits the width and height. The axis need to be set already.

    Args:
        text (matplotlib.text.Text)
        width (float): allowed width in data coordinates
        height (float): allowed height in data coordinates
    '''
    fig = fig or plt.gcf()
    ax = ax or plt.gca()

    # bounding box of text in figure coordinates and transform to data coordinates
    ren = fig.canvas.get_renderer()
    bbox_text = text.get_window_extent(renderer=ren)
    bbox_text = Bbox(ax.transData.inverted().transform(bbox_text))

    # check if already in box
    fits_width = bbox_text.width < width if width else True
    fits_height = bbox_text.height < height if height else True
    # if it does not fit decrease further
    if not all((fits_width, fits_height)):
        if text.get_fontsize() > 1:
            text.set_fontsize(text.get_fontsize()-1)
            use_fontsize_that_fits(text, width, height, fig, ax)


def draw_line(start, end, fig, ax):
    verts = [start, end]

    codes = [Path.MOVETO, Path.LINETO]

    path = Path(verts, codes)
    patch = patches.PathPatch(path, lw=2)
    ax.add_patch(patch)


def draw_move(move: Move, start_x: int, start_y: int, color: str, abbreviations: Dict[str, str], fig, ax, renderer) \
        -> Tuple[int, Dict[Move, Tuple[int, int]], Dict[Move, Tuple[int, int]]]:
    '''
    Visualizes a Move to a given mathplootlib plot.
    :param move: Move that should be visualized.
    :param start_x: Xcoordinate of upper left corner of the box that will represent the move.
    :param start_y: Y coordinate of upper left corner of the box that will represent the move.
    :return: Width this column used.
    '''

    # draw log activity box
    log_act_verts = [
        (start_x, start_y),  # left, top
        (start_x + MOVE_WIDTH, start_y),  # right, top
        (start_x + MOVE_WIDTH, start_y - ACTIVITY_HIGHT),  # right, top
        (start_x, start_y - ACTIVITY_HIGHT),  # left, bottom
        (start_x, start_y),  # left, top
    ]

    log_act_codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
    ]

    log_activity_box_path = Path(log_act_verts, log_act_codes)
    log_activity_box_patch = patches.PathPatch(log_activity_box_path, facecolor=color, lw=2)
    ax.add_patch(log_activity_box_patch)

    # draw log object box
    log_ob_y = start_y - ACTIVITY_HIGHT

    log_obj_verts = [
        (start_x, log_ob_y),  # left, top
        (start_x + MOVE_WIDTH, log_ob_y),  # right, top
        (start_x + MOVE_WIDTH, log_ob_y - OBJECT_HEIGHT),  # right, top
        (start_x, log_ob_y - OBJECT_HEIGHT),  # left, bottom
        (start_x, log_ob_y),  # left, top
    ]

    log_obj_codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
    ]

    log_obj_box_path = Path(log_obj_verts, log_obj_codes)
    log_obj_box_patch = patches.PathPatch(log_obj_box_path, facecolor=color, lw=2)
    ax.add_patch(log_obj_box_patch)

    # draw model activity box
    model_start_y = start_y - ACTIVITY_HIGHT - OBJECT_HEIGHT
    model_act_verts = [
        (start_x, model_start_y),  # left, top
        (start_x + MOVE_WIDTH, model_start_y),  # right, top
        (start_x + MOVE_WIDTH, model_start_y - ACTIVITY_HIGHT),  # right, top
        (start_x, model_start_y - ACTIVITY_HIGHT),  # left, bottom
        (start_x, model_start_y),  # left, top
    ]

    model_act_codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
    ]

    model_activity_box_path = Path(model_act_verts, model_act_codes)
    model_activity_box_patch = patches.PathPatch(model_activity_box_path, facecolor=color, lw=2)
    ax.add_patch(model_activity_box_patch)

    # draw model object box
    model_ob_y = start_y - ACTIVITY_HIGHT - OBJECT_HEIGHT - ACTIVITY_HIGHT

    model_obj_verts = [
        (start_x, model_ob_y),  # left, top
        (start_x + MOVE_WIDTH, model_ob_y),  # right, top
        (start_x + MOVE_WIDTH, model_ob_y - OBJECT_HEIGHT),  # right, top
        (start_x, model_ob_y - OBJECT_HEIGHT),  # left, bottom
        (start_x, model_ob_y),  # left, top
    ]

    model_obj_codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
        Path.LINETO,
    ]

    model_obj_box_path = Path(model_obj_verts, model_obj_codes)
    model_obj_box_patch = patches.PathPatch(model_obj_box_path, facecolor=color, lw=2)
    ax.add_patch(model_obj_box_patch)

    # log activity text
    log_act = move.log_move if move.log_move else ">>"
    if log_act in abbreviations.keys():
        log_act = abbreviations[log_act]
    log_act_text = ax.text(start_x + TEXT_BUFFER_LEFT,
                           start_y - (0.5 * ACTIVITY_HIGHT),
                           log_act,
                           va='center', ha='left',
                           fontsize=12)
    use_fontsize_that_fits(log_act_text, MOVE_WIDTH - (2 * TEXT_BUFFER_LEFT), ACTIVITY_HIGHT, fig=fig, ax=ax)

    # model activity text
    model_act = move.model_move if move.model_move else ">>"
    if model_act in abbreviations.keys():
        model_act = abbreviations[model_act]
    model_act_text = ax.text(start_x + TEXT_BUFFER_LEFT,
                           start_y - ACTIVITY_HIGHT - OBJECT_HEIGHT - (0.5 * ACTIVITY_HIGHT),
                           model_act,
                           va='center', ha='left',
                           fontsize=12)
    use_fontsize_that_fits(model_act_text, MOVE_WIDTH - (2 * TEXT_BUFFER_LEFT), ACTIVITY_HIGHT, fig=fig, ax=ax)

    # log objects text
    log_obj = ""
    for obj in move.objects:
        obj_str = obj
        if obj_str in abbreviations.keys():
            log_obj += obj_str + " "
            continue
        numb_obj_str = re.findall(r'\d+', obj_str)
        no_number_obj_str = ''.join([i for i in obj_str if not i.isdigit()])
        if no_number_obj_str in abbreviations.keys():
            number = reduce(lambda a, b: a+b, numb_obj_str)
            number = number[0]
            log_obj += abbreviations[no_number_obj_str] + number + " "
            continue
        log_obj += obj_str + " "

    log_obj_text = ax.text(start_x + TEXT_BUFFER_LEFT,
                             start_y - ACTIVITY_HIGHT - (0.5 * OBJECT_HEIGHT),
                             log_obj,
                             va='center', ha='left',
                             fontsize=12)
    use_fontsize_that_fits(log_obj_text, MOVE_WIDTH - (2 * TEXT_BUFFER_LEFT), OBJECT_HEIGHT, fig=fig, ax=ax)

    # model objects text
    # use same text as log

    model_obj_text = ax.text(start_x + TEXT_BUFFER_LEFT,
                           start_y - ACTIVITY_HIGHT - ACTIVITY_HIGHT - OBJECT_HEIGHT - (0.5 * OBJECT_HEIGHT),
                           log_obj,
                           va='center', ha='left',
                           fontsize=12)
    use_fontsize_that_fits(model_obj_text, MOVE_WIDTH - (2 * TEXT_BUFFER_LEFT), ACTIVITY_HIGHT, fig=fig, ax=ax)

    return (MOVE_WIDTH, (start_x, model_start_y), (start_x + MOVE_WIDTH, model_start_y))


def alignment_viz(alignment: Alignment, abbreviations=dict()):
    # get all objects
    objects = []
    move: Move
    for move in alignment.moves:
        objects += move.objects
    # remove duplicates
    objects = set(objects)
    objects = list(objects)

    # get minimal set of transition to have equivalent transitive hull
    connections = set()
    for object in objects:
        last_move_with_object = None
        for move in alignment.moves:
            if object in move.objects:
                if last_move_with_object != None:
                    connections.add((last_move_with_object, move))
                last_move_with_object = move

    # get start moves that don't have ingoing arc
    not_selected_moves = alignment.moves[:]
    selected_moves = []
    columns = []
    first_column = []
    for move in not_selected_moves:
        to_add = []
        has_ingoing = False
        for connection in connections:
            if connection[1] == move:
                has_ingoing = True
                break
        if not has_ingoing:
            to_add.append(move)
            not_selected_moves.remove(move)
            first_column.append(move)
        selected_moves += to_add
    columns.append(first_column)

    # always get moves that only have ingoing arcs from currently already selected notes. They then form new front
    while not_selected_moves:
        to_add = []
        to_remove = []
        this_column = []
        for move in not_selected_moves:
            all_ingoing_selected = True
            for connection in connections:
                if connection[1] == move:
                    if connection[0] not in selected_moves:
                        all_ingoing_selected = False
                        break

            if all_ingoing_selected:
                to_add.append(move)
                to_remove.append(move)
                this_column.append(move)
        selected_moves += to_add
        for move in to_remove:
            not_selected_moves.remove(move)
        columns.append(this_column)

    max_column_count = max([len(column) for column in columns])
    total_y_axis_height = BUFFER_HEIGHT + max_column_count * (BUFFER_HEIGHT + 2 * (ACTIVITY_HIGHT + OBJECT_HEIGHT))
    total_x_axis_width = 2 * BUFFER_WIDTH + (len(columns) - 1) * SPACE_BETWEEN_COLUMNS + len(columns) * MOVE_WIDTH
    # draw each column
    fig, ax = plt.subplots()
    renderer = fig.canvas.get_renderer()
    ax.set_xlim(0, total_x_axis_width)
    ax.set_ylim(0, total_y_axis_height)

    # initialize dictionary to save in and outgoing point for moves
    ingoing_points = dict()
    outgoing_points = dict()

    start_x_axis = BUFFER_WIDTH
    for column in columns:
        start_y_axis = 0.5 * total_y_axis_height + 0.5 * (BUFFER_HEIGHT + len(column) * (BUFFER_HEIGHT + 2 * (ACTIVITY_HIGHT + OBJECT_HEIGHT))) - BUFFER_HEIGHT
        current_move_start_x = start_x_axis
        max_used_width = 0
        for move in column:
            color_of_move = DEFAULT_COLOR
            if isinstance(move, DefinedModelMove):
                color_of_move = MODEL_MOVE_COLOR
            if isinstance(move, SynchronousMove):
                color_of_move = SYNC_COLOR
            if isinstance(move, LogMove):
                color_of_move = LOG_MOVE_COLOR
            used_width, ingoing_point, outgoing_point = draw_move(move, current_move_start_x, start_y_axis,
                                                                  color_of_move, abbreviations, fig, ax, renderer)
            if used_width > max_used_width:
                max_used_width = used_width
            ingoing_points[move] = ingoing_point
            outgoing_points[move] = outgoing_point
            start_y_axis = start_y_axis - BUFFER_HEIGHT - (2 * (ACTIVITY_HIGHT + OBJECT_HEIGHT))
        start_x_axis = start_x_axis + max_used_width + SPACE_BETWEEN_COLUMNS

    # draw lines
    for connection in connections:
        draw_line(outgoing_points[connection[0]], ingoing_points[connection[1]], fig, ax)

    ax.set_title(f"Alignment has cost: {alignment.get_cost()}")

    sync_patch = mpatches.Patch(color=SYNC_COLOR, label='Synchronous Move')
    model_patch = mpatches.Patch(color=MODEL_MOVE_COLOR, label='Model Move')
    label_patch = mpatches.Patch(color=LOG_MOVE_COLOR, label='Log Move')
    ax.legend(handles=[sync_patch, model_patch, label_patch])

    ax.set_xlim(0, start_x_axis - SPACE_BETWEEN_COLUMNS + BUFFER_WIDTH)
    ax.set_ylim(0, total_y_axis_height)

    # hide x-axis
    ax.get_xaxis().set_visible(False)

    # hide y-axis
    ax.get_yaxis().set_visible(False)

    plt.show()
