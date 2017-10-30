```
# This file is part of the compressible-ns project:
#   https://github.com/ftschindler-work/compressible-ns
# Copyright holders: Felix Schindler
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)
```

[compressible-ns](https://github.com/ftschindler-work/compressible-ns)
is a git supermodule which serves as a demonstration for the discretization of
viscid and inviscid compressible flow using [dune-gdt](https://github.com/dune-community/dune-gdt).


# Some notes on required software

* We recommend to use [docker](https://www.docker.com/) to ensure a fixed build environment.
  As a good starting point, take a look at our [Dockerfiles](https://github.com/dune-community/Dockerfiles) repository, which will guide you through the full process of working with docker and DUNE.
  While the compiled shared objects will (most likely) not work on your computer (they only work within the build environment of the container), you will have access to a jupyter notebook server from your computer.
* Compiler: we currently test gcc >= 4.9 and clang >= 3.8, other compilers may also work
* For a list of minimal (and optional) dependencies for several linux distributions, you can take a look our
  [Dockerfiles](https://github.com/dune-community/Dockerfiles) repository, e.g.,
  [debian/Dockerfile.minimal](https://github.com/dune-community/Dockerfiles/blob/master/debian/Dockerfile.minimal)
  for the minimal requirements on Debian jessie (and derived distributions).


# To build everything, do the following

First of all

## 1: checkout the repository and initialize all submodules:

```bash
mkdir -p $HOME/Projects/dune                 # <- adapt this to your needs
cd $HOME/Projects/dune
git clone https://github.com/ftschindler-work/compressible-ns.git
cd compressible-ns
git submodule update --init --recursive
```

The next step depends on wether you are running in a specific docker container or directly on you machine.

## 2.a: Preparations within a docker container

Presuming you followed [these instructions](https://github.com/dune-community/Dockerfiles/blob/master/README.md) to get your docker setup working, and you just started and connected to a docker container by calling

```bash
./docker_run.sh arch-minimal-interactive compressible-ns /bin/bash
```

you are now left with an empty bash prompt (`exit` will get you out of there).
Issue the following commands:

```bash
export OPTS=gcc-relwithdebinfo
cd $HOME/compressible-ns/arch-minimal      # <- this should match the docker container
source PATH.sh                             #                           you are running
cd $BASEDIR
rm external-libraries.cfg ; ln -s arch-minimal/external-libraries.cfg . # <- this also
```

Download and build all external libraries by calling (this _might_ take some time):

```bash
./local/bin/download_external_libraries.py
./local/bin/build_external_libraries.py
```

The next time you start the container you should at least issue the following commands before you start your work:

```bash
export OPTS=gcc-relwithdebinfo
cd $HOME/compressible-ns/arch-minimal
source PATH.sh
```

## 2.b: Preparations on your machine

* Take a look at `config.opts/` and find settings and a compiler which suits your system, e.g. `config.opts/gcc`.
  The important part to look for is the definition of `CC` in these files: if, e.g., you wish to use clang in version 3.8 and clang is available on your system as `clang-3.8`, choose `OPTS=clang-3.8`; if it is available as `clang`, choose `OPTS=clang`.
  Select one of those options by defining

  ```bash
  export OPTS=gcc-relwithdebinfo
  ```

* Call

  ```bash
  ./local/bin/gen_path.py
  ```

  to generate a file `PATH.sh` which defines a local build environment. From now on you should source this file
  whenever you plan to work on this project, e.g. (depending on your shell):

  ```bash
  source PATH.sh
  ```

* Download and build all external libraries by calling (this _might_ take some time):

  ```bash
  ./local/bin/download_external_libraries.py
  ./local/bin/build_external_libraries.py
  ```

* To allow DUNE to find some of the locally built dependencies, you need to set the `CMAKE_INSTALL_PREFIX` by either

  - calling

    ```bash
    echo "CMAKE_FLAGS=\"-DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} "'${CMAKE_FLAGS}'"\"" >> config.opts/$OPTS
    ```

    to set this permanently,

  - or by calling

    ```bash
    export CMAKE_FLAGS="-DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX} ${CMAKE_FLAGS}"
    ```

    to set this temporarily (recommended).

## 3: Build all DUNE modules

Using `cmake` and the selected options (this _will_ take some time):

```bash
./dune-common/bin/dunecontrol --opts=config.opts/$OPTS --builddir=$INSTALL_PREFIX/../build-$OPTS all
```

This creates a directory corresponding to the selected options (e.g. `build-gcc-relwithdebinfo`) which contains a subfolder for each DUNE module.

