from .TBonded import TBonded

class TBond(TBonded):
    mol2Type = "" # bond order in tripos mol2 file
    def __init__(self) -> None:
        super().__init__()
        self.iaName = "bond"
        