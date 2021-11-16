from time import time
from source import MirrorSourceList
from source.status import SourceStatus

class SyncMirror():
    def __init__(self, src_list, logger) -> None:
        self.logger = logger
        self.src_list = MirrorSourceList(mirror=self)
        for src in src_list:
            self.src_list.append(src)

    def log_status(self):
        self.logger.info(f'Mirroring from {len(self.src_list.client_list)} clients / {len(self.src_list)} sources')
        self.logger.info(self.src_list.status)
        self.logger.info(dict(self.src_list.counter))

    def _Validate(self, new_src):
        for src in self.src_list:
            if src.target.pointType.type_str != new_src.target.pointType.type_str: continue
            if src.target.address_set.intersection(new_src.target.address_set):
                self.logger.warning(f'Address conflict!! src={src} / new_src={new_src}')
                return -1

    def connect_all(self):
        while self.src_list.wait_connect:
            src = self.src_list.wait_connect[0]
            self._connect_one(src)

        self.log_status()

    def connect_retry(self):
        self.logger.info('Retrying...')
        while self.src_list.wait_retry:
            src = self.src_list.wait_retry[0]
            self._connect_one(src, retry=True)

        for src in self.src_list.retry_failed:
            src.status = SourceStatus.CONNECTED_FAILED

        self.log_status()

    def _connect_one(self, src, retry=False):
        failed = False
        try:
            res,info = src.Connect()
            if res:
                self.src_list.set_connected(src)
                if info:
                    self.logger.debug(' / '.join([f'connected to {src} OK'] + info))
                else:
                    self.logger.info(f'connected to {src} OK')
            else:
                self.logger.warning(f'...not connected : {src} / {info}')
                failed = True

        except Exception as e:
            self.logger.error(f'Connect failed {src} \n{e}')
            failed = True

        if failed:
            if retry:
                self.src_list.set_retry_failed(src)
            else:
                self.src_list.set_connect_failed(src)

    def Disconnect(self):
        for src in self.src_list:
            res = src.Disconnect()
            self.src_list.reset(src)
            if res:
                self.logger.info(f'{src} is disconnected.')

    def __del__(self):
        try:
            self.Disconnect()
        except:
            pass

    def Read(self):
        debug_msg_interval_sec = 60
        for src in self.src_list.wait_read:
            try:
                req,val = src.Read()
                if req:
                    self.src_list.set_reading(src)
                    if time() % debug_msg_interval_sec < 1:
                        self.logger.debug(f'{src} val = {val}')

                else:
                    self.logger.error(f'Read failed {src} {val}')
                    self.src_list.set_read_failed(src)

            except Exception as e:
                self.logger.error(f'Read failed {src} \n{e}')
                self.src_list.set_read_failed(src)

    def _MatchSourceList(self, fx, address):
        matched_list = []
        for src in self.src_list:
            if address == src.target.address_from0 and fx in src.target.pointType.write_fx:
                matched_list.append(src)

        return matched_list

    def _WriteRequestList(self, fx, address, values, req_list=None):
        if req_list is None: req_list = []
        matched_src_list = self._MatchSourceList(fx, address)
        if len(matched_src_list) == 1:
            src = matched_src_list[0]
            if len(values) == src.length:
                req_list.append(src)
                return req_list
            elif len(values) < src.length:
                self.logger.warning(f'Unequal data length src={src} values={src.values} / written_data={values}')
                return req_list
            else:
                req_list.append(src)
                address += src.length
                values = values[src.length:]
                return self._WriteRequestList(fx, address, values, req_list=req_list)

        elif len(matched_src_list) > 1:
            self.logger.warning('\n'.join([f'Duplicated sources of fx={fx} address={address}', *(str(src) for src in matched_src_list)]))
            return req_list
        else:
            self.logger.warning(f'No matched source of fx={fx} address={address}')
            return req_list

    def Write(self, fx, address, values):
        req_list = self._WriteRequestList(fx, address, values)
        for src in req_list:
            original_val = src.values
            req,err = src.Write(values[:src.length])
            if req:
                try:
                    decode_func = src.target.dataType.Decode
                    original_val = decode_func(original_val)
                    src_values = decode_func(src.values)
                except:
                    src_values = src.values

                self.logger.info(f'Writeback success for {src} : {original_val} -> {src_values}')

                values = values[src.length:]
                address += src.length
            else:
                self.logger.error(f'Writeback failed. {src} {err}')
                return 0
