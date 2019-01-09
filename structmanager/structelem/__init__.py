"""
Structural Elements (:mod:`structmanager.structelem`)
==============================================================

.. currentmodule:: structmanager.structelem

"""
from .flanges import InnerFlange, OuterFlange
from .panel import Panel
from .panelcomp import PanelComp
from .shearclip import ShearClipWeb, ShearClipFoot
from .stringer import Stringer
from .web import Web

se_classes = [
        InnerFlange,
        OuterFlange,
        Panel,
        PanelComp,
        ShearClipWeb,
        ShearClipFoot,
        Stringer,
        Web,
        ]
