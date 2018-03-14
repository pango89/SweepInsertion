import math
from enum import Enum


class SectorClusteringMethod(Enum):
    FARTHEST_FROM_DEPOT = 1
    SMALLEST_ANGLE_fROM_DEPOT = 2
    EARLIST_DEADLINE = 3
    LARGEST_SHIPMENT_CAPACITY = 4


class PolarCoordiantesConstants(object):
    CONST_MIN_POLAR_ANGLE_IN_RADIAN = 0.0
    CONST_MAX_POLAR_ANGLE_IN_RADIAN = 2 * math.pi


class Generic(object):
    CONST_DOUBLE_EPSILON = 0.0001


class SweepConstants(object):
    CONST_MAX_VEHICLE_CAPACITY_TOLERANCE_IN_KG = 0.0
    CONST_MU = 1.0
    CONST_ALPHA = 1.0
    CONST_BETA = 1.0
    CONST_LAMBDA = 1.0


class SectorClusteringConstants():
    CONST_ANGULAR_SEED_IN_RADIAN = 0.0
    CONST_ANGULAR_SECTOR_SIZE_IN_RADIAN = 2 * math.pi
    CONST_ANGULAR_STEP_SIZE_IN_RADIAN = CONST_ANGULAR_SECTOR_SIZE_IN_RADIAN / 4 * 3
    CONST_SECTOR_CLUSTERING_METHOD = SectorClusteringMethod.FARTHEST_FROM_DEPOT
