from server import SyncServer, SyncTcpServer
from mirror_sync import SyncMirror


SERVER = {
    'sync': SyncServer,
    'sync-tcp': SyncTcpServer,
    'async': 0,
}
DEFAULT_SERVER_MODE = 'sync-tcp'

MIRROR = {
    'sync': SyncMirror,
    'sync-thread': 0,
    'async': 0
}
DEFAULT_MIRROR_MODE = 'sync'
