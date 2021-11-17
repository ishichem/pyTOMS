from typing import List


class TBondedType():
    #-- class for [bondtypes], [angletypes], etc
    iaName = "" # interaction name, e.g. bond, angle, etc
    bondedTypes: List[str] = [] # atom types for the bonded interaction
    funcType = 0 # gmx bonded functional type
    params: List[float] = [] # parameters, e.g. [1.00, 5.4432]
    comment = "" # comment on the bonded interaction
    defineName = "" # force field defined by #define sentence
    ffId = 0 # force field id used in LAMMPS

    def __init__(self) -> None:
        return
