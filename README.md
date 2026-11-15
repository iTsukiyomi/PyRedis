# PyRedis

a lightweight redis key value database built from scratch in python.

This project uses TCP server which communicates with RESP (Redis Serialization Protocol) and supports basic Redis commands (get, set, ping, echo, expire, etc), in memory database, and automatic key expiration

## tech stack

- python
- TCP sockets
- Selectors (i/o multiplexing)
- RESP (redis serialization protocol)
- `redis-cli` for testing 

## how it works

1. CLient connects using TCP (example, `redis-cli`)
2. Server recieves incoming data
3. `protocol.py` decodes the RESP data into a command and its arguments
4. `commands.py` identifies the command, validates its arguments, and executes it.
5. `storage.py` performs any data access operations like get, set, delete.
6. The result travels back through protocol handler which encodes it back into RESP.
7. Server sends response back to client

### key expiration

the server runs key expiration cycles every 100 millisecond.

- **passive expiration:** checks and remove expired key when theyre accessed
- **active expiration:** randomly samples stored expiration keys and removes expired keys
