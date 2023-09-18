# Peerdom API client

import json
import logging
import time
from typing import Optional

import requests

# API_URL = "https://api.peerdom.org/v1"
API_URL = "http://localhost:3020/v1"


class PeerdomClient:
    """
    Client for interacting with the Peerdom API.

    Attributes:
        api_key (str): API key for authentication.
        max_retries (int, optional): Maximum number of retry attempts for API calls.
    """
    BASE_URL = API_URL

    def __init__(self, api_key: str, max_retries: int = 3):
        self.api_key = api_key
        self.max_retries = max_retries

        self.session = requests.Session()
        self.session.headers.update({
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        })

        self.logger = logging.getLogger("PeerdomClient")
        self.logger.setLevel(logging.DEBUG)

    def _make_request(self, method: str, endpoint: str, **kwargs):

        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(self.max_retries):
            self.logger.debug(f"Request: {method} {url} {kwargs}")
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 429:  # Rate Limit Exceeded
                self.logger.warning("Rate limit exceeded. Retrying...")
                time.sleep(2 ** attempt)
                continue
            elif response.ok:
                return response.json()
            else:
                self.logger.error(
                    f"Error {response.status_code}: {response.text}")
                response.raise_for_status()

        self.logger.error("Max retries reached")
        return None

    def _get_with_customfields(self, endpoint: str, id: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None, with_customfields: bool = False):
        params = {"limit": limit, "offset": offset,
                  "with": "customfields" if with_customfields else None}
        endpoint = f"{endpoint}/{id}" if id else endpoint
        return self._make_request("GET", endpoint, params=params)

    # PEERS
    def get_peers(self, limit=None, offset=None, with_customfields=False):
        """
        Fetch all peers from the API.

        Parameters:
            limit(int, optional): Maximum number of peers to fetch.
            offset(int, optional): Number of peers to skip in the response.
            with_customfields(bool, optional): Whether to include custom fields in the response.

        Returns:
            dict: API response containing peers.
        """
        return self._get_with_customfields("peers", limit=limit, offset=offset, with_customfields=with_customfields)

    def get_peer(self, peer_id, with_customfields=False):
        """
        Get peer with id.
        """
        return self._get_with_customfields("peers", id=peer_id, with_customfields=with_customfields)

    def create_peer(self, first_name: str, last_name: Optional[str] = None, nick_name: Optional[str] = None, birthdate: Optional[str] = None, percentage: Optional[float] = None):
        """
        Create a new peer.

        Parameters:
            first_name(str): First name of the peer.
            last_name(str, optional): Last name of the peer.
            nick_name(str, optional): Nickname of the peer.
            birthdate(str, optional): Birthdate of the peer.
            percentage(float, optional): Percentage value associated with the peer.

        Returns:
            dict: API response containing created peer details.
        """
        data = {
            "firstName": first_name,
            "lastName": last_name,
            "nickName": nick_name,
            "birthdate": birthdate,
            "percentage": percentage
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self._make_request("POST", "peers", data=json.dumps(data))

    def update_peer(self, peer_id: str, first_name: Optional[str] = None, last_name: Optional[str] = None, nick_name: Optional[str] = None, birthdate: Optional[str] = None, percentage: Optional[float] = None):
        """
        Updates the details of a specific peer identified by the peer_id.

        Parameters:
        peer_id (str): The id of the peer to update.
        first_name (str, optional): The new first name of the peer.
        last_name (str, optional): The new last name of the peer.
        nick_name (str, optional): The new nickname of the peer.
        birthdate (str, optional): The new birthdate of the peer.
        percentage (float, optional): The new percentage of the peer.

        Returns:
        dict: A dictionary representing the updated peer.
        """
        data = {
            "firstName": first_name,
            "lastName": last_name,
            "nickName": nick_name,
            "birthdate": birthdate,
            "percentage": percentage
        }
        data = {k: v for k, v in data.items() if v is not None}
        return self._make_request("PUT", f"peers/{peer_id}", data=json.dumps(data))

    def delete_peer(self, peer_id):
        """
        Deletes a specific peer identified by the peer_id.

        Parameters:
        peer_id (str): The id of the peer to delete.

        Returns:
        dict: The API response from the deletion request.
        """

        return self._make_request("DELETE", f"peers/{peer_id}")

    # ROLES
    def get_roles(self, limit=None, offset=None, with_customfields=False):
        """
        Retrieves a list of roles from the API.

        Parameters:
        limit (int, optional): The maximum number of roles to return.
        offset (int, optional): The number of roles to skip in the response.
        with_customfields (bool, optional): Whether to include custom fields in the response.

        Returns:
        list: A list of roles from the API response.
        """
        return self._get_with_customfields("roles", limit=limit, offset=offset, with_customfields=with_customfields)

    def get_role(self, role_id, with_customfields=False):
        """
        Retrieves a specific role from the API.

        Parameters:
        role_id (str): The id of the role to retrieve.
        with_customfields (bool, optional): Whether to include custom fields in the response.

        Returns:
        dict: A dictionary representing the role from the API response.
        """
        return self._get_with_customfields("roles", id=role_id, with_customfields=with_customfields)

    def create_role(self, role_name: str, map_id: str, parent_id: Optional[str] = None, electable: Optional[bool] = None, external: Optional[bool] = None, custom_fields: Optional[dict] = None):
        """
        Creates a new role in the Peerdom system.

        Parameters:
        role_name (str): The name of the role.
        map_id (str): The id of the map to which the role belongs.
        parent_id (str, optional): The id of the parent role.
        electable (bool, optional): A flag indicating whether the role is electable.
        external (bool, optional): A flag indicating whether the role is external.
        custom_fields (dict, optional): A dictionary of custom fields for the role.

        Returns:
        dict: A dictionary representing the newly created role.
        """
        data = {
            "name": role_name,
            "mapId": map_id,
            "parentId": parent_id,
            "electable": electable,
            "external": external,
            "customFields": custom_fields
        }
        # remove None values
        data = {k: v for k, v in data.items() if v is not None}

        return self._make_request("POST", "roles", data=json.dumps(data))

    def update_role(self, role_id: str, role_name: Optional[str] = None, map_id: Optional[str] = None, parent_id: Optional[str] = None, electable: Optional[bool] = None, external: Optional[bool] = None, custom_fields: Optional[dict] = None):
        """
        Updates a specific role in the Peerdom system.

        Parameters:
        role_id (str): The id of the role to update.
        role_name (str, optional): The new name of the role.
        map_id (str, optional): The new id of the map to which the role belongs.
        parent_id (str, optional): The new id of the parent role.
        electable (bool, optional): A flag indicating whether the role is electable.
        external (bool, optional): A flag indicating whether the role is external.
        custom_fields (dict, optional): A dictionary of custom fields for the role.

        Returns:
        dict: A dictionary representing the updated role.
        """
        data = {
            "name": role_name,
            "mapId": map_id,
            "parentId": parent_id,
            "electable": electable,
            "external": external,
            "customFields": custom_fields
        }
        # remove None values
        data = {k: v for k, v in data.items() if v is not None}
        return self._make_request("PUT", f"roles/{role_id}", data=json.dumps(data))

    def delete_role(self, role_id):
        """
        Deletes a specific role identified by the role_id.

        Parameters:
        role_id (str): The id of the role to delete.

        Returns:
        dict: The API response from the deletion request.
        """
        return self._make_request("DELETE", f"roles/{role_id}")

    # HOLDERS
    def get_holders(self, limit=None, offset=None, with_customfields=False):
        """
        Retrieves a list of holders from the API.

        Parameters:
        limit (int, optional): The maximum number of holders to return.
        offset (int, optional): The number of holders to skip in the response.
        with_customfields (bool, optional): Whether to include custom fields in the response.

        Returns:
        list: A list of holders from the API response.
        """
        return self._get_with_customfields("holders", limit=limit, offset=offset, with_customfields=with_customfields)

    def get_holder(self, holder_id, with_customfields=False):
        """
        Retrieves a specific holder from the API.

        Parameters:
        holder_id (str): The id of the holder to retrieve.
        with_customfields (bool, optional): Whether to include custom fields in the response.

        Returns:
        dict: A dictionary representing the holder from the API response.
        """
        return self._get_with_customfields("holders", id=holder_id, with_customfields=with_customfields)

    def create_holder(self, role_id: str, peer_id: str, percentage: Optional[float] = 0, focus: Optional[str] = None):
        """
        Creates a new holder in the Peerdom system. Multiple holders can be created for the same role and peer.

        Parameters:
        role_id (str): The id of the role to which the holder belongs.
        peer_id (str): The id of the peer to which the holder belongs.
        percentage (float, optional): The percentage of the role held by the peer.
        focus (str, optional): The focus of the holder.

        Returns:
        dict: A dictionary representing the newly created holder.
        """
        _assert_percentage(percentage)
        data = {
            "roleId": role_id,
            "peerId": peer_id,
            "percentage": percentage,
            "focus": focus
        }
        # remove None values
        data = {k: v for k, v in data.items() if v is not None}

        return self._make_request("POST", "holders", data=json.dumps(data))

    def update_holder(self, holder_id: str, role_id: Optional[str] = None, peer_id: Optional[str] = None, percentage: Optional[float] = None, focus: Optional[str] = None):
        """
        Updates a specific holder in the Peerdom system.

        Parameters:
        holder_id (str): The id of the holder to update.
        role_id (str, optional): The id of the role to which the holder belongs.
        peer_id (str, optional): The id of the peer to which the holder belongs.
        percentage (float, optional): The percentage of the role held by the peer.
        focus (str, optional): The focus of the holder.

        Returns:
        dict: A dictionary representing the updated holder.
        """
        _assert_percentage(percentage)
        data = {
            "roleId": role_id,
            "peerId": peer_id,
            "percentage": percentage,
            "focus": focus
        }
        # remove None values
        data = {k: v for k, v in data.items() if v is not None}

        return self._make_request("PUT", f"holders/{holder_id}", data=json.dumps(data))

    def delete_holder(self, holder_id):
        """
        Deletes a specific holder identified by the holder_id.

        Parameters:
        holder_id (str): The id of the holder to delete.

        Returns:
        dict: The API response from the deletion request.
        """
        return self._make_request("DELETE", f"holders/{holder_id}")

    # CIRCLES

    def get_circles(self, limit=None, offset=None, with_customfields=False):
        """
        Retrieves a list of circles from the API.

        Parameters:
        limit (int, optional): The maximum number of circles to return.
        offset (int, optional): The number of circles to skip in the response.
        with_customfields (bool, optional): Whether to include custom fields in the response.

        Returns:
        list: A list of circles from the API response.
        """
        return self._get_with_customfields("circles", limit=limit, offset=offset, with_customfields=with_customfields)

    def get_circle(self, circle_id, with_customfields=False):
        """
        Retrieves a specific circle from the API.

        Parameters:
        circle_id (str): The id of the circle to retrieve.
        with_customfields (bool, optional): Whether to include custom fields in the response.

        Returns:
        dict: A dictionary representing the circle from the API response.
        """
        return self._get_with_customfields("circles", id=circle_id, with_customfields=with_customfields)

    def create_circle(self, map_id: str, name: str, parent_id: Optional[str] = None, electable: Optional[bool] = False, external: Optional[bool] = False, custom_fields: Optional[dict] = None):
        """
        Creates a new circle in the Peerdom system.

        Parameters:
        map_id (str): The id of the map to which the circle belongs.
        name (str): The name of the circle.
        parent_id (str, optional): The id of the parent circle.
        electable (bool, optional): A flag indicating whether the circle is electable.
        external (bool, optional): A flag indicating whether the circle is external.
        custom_fields (dict, optional): A dictionary of custom fields for the circle.

        Returns:
        dict: A dictionary representing the newly created circle.
        """
        circle_data = {"name": name,
                       "mapId": map_id,
                       "parentId": parent_id,
                       "electable": electable,
                       "external": external,
                       "customFields": custom_fields
                       }
        # remove None values
        circle_data = {k: v for k, v in circle_data.items() if v is not None}
        return self._make_request("POST", "circles", data=json.dumps(circle_data))

    def update_circle(self,
                      circle_id: str,
                      map_id: Optional[str] = None,
                      name: Optional[str] = None,
                      parent_id: Optional[str] = None,
                      electable: Optional[bool] = False,
                      external: Optional[bool] = False,
                      custom_fields: Optional[dict] = None):
        """
        Updates a specific circle in the Peerdom system.

        Parameters:
        circle_id (str): The id of the circle to update.
        map_id (str, optional): The new id of the map to which the circle belongs.
        name (str, optional): The new name of the circle.
        parent_id (str, optional): The new id of the parent circle.
        electable (bool, optional): A flag indicating whether the circle is electable.
        external (bool, optional): A flag indicating whether the circle is external.
        custom_fields (dict, optional): A dictionary of custom fields for the circle.

        Returns:
        dict: A dictionary representing the updated circle.
        """
        circle_data = {"name": name,
                       "mapId": map_id,
                       "parentId": parent_id,
                       "electable": electable,
                       "external": external,
                       "customFields": custom_fields
                       }
        # remove None values
        circle_data = {k: v for k, v in circle_data.items() if v is not None}

        return self._make_request("PUT", f"circles/{circle_id}", data=json.dumps(circle_data))

    def delete_circle(self, circle_id):
        return self._make_request("DELETE", f"circles/{circle_id}")

    # MAPS
    def get_maps(self, limit=None, offset=None, with_customfields=False):
        """
        Retrieves a list of maps from the API.

        Parameters:
        limit (int, optional): The maximum number of maps to return.
        offset (int, optional): The number of maps to skip in the response.
        with_customfields (bool, optional): Whether to include custom fields in the response.

        Returns:
        list: A list of maps from the API response.
        """
        return self._get_with_customfields("maps", limit=limit, offset=offset, with_customfields=with_customfields)


def _assert_percentage(percentage):
    if percentage is not None and (percentage < 0 or percentage > 100):
        raise ValueError("Percentage must be between 0 and 100")
