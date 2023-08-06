"""Ingestor for netmiko_linux_hostname."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-07"
__version__ = "0.9.19"

from netdoc.schemas import device, discoverable
from netdoc import utils


def ingest(log):
    """Processing parsed output."""
    # See https://github.com/netbox-community/devicetype-library/tree/master/device-types # pylint: disable=line-too-long
    vendor = "Linux"
    name = log.parsed_output

    # Parsing hostname
    name = utils.normalize_hostname(name)

    # Get or create Device
    data = {
        "name": name,
        "site_id": log.discoverable.site.id,
        "manufacturer": vendor,
    }
    device_o = device.get(name=data.get("name"))
    if not device_o:
        device_o = device.create(**data)

    # Link Device to Discoverable
    discoverable.update(log.discoverable, device_id=device_o.id)

    # Update the log
    log.ingested = True
    log.save()
