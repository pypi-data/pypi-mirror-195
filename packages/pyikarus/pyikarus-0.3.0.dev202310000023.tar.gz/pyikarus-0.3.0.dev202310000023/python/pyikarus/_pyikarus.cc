// SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
// SPDX-License-Identifier: LGPL-3.0-or-later

#include <dune/python/common/typeregistry.hh>
#include <dune/python/pybind11/eigen.h>
#include <dune/python/pybind11/pybind11.h>

#include <pyikarus/finiteElements/feRequirements.hh>

PYBIND11_MODULE(_pyikarus, m) {
  namespace py = pybind11;
  using namespace pybind11::literals;
  using namespace Ikarus;
  using namespace Eigen;

  py::enum_<ScalarAffordances> enumSA(m, "ScalarAffordances");
  enumSA.value("noAffordance", ScalarAffordances::noAffordance);
  enumSA.value("mechanicalPotentialEnergy", ScalarAffordances::mechanicalPotentialEnergy);
  enumSA.value("microMagneticPotentialEnergy", ScalarAffordances::microMagneticPotentialEnergy);

  py::enum_<FESolutions> feSol(m, "FESolutions");
  feSol.value("noSolution", FESolutions::noSolution);
  feSol.value("displacement", FESolutions::displacement);
  feSol.value("velocity", FESolutions::velocity);
  feSol.value("director", FESolutions::director);
  feSol.value("magnetizationAndVectorPotential", FESolutions::magnetizationAndVectorPotential);

  py::enum_<FEParameter> fePar(m, "FEParameter");
  fePar.value("noParameter", FEParameter::noParameter);
  fePar.value("loadfactor", FEParameter::loadfactor);
  fePar.value("time", FEParameter::time);

  using FEreq   = FErequirements<Ref<VectorXd>>;
  auto includes = Dune::Python::IncludeFiles{"ikarus/finiteElements/feRequirements.hh"};
  auto lv       = Dune::Python::insertClass<FEreq>(
                m, "FErequirements", Dune::Python::GenerateTypeName("FErequirements<Eigen::Ref<Eigen::VectorXd>>"),
                includes)
                .first;
  lv.def(py::init());
  lv.def("addAffordance", [](FEreq& req, const ScalarAffordances& affordances) { req.addAffordance(affordances); });
  lv.def(
      "insertGlobalSolution",
      [](FEreq& req, FESolutions solType, Ref<VectorXd> solVec) {
        req.insertGlobalSolution(std::move(solType), solVec);
      },
      py::arg("solutionType"), py::arg("solutionVector").noconvert());
  lv.def(
      "getGlobalSolution", [](FEreq& req, FESolutions solType) { return req.getGlobalSolution(std::move(solType)); },
      py::return_value_policy::reference_internal);
  lv.def("insertParameter",
         [](FEreq& req, FEParameter parType, double& parVal) { req.insertParameter(std::move(parType), parVal); });
}
