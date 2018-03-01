"""
Corenet Configuration
"""

# MME Settings
MME_NAME = 'CorenetMME'
MME_CODE = '1a' #HEX value
MME_GROUP = '0001' #HEX value
MCC = '001'
MNC = '01'

DEF_APN = 'corenet' # default APN

# list of configured APN
PDN = {'corenet': {
            'IP':[1, '0.0.0.0'], # PDN type (1:IPv4, 2:IPv6, 3:IPv4v6), UE IP@ will be set at runtime
            'DNS': '8.8.8.8',
            'QCI': 9, # QoS class id (9: internet browsing), NAS + S1 parameter
            'PriorityLevel': 15, # no priority (S1 parameter)
            'PreemptCap': 'shall-not-trigger-pre-emption', # or 'may-trigger-pre-emption' (S1 parameter)
            'PreemptVuln': 'not-pre-emptable', # 'pre-emptable' (S1 parameter)
            },
        }

SGI_GW_IP = '172.19.99.1' # coresponds to sgi network from docker-compose

# list of UE IMSI and associated IP address and phone number (for SMS)
# those IMSI also need to be configured in AUC DB file
AUC_DB_PATH = '/conf/user_db.csv'
UE = {
    '001010123456789': {'IP': '172.19.100.101', 'Num': '0001'},
    '001010123456780': {'IP': '172.19.100.102', 'Num': '0002'}
}