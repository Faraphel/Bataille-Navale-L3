from source.type import Point2D, BBox


def in_bbox(point: Point2D, bbox: BBox) -> bool:
    """
    Return true if a point is inside a bounding box
    :param point: the point to check
    :param bbox: the bbox where to check the point
    :return: True if the point is inside the bbox, False otherwise
    """

    point_x, point_y = point
    bbox_x1, bbox_y1, bbox_x2, bbox_y2 = bbox

    if not bbox_x1 <= point_x <= bbox_x2: return False
    if not bbox_y1 <= point_y <= bbox_y2: return False
    return True
