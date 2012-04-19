# -*- coding: utf-8 -*-
"""
gyroid.common
=============

This moudle define all global constants.

It includes::

    EPS, SMALL, LARGE
    BRAVAIS, CARTESIAN
    LAMELLAR
    SQUARE, RECTANGULAR, HEXAGONAL, OBLIQUE
    CUBIC, TETRAGONAL, ORTHORHOMBIC, TRIGONAL, MONOCLINIC, TRICLINIC
    DEFAULT
    CRYSTAL_SYSTEM1, CRYSTAL_SYSTEM2, CRYSTAL_SYSTEM3
    HM_ITA_TABLE1, HM_ITA_TABLE2, HM_ITA_TABLE3
    GROUP_ORDER_TABLE1, GROUP_ORDER_TABLE2, GROUP_ORDER_TABLE3

"""

import numpy as np
from numpy.linalg import inv

# To let the G2 comparison pass, EPS should not be too small
EPS = 1e-6

SMALL = 1e-10
LARGE = 1e+10

BRAVAIS = "Bravais"
CARTESIAN = "Cartesian"

LAMELLAR = "Lamellar"
SQUARE = "Square"
RECTANGULAR = "Rectangular"
HEXAGONAL = "Hexagonal"
OBLIQUE = "Oblique"
CUBIC = "Cubic"
TETRAGONAL = "Tetragonal"
ORTHORHOMBIC = "Orthorhombic"
TRIGONAL = "Trigonal"
MONOCLINIC = "Monoclinic"
TRICLINIC = "Triclinic"
DEFAULT = "Default"
CRYSTAL_SYSTEM1 = [LAMELLAR,DEFAULT]
CRYSTAL_SYSTEM2 = [SQUARE,RECTANGULAR,HEXAGONAL,OBLIQUE,DEFAULT]
CRYSTAL_SYSTEM3 = [CUBIC,TETRAGONAL,ORTHORHOMBIC,HEXAGONAL,
                   TRIGONAL,MONOCLINIC,TRICLINIC,DEFAULT]

HM_ITA_TABLE1 = ["P1","P-1"]
HM_ITA_TABLE2 = ["P1","P2","Pm","Pg","Cm",
                "P2mm","P2mg","P2gg","C2mm","P4",
                "P4mm","P4gm","P3","P3m1","P31m",
                "P6","P6mm"]

HM_ITA_TABLE3 = ["P1","P-1","P2","P21","C2",
                "Pm","Pc","Cm","Cc","P2/m",
                "P21/m","C2/m","P2/c","P21/c","C2/c",
                "P222","P2221","P21212","P212121","C2221",
                "C222","F222","I222","I212121","Pmm2",
                "Pmc21","Pcc2","Pma2","Pca21","Pnc2",
                "Pmn21","Pba2","Pna21","Pnn2","Cmm2",
                "Cmc21","Ccc2","Amm2","Aem2","Ama2",
                "Aea2","Fmm2","Fdd2","Imm2","Iba2",
                "Ima2","Pmmm","Pnnn","Pccm","Pban",
                "Pmma","Pnna","Pmna","Pcca","Pbam",
                "Pccn","Pbcm","Pmna","Pcca","Pbam",
                "Pbca","Pnma","Cmcm","Cmce","Cmmm",
                "Cccm","Cmme","Ccce","Fmmm","Fddd",
                "Immm","Ibam","Ibca","Imma","P4",
                "P41","P42","P43","I4","I41",
                "P-4","I-4","P4/m","P42/m","P4/n",
                "P42/n","I4/m","I41/a","P422","P4212",
                "P4122","P41212","P4222","P42212","P4322",
                "P43212","I422","I4122","P4mm","P4bm",
                "P42cm","P42nm","P4cc","P4nc","P42mc",
                "P42bc","I4mm","I4cm","I41md","I41cd",
                "P-42m","P-42c","P-421m","P-421c","P-4m2",
                "P-4c2","P-4b2","P-4n2","I-4m2","I-4c2",
                "I-42m","I-42d","P4/mmm","P4/mcc","P4/nbm",
                "P4/nnc","P4/mbm","P4/mnc","P4/nmm","P4/ncc",
                "P42/mmc","P42/mcm","P42/nbc","P42/nnm","P42/mbc",
                "P42/mnm","P42/nmc","P42/ncm","I4/mmm","I4/mcm",
                "I41/amd","I41/acd","P3","P31","P32",
                "R3","P-3","R-3","P312","P321",
                "P3112","P3121","P3212","P3221","R32",
                "P3m1","P31m","P3c1","P31c","P3m",
                "R3c","P-31m","P-31c","P-3m1","P-3c1",
                "R-3m","R-3c","P6","P61","P65",
                "P62","P64","P63","P-6","P6/m",
                "P63/m","P622","P6122","P6522","P6222",
                "P6422","P6322","P6mm","P6cc","P63cm",
                "P63/mc","P-6m2","P-6c2","P-62m","P-62c",
                "P6/mmm","P6/mcc","P63/mcm","P63/mmc","P23",
                "F23","I23","P213","I213","Pm-3",
                "Pn-3","Fm-3","Fd-3","Im-3","Pa-3",
                "Ia-3","P432","P4232","F432","F4132",
                "I432","P4332","P4132","I4132","P-43m",
                "F-43m","I-43m","P-43n","F-43c","I-43d",
                "Pm-3m","Pn-3n","Pm-3n","Pn-3m","Fm-3m",
                "Fm-3c","Fd-3m","Fd-3c","Im-3m","Ia-3d"]

GROUP_ORDER_TABLE1 = [1,2]
GROUP_ORDER_TABLE2 = [1,2,2,2,4,
                     4,4,4,8,4,
                     8,8,3,6,6,
                     6,12]
GROUP_ORDER_TABLE3 = [1,2,2,2,4,2,2,4,4,4,
                     4,8,4,4,8,4,4,4,4,8,
                     8,16,8,8,4,4,4,4,4,4,
                     4,4,4,4,8,8,8,8,8,8,
                     8,16,16,8,8,8,8,8,8,8,
                     8,8,8,8,8,8,8,8,8,8,
                     8,8,16,16,16,16,16,16,32,32,
                     16,16,16,16,4,4,4,4,8,8,
                     4,8,8,8,8,8,16,16,8,8,
                     8,8,8,8,8,8,16,16,8,8,
                     8,8,8,8,8,8,16,16,16,16,
                     8,8,8,8,8,8,8,8,16,16,
                     16,16,16,16,16,16,16,16,16,16,
                     16,16,16,16,16,16,16,16,32,32,
                     32,32,3,3,3,3,6,6,6,6,
                     6,6,6,6,6,6,6,6,6,6,
                     6,12,12,12,12,12,12,6,6,6,
                     6,6,6,6,12,12,12,12,12,12,
                     12,12,12,12,12,12,12,12,12,12,
                     24,24,24,24,12,48,24,12,24,24,
                     24,96,96,48,24,48,24,24,96,96,
                     48,24,24,48,24,96,48,24,96,48,
                     48,48,48,48,192,192,192,192,96,96]

