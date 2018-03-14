from Utilities import PolarCoordinate


class SectorClusteringParameter(object):
    def __init__(self, angular_seed, angular_sector_size, angular_step_size, sector_clustering_method):
        self.angular_seed = angular_seed
        self.angular_offset = angular_seed
        self.angular_sector_size = angular_sector_size
        self.angular_step_size = angular_step_size
        self.sector_clustering_method = sector_clustering_method

    def update_angular_offset(self):
        self.angular_offset = self.angular_offset + self.angular_step_size
        if self.angular_offset >= PolarCoordinate.max_angle_in_radian:
            self.angular_offset -= PolarCoordinate.period_length_in_radian

    def __str__(self):
        return "Se:{}_Sc:{}_St:{}".format(PolarCoordinate.to_degree(self.angular_seed),
                                          PolarCoordinate.to_degree(self.angular_sector_size),
                                          PolarCoordinate.to_degree(self.angular_step_size))
