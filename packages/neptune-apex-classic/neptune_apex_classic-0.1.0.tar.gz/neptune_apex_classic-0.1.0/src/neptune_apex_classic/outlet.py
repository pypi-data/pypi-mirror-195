""" Representation of an outlet connected to an Apex. Consists of a name, device ID, output ID, and state"""
from bs4 import PageElement
from .connection import ApexConnection


class Outlet:
    """Define an outlet connected to an Apex"""

    ON = "ON"
    OFF = "OFF"
    AUTO_ON = "AON"
    AUTO_OFF = "AOF"
    AUTO = "AUTO"

    def __init__(self, conn: ApexConnection, node: PageElement) -> None:
        self._conn = conn
        self.device_id = node.find_next("deviceID").text
        self.name = node.find_next("name").text
        self.output_id = node.find_next("outputID").text

    async def set_state(self, new_state: str) -> bool:
        """Set the state of the outlet: ON, OFF, or AUTO"""
        if new_state not in [Outlet.ON, Outlet.OFF, Outlet.AUTO]:
            return False

        new_state_value = 1  # Outlet.OFF
        if new_state == Outlet.AUTO:
            new_state_value = 0
        elif new_state == Outlet.ON:
            new_state_value = 2

        payload = {f"{self.name}_state": new_state_value, "noResponse": 1}
        return await self._conn.post_status_update(payload)

    @property
    def value(self) -> str:
        """Get the outlet's state from its ApexConnection's data cache"""
        soup = self._conn.get_status()
        if soup is not None:

            def match_by_device_id(tag):
                return tag.find("deviceID", text=self.device_id) is not None

            node = soup.status.outlets.find(match_by_device_id)
            if node is not None:
                return node.state.text
        return ""


def get_connected_outlets(conn: ApexConnection) -> list[Outlet]:
    """Return a list of the outlets connected to this Apex from the cached connection state"""
    soup = conn.get_status()
    Outlets = list[Outlet]
    retval = Outlets()
    if soup is not None:
        for outlet in soup.find_all("outlet"):
            retval.append(Outlet(conn, outlet))

    # Ignore outlets which are unconfigured "base" outlets and ones explicitly named "Unused"
    return [
        o
        for o in retval
        if not o.device_id.startswith("base") and not o.name.startswith("Unused")
    ]
