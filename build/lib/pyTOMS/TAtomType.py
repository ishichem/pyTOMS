from typing import List

class TAtomType:
    #-- class implementation of [atomtypes] directive
    nonbondedType = "" # nonbonded atom type
    bondedType = "" # bonded atom type
    mass = 0.0
    charge = 0.0
    particleType = "" # "A" for atom
    params: List[float] = [] # LJ parameters
    nonbondedId = 0 # LAMMPS nonbonded atom type id

    def __init__(self) -> None:
        return
    
