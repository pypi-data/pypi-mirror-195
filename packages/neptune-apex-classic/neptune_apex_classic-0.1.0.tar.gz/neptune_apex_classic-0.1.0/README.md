# neptune_apex_classic

Python module for getting the state of and controlling a classic Neptune Apex from your LAN

## Requirements

This module requires the "XML Access" to be set on the Apex in order for the status of probes and outlets to be retrieved. Outlets can be set between OFF, AUTO, and ON if the ApexConnection object is created with a username and password.

HTTP access is governed by an [`aiohttp.ClientSession`](https://docs.aiohttp.org/en/stable/client_reference.html) supplied by the caller.
## Example Usage

```python
async def do_apex_stuff(clientSession: aiohttp.ClientSession) -> None:
    # Create an ApexConnection - one connection per Apex is all that's required
    conn = ApexConnection("ip-address", clientSession, "admin", "1234")

    # The hardware serial number is an ID unique to each Apex and can be used
    # to differentiate between different units on the same network
    serial_number = await conn.get_serial_number()

    # Fetch probe and outlet data
    await conn.refresh()

    # Iterate through connected probes
    for probe in get_connected_probes(conn):
        print(probe.name)
        print(probe.value)

    # Iterate through connected outlets and print the state
    for outlet in get_connected_outlets(conn):
        print(outlet.name)
        print(outlet.value)

    # Probe values and outlet states are cached and are only updated when the ApexConnection is refreshed!
    conn.refresh()

    outlet = get_connected_outlets(conn)[0]
    await outlet.set_state(Outlet.ON)
```