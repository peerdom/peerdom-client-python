import json
import unittest
from unittest.mock import MagicMock, patch

from peerdomclient import PeerdomClient


class TestPeerdomClient(unittest.TestCase):
    def setUp(self):
        self.client = PeerdomClient("api_1234")

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_peers(self, mock_request):
        self.client.get_peers()
        mock_request.assert_called_once_with(
            "GET", "peers", params={"limit": None, "offset": None, "with": None}
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_peer(self, mock_request):
        self.client.get_peer("123")
        mock_request.assert_called_once_with(
            "GET", "peers/123", params={"limit": None, "offset": None, "with": None}
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_create_peer(self, mock_request):
        self.client.create_peer("John", "Doe", "johndoe", 1.0)
        mock_request.assert_called_once_with(
            "POST",
            "peers",
            data=json.dumps({
                "firstName": "John",
                "lastName": "Doe",
                "nickName": "johndoe",
                "percentage": 1.0
            })

        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_update_peer(self, mock_request):
        self.client.update_peer(
            "123",
            first_name="John",
            last_name="Doe",
            nick_name="johndoe",
            birthdate="2000-01-01",
            percentage=1.0,
        )
        mock_request.assert_called_once_with(
            "PUT",
            "peers/123",
            data=json.dumps({
                "firstName": "John",
                "lastName": "Doe",
                "nickName": "johndoe",
                "birthdate": "2000-01-01",
                "percentage": 1.0
            })

        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_delete_peer(self, mock_request):
        self.client.delete_peer("123")
        mock_request.assert_called_once_with("DELETE", "peers/123")

    ### ROLES ###
    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_roles(self, mock_request):
        self.client.get_roles()
        mock_request.assert_called_once_with(
            "GET", "roles", params={"limit": None, "offset": None, "with": None}
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_role(self, mock_request):
        self.client.get_role("123")
        mock_request.assert_called_once_with(
            "GET", "roles/123", params={"limit": None, "offset": None, "with": None}
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_create_role(self, mock_request):
        self.client.create_role(
            role_name="Test Role",
            map_id="42",
            parent_id="123",
            electable=True,
            external=True,
            custom_fields={"test": "test"},
            goals={"goals": "goals"},
        )
        mock_request.assert_called_once_with(
            "POST",
            "roles",
            data=json.dumps({
                "name": "Test Role",
                "mapId": "42",
                "parentId": "123",
                "electable": True,
                "external": True,
                "customFields": {"test": "test"},
                "goals": {"goals": "goals"}
            })

        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_update_role(self, mock_request):
        self.client.update_role(role_id="123", role_name="Test Role")
        mock_request.assert_called_once_with(
            "PUT", "roles/123", data="""{"name": "Test Role"}"""
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_delete_role(self, mock_request):
        self.client.delete_role("123")
        mock_request.assert_called_once_with("DELETE", "roles/123")

    ### ASSIGN ###
    @patch("peerdomclient.PeerdomClient._make_request")
    def test_assign_role_to_peer(self, mock_request):
        self.client.assign_role_to_peer(
            role_id="123",
            peer_id="456",
            percentage=50,
            focus="Test",
            elected_until="2023-01-01",
        )

        mock_request.assert_called_once_with(
            "POST",
            "roles/123/peers",
            data=json.dumps({
                "peerId": "456",
                "percentage": 50,
                "focus": "Test",
                "electedUntil": "2023-01-01"
            })

        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_unassign_role_from_peer(self, mock_request):
        self.client.unassign_role_from_peer(role_id="123", peer_id="456")
        mock_request.assert_called_once_with(
            "DELETE", "roles/123/peers/456")

    ### CIRCLES ###

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_circles(self, mock_request):
        self.client.get_circles()
        mock_request.assert_called_once_with(
            "GET", "circles", params={"limit": None, "offset": None, "with": None}
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_circle(self, mock_request):
        self.client.get_circle("123")
        mock_request.assert_called_once_with(
            "GET", "circles/123", params={"limit": None, "offset": None, "with": None}
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_create_circle(self, mock_request):
        self.client.create_circle(
            name="Test Circle",
            map_id="123",
            parent_id="p42",
            electable=False,
            external=False,
        )
        mock_request.assert_called_once_with(
            "POST",
            "circles",
            data=json.dumps({
                "name": "Test Circle",
                "mapId": "123",
                "parentId": "p42",
                "electable": False,
                "external": False
            })

        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_update_circle(self, mock_request):
        self.client.update_circle(
            "123",
            name="Test Circle",
            map_id="123",
            parent_id="456",
            electable=True,
            external=True,
        )
        mock_request.assert_called_once_with(
            "PUT",
            "circles/123",
            data=json.dumps({
                "name": "Test Circle",
                "mapId": "123",
                "parentId": "456",
                "electable": True,
                "external": True
            })

        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_delete_circle(self, mock_request):
        self.client.delete_circle("123")
        mock_request.assert_called_once_with("DELETE", "circles/123")

    ### MAPS ###
    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_maps(self, mock_request):
        self.client.get_maps()
        mock_request.assert_called_once_with(
            "GET", "maps", params={"limit": None, "offset": None, "with": None}
        )

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_active_map(self, mock_request):
        self.client.get_maps = MagicMock(
            return_value=[{"id": "1", "draft": False},
                          {"id": "2", "draft": True}]
        )
        self.assertEqual(self.client.get_active_map(), "1")

        self.client.get_maps = MagicMock(
            return_value=[{"id": "1", "draft": True},
                          {"id": "2", "draft": True}]
        )
        with self.assertRaises(Exception) as context:
            self.client.get_active_map()
        self.assertEqual(str(context.exception), "No active map found")

    @patch("peerdomclient.PeerdomClient._make_request")
    def test_get_root_node(self, mock_request):
        self.client.get_active_map = MagicMock(return_value="1")
        self.client.get_circles = MagicMock(
            return_value=[{"id": "1", "parentId": "0"}, {"id": "2"}]
        )
        self.assertEqual(self.client.get_root_node(), "2")

        self.client.get_circles = MagicMock(
            return_value=[{"id": "1", "parentId": "0"},
                          {"id": "2", "parentId": "1"}]
        )
        with self.assertRaises(Exception) as context:
            self.client.get_root_node()
        self.assertEqual(str(context.exception), "No root circle found")
