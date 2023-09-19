import unittest
from unittest.mock import patch

from peerdomclient import PeerdomClient


class TestPeerdomClient(unittest.TestCase):

    def setUp(self):
        self.client = PeerdomClient("api_1234")

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_peers(self, mock_request):
        self.client.get_peers()
        mock_request.assert_called_once_with(
            "GET", "peers", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_peer(self, mock_request):
        self.client.get_peer("123")
        mock_request.assert_called_once_with(
            "GET", "peers/123", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_create_peer(self, mock_request):
        self.client.create_peer("John", "Doe", "johndoe", "2000-01-01", 1.0)
        mock_request.assert_called_once_with(
            "POST",
            "peers",
            data='{"firstName": "John", "lastName": "Doe", "nickName": "johndoe", "birthdate": "2000-01-01", "percentage": 1.0}'
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_update_peer(self, mock_request):
        self.client.update_peer("123", first_name="John", last_name="Doe",
                                nick_name="johndoe", birthdate="2000-01-01", percentage=1.0)
        mock_request.assert_called_once_with(
            "PUT",
            "peers/123",
            data='{"firstName": "John", "lastName": "Doe", "nickName": "johndoe", "birthdate": "2000-01-01", "percentage": 1.0}'
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_delete_peer(self, mock_request):
        self.client.delete_peer("123")
        mock_request.assert_called_once_with(
            "DELETE", "peers/123")

    ### ROLES ###
    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_roles(self, mock_request):
        self.client.get_roles()
        mock_request.assert_called_once_with(
            "GET", "roles", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_role(self, mock_request):
        self.client.get_role("123")
        mock_request.assert_called_once_with(
            "GET", "roles/123", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_create_role(self, mock_request):
        self.client.create_role(role_name="Test Role", map_id="42", parent_id="123",
                                electable=True, external=True, custom_fields={"test": "test"})
        mock_request.assert_called_once_with(
            "POST", "roles", data='{"name": "Test Role", "mapId": "42", "parentId": "123", "electable": true, "external": true, "customFields": {"test": "test"}}')

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_update_role(self, mock_request):
        self.client.update_role(role_id="123", role_name="Test Role")
        mock_request.assert_called_once_with(
            "PUT", "roles/123", data='{"name": "Test Role"}')

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_delete_role(self, mock_request):
        self.client.delete_role("123")
        mock_request.assert_called_once_with(
            "DELETE", "roles/123")

    ### HOLDERS ###
    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_holders(self, mock_request):
        self.client.get_holders()
        mock_request.assert_called_once_with(
            "GET", "holders", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_holder(self, mock_request):
        self.client.get_holder("123")
        mock_request.assert_called_once_with(
            "GET", "holders/123", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_create_holder(self, mock_request):
        self.client.create_holder(
            peer_id="42", role_id="123", percentage=100, focus="good")
        mock_request.assert_called_once_with(
            "POST", "holders", data='{"roleId": "123", "peerId": "42", "percentage": 100, "focus": "good"}')

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_update_holder(self, mock_request):
        self.client.update_holder(
            holder_id="123", peer_id="42", role_id="123", percentage=50, focus="bad")
        mock_request.assert_called_once_with(
            "PUT", "holders/123", data='{"roleId": "123", "peerId": "42", "percentage": 50, "focus": "bad"}')

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_delete_holder(self, mock_request):
        self.client.delete_holder("123")
        mock_request.assert_called_once_with(
            "DELETE", "holders/123")

    ### CIRCLES ###

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_circles(self, mock_request):
        self.client.get_circles()
        mock_request.assert_called_once_with(
            "GET", "circles", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_circle(self, mock_request):
        self.client.get_circle("123")
        mock_request.assert_called_once_with(
            "GET", "circles/123", params={"limit": None, "offset": None, "with": None})

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_create_circle(self, mock_request):
        self.client.create_circle(
            name="Test Circle", map_id="123", parent_id="p42", electable=False, external=False)
        mock_request.assert_called_once_with(
            "POST",
            "circles",
            data='{"name": "Test Circle", "mapId": "123", "parentId": "p42", "electable": false, "external": false}'
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_update_circle(self, mock_request):
        self.client.update_circle(
            "123", name="Test Circle", map_id="123", parent_id="456", electable=True, external=True)
        mock_request.assert_called_once_with(
            "PUT",
            "circles/123",
            data='{"name": "Test Circle", "mapId": "123", "parentId": "456", "electable": true, "external": true}'
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_delete_circle(self, mock_request):
        self.client.delete_circle("123")
        mock_request.assert_called_once_with(
            "DELETE", "circles/123")

    ### MAPS ###
    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_maps(self, mock_request):
        self.client.get_maps()
        mock_request.assert_called_once_with(
            "GET", "maps", params={"limit": None, "offset": None, "with": None})
