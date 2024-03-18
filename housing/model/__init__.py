from housing.model.base import Base
from pyproj import CRS

# This is the State Plane Coordinate System projection for the counties of interest
#
# NAD83/New York East: https://spatialreference.org/ref/epsg/32115/
#
# Surprised there isn't a more official list than this:
# https://github.com/ret3/stateplane/blob/main/state_plane_reference.csv
PROJECT_SRID = 32115
PROJECT_CRS = CRS.from_epsg(PROJECT_SRID)

__all__ = ['Base']
