import os
import sys
import json

def getname(**kwargs):
    """ naming a parts

    Parameters
    ----------

    sector(1) : str
        (CAR, AERO, GENERIC, MECA, ELEC)
    domain(2)  : str
        (SUSPENSION,WING,FASTENER)
    function(3) :
        (PISTON,SPAR,SCREW)
    dimension(4) (real separated by #)
        (21#29,7)
    material(5) (STEEL,CARBON, PVC)
    origin(6) (GENERIC, AUDI)
    alpha(7) (arbitrary number, external ref)

    Examples
    --------

    >>> name = getname(material="PAPER")

    """

    sector = kwargs.pop('sector','')
    domain = kwargs.pop('domain','')
    function = kwargs.pop('function','')
    dimension = kwargs.pop('dimension','')
    material = kwargs.pop('material','')
    origin = kwargs.pop('origin','')
    alpha = kwargs.pop('alpha','1')

    lattributes = [sector,domain,function,dimension,material,origin,alpha]
    name = "_".join(lattributes)

    return(name)

