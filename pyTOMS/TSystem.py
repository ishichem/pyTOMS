from typing import Dict, List
from .TMolecule import TMolecule
from .TAtomType import TAtomType
from .TBondedType import TBondedType
from .TBond import TBond
from .TAngle import TAngle
from .TDihedral import TDihedral

class TSystem:
    molecules: List[TMolecule] = []
    atomTypes: List[TAtomType] = []
    bondedTypes: List[TBondedType] = []
    fudgeLJ = 0
    fudgeQQ = 0.0
    boxTensor = [0.0,0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0]
        # gromacs box tensor for the cell (nm). [xx, yy, zz, ...]
    crossBonds: List[TBond] = [] # bonds between different molecules
    crossAngles: List[TAngle] = []
    crossDihedrals: List[TDihedral] = []
    

