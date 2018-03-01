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

FROM python:2

RUN apt-get update \
 && apt-get install -y \
      git \
      libmnl-dev \
      libsctp-dev \
      net-tools \
 && rm -rf /var/lib/apt/lists/*

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr
RUN git clone https://github.com/tudo-cni/corenet \
 && cd corenet \
 && git checkout 6e5ac28bda22b6d66414aff4b010584b626d2223 \
 && mv gtp_tunnel_mgmt.sh /usr/local/bin/

WORKDIR /usr/corenet/deps
RUN git config --global advice.detachedHead false

RUN git clone http://git.osmocom.org/libgtpnl
RUN cd libgtpnl \
 && autoreconf -i && ./configure \
 && make && make install \
 && cd tools \
 && make gtp-tunnel && cp gtp-tunnel /usr/bin/gtp-tunnel \
 && make gtp-link && cp gtp-link /usr/bin/gtp-link

RUN git clone https://github.com/mitshell/CryptoMobile \
  && cd CryptoMobile \
  && git checkout 240e288f926b834152e30c9339c2822033bf1a86

RUN cd CryptoMobile \
 && gcc -c -O2 -fPIC Kasumi.c -o Kasumi.o && gcc -shared -o Kasumi.so Kasumi.o \
 && gcc -c -O2 -fPIC SNOW_3G.c -o SNOW_3G.o && gcc -shared -o SNOW_3G.so SNOW_3G.o \
 && gcc -c -O2 -fPIC ZUC.c -o ZUC.o && gcc -shared -o ZUC.so ZUC.o
RUN python -c "from CryptoMobile.test import * ; testall()"

RUN git clone https://github.com/tudo-cni/libmich \
 && cd libmich \
 && git checkout 7f313545eef4af0b7ae47f8f56ebbbbbac80dee6 \
 && python setup.py install

WORKDIR /usr/corenet

ENV PYTHONPATH $PYTHONPATH:/conf


