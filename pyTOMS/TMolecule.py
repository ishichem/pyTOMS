from typing import List
from .TAtom import TAtom
from .TBond import TBond

class TMolecule:
    molName = "" # molecule name
    molId = 0 # molecule id used in LAMMPS
    __atoms: List[TAtom] = []
    __bonds: List[TBond] = []


