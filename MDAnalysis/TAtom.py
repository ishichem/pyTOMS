import numpy as np


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

        self.atmno=0
        self.element="" # element name C, SI, O, C, C, ...
        self.atmname="" # atom name C, Si, O, C, C, ...  not include numbering
        self.atmlb="" # atom lable C, Si, O, C1, C2, ... includes numbering: see TMol.labelatm()
        self.xyz=[0.0,0.0,0.0] # in Angstrome
        self.xyzs=[] # trajectory [ [xyz], [xyz], ... ]
        self.v=[0.0,0.0,0.0] # nm/ps
        self.vs=[] # trajectory nm/ps
        self.mol2typ=""
        self.cg=0.0
        self.cgno=0 # charge group number
        self.resname=""
        self.resno=0
        self.mass=0.0
        self.bondedtyp=""
        self.nonbondedtyp=""
        self.nbtypid=0
        self.maptyp=""
        self.subatms=[]
        self.cgweight=0 # the weight in CG mapping
        self.comment=""
        self.params=[]
        self.ptyp=""