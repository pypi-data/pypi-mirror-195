# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later

from dune.generator.generator import SimpleGenerator
from dune.common.hashit import hashIt
from dumux.wrapping import cppWrapperCreator, cppWrapperClassAlias


def FlatAssembler(fe_vector, basis)
