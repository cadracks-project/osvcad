# coding: utf-8

r"""Graph edges"""

import abc


class Constraint(object):
    r"""Abstract base class for constraints"""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def transform(self, *args):
        r"""Shape placement function to respect the constraint"""
        raise NotImplementedError


class ConstraintAnchor(Constraint):
    r"""A constraint created by 2 anchors on different GeometryNode(s). For the
    constraint to be satisfied, the 2 anchors have to:
    - be of opposite directions
    - have their positions separated by distance

    Parameters
    ----------
    anchor_name_master : str
        The name of the anchor on the master GeometryNode
    anchor_name_slave : str
        The name of the anchor on the slave GeometryNode
    distance : float, optional (default is 0.)
        The distance between the anchors positions
    angle : float, optional (default is 0.)
        The angle to rotate the slave by after both anchors are colinear

    """
    def __init__(self,
                 anchor_name_master,
                 anchor_name_slave,
                 distance=0.,
                 angle=0.):
        super(ConstraintAnchor, self).__init__()
        self.anchor_name_master = anchor_name_master
        self.anchor_name_slave = anchor_name_slave
        self.distance = distance
        self.angle = angle

    def transform(self, geometry_node_master, geometry_node_slave):
        r"""Transform a slave GeometryNode that is the target of an edge coming
        from a master GeometryNode

        Parameters
        ----------
        geometry_node_master : GeometryNode
            The master GeometryNode (i.e. the node that does not move)
        geometry_node_slave : GeometryNode
            The slave GeometryNode (i.e. the node that moves to satisfy the
            anchor constraint)

        Returns
        -------
        GeometryNode

        """
        return geometry_node_master.place(self_anchor=self.anchor_name_master,
                                          other=geometry_node_slave,
                                          other_anchor=self.anchor_name_slave,
                                          angle=self.angle,
                                          distance=self.distance)

    def __repr__(self):
        return "%s -> %s" % (str(self.anchor_name_master),
                             str(self.anchor_name_slave))
