# PeerdomClient

PeerdomClient is a Python client for interacting with the Peerdom API, which allows organizations to manage their data within Peerdom. This client provides a convenient way to access and perform CRUD operations on peers, roles, and circles through a simple interface.

## Installation

You can install the PeerdomClient using pip:

```bash
pip install peerdomclient
```

## Usage

To use the PeerdomClient, you need to obtain an API key from Peerdom. Once you have the API key, you can instantiate the client and start making API calls.

Here's an example of how to use the PeerdomClient:

```python
from peerdomclient import PeerdomClient

# Initialize the client
api_key = "your-api-key"
client = PeerdomClient(api_key)

# Get a list of peers
peers = client.get_peers(limit=10)
for peer in peers:
    print(peer)

# Get details of a specific peer
peer_id = "123" #replace with a peer id
peer = client.get_peer(peer_id)
print(peer)

# Create a new peer
new_peer = client.create_peer(first_name="John", last_name="Doe", birthdate="1990-01-01")
print(new_peer)

# Update an existing peer
peer_id = new_peer["id"]
updated_peer = client.update_peer(peer_id=peer_id, first_name="Jane", last_name="Doe", birthdate="1990-01-01")
print(updated_peer)

# Delete a peer
client.delete_peer(peer_id)
print("Peer deleted.")
```

Replace `"your-api-key"` with your actual API key and `"peer-id"` with the ID of the peer you want to retrieve, update, or delete.

## Documentation

For more details on the available methods and parameters, please refer to the [API documentation](https://api.peerdom.org/v1/docs).

## Contributing

Contributions to the PeerdomClient are welcome! If you find a bug, have a suggestion, or want to contribute code improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/peerdom/peerdom-client-python).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
