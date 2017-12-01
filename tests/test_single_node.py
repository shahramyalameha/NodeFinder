"""
Tests with a single nodal point.
"""

import numpy as np
import scipy.linalg as la

from nodefinder import NodeFinder


def test_single_node():
    """
    Test that a single nodal point is found.
    """
    node_position = [0.5] * 3

    def gap_fct(x):
        return la.norm(np.array(x) - node_position)

    node_finder = NodeFinder(gap_fct=gap_fct, fct_listable=False)
    result = node_finder.run()
    nodes = result.nodal_points
    assert len(nodes) == 1
    node = nodes[0]
    assert np.isclose(node.gap, 0)
    assert np.allclose(node.k, node_position)
