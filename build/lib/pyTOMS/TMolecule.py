from typing import List, Dict
from .TAtom import TAtom
from .TBond import TBond
from .TAngle import TAngle
from .TDihedral import TDihedral
from .TPair import TPair
import numpy as np

class TMolecule:
    molName = "" # molecule name
    molId = 0 # molecule id used in LAMMPS
    __atoms: List[TAtom] = []
    __bonds: List[TBond] = []
    __angles: List[TAngle] = []
    __dihedrals: List[TDihedral] = []
    __pairs: List[TPair] = []
    __pairsNb: List[TPair] = [] # gmx [pair_nb] directive
    box = np.zeros([9], dtype = "float")
        # gmx box tensor in [nm]
        # [xx,yy,zz, xy,xz, yx,yz, zx,zy ]
    __atomNr2atom: Dict[int, TAtom] = {}
    
    def __init__(self) -> None:
        return
    




