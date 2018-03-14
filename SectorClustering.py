from Utilities import PolarCoordinate


def get_next_cluster(orders, clustering_parameters):
    reorder_cluster(orders)
    clustered_orders = get_cluster(orders, clustering_parameters.angular_offset,
                                   clustering_parameters.angular_sector_size)
    clustering_parameters.update_angular_offset()

    return clustered_orders


def get_cluster(orders, angular_offset, sector_size):
    order_filter = make_filter_orders(angular_offset, sector_size)
    return list(filter(order_filter, orders))


def make_filter_orders(angular_offset, sector_size):
    def filter_order(order):
        PolarCoordinate.is_in_range(order.PolarCoordinate.theta, angular_offset, angular_offset + sector_size)

    return filter_order


def reorder_cluster(orders):
    orders.sort(key=lambda x: x.distance_from_depot, reverse=True)
