# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later

import setpath
setpath.set_path()
import pyikarus as iks
import pyikarus.finite_elements
import numpy as np

import dune.grid
import dune.functions

if __name__ == "__main__":
    # help(iks)
    lowerLeft = []
    upperRight = []
    elements = []
    for i in range(2):
        lowerLeft.append(-1)
        upperRight.append(1)
        elements.append(3)

    req= pyikarus.FErequirements()
    req.addAffordance(iks.ScalarAffordances.mechanicalPotentialEnergy)

    grid = dune.grid.structuredGrid(lowerLeft,upperRight,elements)
    basisLagrange1 = dune.functions.defaultGlobalBasis(grid, dune.functions.Power(dune.functions.Lagrange(order=1),2))

    d = np.zeros(len(basisLagrange1))
    d[0]=0.1

    req.insertParameter(iks.FEParameter.loadfactor,3)
    req.insertGlobalSolution(iks.FESolutions.displacement,d)

    d2= req.getGlobalSolution(iks.FESolutions.displacement)

    assert ('{}'.format(hex(d2.__array_interface__['data'][0]))) == ('{}'.format(hex(d.__array_interface__['data'][0])))
    assert len(d2)== len(d)
    assert d2[0]== d[0]
    fes = []

    forces = np.zeros(8)
    stiffness = np.zeros((8,8))
    for e in grid.elements:
        fes.append(iks.finite_elements.linearElasticElement(basisLagrange1,e,1000,0.2))
        print(fes[0].calculateScalar(req))
        fes[0].calculateVector(req,forces)
        fes[0].calculateMatrix(req,stiffness)
        print("forces: ",forces)
        print("stiffness: ",stiffness)
        # print(fes[0].getMaterialTangent())
        # localview = fes[0].localView()
        # localview.bind(e)
