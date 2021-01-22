class Source:
    def __init__(self, row, config_dict):
        self.ip = row['SourceIP']
        self.address = int(row['SourceAddress'])
        self.port = row.get('SourcePort', config_dict['default_source_port'])
        self.length = int(_get(row, 'SourceLength', config_dict['default_source_length']))
        self.point_type = _get(row, 'SourcePointType', config_dict['default_source_pointtype'])
        self.slave_id = _get(row, 'SourceSlaveID', 0x00)
        self.desc = row.get('SourceDesc')

        self.target_address = int(row['TargetAddress'])
        self.target_desc = row.get('TargetDesc')

        self.client = None
        self.is_connected = False
        self.value = None
    
    def __repr__(self) -> str:
        return f'<{self.value}@{self.ip}/{self.address}:{self.target_address}>'


def _get(_dict, key, val_if_none):
    if _dict.get(key):
        return _dict.get(key)
    else:
        return val_if_none
    
