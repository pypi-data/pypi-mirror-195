""" A basic connection for HTTP communication with a classic Apex """

import aiohttp
from bs4 import BeautifulSoup


def _normalize_hostname(hostname: str) -> str:
    """Stick an HTTP onto the front of the hostname entered by the user if it doesn't have one"""
    hostname = hostname.lower()
    if not hostname.startswith("http://") and not hostname.startswith("https://"):
        hostname = "http://" + hostname
    return hostname


def _get_status_xml_url(hostname: str) -> str:
    """Form the URL to the Apex's status XML"""
    return f"{_normalize_hostname(hostname)}/cgi-bin/status.xml"


def _get_status_update_url(hostname: str) -> str:
    """Form the URL to the Apex's status CGI bridge"""
    return f"{_normalize_hostname(hostname)}/cgi-bin/status.cgi"


class ApexConnection:
    """A connection to an Apex Classic unit"""

    STATUS = "status"

    def __init__(
        self,
        hostname: str,
        client_session: aiohttp.ClientSession,
        username: str | None,
        password: str | None,
    ) -> None:
        self._session = client_session
        self._hostname = _normalize_hostname(hostname)
        self._username = username
        self._password = password
        self._status_soup = None

    async def get_serial_number(self) -> str | None:
        """Get the serial number reported by the Apex hardware"""
        self._status_soup = await self._get_xml_by_name(ApexConnection.STATUS)
        return (
            None if self._status_soup is None else self._status_soup.status.serial.text
        )

    async def refresh(self) -> None:
        """Refresh cached probe and outlet statuses"""
        self._status_soup = await self._get_xml_by_name(ApexConnection.STATUS)

    def get_status(self) -> BeautifulSoup | None:
        """Get the cached BeautifulSoup representation of the status XML"""
        return self._status_soup

    async def post_status_update(self, payload) -> bool:
        """
        Send a payload to the status CGI bridge as form-encoded data.
        Requires that the ApexConnection be instantiated with username and password.
        """
        if self._username is None or self._password is None:
            return False

        url = _get_status_update_url(self._hostname)
        try:
            async with self._session.post(
                url,
                data=payload,
                auth=aiohttp.BasicAuth(self._username, self._password),
            ) as resp:
                return resp.status == 200
        except aiohttp.ClientConnectionError:
            return False
        except aiohttp.ClientResponseError:
            return False

    async def _get_xml_by_name(self, name: str) -> BeautifulSoup | None:
        """
        Get a BeautifulSoup representation of the specified XML file
        `name` can be:
           ApexConnection.STATUS - the status.xml with probe and outlet states
        """
        if name == ApexConnection.STATUS:
            url = _get_status_xml_url(self._hostname)
        else:
            # Currently unsupported XML name
            return None

        try:
            async with self._session.get(url) as resp:
                if resp.status != 200:
                    return None
                return BeautifulSoup(await resp.text(), "xml")
        except aiohttp.ClientConnectionError:
            return None
        except aiohttp.ClientResponseError:
            return None
