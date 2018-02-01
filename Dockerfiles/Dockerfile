# This file is part of the dune-community/Dockerfiles project:
#   https://github.com/dune-community/Dockerfiles
# Copyright 2017 dune-community/Dockerfiles developers and contributors. All rights reserved.
# License: Dual licensed as BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)
#      or  GPL-2.0+ (http://opensource.org/licenses/gpl-license)
# Authors:
#   Felix Schindler (2017)

FROM dunecommunity/arch-full-interactive

MAINTAINER Felix Schindler <felix.schindler@wwu.de>

RUN pacman -Syyuu --noconfirm && \
    pacman -S --noconfirm less openmpi

# clean up, there might be some leftovers
RUN pacman -Rns --noconfirm $(pacman -Qtdq) || echo "no orphans present" && \
    pacman -Sc --noconfirm

RUN export USERNAME_=user && \
    export UID_=1000 && \
    export GID_=$UID_ && \
    groupadd -g $GID_ $USERNAME_ && \
    useradd -md /home/$USERNAME_ -g $GID_ -s /bin/bash -u $UID_ $USERNAME_ && \
    chown -R $USERNAME_:$GID_ /home/$USERNAME_ && \
    echo "$USERNAME_ ALL=(ALL) NOPASSWD:/usr/bin/pacman" >> /etc/sudoers

ADD bashrc /home/user/.bashrc
ADD bash_profile /home/user/.bash_profile
RUN chown -R user:user /home/user

USER user
WORKDIR /home/user
ENV LANG en_US.UTF-8
ENV OPTS gcc-relwithdebinfo
RUN git clone https://github.com/ftschindler-work/compressible-ns.git && \
    cd compressible-ns && \
    git submodule update --init --recursive
RUN cd compressible-ns/arch-full && \
    source $PWD/PATH.sh && \
    cd $BASEDIR && \
    ./local/bin/download_external_libraries.py && \
    ./local/bin/build_external_libraries.py
RUN cd compressible-ns/arch-full && \
    source $PWD/PATH.sh && \
    cd $BASEDIR && \
    ./dune-common/bin/dunecontrol --opts=config.opts/$OPTS --builddir=$INSTALL_PREFIX/../ all

USER root

ADD entrypoint.sh /usr/local/bin/
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

