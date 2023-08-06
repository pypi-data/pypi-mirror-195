import rocksdb
from rocksdb.errors import RocksIOError, Corruption
from os import makedirs, remove
from shutil import rmtree
from pathlib import Path
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
import logging

LOGGER = logging.getLogger(__name__)


class RdbTableInUse(Exception):
    def __init__(self, table_name):
        super().__init__(f'Table "{table_name}" is currently in use by another instance.')


class RDB:
    def __init__(self, table_name, table_path=None, delete_existing_lock=False, auto_init=True, auto_delete_corrupt=True):
        self.rdb = None
        self.active_lock = False  # intended to represent an active lock file made by THIS instance

        self.table_name = table_name
        if not table_path:
            table_path = env_vars()['NU_TABLE_PATH']
        makedirs(table_path, exist_ok=True)
        self.full_db_path = Path(f"{table_path}/{table_name}.rocksdb").absolute()
        self._lock_file_path = self.full_db_path/'LOCK'

        if auto_init:
            self._init_rdb(delete_existing_lock=delete_existing_lock)
        self.auto_delete_corrupt = auto_delete_corrupt

    def _init_rdb(self, delete_existing_lock=False):
        opts = rocksdb.Options()
        opts.create_if_missing = True
        opts.max_open_files = 500
        opts.write_buffer_size = self.get_mb(16)
        opts.max_write_buffer_number = 2
        opts.target_file_size_base = self.get_mb(16)
        opts.skip_log_error_on_recovery = True

        opts.table_factory = rocksdb.BlockBasedTableFactory(
            filter_policy=rocksdb.BloomFilterPolicy(10),
            block_cache=rocksdb.LRUCache(self.get_mb(64)))
        try:
            self.rdb = rocksdb.DB(self.full_db_path.as_posix(), opts)
            self.active_lock = True
        # TODO try and handle corrupt files
        except RocksIOError as e:
            if 'Resource temporarily unavailable' or 'No locks available' in e.args[0].decode():
                if delete_existing_lock:
                    self.delete_lock_file()
                    self._init_rdb(delete_existing_lock=False)
                else:
                    raise RdbTableInUse(self.table_name)
            else:
                raise
        except Corruption:
            if self.auto_delete_corrupt:
                LOGGER.info(f'{self.table_name}.rocksdb was corrupt; deleting, which will cause a table rebuild')
                rmtree(self.full_db_path.as_posix())
                self._init_rdb(delete_existing_lock=False)
            else:
                raise

    def get_mb(self, value):
        return value * 2**20

    def write(self, key, value):
        self.rdb.put(key.encode(), value.encode())

    def write_batch(self, write_dict):
        batch = rocksdb.WriteBatch()
        for k, v in write_dict.items():
            try:
                v = v.encode()
            except ValueError:
                pass
            batch.put(k.encode(), v)
        self.rdb.write(batch)

    def read(self, k):
        result = self.rdb.get(k.encode())
        if result:
            return result.decode()
        return result

    def delete(self, key):
        self.rdb.delete(key.encode())

    def lock_file_exists(self):
        return self._lock_file_path.is_file()

    def delete_lock_file(self):
        if self.lock_file_exists():
            remove(self._lock_file_path)
            self.active_lock = False

    def close(self):
        self.rdb.close()
        self.active_lock = False
        # self.delete_lock_file()
