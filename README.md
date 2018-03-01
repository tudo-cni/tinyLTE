# tinyLTE

tinyLTE is a low cost, lightweight autonomous LTE network, building upon
virtualization techniques and open source software stacks. It is a pragmatic approach for building standalone LTE cells with off the shelf software defined radio (SDR) hardware.

The following software is virtualized:
* [srsLTE](https://github.com/srsLTE/srsLTE) by [SRS](http://www.softwareradiosystems.com)
* [corenet](https://github.com/tudo-cni/corenet) by [Benoit Michau](https://github.com/mitshell)

There are two types of containers: one for infrastructure (op) and one for network clients (ue). Infrastructure containers deploy a base station backed by a local core network (eNB + EPC), while clients act as LTE user devices (UE). A host can be both infrastructure and client at the same time if it has access to two SDRs. The setup has been developed and tested with *USRP B210* SDRs.

## Getting started

Install [Docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/). Make sure your installed version of docker-compose is >1.13.0.

## Run

Change either into tinyLTE-op or tinyLTE-ue directory, then start it with:

    docker-compose up

**NOTE:** If your user is not a member of the docker group this command must be run with sudo.


To enable the overlay network on the host machine run:

**Stationary tinyLTE node:**

    sudo python3 configure_host.py corenet_tun_conf

**UE node:**

    sudo python3 configure_host.py corenet_tun_conf_ue


## Configuration

tinyLTE opens point-to-point tunnels between eNBs and UEs. The tunnel endpoints are identified with virtual IP-addresses in an overlay network.

### UE IP-Assignment
UEs get IP addresses assigned by corenet. Mapping of IPs is defined in
corenet_conf.py. They are assigned from `172.19.100.100` upwards.

### Overlay network
Each node in the overlay network is identified by a virtual IP. It relates to its corenet-assigned IP by replacing the third byte by `200`. So
`172.19.100.101` maps to `172.19.200.101`. The stationary tinyLTE node that is directly connected to the internet, has `172.19.200.1`. Tunnels connect nodes in the `172.19.200.0/24` network via GTP. The dummy interface representing the tunnel endpoint at the stationary tinyLTE node has IP `172.19.100.1`. The IP adresses of the network overlay can be customized within the *corenet_tun_conf* files.

* GTPFake sets routing within the corenet container
* configure_host.py creates tunnels/routing on host machine

## Cite as
* [**tinyLTE: Lightweight, Ad Hoc Deployable Cellular Network for Vehicular Communication**](https://arxiv.org/abs/1802.09262) *IEEE Vehicular Technology Conference (VTC-Spring)*
