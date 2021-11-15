# Bonded interaction object. Superclass of bond, angle, and dihedral objects
from .TAtom import TAtom
from .TBondedType import TBondedType
from typing import List

class TBonded:
    atoms: List[TAtom] = []
    funcType = 0 # gmx bonded function type
    params: List[float] = [] # bonded interaction parameters e.g. [k, r_eq]
    # mol2Type = "1" # TRIPOS mol2 bond order
    comment = "" # comment line in [bond], [angle] or [dihedral] section
    ifAssigned = False # whether a forcefield is assigned
    ffId = 0 # force field id in LAMMPS
    iaName = "" # interaction name: bond, angle, dihedral, etc

    def __init__(self) -> None:
        return
    
    def get_atomNumbers(self) -> List[int]:
        return [atom.atomNumber for atom in self.atoms]
    
    def toBondedType(self) -> TBondedType:
        bondedType = TBondedType()
        bondedType.bondedTypes = [atom.bondedType for atom in self.atoms]
        bondedType.funcType = self.funcType
        bondedType.params = self.params[:]
        bondedType.iaName = self.iaName
        bondedType.comment = self.comment
        bondedType.ffId = self.ffId
        return bondedType
    
    def getAtomNumbers(self) -> List[int]:
        return [atom.atomNumber for atom in self.atoms]
    
    def assignFF(self, bondedTypes: List[TBondedType], assignWarn = False, overWrite = False) -> None:
        ffs = [bondedType for bondedType in bondedTypes if bondedType.iaName == self.iaName]
        assert len(self.atoms) > 2
        atmtyps = [ atom.bondedType for atom in self.atoms]
        for ff in ffs:
            if len(ff.bondedTypes) < 2:
                continue
            for atmtyp in atmtyps:
                if atmtyp[1] == ff.bondedTypes[1]:
                    flag = 0
                    


    

    


