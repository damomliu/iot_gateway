from server import SyncTcpServer
from mirror_sync import SyncMirror


SERVER = {
    # 'sync': SyncServer,
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

FORMULA_X_VALIABLE_CHRS = [
    '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '+', '-', '*', '/', '(', ')', 'x', 'X'
]
