""" Representation of a probe connected to an Apex. Contains a name, type, and value. """
from bs4 import PageElement
from .connection import ApexConnection


class Probe:
    """Define a probe connected to an Apex"""

    def __init__(self, conn: ApexConnection, node: PageElement) -> None:
        self._conn = conn
        self.name = node.find_next("name").text
        self.type = node.find_next("type").text

    @property
    def value(self) -> str:
        """Get the probe's value from its ApexConnection's data cache"""
        soup = self._conn.get_status()
        if soup is not None:

            def match_by_probe(tag):
                return (
                    tag.find("name", text=self.name) is not None
                    and tag.find("type", text=self.type) is not None
                )

            node = soup.status.probes.find(match_by_probe)
            if node is not None:
                return node.value.text
        return ""


def get_connected_probes(conn: ApexConnection) -> list[Probe]:
    """Return a list of the probes connected to this Apex from the cached connection state"""
    soup = conn.get_status()
    retval = []
    if soup is not None:
        for probe in soup.find_all("probe"):
            retval.append(Probe(conn, probe))
    return retval
