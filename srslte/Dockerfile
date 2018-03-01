#/*******************************************************************************
# * 
# *  This file is part of the scientific research and development work conducted
# *  at the Communication Networks Institute (CNI), TU Dortmund University.
# *  
# *  Copyright (C) 2018 Communication Networks Institute (CNI)
# *  Technische Universität Dortmund
# *
# *  Contact: kn.etit@tu-dortmund.de    
# *  Authors: Fabian Eckermann and Philipp Gorczak 
# *           {fabian.eckermann, philipp.gorczak}@tu-dortmund.de
# *
# *  This program is free software: you can redistribute it and/or modify
# *  it under the terms of the GNU Lesser General Public License as published by
# *  the Free Software Foundation in version 3 of the License
# *   
# *  This program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *   
# *  You should have received a copy of the GNU Lesser General Public License
# *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# *
# *  For more information on this software, see the institute's project website at: 
# *  http://www.cni.tu-dortmund.de
# *
#*******************************************************************************/

ARG UBUNTU_VERSION=xenial

# Intermediate builder container
FROM ubuntu:${UBUNTU_VERSION} as builder
ARG UBUNTU_VERSION
ARG SRSLTE_REPO=https://github.com/srsLTE/srsLTE
ARG SRSLTE_CHECKOUT=master

# Install build dependencies
# warning: pulled libboost-all-dev because libboost(-dev) alone left
# cmake unable to find boost when building the makefiles for srsUE
RUN echo "deb http://ppa.launchpad.net/ettusresearch/uhd/ubuntu \
          ${UBUNTU_VERSION} main" > /etc/apt/sources.list.d/uhd-latest.list \
 && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6169358E \
 && apt-get update \
 && apt-get install -y \
      build-essential \
      git \
      cmake \
      libuhd-dev \
      uhd-host \
      libboost-all-dev \
      libvolk1-dev \
      libfftw3-dev \
      libmbedtls-dev \
      libsctp-dev \
      libconfig++-dev \
 && rm -rf /var/lib/apt/lists/*

# Clone repo and build
RUN mkdir /srslte \
 && cd /srslte \
 && git clone $SRSLTE_REPO srslte \
 && cd srslte \
 && git checkout $SRSLTE_CHECKOUT \
 && cd .. \
 && mkdir build \
 && cd build \
 && cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/srslte ../srslte \
 && make install


# Final container
FROM ubuntu:${UBUNTU_VERSION}
ARG UBUNTU_VERSION

# Install runtime dependencies
RUN echo "deb http://ppa.launchpad.net/ettusresearch/uhd/ubuntu \
          ${UBUNTU_VERSION} main" > /etc/apt/sources.list.d/uhd-latest.list \
 && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6169358E \
 && apt-get update \
 && apt-get install -y \
      uhd-host \
      libuhd003 \
      libvolk1.1 \
      libfftw3-3 \
      libmbedtls10 \
      libsctp1 \
      libconfig++9v5 \
 && python /usr/lib/uhd/utils/uhd_images_downloader.py \
 && rm -rf /var/lib/apt/lists/*

# Get compiled srsLTE
COPY --from=builder /opt/srslte /opt/srslte

RUN touch /tmp/enb.log \
 && touch /tmp/ue.log

# Set up paths
ENV LD_LIBRARY_PATH /opt/srslte/lib:$LD_LIBRARY_PATH
ENV PATH /opt/srslte/bin:$PATH

WORKDIR /conf