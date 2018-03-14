import math
from Constants import PolarCoordinatesConstants, Generic


class PolarCoordinate(object):
    min_angle_in_radian = PolarCoordinatesConstants.CONST_MIN_POLAR_ANGLE_IN_RADIAN
    max_angle_in_radian = PolarCoordinatesConstants.CONST_MAX_POLAR_ANGLE_IN_RADIAN
    period_length_in_radian = max_angle_in_radian - min_angle_in_radian

    def __init__(self, loc_p=None, origin=None):

        if loc_p is not None or origin is not None:
            self.theta = (math.atan2(loc_p.latitude - origin.latitude,
                                     loc_p.longitude - origin.longitude)
                          + PolarCoordinate.period_length_in_radian) % PolarCoordinate.period_length_in_radian
            self.rho = math.sqrt((loc_p.latitude - origin.latitude) * (loc_p.latitude - origin.latitude) + (
                    loc_p.longitude - origin.longitude) * (loc_p.longitude - origin.longitude))

    @classmethod
    def from_rho_theta(cls, rho, theta):
        pc = cls()
        pc.rho = rho
        pc.theta = theta
        return pc

    def __str__(self):
        return "Theta = {}, Rho ={}".format(self.theta, self.rho)

    def __eq__(self, other):
        if other is None:
            return False
        if self == other:
            return True
        if type(self) != type(other):
            return False
        return self.theta.__eq__(other.theta) and self.rho.__eq__(other.rho)

    def __hash__(self):
        return (self.theta.__hash__() * 397) ** self.rho.__hash__()

    def __lt__(self, other):
        return (self.theta < other.theta) or (
                math.fabs(self.theta - other.theta) < Generic.CONST_DOUBLE_EPSILON and self.rho < other.rho)

    def __cmp__(self, other):
        if self < other:
            return -1
        return True if self == other else False

    @staticmethod
    def is_in_range(theta, lower_bound_radian, upper_bound_radian):
        lo = lower_bound_radian % PolarCoordinate.period_length_in_radian
        up = upper_bound_radian % PolarCoordinate.period_length_in_radian
        if up <= lo:
            up += PolarCoordinate.period_length_in_radian
        return (up > theta >= lo) or (
                up > theta + PolarCoordinate.period_length_in_radian >= lo)

    @staticmethod
    def to_degree(in_radian):
        return in_radian / math.pi * 180

    @staticmethod
    def get_coordinate(location, origin_location):
        return PolarCoordinate(location, origin_location)
