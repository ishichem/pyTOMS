from typing import Dict, List, Iterable
from .TMolecule import TMolecule
from .TAtomType import TAtomType
from .TBondedType import TBondedType
from .TBond import TBond
from .TAngle import TAngle
from .TDihedral import TDihedral
import copy

def hoge(x):
    print(x)
    if type(x) == int:
        return 2
    else:
        return x

class TSystem:
    __mols: List[TMolecule] = []
    atomTypes: List[TAtomType] = []
    bondedTypes: List[TBondedType] = []
    fudgeLJ = 0
    fudgeQQ = 0.0
    boxTensor = [0.0,0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0]
        # gromacs box tensor for the cell (nm). [xx, yy, zz, ...]
    crossBonds: List[TBond] = [] # bonds between different molecules
    crossAngles: List[TAngle] = []
    crossDihedrals: List[TDihedral] = []
    __maxSubatomNr = 0 # largest TAtom.subatomNumbers in the system



    def molecules(self) -> Iterable[TMolecule]:
        return iter(self.__mols)
    
    def addMolecule(self, mol: TMolecule) -> None:
        nwmol = copy.deepcopy(mol)
        if len(self.__mols) ==0:
            nwmol.moleculeId = 1
        else:
            lmol = self.__mols[-1]
            maxAtomNr = max([a.atomNumber for a in lmol.atoms()])
    
    

