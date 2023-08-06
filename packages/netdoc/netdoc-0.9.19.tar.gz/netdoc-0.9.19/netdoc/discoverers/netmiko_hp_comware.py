"""Discovery task for HP Comware devices via Netmiko."""
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
    """Discovery Cisco IOS devices."""
    platform = "hp_comware"
    filtered_devices = nrni.filter(platform=platform)

    def multiple_tasks(task):
        """Define commands (in order) for the playbook."""
        utils.append_nornir_task(
            task,
            "display current-configuration | include sysname",
            template="HOSTNAME",
            order=0,
        )
        utils.append_nornir_task(
            task,
            [
                "display current-configuration",
                # "display version", # Missing NTC template
                "display interface",
                "display ip interface",
                "display lldp neighbor-information verbose",
                "display vlan brief",
                "display ip vpn-instance",
            ],
            order=10,
        )
        utils.append_nornir_task(
            task,
            [
                # "display logbuffer level 6", # Missing NTC template
                "display mac-address",
                # "display stp", # Missing NTC template
                "display link-aggregation verbose",
                # "display port trunk", # Missing NTC template
                # "display vrrp", # Missing NTC template
                # "display ospf peer", # Missing NTC template
                # "display bgp peer", # Missing NTC template
            ],
        )

    # Run the playbook
    aggregated_results = filtered_devices.run(task=multiple_tasks)

    # Print the result
    print_result(aggregated_results)

    # Save outputs and define additional commands
    for key, multi_result in aggregated_results.items():
        vrfs = ["default"]  # Adding default VRF
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
            if details.get("command") == "display ip vpn-instance":
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
                if vrf == "default":
                    # Default VRF has no name
                    utils.append_nornir_task(
                        task,
                        [
                            "display arp",
                            "display ip routing-table",
                        ],
                    )
                else:
                    # with non default VRF commands and templates differ
                    utils.append_nornir_task(
                        task,
                        commands=f"display arp vpn-instance {vrf}",
                        template="display arp",
                    )
                    utils.append_nornir_task(
                        task,
                        commands=f"display ip vpn-instance instance-name {vrf}",
                        template="display ip vpn-instance instance-name",
                    )
                    utils.append_nornir_task(
                        task,
                        commands=f"display ip routing-table vpn-instance {vrf}",
                        template="display ip routing-table",
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
                if " vpn-instance " in details.get("command"):
                    # Save the VRF in details
                    details["vrf"] = (
                        details.get("command").split(" vpn-instance ").pop()
                    )
                elif " instance-name " in details.get("command"):
                    # Save the VRF in details
                    details["vrf"] = (
                        details.get("command").split(" instance-name ").pop()
                    )
                discoverylog.create(
                    command=details.get("command"),
                    discoverable_id=discoverable_o.id,
                    raw_output=result.result,
                    template=details.get("template"),
                    order=details.get("order"),
                    details=details,
                )
