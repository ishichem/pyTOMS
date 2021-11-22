from typing import List, Dict
from .TAtom import TAtom
from .TBond import TBond
from .TAngle import TAngle
from .TDihedral import TDihedral
from .TPair import TPair
from .mass import element2mass
from .utils import warn
import numpy as np


class TMolecule:
    moleculeName = "" # molecule name
    moleculeId = 0 # molecule id used in LAMMPS
    __atoms: List[TAtom] = []
    bonds: List[TBond] = []
    angles: List[TAngle] = []
    dihedrals: List[TDihedral] = []
    pairs: List[TPair] = []
    pairsNb: List[TPair] = [] # gmx [pairs_nb] directive
    box = np.zeros([9], dtype = "float")
        # gmx box tensor in [nm]
        # [xx,yy,zz, xy,xz, yx,yz, zx,zy ]
    __nr2atom: Dict[int, TAtom] = {}
    
    def __init__(self) -> None:
        return

    def getAtom(self, i: int) -> TAtom:
        return self.__atoms[i]
    
    def atomNumberToAtom(self, atomNumber: int) -> TAtom:
        return self.__nr2atom[atomNumber]
    
    def addAtom(self, atom: TAtom) -> None:
        self.__atoms.append(atom)
        self.__nr2atom[atom.atomNumber] = atom
    
    def readMol2(self, fn: str, setMass = True) -> None:
        f = open(fn, "r")
        natom, nbond = 0, 0
        ibondss: List[List[int]] = [] # a list of atom numbers for bonds
        bondTypes: List[str] = [] # bond orders: "1", "2", "3", "ar", etc
        rline = f.readline()
        while rline:
            if "@<TRIPOS>MOLECULE" in rline:
                rline = f.readline()
                self.moleculeName = str(rline).strip()
                rline = f.readline()
                row = str(rline).split()
                natom = int(row[0])
                nbond = int(row[1])
            elif "@<TRIPOS>ATOM" in rline:
                j = 0
                while j < natom:
                    #      1 O           0.0000    0.0000    0.0000 O.3     1  UNL1        0.0000
                    atom = TAtom()
                    row = str(rline).split()
                    atom.atomNumber = int(row[0])
                    atom.atomName = row[1]
                    atom.xyz = np.array([row[2], row[3], row[4]], dtype = "float64")
                    atom.mol2Type = row[5]
                    atom.residueNumber = int(row[6])
                    atom.residueName = row[7]
                    atom.charge = float(row[8])
                    atom.chargeGroupNumber = atom.atomNumber
                    if setMass:
                        elem = atom.atomName.upper()
                        if elem in element2mass:
                            atom.mass = element2mass[elem]
                            atom.element = elem
                        else:
                            warn(f"Unknown element {elem}. Mass wasn't set!")
                    self.addAtom(atom)
                    rline = f.readline()
                    j += 1
            elif "@<TRIPOS>BOND" in rline:
                j = 0
                while j < nbond:
                    #     1    11     6    1
                    row = str(rline).split()
                    ibondss.append( [int(row[1]), int(row[2])] )
                    bondTypes.append(row[3])
                    j += 1
                    rline = f.readline()          
            rline = f.readline()              
        f.close()
        for i, ibonds in enumerate(ibondss):
            bond = TBond()
            bond.atoms = [self.atomNumberToAtom(atomNr) for atomNr in ibonds]
            bond.mol2Type = bondTypes[i]
            self.bonds.append(bond)
        self.labelAtom()
        self.findAngles()
        self.findDihedrals()
        self.findImpropers()
        self.findPairs()
        return


    




