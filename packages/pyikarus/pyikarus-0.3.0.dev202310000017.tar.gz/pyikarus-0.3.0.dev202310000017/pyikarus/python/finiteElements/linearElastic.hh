// SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
// SPDX-License-Identifier: LGPL-3.0-or-later

#pragma once

#include <dune/functions/functionspacebases/lagrangebasis.hh>
#include <dune/functions/functionspacebases/powerbasis.hh>
#include <dune/grid/yaspgrid.hh>
#include <dune/python/common/typeregistry.hh>
#include <dune/python/pybind11/eigen.h>
#include <dune/python/pybind11/pybind11.h>
#include <dune/python/pybind11/stl.h>

#include <pyikarus/finiteElements/feRequirements.hh>

namespace Ikarus::Python {

  // Python wrapper for the FVAssembler C++ class
  template <class LinearElastic, class... options>
  void registerLinearElastic(pybind11::handle scope, pybind11::class_<LinearElastic, options...> cls) {
    using pybind11::operator""_a;
    //  static_assert(sizeof...(options)==1);
    //  using Problem = typename FVAssembler::Problem;
    using GlobalBasis    = typename LinearElastic::GlobalBasis;
    using Element        = typename LinearElastic::Element;
    using LocalView      = typename LinearElastic::LocalView;
    using FErequirements = typename LinearElastic::FERequirementType;
    //  using GridVariables = typename FVAssembler::GridVariables;
    //  using SolutionVector = typename FVAssembler::SolutionVector;

    cls.def(pybind11::init([](const GlobalBasis& basis, const Element& element, double emod, double nu) {
              return new LinearElastic(basis, element, emod, nu);
            }),
            pybind11::keep_alive<1, 2>(), pybind11::keep_alive<1, 3>());

    //  cls.def_property_readonly("localView", [](LinearElastic& self){
    //    return self.localView();
    //  });

    cls.def(
        "localView", [](LinearElastic& self) { return self.localView(); }, pybind11::return_value_policy::reference);
    cls.def("calculateScalar",
            [](LinearElastic& self, const FErequirements& req) { return self.calculateScalar(req); });
    cls.def("calculateVector", [](LinearElastic& self, const FErequirements& req, Eigen::Ref<Eigen::VectorXd> vec) {
      return self.calculateVector(req, vec);
    });
    cls.def(
        "calculateMatrix",
        [](LinearElastic& self, const FErequirements& req, Eigen::Ref<Eigen::MatrixXd> mat) {
          return self.calculateMatrix(req, mat);
        },
        pybind11::arg("FErequirements"), pybind11::arg("elementMatrix").noconvert());

    //  // TODO assembler with time loop
    //
    //  cls.def_property_readonly("numDofs", &FVAssembler::numDofs);
    //  cls.def_property_readonly("problem", &FVAssembler::problem);
    //  cls.def_property_readonly("gridGeometry", &FVAssembler::gridGeometry);
    //  cls.def_property_readonly("gridView", &FVAssembler::gridView);
    //  cls.def_property_readonly("jacobian", &FVAssembler::jacobian);
    //  cls.def_property_readonly("residual", &FVAssembler::residual);
    //  cls.def_property_readonly("prevSol", &FVAssembler::prevSol);
    //  cls.def_property_readonly("isStationaryProblem", &FVAssembler::isStationaryProblem);
    //  cls.def_property_readonly("gridVariables", [](FVAssembler& self) { return self.gridVariables(); });

    cls.def("getMaterialTangent", [](LinearElastic& self) { return self.getMaterialTangent(); });

    //  cls.def("assembleJacobianAndResidual", [](FVAssembler& self, const SolutionVector& curSol){
    //    self.assembleJacobianAndResidual(curSol);
    //  });
  }

}  // namespace Ikarus::Python
