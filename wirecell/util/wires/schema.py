#!/usr/bin/env python
'''
This module defines an object schema which gives the terms in which
wires are described for the Wire Cell Toolkit.

The wire end points are expressed in a Cartesian 3-space associated
with the anode plane face in which the wire resides.  For double-sided
anode planes there will be two such coordinate systems one for each
face.  From tail to head, a wire points in the direction that signal
travels towards electronics.

Any "ident" attribute of an object is a number which is considered
opaque to the toolkit.  It will be passed through to implementations.
Generally, the number is required to be unique to that object.

Objects are referenced through their index in the associated Store
collection.  Except for the lists in the Store, lists of references
have ordering requirements.

Some information is assumed implicit or calculated by the application
such as wire plane direction and pitch.

Units Warning: distance must be specified in millimeters.
'''


from collections import namedtuple


class Point(namedtuple("Point", "x y z")):
    '''
    A point in 3 space.

    Each point is in terms of the coordinate system (as described
    below for each coordinate) of its drift cell.  This means that for
    double-sided anode planes one must understand the context in which
    the point is referenced to know where a point is in some external
    coordinate system in which both drift cells are related.

    :param float x: Measure along the X-axis which points counter to
        the electron drift direction.
    :param float y: Measure along the Y-axis which points counter to
        the force of gravity.
    :param float z: Measure along the Z-axis which is X cross Y.
    '''
    __slots__ = ()


class Wire(namedtuple("Wire","ident channel segment tail head")):
    '''
    A Wire object holds information about one physical wire segment.

    A wire is a ray which points in the direction that signals flow
    toward the electronics.

    :param int ident: numerical identifier unique to this wire in the
        anode plane.  This is made available via IWire::ident().
    :param int channel: numerical identifier unique to this conductor
        in the anode plane.  It is made available via
        IWire::channel().
    :param int segment: count the number of wires between this and
        the channel input.
    :param int tail: index referencing the tail end point of the wire
        in the coordinate system for the anode face.
    :param int head: index referencing the head end point of the wire
        in the coordinate system for the anode face.
    '''
    __slots__ = ()


class Plane(namedtuple("Plane", "ident wires")):
    '''
    A WirePlane object collects the wires that make up one physical
    plane.

    :param int ident: numerical identifier unique to the anode plane.
        It is made available as IWire::planeid().
    :param list wires: list of indices referencing the wires that make
        up this plane.  This list must be sorted in increasing wire Z.
    '''
    __slots__ = ()


class Face(namedtuple("Face", "ident planes")):
    '''
    A Face collects the wire and conductor planes making up one face
    of an anode plane.

    :param int ident: numerical identifier unique to the face.  This
        is used to refer to the face in IAnodePlane::face() and
        available from IAnodeFace::ident().
    :param list planes: list of indices referencing planes.  This list
        must be in the order of which drifting electrons pass (ie,
        negative-X order).
    '''
    __slots__ = ()


class Anode(namedtuple("Anode","ident faces")):
    '''
    An Anode object collects together Faces.

    A detector like MicroBooNE has just one face per its single anode.
    protoDUNE/SP has two faces per each of its six anodes (aka APAs).

    :param int ident: numerical identifier unique to this anode.  This
        is available from IAnodePlane::ident().
    :param list faces: list indices referencing faces.  As a
        guideline, the first face is considered "front" (eg, for
        protoDUNE, it points at the larger drift cell).  The second is
        considered "back".  These meaning ultimately are interpreted
        by implementation.
    '''
    __slots__ = ()    


class Store(namedtuple("Store","anodes faces planes wires points")):
    '''
    A store of collections of the objects of this schema.

    :param list anodes: list of the Anode objects.
    :param list faces: list of the Face objects
    :param list planes: list of the Plane objects.
    :param list wires: list of the Wire objects.
    :param list points: list of the Point objects.

    '''
    __slots__ = ()


def classes():
    import sys, inspect
    ret = list()
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            ret.append(obj)
    return ret

