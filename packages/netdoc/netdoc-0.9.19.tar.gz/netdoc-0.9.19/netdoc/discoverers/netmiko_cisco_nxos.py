"""Discovery task for Cisco NX-OS devices via Netmiko."""
__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2022, Andrea Dainese"
__license__ = "GPLv3"
__date__ = "2022-09-19"
__version__ = "0.9.19"

import json
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F

from netdoc import utils
from netdoc.schemas import discoverable, discoverylog


def discovery(nrni):
    """Discovery Cisco NX-OS devices."""
    platform = "cisco_nxos"
    filtered_devices = nrni.filter(platform=platform)

    def multiple_tasks(task):
        """Define commands (in order) for the playbook."""
        utils.append_nornir_task(
            task, "show running-config | include hostname", template="HOSTNAME", order=0
        )
        utils.append_nornir_task(
            task,
            [
                "show running-config",
                "show version",
                "show interface",
                "show cdp neighbors detail",
                "show lldp neighbors detail",
                "show vlan",
                "show vrf",
            ],
            order=10,
        )
        utils.append_nornir_task(
            task, "show mac address-table dynamic", template="show mac address-table"
        )
        utils.append_nornir_task(
            task,
            [
                # "show logging", # Missing NTC template
                "show ip route vrf all",
                "show port-channel summary",
                "show interface switchport",
                # "show spanning-tree", # Missing NTC template
                # "show interface trunk", # Missing NTC template
                # "show vpc", # Not yet ingested
                # "show vdc", # Not yet ingested
                # "show hsrp all", # Not yet ingested
                # "show vrrp", # Missing NTC template
                # "show glbp", # Missing NTC template
                # "show ip ospf neighbor", # Not yet ingested
                # "show ip eigrp neighbors", # Missing NTC template
                # "show ip bgp neighbors", # Not yet ingested
            ],
        )

    # Run the playbook
    aggregated_results = filtered_devices.run(task=multiple_tasks)

    # Print the result
    print_result(aggregated_results)

    # Save outputs and define additional commands
    for key, multi_result in aggregated_results.items():
        vrfs = []
        current_nr = nrni.filter(F(name=key))

        # MultiResult is an array of Result
        for result in multi_result:
            if result.name == "multiple_tasks":
                # Skip MultipleTask
                continue

            address = result.host.dict().get("hostname")
            discoverable_o = discoverable.get(address, discovered=True)
            details = json.loads(result.name)
            discoverylog.create(
                command=details.get("command"),
                discoverable_id=discoverable_o.id,
                raw_output=result.result,
                template=details.get("template"),
                order=details.get("order"),
                details=details,
            )

            # Save VRF list for later
            if details.get("command") == "show vrf":
                parsed_vrfs, parsed = utils.parse_netmiko_output(
                    result.result, details.get("command"), platform
                )
                if parsed:
                    for vrf in parsed_vrfs:
                        vrfs.append(vrf.get("name"))

        # Additional commands out of the multi result loop
        def additional_tasks(task):
            """Define additional commands (in order) for the playbook."""
            # Per VRF commands
            for vrf in vrfs:  # pylint: disable=cell-var-from-loop
                utils.append_nornir_task(
                    task,
                    commands=f"show ip interface vrf {vrf}",
                    template="show ip interface",
                )
                utils.append_nornir_task(
                    task,
                    commands=f"show ip arp vrf {vrf}",
                    template="show ip arp",
                )

        # Run the additional playbook
        additional_aggregated_results = current_nr.run(task=additional_tasks)

        # Print the result
        print_result(additional_aggregated_results)

        for key, additional_multi_result in additional_aggregated_results.items():
            # MultiResult is an array of Result
            for result in additional_multi_result:
                if result.name == "additional_tasks":
                    # Skip MultipleTask
                    continue

                details = json.loads(result.name)
                if " vrf " in details.get("command"):
                    # Save the VRF in details
                    details["vrf"] = details.get("command").split(" vrf ").pop()
                discoverylog.create(
                    command=details.get("command"),
                    discoverable_id=discoverable_o.id,
                    raw_output=result.result,
                    template=details.get("template"),
                    order=details.get("order"),
                    details=details,
                )
