from housing.model.base import Base

# This is the State Plane Coordinate System projection for the counties of interest
#
# NAD83/New York East: https://spatialreference.org/ref/epsg/32115/
#
# Surprised there isn't a more official list than this:
# https://github.com/ret3/stateplane/blob/main/state_plane_reference.csv
SRID = 32115

__all__ = ['Base']
