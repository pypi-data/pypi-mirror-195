# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later
add_subdirectory(ikarus)
set(CXX_MAX_STANDARD 20)
configure_file(setup.py.in setup.py)
find_package(dune-common REQUIRED EXCLUDE_FROM_ALL)
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/modules" ${dune-common_MODULE_PATH})
include(DuneMacros)
dune_python_configure_bindings(
  PATH
  "."
  PACKAGENAME
  pyikarus
  CMAKE_METADATA_FLAGS
  DUNE_OPTS_FILE
  CXX_MAX_STANDARD
)
if(POLICY CMP0087)
  cmake_policy(SET CMP0087 NEW)
endif()
