"""
Defines functions for plotting the results of the identify step.
"""

from functools import singledispatch

import numpy as np
import scipy.linalg as la
from fsc.export import export

from ._evaluate import NodalPoint, NodalLine

from .._common_plot import _setup_plot


@export
def result(res, *, axis=None):
    """Plot the result of the identify step.

    Arguments
    ---------
    res : IdentificationResultContainer
        Result of the identify step.
    axis : matplotlib.axes.Axes, optional
        Axes on which the result is plotted.
    """
    fig, axis, _ = _setup_plot(res.coordinate_system.limits, axis=axis)
    feature_size = res.feature_size
    for identification_result in res:
        shape = identification_result.shape
        color = axis._get_lines.get_next_color()  # pylint: disable=protected-access
        if shape is None:
            _plot_positions(
                identification_result.positions, axis=axis, color=color
            )
        else:
            _plot_result(
                shape, axis=axis, color=color, feature_size=feature_size
            )
    return fig, axis


def _plot_positions(positions, *, axis, color):
    coordinates = list(np.array(list(positions)).T)
    axis.scatter(*coordinates, color=color)


@singledispatch
def _plot_result(shape, axis, color, feature_size):  # pylint: disable=unused-argument
    raise NotImplementedError


@export
@_plot_result.register(NodalPoint)
def nodal_point(shape, *, axis, color, feature_size=None):
    """
    Plot a nodal point.

    Arguments
    ---------
    shape : NodalPoint
        Nodal point to be plotted.
    axis : matplotlib.axes.Axes
        Axes on which to plot.
    color : str
        Color of the point.
    feature_size : float
        TODO, not used in this function.
    """
    coordinates = [[val] for val in shape.position]
    axis.scatter(*coordinates, color=color)


@export
@_plot_result.register(NodalLine)
def nodal_line(shape, *, axis, color, feature_size):
    """
    Plot a nodal line.

    Arguments
    ---------
    shape : NodalLine
        Nodal line to be plotted.
    axis : matplotlib.axes.Axes
        Axes on which to plot.
    color : str
        Color of the nodal line.
    feature_size : float
        TODO, used for cutting the line when it goes across periodic boundaries.
    """
    start_idx = 0
    # Segment line when crossing the periodic boundary.
    for i, (pos1, pos2) in enumerate(zip(shape.path, shape.path[1:])):
        if la.norm(np.array(pos2) - np.array(pos1)) > 2 * feature_size:
            axis.plot(*np.array(shape.path[start_idx:i + 1]).T, color=color)
            start_idx = i + 1
    axis.plot(*np.array(shape.path[start_idx:]).T, color=color)
