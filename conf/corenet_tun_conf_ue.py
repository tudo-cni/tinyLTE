'''
Tunnel Configuration

Configuration of the overlay network

## tinyLTE stationary configuration example:
# OWN_VIRT_IP = '172.19.200.1'
# PARENT_VIRT_IP = None
# CHILD_UE_IP = '172.19.200.101' # multihop: '172.19.200.102'
# EXT_NET_IF = 'eth0'

## tinyLTE mobile configuration example:
# OWN_VIRT_IP = '172.19.200.102'
# PARENT_VIRT_IP = '172.19.200.1
# CHILD_UE_IP = '172.19.200.101'
# EXT_NET_IF = 'eth0'

## tinyLTE UE configuration example:
# OWN_VIRT_IP = '172.19.200.101'
# PARENT_VIRT_IP = '172.19.200.1' # multihop: '172.19.200.102'
# CHILD_UE_IP =  None
# EXT_NET_IF = None
'''

OWN_VIRT_IP = '172.19.200.101'
PARENT_VIRT_IP = '172.19.200.1'
CHILD_UE_IP =  None
EXT_NET_IF = None