# coding: utf-8

r"""Graph nodes"""

import logging
from math import radians
import re

from os.path import basename, splitext, exists, join, dirname

import imp
import networkx as nx
import jsonpickle
import matplotlib.pyplot as plt
import numpy as np
from random import uniform
from OCC.gp import gp_Pnt, gp_Vec
from aocutils.display.wx_viewer import colour_wx_to_occ
from ccad.model import transformed, from_step

import ccad.display as cd

from party.library_use import generate

from osvcad.geometry import transformation_from_2_anchors, transform_anchor
from osvcad.transformations import translation_matrix, rotation_matrix
from osvcad.stepzip import extract_stepzip
from osvcad.coding import overrides


logger = logging.getLogger(__name__)


class GeometryNode(object):
    r"""Geometry node class
    
    A geometry node is a shape with ist accompanying anchors
    
    Parameters
    ----------
    shape : 
    anchors : dict
    instance_id : str, optional (default is None)
        An identifier for the GeometryNode

    """
    def __init__(self, node_shape, anchors, instance_id=None):
        logger.debug("Direct instantiation of GeometryNode %s" % self)
        self._node_shape = node_shape
        self._anchors = anchors
        self._instance_id = instance_id

    @classmethod
    def from_library_part(cls, library_file_path, part_id, instance_id=None):
        r"""Create the GeometryNode from a library part"""
        logger.info("Creating GeometryNode from library (%s) part (id: %s)" % (library_file_path, part_id))
        generate(library_file_path)
        scripts_folder = join(dirname(library_file_path), "scripts")
        module_path = join(scripts_folder, "%s.py" % part_id)
        module_ = imp.load_source(splitext(module_path)[0],
                                  module_path)

        if not hasattr(module_, 'part'):
            raise ValueError("The Python module should have a 'part' variable")
        return cls(module_.part, module_.anchors, instance_id)

    @classmethod
    def from_step(cls, step_file_path, anchors=None, instance_id=None):
        r"""Create the GeometryNode from a step file and anchors definition"""
        logger.info("Creating GeometryNode from step file %s" % basename(step_file_path))
        assert exists(step_file_path)
        return cls(from_step(step_file_path), anchors, instance_id)

    @classmethod
    def from_stepzip(cls, stepzip_file, instance_id=None):
        r"""Alternative constructor from a STEP + anchors zip file"""
        logger.info("Creating GeometryNode from stepzip file %s" % basename(stepzip_file))
        anchors = dict()
        stepfile_path, anchorsfile_path = extract_stepzip(stepzip_file)
        with open(anchorsfile_path) as f:
            lines = f.readlines()
            for line in lines:
                # print(line)
                if line != "\n" and not line.startswith("#"):
                    items = re.findall(r'\S+', line)
                    # print(items)
                    key = items[0]
                    data = [float(v) for v in items[1].split(",")]
                    position = (data[0], data[1], data[2])
                    direction = (data[3], data[4], data[5])
                    anchors[key] = {"position": position,
                                    "direction": direction}
        return cls.from_step(stepfile_path, anchors, instance_id)

    @classmethod
    def from_py_script(cls, py_script_path, instance_id=None):
        r"""Create the GeometryNode from a python script (module) that has a
        part and an anchors attributes"""
        logger.info("Creating GeometryNode from py script %s" % basename(py_script_path))
        # TODO : use Part.from_py of ccad
        # cm.Part.from_py("sphere_r_2.py").geometry

        name, ext = splitext(basename(py_script_path))
        module_ = imp.load_source(name, py_script_path)

        return cls(module_.part, module_.anchors, instance_id)

    @property
    def instance_id(self):
        r"""Instance id getter"""
        return self._instance_id

    @property
    def node_shape(self):
        r"""Shape getter"""
        return self._node_shape

    @node_shape.setter
    def node_shape(self, value):
        self._node_shape = value

    @property
    def anchors(self):
        r"""Anchors getter"""
        return self._anchors

    @anchors.setter
    def anchors(self, value):
        self._anchors = value

    def place(self,
              self_anchor,
              other,
              other_anchor,
              angle=0.,
              distance=0.,
              inplace=False):
        r"""Place other node so that its anchor origin is on self anchor
        origin and its direction is opposite to the 'self' anchor direction
        
        Parameters
        ----------
        self_anchor : str
            Anchor identifier
        other : GeometryNode or subclass
        other_anchor : str
            Anchor identifier on the 'other' node
        angle : float
            The rotation angle around the anchor
        distance : float
            The distance between the anchor origin
        inplace : bool, optional (default is False)

        Returns
        -------
        GeometryNode if inplace is False, None if inplace is True

        """
        logger.info("GeometryNode.Place() %s/%s on %s/%s witk angle:%f -distance%f :inplace=%s" % (other, other_anchor, self, self_anchor, angle, distance, inplace))
        transformation_mat_ = transformation_from_2_anchors(
            self.anchors[self_anchor], other.anchors[other_anchor],
            angle=angle,
            distance=distance)

        if inplace is False:
            return other.transform(transformation_mat_)
        else:
            modified = other.transform(transformation_mat_)
            other.node_shape = modified.node_shape
            other.anchors = modified.anchors

        # print("Anchors of %s: %s" % (other, other.anchors))

    def transform(self, transformation_matrix):
        r"""Transform the node with a 4x3 transformation matrix
        
        Parameters
        ----------
        transformation_matrix : np.ndarray
        
        Returns
        -------
        GeometryNode

        """
        # logger.debug("transform()")
        # logger.debug("transformation matrix : %s" % transformation_matrix)
        new_shape = transformed(self.node_shape, transformation_matrix)
        new_anchors = dict()

        for anchor_name, anchor_dict in self.anchors.items():
            new_anchors[anchor_name] = transform_anchor(anchor_dict,
                                                        transformation_matrix)
        return GeometryNode(new_shape, new_anchors)

    def translate(self, vector):
        r"""Translate the node
        
        Parameters
        ----------
        vector : Tuple[float, float, float]
            The translation vector

        Returns
        -------
        GeometryNode

        """
        # logger.debug("translate()")
        return self.transform(translation_matrix(vector))

    def rotate(self, rotation_angle, rotation_axis, axis_point):
        r"""Rotate the node
        
        Parameters
        ----------
        rotation_angle : float
            Rotation angle in degrees
            Positive is the 'screwing' direction to progress along rotation axis
        rotation_axis : Tuple[float, float, float]
            Axis of rotation
        axis_point : Tuple[float, float, float]
            A point through which the axis of rotation passes

        Returns
        -------

        """
        # logger.debug("rotate() with angle:%f, axis: %s, point: %s" %
        #              (rotation_angle, str(rotation_axis), str(axis_point)))
        return self.transform(rotation_matrix(radians(rotation_angle),
                                              rotation_axis,
                                              axis_point))

    def display(self, viewer, color_255, transparency=0.):
        r"""Display the node in a 
        
        Parameters
        ----------
        viewer : aocutils.display.wx_viewer.Wx3dViewer
            The viewer where the node should be displayed
        color_255 : Tuple[float, float, float]
            8-bit (0 - 255) color tuple
        transparency : float
            From 0. (not transparent) to 1 (fully transparent)

        Returns
        -------

        """
        for k, _ in self.anchors.items():
            viewer.display_vector(gp_Vec(*self.anchors[k]["direction"]),
                                  gp_Pnt(*self.anchors[k]["position"]))
        viewer.display_shape(self.node_shape.node_shape,
                             color=colour_wx_to_occ(color_255),
                             transparency=transparency)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "GeometryNode : " + str(id(self))

    def ldesc(self):
        r"""Long description"""
        l = list()
        l.append("GeometryNode")
        l.append("\tShape : %s" % str(self.node_shape))
        l.append("\tAnchors :")
        if self.anchors is not None:
            for anchor_name, anchor_dict in self.anchors.items():
                l.append("\t\t%s : <dir>:%s@<pos>:%s" % (anchor_name,
                                                         str(anchor_dict["direction"]),
                                                         str(anchor_dict["position"])))
            else:
                l.append("\t\tNo anchor")
        return "\n".join(l)


class Assembly(nx.DiGraph, GeometryNode):
    r"""Acyclic directed graph modelling of a assembly

    The Assembly is an nx.DiGraph with serialization, deserialization and
    3D viewing methods
    
    Parameters
    ----------
    root : GeometryNode 
        The node of the assembly on which other nodes are positioned
        (aka the node that does not move)

    """

    def __init__(self, root, instance_id=None):
        super(Assembly, self).__init__()
        self._node_shape = None
        self._anchors = None
        self._instance_id = instance_id
        self.add_node(root)
        self.root = root
        # self._instance_id = instance_id

        self.built = False

    @overrides
    def transform(self, transformation_matrix):
        r"""Transform the node with a 4x3 transformation matrix

        Parameters
        ----------
        transformation_matrix : np.ndarray

        Returns
        -------
        GeometryNode

        """
        # Do it in place
        # for node in self.nodes():
        self._node_shape = transformed(self.node_shape, transformation_matrix)
        new_anchors = dict()

        for anchor_name, anchor_dict in self.anchors.items():
            new_anchors[anchor_name] = transform_anchor(anchor_dict,
                                                        transformation_matrix)
        self._anchors = new_anchors

    def build(self):
        r"""Build the assembly using the graph used to represent it"""
        if self.built is False:
            logger.debug("Building assembly %s" % self)
            assert self.root in self.nodes()

            # for edge in nx.bfs_edges(self, self.root):
            for edge in nx.bfs_edges(self, self.root):
                edge_origin = edge[0]
                edge_target = edge[1]
                edge_constraint = self.get_edge_data(edge_origin, edge_target)["object"]
                try:
                    edge_origin.place(self_anchor=edge_constraint.anchor_name_master,
                                      other=edge_target,
                                      other_anchor=edge_constraint.anchor_name_slave,
                                      angle=edge_constraint.angle,
                                      distance=edge_constraint.distance,
                                      inplace=True)
                except nx.exception.NetworkXError:
                    msg = "NetworkX error"
                    logger.warning(msg)

            # node shape
            shapes = list()
            logger.debug("%i nodes in %s" % (len(self.nodes()), id(self)))
            for node in self.nodes():
                logger.debug("Adding shape of node %s" % node)
                try:
                    node.build()
                except:
                    pass
                shapes.append(node._node_shape)
            # s = shapes[0]
            # for shape in shapes[1:]:
            #     s += shape

            self._node_shape = self.compound(shapes)

            # anchors

            a = dict()
            for node in self.nodes():
                for anchor_name, anchor_value in node._anchors.items():
                    if node.instance_id is not None:
                        a[node.instance_id + "/" + str(
                            anchor_name)] = anchor_value
                    else:
                        a[str(hash(node)) + "/" + str(
                            anchor_name)] = anchor_value
            self._anchors = a

            self.built = True

    # def write_yaml(self, yaml_file_name):
    #     r"""Export to YAML format
    #
    #     Parameters
    #     ----------
    #     yaml_file_name : str
    #         Path to the YAML file
    #
    #     """
    #     nx.write_yaml(self, yaml_file_name)

    def write_json(self, json_file_name):
        r"""Export to JSON format

        Parameters
        ----------
        json_file_name : str
            Path to the JSON file

        """
        jsonpickle.load_backend('json')
        jsonpickle.set_encoder_options('json', sort_keys=False, indent=4)

        with open(json_file_name, "w") as f:
            f.write(jsonpickle.encode(self))

    @classmethod
    def read_json(cls, json_file_name):
        r"""Construct the assembly from a JSON file"""
        j_ = ""
        with open(json_file_name) as f:
            j_ = f.read()
        return jsonpickle.decode(j_)

    def show_plot(self):
        r"""Create a Matplotlib graph of the plot"""
        val_map = {'A': 1.0,
                   'D': 0.5714285714285714,
                   'H': 0.0}

        values = [val_map.get(node, 0.25) for node in self.nodes()]

        pos = nx.circular_layout(self)
        nx.draw_networkx_nodes(self,
                               pos,
                               cmap=plt.get_cmap('jet'),
                               node_color=values)
        nx.draw_networkx_edges(self,
                               pos,
                               edgelist=self.edges(),
                               edge_color='r',
                               arrows=True)
        nx.draw_networkx_labels(self, pos)
        nx.draw_networkx_edge_labels(self, pos)
        plt.show()

    def display_3d(self):
        r"""Display the Assembly in a 3D viewer (currently ccad viewer)"""
        v = cd.view()

        self.build()

        for node in self.nodes():
            v.display(node._node_shape,
                      color=(uniform(0, 1), uniform(0, 1), uniform(0, 1)),
                      transparency=0.)
        # v.display(self._node_shape,
        #           color=(uniform(0, 1), uniform(0, 1), uniform(0, 1)),
        #           transparency=0.)

        cd.start()

    @overrides
    def place(self,
              self_anchor,
              other,
              other_anchor,
              angle=0.,
              distance=0.,
              inplace=True):
        r"""Place other node so that its anchor origin is on self anchor
        origin and its direction is opposite to the 'self' anchor direction

        Parameters
        ----------
        self_anchor : str
            Anchor identifier
        other : GeometryNode or subclass
        other_anchor : str
            Anchor identifier on the 'other' node
        angle : float
            The rotation angle around the anchor
        distance : float
            The distance between the anchor origin

        Returns
        -------
        GeometryNode if inplace is False, None if inplace is True

        """
        logger.info(
            "Assembly.Place() %s/%s on %s/%s witk angle:%f -distance%f :inplace=%s" % (
            other, other_anchor, self, self_anchor, angle, distance, inplace))
        transformation_mat_ = transformation_from_2_anchors(
            self.anchors[self_anchor], other.anchors[other_anchor],
            angle=angle,
            distance=distance)

        other.transform(transformation_mat_)

    @property
    def node_shape(self):
        r"""Abstract property implementation"""
        logger.debug("Accessing shapes of assembly %s" % id(self))
        self.build()
        return self._node_shape

    # TODO : separate function (it is static)
    def compound(self, topo):
        r"""Accumulate a bunch of TopoDS_* in list `topo` to a OCC.TopoDS.TopoDS_Compound

        Parameters
        ----------
        topo : list[TopoDS_*]

        Returns
        -------
        OCC.TopoDS.TopoDS_Compound

        """
        import OCC.TopoDS
        from ccad.model import Solid
        bd = OCC.TopoDS.TopoDS_Builder()
        comp = OCC.TopoDS.TopoDS_Compound()
        bd.MakeCompound(comp)
        for i in topo:
            bd.Add(comp, i.shape)

        return Solid(comp)

    @property
    def anchors(self):
        r"""Abstract property implementation"""
        logger.debug("Accessing anchors of assembly %s" % self)
        self.build()
        return self._anchors
