# SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later
# this file is modified from dumux https://git.iws.uni-stuttgart.de/dumux-repositories/dumux/-/blob/master/setup.py
from datetime import datetime

try:
    from dune.packagemetadata import metaData
except ImportError:
    from packagemetadata import metaData
from setuptools import find_namespace_packages
from skbuild import setup

# When building a new package, update the version numbers below and run:
# > /dune/dune-common/build-cmake/run-in-dune-env pip install twine
# > /dune/dune-common/build-cmake/run-in-dune-env python setup.py sdist
# > /dune/dune-common/build-cmake/run-in-dune-env python -m twine upload dist/* --verbose
# install locally:  pip install -v --pre --log logfile --find-links file://$PWD/dist ikarus==version

pyikarusVersion = "0.3.0.dev" + datetime.today().time().strftime("%H%M%S")
duneVersion = "2.9.0"

metadata = metaData(duneVersion)[1]
metadata["version"] = pyikarusVersion

metadata["packages"] = find_namespace_packages(where="python", include=["ikarus.*"])

# auto-generate pyproject.toml with duneVersion when building sdist
from skbuild.command.sdist import sdist


class mysdist(sdist):
    def run(self):
        # requires = ["setuptools", "wheel", "scikit-build", "cmake", "ninja", "requests"]
        # requires += metadata["install_requires"]
        # with open("pyproject.toml", "w") as f:
        #     f.write("[build-system]\n")
        #     f.write("requires = ['" + "', '".join(requires) + "']\n")
        #     f.write("build-backend = 'setuptools.build_meta'\n")
        sdist.run(self)


metadata["cmdclass"] = {"sdist": mysdist}
metadata["name"] = "pyikarus"
setup(**metadata)
