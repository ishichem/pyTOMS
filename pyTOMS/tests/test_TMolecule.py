from ..TMolecule import TMolecule
import numpy as np
import os

dn = os.path.dirname(__file__) + "/samples"
print(dn)

def test_readMol2():
    fn = "acetamide.mol2"
    mol = TMolecule()
    mol.readMol2(dn+"/"+fn)
    mol.labelAtom()
    #-- atoms
    assert mol.moleculeName == "acetamide"
    assert mol.natom() == 9
    atom2 = mol.getAtom(2)
    assert atom2.atomName == "N"
    assert atom2.atomLabel == "N"
    assert atom2.atomNumber == 3
    assert atom2.xyz[1] == -0.2276
    assert atom2.residueName == "UNL1"
    assert atom2.charge == -0.3295
    atom7 = mol.getAtom(7)
    assert mol.atomNumberToAtom(8) == atom7
    assert atom7.atomLabel == "H3"
    #-- bonds
    assert len(mol.bonds) == 8
    bond2 = mol.bonds[2]
    assert bond2.atoms[0].atomNumber == 2
    assert bond2.atoms[1].atomNumber == 4
    assert bond2.mol2Type == "2"
    #-- angles
    assert len(mol.angles) == 12
    #-- dihedrals
    propers = [dih for dih in mol.dihedrals if dih.functionType == 1]
    impropers = [dih for dih in mol.dihedrals if dih.functionType == 4]
    assert len(propers) == 10
    assert len(impropers) == 2
    #-- pairs
    assert len(mol.pairs) == 10

