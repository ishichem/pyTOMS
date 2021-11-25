import numpy as np
from typing import List
from .TAtomType import TAtomType
# from .mass import element2mass

class TAtom:
    atomNumber = 0
    element = "" # element name in CAPITAL letters, C, SI, H, O, ...
    atomName = "" # arbitrary atom name C, Si, O, UA, ...
    atomLabel = "" # atom name + numbering. C, C1, H, C2, H2, ...
    xyz = np.zeros([3], dtype = "float") # cartesian coordinate in nm
    v = np.zeros([3], dtype = "float") # velocity in nm/ps
    mol2Type = "" # TRIPOS mol2 atom type
    charge = 0. # partial charge
    chargeGroupNumber = 0 # charge group number
    residueName = "" # residue name or monomer name
    residueNumber = 0 # residue number
    mass = 0.0
    bondedType = "" # atom type for bonded interactions
    nonbondedType = "" # atom type for non-bonded interaction
    nonbondedId = 0 # LAMMPS atom type id for non-bonded interaction
    mapType = ""
        # CG atom label to specify how to map all-atom geometry to CG one.
        # The same label is used in the title section for mapping definition in VOTCA
    subatomNumbers: List[int] = [] # constituting atoms for the CG atom
    # subatoms = [] # all atom TAtom objects for the CG atom
    mapWeight = 0. # the weight of the atom for CG geometry mapping
    comment = "" # comment in [atoms] section
    params: List[float] = [] # LJ parameters
    particleType = "" # particle type in GROMACS. "A" for atoms.

    def __init__(self) -> None:
        return
    
    def toAtomType(self) -> TAtomType:
        atomType = TAtomType()
        atomType.nonbondedType = self.nonbondedType
        atomType.bondedType = self.bondedType
        atomType.mass = self.mass
        atomType.charge = self.charge
        atomType.particleType = self.particleType
        atomType.params = self.params[:]
        atomType.nonbondedId = self.nonbondedId
        return atomType

