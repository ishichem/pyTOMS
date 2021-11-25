from typing import List, Dict, Iterator
from .TAtom import TAtom
from .TBond import TBond
from .TAngle import TAngle
from .TDihedral import TDihedral
from .TPair import TPair
from .mass import element2mass
from .utils import warn
import numpy as np
import copy


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
    
    def atoms(self) -> Iterator[TAtom]:
        return iter(self.__atoms)

    def labelAtom(self) -> None:
        tmp: List[str] = []
        for i, atom in enumerate(self.__atoms):
            if i > 0:
                if self.__atoms[i-1].residueNumber != atom.residueNumber:
                    tmp = []
            name = atom.atomName
            num = tmp.count(name)
            if num == 0:
                atmlb = name
            else:
                atmlb = name + str(num)
            tmp.append(name)
            atom.atomLabel = atmlb
        return
    
    def findAngles(self) -> None:
        iangs: List[List[int]] = [] # angle list with duplications
        ibonds: List[List[int]] = [] # bond list
        for bond in self.bonds:
            ibonds.append(bond.getAtomNumbers())
        nbond = len(ibonds)
        for i in range(nbond):
            for k in range(2):
                for j in range(nbond):
                    for l in range(2):
                        if ibonds[i][1-k] == ibonds[j][l] and i != j:
                            #- ibonds[i] and ibonds[j] share the same atom
                            #-   ibonds[i][k]---ibonds[i][1-k]---ibonds[j][1-l]
                            iangs.append([ibonds[i][k], ibonds[i][1-k], ibonds[j][1-l]])
        #-- remove duplications
        nang = len(iangs)
        save = list(range(nang))
        for i in range(nang - 1):
            for j in range(i+1, nang, 1):
                if iangs[i] == list(reversed(iangs[j])):
                    save.remove(j)
        for s in save:
            angle = TAngle()
            angle.funcType = 1
            angle.atoms = [self.atomNumberToAtom(nr) for nr in iangs[s]]
            self.angles.append(angle)
        return
    
    def findDihedrals(self, removeImpropers = False) -> None:
        idihs: List[List[int]] = [] # dihedrals with duplications
        ibonds: List[List[int]] = []
        for bond in self.bonds:
            ibonds.append(bond.getAtomNumbers())
        nbond = len(ibonds)
        for i in range(nbond):
            for k in range(2):
                for j in range(nbond):
                    for l in range(2):
                        if ibonds[i][k] == ibonds[j][l] and i != j:
                            #--    ibonds[i][1-k]---ibonds[i][k]---ibonds[j][1-l]
                            for m in range(nbond):
                                for n in range(nbond):
                                    if (ibonds[i][1-k] == ibonds[m][n] and
                                        i != m and
                                        ibonds[j][1-l] != ibonds[m][1-n]):
                                        #--   ibonds[m][1-n]---ibonds[i][1-k]---ibonds[i][k]---ibonds[j][1-l]
                                        idihs.append([ibonds[m][1-n], ibonds[i][1-k], ibonds[i][k], ibonds[j][1-l]])
        #-- remove duplications
        ndih = len(idihs)
        if ndih == 0:
            return
        save = list(range(ndih))
        for i in range(ndih-1):
            for j in range(j+1, ndih):
                if idihs[i] == list(reversed(idihs[j])):
                    save.remove(j)
        if removeImpropers == True:
            #-- remove dihedrals with aromatic rings or double bonds
            for k in range(nbond):
                bondType = self.bonds[k].mol2Type
                if bondType in ["ar", "2"]:
                    for m in range(2):
                        for i in range(ndih):
                            if (idihs[i][1] == ibonds[k][m] and
                                idihs[i][2] == ibonds[k][1-m]):
                                save.remove(i)
            #-- remove dihedrals in pi conjugate
            flag1, flag2 = 0, 0
            for i, idih in enumerate(idihs):
                for k in range(nbond):
                    bondType = self.bonds[k].mol2Type
                    if bondType == "2":
                        for m in range(2):
                            if ibonds[k][m] == idih[1]:
                                flag1 += 1
                            if ibonds[k][m] == idih[2]:
                                flag2 += 1
                if flag1 > 0 and flag2 > 0:
                    save.remove(i)
                    flag1, flag2 = 0, 0 
        for s in save:
            dihedral = TDihedral()
            dihedral.funcType = 1
            dihedral.atoms = [self.atomNumberToAtom(nr) for nr in idihs[s]]
        return

    def findImpropers(self) -> None:
        ibonds: List[List[int]] = []
        for bond in self.bonds:
            ibonds.append(bond.getAtomNumbers())
        iimps: List[List[int]] = []
        nbond = len(self.bonds)
        for atom in self.atoms():
            center = atom.atomNumber
            iimp = [center]
            for ibond in ibonds:
                for m in range(2):
                    if ibond[m] == center:
                        iimp.append(ibond[1-m])
            if len(iimp) == 4: # i.e. 3 bonds connected to one atom
                iimps.append(iimp)
        for iimp in iimps:
            improper = TDihedral()
            improper.funcType = 4
            improper.atoms = [self.atomNumberToAtom(nr) for nr in iimp]
            self.dihedrals.append(improper)
        return

    def findPairs(self) -> None:
        mol = copy.deepcopy(self)
        mol.dihedrals = []
        mol.findDihedrals()
        if len(mol.dihedrals) == 0:
            return
        for dih in mol.dihedrals:
            pair = TPair()
            pair.funcType = 1
            pair.atoms = [dih.atoms[0], dih.atoms[1]]
            self.pairs.append(pair)
        return
    
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
            bond.funcType = 1
            self.bonds.append(bond)
        self.labelAtom()
        self.findAngles()
        self.findDihedrals()
        self.findImpropers()
        self.findPairs()
        return


    




