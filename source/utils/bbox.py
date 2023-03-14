from source.type import Point2D, BBox


def in_bbox(point: Point2D, bbox: BBox) -> bool:
    """
    Indique si un point est dans un rectangle
    :param point: le point à vérifier
    :param bbox: la bbox à vérifier
    :return: True si le point est dans la bbox, sinon Faux
    """

    point_x, point_y = point
    bbox_x1, bbox_y1, bbox_x2, bbox_y2 = bbox

    if not bbox_x1 <= point_x <= bbox_x2: return False
    if not bbox_y1 <= point_y <= bbox_y2: return False
    return True
