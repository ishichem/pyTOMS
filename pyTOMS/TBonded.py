# Bonded interaction object. Superclass of bond, angle, and dihedral objects
from .TAtom import TAtom
from .TBondedFF import TBondedFF
from typing import List

class TBonded:
    atoms: List[TAtom] = []
    funcType = 0 # gmx bonded function type
    params: List[float] = [] # bonded interaction parameters e.g. [k, r_eq]
    # mol2Type = "1" # TRIPOS mol2 bond order
    comment = "" # comment line in [bond], [angle] or [dihedral] section
    ifAssigned = False # whether a forcefield is assigned
    ffId = 0 # force field id in LAMMPS

    def __init__():
        return
    
    def get_atomNumbers(self) -> List[int]:
        return [atom.atomNumber for atom in self.atoms]
    
    def toBondedFF(self) -> TBondedFF:
        return
    

    


