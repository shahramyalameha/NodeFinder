import pytest

import nodefinder as nf
from nodefinder.search._controller import _DIST_CUTOFF_FACTOR
from nodefinder.identify._cluster import create_clusters


@pytest.mark.parametrize(
    'sample_name, num_clusters',
    [('search/two_lines.hdf5', 2), ('search/point.hdf5', 1),
     ('search/line.hdf5', 1), ('search/surface.hdf5', 1)]
)
def test_clustering(sample, sample_name, num_clusters):
    search_result = nf.io.load(sample(sample_name))

    positions = [res.pos for res in search_result.minimization_results]
    coordinate_system = search_result.coordinate_system
    feature_size = search_result.dist_cutoff * _DIST_CUTOFF_FACTOR

    clusters, _ = create_clusters(
        positions=positions,
        coordinate_system=coordinate_system,
        feature_size=feature_size
    )
    assert len(clusters) == num_clusters
