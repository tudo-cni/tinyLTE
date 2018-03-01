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

import fcntl
import importlib
import shlex
import socket
import struct
import subprocess
import sys


def check_call(cmd):
    try:
        subprocess.check_call(shlex.split(cmd))
    except subprocess.CalledProcessError as err:
        print('Error calling {}'.format(' '.join(err.cmd)))
        print('    {}'.format(err.output))
        print('    {}'.format(err.returncode))


def add_dummy(dummy_ip):
    """Add dummy Interface"""
    check_call('ip link add name host_dummy type dummy')
    check_call('ip address add dev host_dummy {}'.format(dummy_ip))


def tunnel_to_ue(ue_ip, virtual_enb_ip, virtual_ue_ip, virtual_net_range,
                 own_ip, corenet_ip):
    """ Open a tunnel from eNB host to UE host (eNB side).

    On a node acting as eNB, opens a tunnel to a connected UE.
    The tunnel connects them in a virtual overlay network, in which both get
    dedicated IPs.

    Args:
        ue_ip: the IP assigned to the target UE by corenet.
        virtual_enb_ip: the IP of this host in the overlay network.
        virtual_ue_ip: the IP of the target UE in the overlay network.
        virtual_net_range: the IP-range of the overlay network.
        own_ip: the IP to which the target UE tunnels its packets.
        corenet_ip: the IP of the corenet container.
    """
    check_call('ip tunnel del to_ue')
    check_call('ip tunnel add to_ue mode gre remote {}'.format(ue_ip))
    check_call('ip address add dev to_ue {} peer {}'.format(
        virtual_enb_ip, virtual_ue_ip))
    check_call('ip link set to_ue up')
    check_call('ip route replace {} via {} src {}'.format(
        ue_ip, corenet_ip, own_ip))
    check_call('ip route replace {} dev to_ue'.format(
        virtual_net_range))
    # FIXME run this only if rules don't exist
    check_call('iptables -A FORWARD -o to_ue -j ACCEPT')
    check_call('iptables -A FORWARD -i to_ue -j ACCEPT')


def tunnel_to_enb(virtual_enb_ip, virtual_ue_ip, parent_enb_ip):
    """ Open a tunnel from UE host to eNB host (UE side).

    On a node acting as UE, opens a tunnel to its eNB.
    The tunnel connects them in a virtual overlay network, in which both get
    dedicated IPs.

    Args:
        virtual_enb_ip: the IP of the eNB in the overlay network.
        virtual_ue_ip: the IP of this host in the overlay network.
        parent_enb_ip: the IP to which the tunnel sends its packets.
    """
    check_call('ip tunnel del to_enb')
    check_call('ip tunnel add to_enb mode gre remote {}'.format(parent_enb_ip))
    check_call('ip address add dev to_enb {} peer {}'.format(virtual_ue_ip, virtual_enb_ip))
    check_call('ip link set to_enb up')
    check_call('ip route replace default dev to_enb')


def from_virt(virt_ip):
    """Convert virtual IP address to "regular" IP address"""
    temp = virt_ip.split('.')
    temp[2] = '100'
    return '.'.join(temp)


def to_virt(reg_ip):
    """Convert "regular" IP address to virtual IP address"""
    temp = reg_ip.split('.')
    temp[2] = '200'
    return '.'.join(temp)


if __name__ == '__main__':

    try:
        config_name = sys.argv[1]
    except:
        print("Fallback to default config")
        config_name = 'corenet_tun_conf'

    config = importlib.import_module('conf.' + config_name)

    # set DNS to 8.8.8.8
    check_call(r"sed -i '/nameserver */c\nameserver 8.8.8.8' /etc/resolv.conf")

    my_virt_ip = config.OWN_VIRT_IP
    my_enb_virt_ip = config.PARENT_VIRT_IP
    my_ue_virt_ip = config.CHILD_UE_IP

    own_ip = from_virt(my_virt_ip)

    if my_enb_virt_ip:
        parent_enb_ip = from_virt(my_enb_virt_ip)

    if my_ue_virt_ip:
        ue_ip = from_virt(my_ue_virt_ip)

    virtual_net_range = '172.19.200.0/24'
    corenet_ip = '172.19.99.2'

    if my_ue_virt_ip and not my_enb_virt_ip:
        # We are the root eNB
        add_dummy(own_ip)
        tunnel_to_ue(ue_ip, my_virt_ip, my_ue_virt_ip, virtual_net_range,
                     own_ip, corenet_ip)
        check_call('iptables -t nat -A POSTROUTING -s {} ! -o to_ue -j MASQUERADE'.format(
                    virtual_net_range))
        check_call('iptables -A FORWARD -o {} -j ACCEPT'.format(config.EXT_NET_IF))

    if my_enb_virt_ip and not my_ue_virt_ip:
        # We are a UE
        tunnel_to_enb(my_enb_virt_ip, my_virt_ip, parent_enb_ip)

    if my_enb_virt_ip and my_ue_virt_ip:
        # We are a MeNB
        tunnel_to_enb(my_enb_virt_ip, my_virt_ip, parent_enb_ip)
        tunnel_to_ue(ue_ip, my_virt_ip, my_ue_virt_ip, virtual_net_range,
                     own_ip, corenet_ip)
        check_call('iptables -A FORWARD -i {} -j ACCEPT'.format(config.EXT_NET_IF))