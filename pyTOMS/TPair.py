from .TBonded import TBonded

class TPair(TBonded):
    def __init__(self) -> None:
        super().__init__()
        self.iaName = "pair"