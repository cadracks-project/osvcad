# coding: utf-8

r"""Nomenclature management"""

sectors = {"CAR": {"en": "CAR",
                   "fr": "VOITURE"},
           "AERO": {"en": "AERO",
                    "fr": "AERO"},
           "MECA": {"en": "MECA",
                    "fr": "MECA"},
           "ELEC": {"en": "ELEC",
                    "fr": "ELEC"},
           "GEN": {"en": "GEN",
                   "fr": "GEN"}}

domains = {"CAR": {"SUSPENSION": {"en": "SUSPENSION",
                                  "fr": "SUSPENSION"}},
           "AERO": {"LANDING-GEAR": {"en": "LANDING-GEAR",
                                     "fr": "TRAIN-ATERRISSAGE"},
                    "WING": {"en": "WING",
                             "fr": "AILE"}},
           "MECA": {"FASTENER": {"en": "FASTENER",
                                 "fr": "FIXATION"}}}

functions = {"CAR": {"SUSPENSION": {"RAM": {"en": "RAM",
                                            "fr": "VERIN"}}},
             "MECA": {"FASTENER": {"SCREW": {"en": "SCREW",
                                             "fr": "VIS"}}}}

materials = {"STEEL": {"en": "STEEL",
                       "fr": "ACIER"},
             "SSTEEL": {"en": "STAINLESS-STEEL",
                        "fr": "INOX"},
             "CRF": {"en": "CARBON-FIBER",
                     "fr": "FIBRE-CARBONE"}}

origins = ["GENERIC", "AUDI", "BOEING"]

zones = {"TOP": {"en": "TOP",
                 "fr": "HAUT"},
         "BOTTOM": {"en": "BOTTOM",
                    "fr": "BAS"},
         "LEFT": {"en": "LEFT",
                  "fr": "GAUCHE"},
         "RIGHT": {"en": "RIGHT",
                   "fr": "DROITE"},
         "FRONT": {"en": "FRONT",
                   "fr": "AVANT"},
         "BACK": {"en": "BACK",
                  "fr": "ARRIERE"}}


def nomenclature_part_plan(sector,
                           domain,
                           function_,
                           dimensional,
                           material,
                           origin,
                           alpha,
                           language="neutral"):
    r"""Nomenclature of a part plan
    
    Parameters
    ----------
    sector: str
    domain: str
    function_: str
    dimensional: str
    material: str
    origin: str
    alpha: str or int
    language: str

    Returns
    -------
    str
        The name of the part plan

    """
    if sector not in sectors.keys():
        raise ValueError("Unknown sector")

    if domain not in domains[sector].keys():
        raise ValueError("Unknown domain for sector")

    if function_ not in functions[sector][domain].keys():
        raise ValueError("Unknown function_ for sector/domain")

    if material not in materials.keys():
        raise ValueError("Unknown material")

    if origin not in origins:
        raise ValueError("Unknown origins")

    if language == "neutral":
        return "%s_%s_%s_%s_%s_%s_%s" % (sector,
                                         domain,
                                         function_,
                                         dimensional,
                                         material,
                                         origin,
                                         alpha)
    else:
        return "%s_%s_%s_%s_%s_%s_%s" % (sectors[sector][language],
                                         domains[sector][domain][language],
                                         functions[sector][domain][function_][language],
                                         dimensional,
                                         materials[material][language],
                                         origin,
                                         alpha)


def nomenclature_part_instance(sector,
                               domain,
                               function_,
                               dimensional,
                               material,
                               origin,
                               alpha,
                               zone,
                               beta,
                               language="neutral"):
    r"""Nomenclature of a part instance
    
    Parameters
    ----------
    sector: str
    domain: str
    function_: str
    dimensional: str
    material: str
    origin: str
    alpha: str or int
    zone: str
    beta: str or int
    language: str

    Returns
    -------
    str
        The name of the part instance

    """
    if zone not in zones.keys():
        raise ValueError("Unknown position")

    if language == "neutral":
        zone = zone
    else:
        zone = zones[zone][language]

    return "%s_%s_%s" % (nomenclature_part_plan(sector,
                                                domain,
                                                function_,
                                                dimensional,
                                                material,
                                                origin,
                                                alpha,
                                                language),
                         zone,
                         str(beta))


anchor_types = {"AXIS": {"en": "AXIS", "fr": "AXE"},
                "PERP": {"en": "PERPENDICULAR", "fr": "PERPENDICULAIRE"}}


def nomenclature_anchor(type_, zone, dimensional, ref, language="neutral"):
    r"""
    
    Parameters
    ----------
    type_: str
    zone: str
    dimensional: str
    ref: str or int
    language: str

    Returns
    -------
    str
        The name of the anchor

    """
    if type_ not in anchor_types.keys():
        raise ValueError("Unknown anchor type")

    if zone not in zones.keys():
        raise ValueError("Unknown zone")

    if language == "neutral":
        return "%s_%s_%s_%s" % (type_, zone, dimensional, str(ref))
    else:
        return "%s_%s_%s_%s" % (anchor_types[type_][language],
                                zones[zone][language],
                                dimensional,
                                str(ref))


def getname(**kwargs):
    """naming a parts (legacy from Bernard)

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

    sector = kwargs.pop('sector', '')
    domain = kwargs.pop('domain', '')
    func_ = kwargs.pop('function', '')
    dimension = kwargs.pop('dimension', '')
    material = kwargs.pop('material', '')
    origin = kwargs.pop('origin', '')
    alpha = kwargs.pop('alpha', '1')

    lattributes = [sector, domain, func_, dimension, material, origin, alpha]
    return "_".join(lattributes)


if __name__ == "__main__":
    print(nomenclature_part_plan("CAR", "SUSPENSION", "RAM", "long", "STEEL",
                                 "AUDI", "XZW2"))
    print(nomenclature_part_plan("CAR", "SUSPENSION", "RAM", "long", "STEEL",
                                 "AUDI", "XZW2", language="fr"))
    print(nomenclature_part_instance("CAR", "SUSPENSION", "RAM", "long",
                                     "STEEL", "AUDI", "XZW2",
                                     zone="TOP", beta=73, language="fr"))
    print(nomenclature_anchor("AXIS", "TOP", "d10", "A"))
    print(nomenclature_anchor("AXIS", "TOP", "d10", "A", language="fr"))
    print(getname(material="PAPER"))
