import getpass

import requests

from .seek_objects import (
    OBJECTS_CREATE,
    OBJECTS_DELETE,
    OBJECTS_FETCH,
    OBJECTS_LIST,
    OBJECTS_UPDATE,
)


class FairdomSeekApiException(Exception):
    """A class to handle errors received from the FAIRDOM-SEEK API"""

    def __init__(self, message: str = "", error: dict = {}):
        errors = error.get("errors", "")
        api_message = ". ".join(
            [
                ", ".join(
                    [y for y in [e.get("title", None), e.get("detail", None)] if y]
                )
                for e in errors
            ]
        )
        message = api_message if api_message else message
        super().__init__(message)


class FairdomSeek(object):
    me = None
    session = None
    request_timeout = 60

    _api_num_limit = 20
    _base_headers = {
        "Accept": "application/vnd.api+json",
        "Accept-Encoding": "ISO-8859-1",
        # "Connection": "close",
    }
    _objects_create = OBJECTS_CREATE
    _objects_delete = OBJECTS_DELETE
    _objects_fetch = OBJECTS_FETCH
    _objects_list = OBJECTS_LIST
    _objects_update = OBJECTS_UPDATE

    def __init__(
        self,
        api_base_url: str,
        ipv6: bool = True,
    ):
        self._api_base_url = api_base_url
        if not ipv6:
            requests.packages.urllib3.util.connection.HAS_IPV6 = False

    def _check_logged_in(self) -> bool:
        """
        Check if session is set = a user has been logged in.
        """

        if not self.session:
            raise Exception(
                "You are not logged in. Please log in before performing this action."
            )

        return True

    def login(self, token: str = "") -> None:
        """
        Log in user
        """

        session = requests.Session()
        session.headers.update(self._base_headers)
        if token:
            session.headers.update({"Authentication": token})
        else:
            session.auth = (input("Username: "), getpass.getpass("Password: "))

        r = session.get(
            f"{self._api_base_url}/people/current",
            timeout=self.request_timeout,
        )

        if r.status_code == 200:
            self.session = session
            self.me = r.json()["data"]
            print(f"You are logged in as: {self.me['attributes']['title']}")
        elif token and r.status_code == 404:
            self.session = session
        else:
            raise FairdomSeekApiException(error=r.json())

    def list(self, object_type: str) -> dict:
        """List objects of a given type."""

        if object_type not in self._objects_list:
            raise Exception(
                f'Object type "{object_type}" not recognized. Valid types are: {", ".join(self._objects_list)}'
            )

        self._check_logged_in()

        r = self.session.get(
            f"{self._api_base_url}/{object_type}",
            timeout=self.request_timeout,
        )

        if r.status_code == 200:
            return r.json()["data"]
        else:
            raise FairdomSeekApiException(error=r.json())

    def create(self, object_type: str, attributes: dict, relationships: dict) -> dict:
        """Create an object of a given type."""

        if object_type not in self._objects_create:
            raise Exception(
                f'Object type "{object_type}" not recognized. Valid types are: {", ".join(self._objects_create)}'
            )

        self._check_logged_in()

        data = {
            "data": {
                "type": object_type,
                "attributes": attributes,
                "relationships": relationships,
            }
        }

        r = self.session.post(
            f"{self._api_base_url}/{object_type}",
            json=data,
            timeout=self.request_timeout,
        )

        if r.status_code == 201 or r.status_code == 200:
            return r.json()["data"]
        else:
            raise FairdomSeekApiException(error=r.json())

    def update(
        self, object_type: str, object_id: str, attributes: dict, relationships: dict
    ) -> dict:
        """Update an object of a given type."""

        if object_type not in self._objects_update:
            raise Exception(
                f'Object type "{object_type}" not recognized. Valid types are: {", ".join(self._objects_update)}'
            )

        self._check_logged_in()

        data = {
            "data": {
                "type": object_type,
                "id": object_id,
                "attributes": attributes,
                "relationships": relationships,
            }
        }

        r = self.session.patch(
            f"{self._api_base_url}/{object_type}/{object_id}",
            json=data,
            timeout=self.request_timeout,
        )

        if r.status_code == 200:
            return r.json()["data"]
        else:
            raise FairdomSeekApiException(error=r.json())

    def delete(self, object_type: str, object_id: str) -> None:
        """Delete an object of a given type."""

        if object_type not in self._objects_delete:
            raise Exception(
                f'Object type "{object_type}" not recognized. Valid types are: {", ".join(self._objects_delete)}'
            )

        self._check_logged_in()

        r = self.session.delete(
            f"{self._api_base_url}/{object_type}/{object_id}",
            timeout=self.request_timeout,
        )

        if r.status_code == 200:
            print(f"{object_type} {object_id} deleted successfully.")
        else:
            raise FairdomSeekApiException(error=r.json())

    def fetch(self, object_type: str, object_id: str) -> dict:
        """Fetch an object of a given type."""

        if object_type not in self._objects_fetch:
            raise Exception(
                f'Object type "{object_type}" not recognized. Valid types are: {", ".join(self._objects_fetch)}'
            )

        self._check_logged_in()

        r = self.session.get(
            f"{self._api_base_url}/{object_type}/{object_id}",
            timeout=self.request_timeout,
        )

        if r.status_code == 200:
            return r.json()["data"]
        else:
            print(r.json())
            raise FairdomSeekApiException(error=r.json())

    def fetch_or_create(
        self,
        object_type: str,
        object_id: str,
        attributes: dict,
        relationships: dict,
    ) -> dict:
        """Fetch an object of a given type by ID, or create it if it does not exist."""

        objects_fetch_create = list(
            set(self._objects_fetch).intersection(self._objects_create)
        )
        if object_type not in objects_fetch_create:
            raise Exception(
                f'Object type "{object_type}" not recognized. Valid types are: {", ".join(objects_fetch_create)}'
            )

        self._check_logged_in()

        # First, try to fetch the object by ID
        try:
            return self.fetch(object_type, object_id)
        except FairdomSeekApiException as e:
            # If not found, create the object
            print(e)
            return self.create(object_type, attributes, relationships)
