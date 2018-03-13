from Utilities import PolarCoordinate
from Constants import SectorClusteringConstants
from operator import attrgetter
import copy


class SectorClusteringParameters(object):
    def __init__(self, angular_seed=None, angular_sector_size=None, angular_step_size=None,
                 sector_clustering_method=None):
        self.angular_seed = angular_seed
        self.angular_sector_size = angular_sector_size
        self.angular_step_size = angular_step_size
        self.sector_clustering_method = sector_clustering_method

    @classmethod
    def from_scetor_clustering_method(cls):
        pc = cls()
        pc.sector_clustering_method = SectorClusteringConstants.CONST_SECTOR_CLUSTERING_METHOD
        pc.angular_seed = SectorClusteringConstants.CONST_ANGULAR_SEED_IN_RADIAN
        pc.angular_sector_size = SectorClusteringConstants.CONST_ANGULAR_SECTOR_SIZE_IN_RADIAN
        pc.angular_step_size = SectorClusteringConstants.CONST_ANGULAR_STEP_SIZE_IN_RADIAN
        return pc

    def __str__(self):
        return "Se:{}_Sc:{}_St:{}".format(PolarCoordinate.to_degree(self.angular_seed),
                                          PolarCoordinate.to_degree(self.angular_sector_size),
                                          PolarCoordinate.to_degree(self.angular_step_size))


class SectorClustering():

    def __init__(self, orders, clustering_parameters):
        self.clustering_parameters = clustering_parameters
        self.orders = orders
        self.current_offset = clustering_parameters.angular_seed
        self.reorder_cluster()

    def get_next_cluster(self):
        clustered_orders = self.get_cluster(self.orders, self.current_offset,
                                            self.clustering_parameters.angular_sector_size)
        current_angular_offset = self.current_offset + self.clustering_parameters.angular_step_size

        if current_angular_offset >= PolarCoordinate.max_angle_in_radian:
            current_angular_offset -= PolarCoordinate.period_length_in_radian

        self.current_offset = current_angular_offset
        return clustered_orders

    def make_filter_orders(self, angular_offset, sector_size):
        def filter_order(order):
            PolarCoordinate.is_in_range(order.PolarCoordinate.theta, angular_offset, angular_offset + sector_size)

        return filter_order

    def get_cluster(self, orders, angular_offset, sector_size):
        order_filter = self.make_filter_orders(angular_offset, sector_size)
        return filter(order_filter, orders)

    def reorder_cluster(self):
        temp_list = copy.deepcopy(self.orders)
        temp_list = sorted(temp_list, key=attrgetter("DistanceFromDepot"), reverse=True)
        temp_list = sorted(temp_list, key=attrgetter("Id"))
        self.orders = temp_list
