#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
from types import SimpleNamespace

import numpy as np
from ._nelder_mead import root_nelder_mead

class NodalPoint(SimpleNamespace):
    def __init__(self, k, gap):
        self.k = tuple(np.array(k) % 1)
        self.gap = gap

class NodeFinder:
    def __init__(self, gap_fct, *, gap_threshold=1e-6, mesh_size=(10, 10, 10), feature_size=1e-3):
        self.gap_fct = gap_fct
        self._gap_threshold = gap_threshold
        self._mesh_size = tuple(mesh_size)
        self._feature_size = feature_size
        self._nodal_points = []
        self._initialize()

    def _initialize(self):
        self._calculate_box(
            box_position=((0, 1),) * 3,
            mesh_size=self._mesh_size,
            periodic=True
        )

    def _calculate_box(self, *, box_position, mesh_size, periodic=False):
        mesh = itertools.product(*[
            np.linspace(min_val, max_val, N, endpoint=not periodic)
            for (min_val, max_val), N in zip(box_position, mesh_size)
        ])
        for m in mesh:
            trial_point = self._minimize(starting_point=m)
            if trial_point.fun < self._gap_threshold:
                self._nodal_points.append(
                    NodalPoint(k=trial_point.x, gap=trial_point.fun)
                )

    def _minimize(self, starting_point):
        # TODO:
        # * Change the minimization to contain the dynamic cutoff criterion
        # * Make cutoff values configurable
        # * Allow setting the other starting vertices of the Nelder-Mead algorithm
        # res = so.minimize(self.gap_fct, x0=starting_point, method='Nelder-Mead', tol=1e-8, options=dict(maxfev=20))
        # if res.fun < 0.1:
        #     res = so.minimize(self.gap_fct, x0=res.x, method='Nelder-Mead', tol=1e-8, options=dict(maxfev=100))
        #     if res.fun < 1e-2:
        res = root_nelder_mead(self.gap_fct, x0=starting_point)
        print(res)
        return res