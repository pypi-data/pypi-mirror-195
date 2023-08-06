"""Ingestor for netmiko_cisco_ios_show_vrf."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-07"
__version__ = "0.9.19"

from netdoc.schemas import vrf


def ingest(log):
    """Processing parsed output.

    VRF - Interface association is ingested in the "show ip interface" output.
    """
    for item in log.parsed_output:
        # See https://github.com/networktocode/ntc-templates/tree/master/tests/cisco_ios/show_vrf # pylint: disable=line-too-long
        vrf_name = item.get("name")
        vrf_rd = item.get("default_rd") if item.get("default_rd") else None

        data = {
            "name": vrf_name,
            "rd": vrf_rd,
        }
        vrf_o = vrf.get(name=vrf_name)
        if vrf_o:
            vrf_o = vrf.update(vrf_o, **data)
        else:
            vrf_o = vrf.create(**data)

    # Update the log
    log.ingested = True
    log.save()
