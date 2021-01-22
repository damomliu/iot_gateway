from server_sync import SyncServer
from mirror_sync import SyncMirror


SERVER = {
    'sync': SyncServer,
    'async': 0,
}
DEFAULT_SERVER_MODE = 'sync'

MIRROR = {
    'sync': SyncMirror,
    'sync-thread': 0,
    'async': 0
}
DEFAULT_MIRROR_MODE = 'sync'
