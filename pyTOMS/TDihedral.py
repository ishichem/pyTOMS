from .TBonded import TBonded

class TDihedral(TBonded):
    def __init__(self) -> None:
        super().__init__()
        self.iaName = "dihedral"