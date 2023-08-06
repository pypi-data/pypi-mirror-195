import tempfile
from typing import Generator
import pickle
from struct import pack, unpack
from glob import glob
import secrets
from pathlib import Path
from mines_data_engineering.relalg import Record, Relation
from mines_data_engineering.util import batched

# constants
PAGE_SIZE_NUMREC = 1000 # number of records in each page

class UnsortedDiskManager:
    """
    Saves/loads relations on disk
    """
    def __init__(self):
        self.tmpdir = tempfile.TemporaryDirectory()
    
    def save_relation(self, R: Relation):
        """Saves the relation to disk"""
        p = Path(self.tmpdir.name)
        for b in batched(R.records, PAGE_SIZE_NUMREC):
            pagefile = p/f"{R.name}-{secrets.token_hex(8)}"
            with open(pagefile, 'wb') as f:
                for rec in b:
                    f.write(rec.serialize())
            with open(p/f"schema-{R.name}", "wb") as f:
                f.write(pickle.dumps((R.name, R.attributes)))
    
    def read_records(self, name: str) -> Generator[Record, None, None]:
        """Returns an iterator over records in the given relation"""
        p = Path(self.tmpdir.name)
        for pagefile in glob(str(p/f"{name}-*")):
            with open(pagefile, 'rb') as f:
                while True:
                    try:
                        l = unpack('<I', f.read(4))[0]
                        r = Record.deserialize(f.read(l))
                        yield r
                    except:
                        break

    def load_relation(self, name: str) -> Relation:
        """Returns a relation from disk"""
        p = Path(self.tmpdir.name)
        with open(p/f"schema-{name}", "rb") as f:
            name, attributes = pickle.loads(f.read())
        records = self.read_records(name)
        return Relation(name, attributes, records)
