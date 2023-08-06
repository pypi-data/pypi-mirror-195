from dataclasses import dataclass
from typing import List, Tuple, Any, Union, Dict, Callable, Generator, Optional, Set
from itertools import takewhile
from prettytable import PrettyTable
import tempfile
from struct import pack, unpack
import random
import pickle
from pathlib import Path
from glob import glob
from faker import Faker
import time
from mines_data_engineering.data_generation import city_generator
from mines_data_engineering.util import batched, take, nth
fake = Faker()

# define set of domains for our attributes
AtomicType = Union[int, str, bool]
# define conditions for filters
Condition = Callable[['Record'], bool]

"""
Simplified implementation:

@dataclass
class Record:
    fields: Tuple[AtomicType]
"""

@dataclass
class Record:
    """
    The Record type represents a tuple in a relation
    """
    fields: Tuple[AtomicType]

    def __getitem__(self, key):
        return self.fields[key]
    
    def serialize(self) -> bytes:
        """Serialize 4-byte length, then pickled tuple of fields"""
        f = pickle.dumps(self.fields)
        return pack('<I', len(f)) + f
    
    @classmethod
    def deserialize(cls, b: bytes):
        """Load a record from a pickled tuple of fields"""
        fields = pickle.loads(b)
        return cls(fields)

@dataclass
class Attribute:
    """Represents an attribute of a relational schema"""
    name: str
    dtype: type # assume to be valid types...


"""
Simplified Relation representation

@dataclass
class Relation:
    name: str
    attributes: List[Attribute]
    records: List[Record]
"""

@dataclass
class Relation:
    name: str # name of the relation
    attributes: List[Attribute] # relation schema
    _records: Generator[Record, None, None] # internal iterator for records
    
    @property
    def records(self):
        """Iterator over the relation's records"""
        for r in self._records:
            if isinstance(r, tuple):
                yield Record(fields=r)
            else:
                yield r

    @property
    def attribute_names(self) -> Set[str]:
        return {a.name for a in self.attributes}

    def index_of_attribute(self, name: str) -> int:
        """Returns the position of the given attribute in the relation
        as an index"""
        assert name in self.attribute_names
        for idx, att in enumerate(self.attributes):
            if att.name == name:
                return idx
    
    def uniquify_attributes(self, wrt: Set[str]) -> List[Attribute]:
        return [
            Attribute(a.name if a.name not in wrt else f'{self.name}.{a.name}', a.dtype)
            for a in self.attributes
        ]
    
    def copy_schema(self, name: str) -> "Relation":
        """return new empty relation w/ same schema but new name"""
        return Relation(name, self.attributes, [])

    def record_at(self, idx: int) -> Optional[Record]:
        i = nth(self._records, idx)
        if i is not None and isinstance(i, tuple):
            return Record(i)
        return i

    def size(self) -> Tuple[int, int]:
        c = 0
        for _ in self.records:
            c += 1
        return (len(self.attributes), c)
            
    def generate_records(self, n: int, generators: List[Callable]):
        """Generate N random records for this relation"""
        for _ in range(n):
            tmp = []
            for idx, a in enumerate(self.attributes):
                if generators[idx] is not None:
                    tmp.append(generators[idx]())
                elif a.dtype == str:
                    tmp.append(fake.text(20))
                elif a.dtype == int:
                    tmp.append(random.randint(1,100000))
                elif a.dtype == bool:
                    tmp.append(random.random() < .5)
            self.insert(Record(tuple(tmp)))
    
    def insert(self, rec: Record):
        """Add a record to the relation"""
        assert isinstance(self._records, list)
        self._records.append(rec)

    def materialize(self) -> "Relation":
        return Relation(self.name, self.attributes, list(self.records))

    def __repr__(self):
        t = PrettyTable()
        t.field_names = [a.name for a in self.attributes]
        ri = iter(self.records)
        for rec in take(ri, 10):
            t.add_row(rec.fields)
        try:
            next(ri)
            t.add_row(['...' for _ in range(len(self.attributes))])
        except StopIteration:
            pass
        return t.get_string()


######################
# Relational Operators
######################


def scan(R: Relation):
    for record in R.records:
        for attr, val in zip(R.attributes, record.fields):
            print(f"{attr.name}={val}",end='')
        print('')

def rename(R: Relation, mapping: Dict[str, str]) -> Relation:
    new_att = [
        Attribute(mapping.get(a.name, a.name), a.dtype)
        for a in R.attributes        
    ]
    return Relation(R.name, new_att, R._records)

def project(R: Relation, A: List[int]) -> Relation:
    """keep all attributes in A from R"""
    new_attributes = [R.attributes[i] for i in A]
    new_tuples = map(lambda r: [r.fields[i] for i in A], R.records)
    new_R = Relation(f"{R.name}-project", new_attributes, new_tuples)
    return new_R

def forselect(R: Relation, C: Condition) -> Relation:
    for record in R.records:
        if C(record):
            yield record

def select(R: Relation, C: Condition) -> Relation:
    new_records = filter(C, R.records)
    return Relation(f"{R.name}-select", R.attributes, new_records)

def cross(R: Relation, S: Relation) -> Relation:
    # handle renaming!
    shared_names = R.attribute_names.intersection(S.attribute_names)
    new_attributes = R.uniquify_attributes(shared_names) + S.uniquify_attributes(shared_names)
    
    def _generate_tuples():
        for r_rec in R.records:
            for s_rec in S.records:
                yield Record(r_rec.fields + s_rec.fields)
            
    return Relation(f"{R.name}-join-{S.name}", new_attributes, _generate_tuples())

def join(R: Relation, S: Relation, C: Condition) -> Relation:
    tmp = cross(R, S)
    return select(tmp, C)

def natural_join(R: Relation, S: Relation) -> Relation:
    # determine shared attributes
    shared_attributes = R.attribute_names.intersection(S.attribute_names)
    # figure out their indices
    R_indices = [R.index_of_attribute(a) for a in shared_attributes]
    S_indices = [len(R.attributes) + S.index_of_attribute(a) for a in shared_attributes]
    def _condition(r: Record) -> bool:
        for (Ridx, Sidx) in zip(R_indices, S_indices):
            if r[Ridx] != r[Sidx]:
                return False
        return True

    tmp = cross(R, S)
    return select(tmp, _condition)

def sort(R: Relation, by: Optional[List[int]]) -> Relation:
    def _fn(r: Record):
        return [r[i] for i in by] if by else r.fields
    new_tups = sorted(R.records, key=_fn)
<<<<<<< Updated upstream
    return Relation(f'sort-{R.name}', R.attributes, new_tups)
=======
    return Relation(f"sort-{R.name}", R.attributes, new_tups)
>>>>>>> Stashed changes


def inner_merge_join(R: Relation, S: Relation, A: List[int]) -> Relation:
    """
    Assumes that R and S are sorted according to the attributes in A
    """
    def _join():
        _R = R.records
        _S = S.records
        lwm = 0
        spos = 0
        def advanceR():
            return next(_R)
        def advanceS():
            nonlocal _S, spos
            try:
                r = next(_S)
                spos += 1
                return r
            except StopIteration:
                return None
        def resetS():
            nonlocal _S, spos, lwm
            spos = 0
            _S = S.records
            for i in range(max(0, lwm-1)):
                next(_S)
        def key(rec):
            return [rec[i] for i in A]
        while True:
            try:
                r_rec = advanceR()
            except StopIteration:
                break
            resetS()
            s_rec = advanceS()
            while key(r_rec) > key(s_rec):
                s_rec = advanceS()
                if s_rec is None:
                    break
            lwm = spos
            while key(r_rec) == key(s_rec):
                assert s_rec is not None
                yield r_rec.fields + s_rec.fields
                s_rec = advanceS()
                if s_rec is None:
                    break

    shared_names = R.attribute_names.intersection(S.attribute_names)
    new_attributes = R.uniquify_attributes(shared_names) + S.uniquify_attributes(shared_names)
    return Relation(f"{R.name}-join-{S.name}", new_attributes, _join())

def join2(R: Relation, S: Relation, A: List[int]):
    return inner_merge_join(R, S, A)

def select2(R: Relation, C: Condition):
    def _select():
        rows = R.records
        list(takewhile(lambda x: not C(x), rows))
        for row in R.records:
            if C(row):
                yield row
            else:
                break

    return Relation(f"{R.name}-select", R.attributes, _select())

if __name__ == '__main__':
    SmallZips = Relation("Zips",
              [Attribute("loc", str), Attribute("zip", int)],
              [("Denver", 80114), ("Denver", 80115), ("Lakewood", 80228), ("Golden", 80401)]
             )

    SmallStops = Relation("Stops",
        [Attribute("loc", str), Attribute("cit", bool)],
        [("Golden", False), ("Denver", True),("Denver", False), ("Lakewood", True)]
    )

    BigZips = Relation("BigZips",
    [Attribute("loc", str), Attribute("zip", int)], [])
    BigZips.generate_records(10_000, [city_generator, None])

    BigStops = Relation("BigStops",
        [Attribute("loc", str), Attribute("cit", bool)], [])
    BigStops.generate_records(10_000, [city_generator, None])

    # sorted
    t0 = time.time()
    BigZips2 = sort(BigZips, [0]).materialize()
    BigStops2 = sort(BigStops, [0]).materialize()
    print(inner_merge_join(BigZips2, BigStops2, [0]).size())
    print(time.time() - t0)

    # unsorted
    t0 = time.time()
    print(join(BigStops, BigZips, lambda r: r[0] == r[2]).size())
    print(time.time() - t0)
    
