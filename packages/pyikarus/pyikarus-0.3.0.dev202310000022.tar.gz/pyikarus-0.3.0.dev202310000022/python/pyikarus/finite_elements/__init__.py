# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later

from dune.generator.generator import SimpleGenerator
from dune.common.hashit import hashIt
import dune

def decoratePre(pre):
    def wrappedPre(*args, **kwargs):
        preamble = pre(*args, **kwargs)
        newPreamble = ""
        for line in preamble.split("\n"):
            newPreamble += line + "\n"
            newPreamble += "#define DUNE_LOCALFEFUNCTIONS_USE_EIGEN 1 \n"
            newPreamble += "#define EIGEN_DEFAULT_TO_ROW_MAJOR 1 \n" #needed to have conforming Matrix storage between eigen and numpy otherwise references are not working
        return newPreamble

    return wrappedPre


myAttributes = vars(SimpleGenerator).copy()
myAttributes["pre"] = decoratePre(myAttributes["pre"])
MySimpleGenerator = type("MySimpleGenerator", (object,), myAttributes)


def linearElasticElement(basis, element, youngsMod, nu) :
    dune.generator.addToFlags(pre="-DCMAKE_PREFIX_PATH=/dune/dune-fufem ")
    generator = MySimpleGenerator("LinearElastic", "Ikarus::Python")
    element_type = f"Ikarus::LinearElastic<{basis.cppTypeName},Ikarus::FErequirements<Eigen::Ref<Eigen::VectorXd>>,true>"

    includes = []
    includes += ["pyikarus/finiteElements/mechanics/linearElastic.hh"]
    includes += ["pyikarus/python/finiteElements/linearElastic.hh"]
    moduleName = "linearElastic_" + hashIt(element_type)
    module = generator.load(
        includes=includes,
        typeName=element_type,
        moduleName=moduleName
    )
    return module.LinearElastic(basis, element, youngsMod, nu)
