# coding: utf-8

r"""Geometry computations"""

import numpy as np

from osvcad.transformations import translation_matrix, rotation_matrix,\
    angle_between_vectors, vector_product


def transformation_from_2_anchors(anchor_master,
                                  anchor_slave,
                                  angle=0.,
                                  distance=0.):
    r"""Compute the transformation to bring vector_b's origin 
    to vector_a's origin and to align vector_b with vector_a
    
    vector_a does not move.
    
    Parameters
    ----------
    anchor_master : dict
        {"position": (1, 2, 3), "direction": (4, 5, 6)}
    anchor_slave : same as vector_a
    angle : float
        Angle in degrees
        Putting the master and slave anchors in opposition
        leaves one degree of freedom that is dealt with by the angle
    distance : float
        Distance between the anchor positions

    Returns
    -------

    """
    # translation
    pa_x, pa_y, pa_z = anchor_master["position"]
    pb_x, pb_y, pb_z = anchor_slave["position"]

    translation_1 = (-pb_x, -pb_y, -pb_z)

    # rotation
    angle = angle_between_vectors(anchor_master["direction"],
                                  anchor_slave["direction"])

    axis_dir = vector_product(anchor_master["direction"],
                              anchor_slave["direction"])

    if np.array_equal(axis_dir, np.array([0, 0, 0])):
        # anchor directions are collinear, any perpendicular axis will do

        # arbitrary unit vector
        k = np.array([1.,  0., 0.])
        y = np.cross(k, anchor_master["direction"])

        axis_dir = y

    rot_matrix = rotation_matrix(angle + np.pi, axis_dir)

    translation_2 = (pa_x, pa_y, pa_z)

    transformation_mat = np.dot(rot_matrix, translation_matrix(translation_1))
    transformation_mat = np.dot(translation_matrix(translation_2),
                                transformation_mat)[:3]

    return transformation_mat,\
        translation_matrix(translation_1),\
        rot_matrix,\
        translation_matrix(translation_2)
