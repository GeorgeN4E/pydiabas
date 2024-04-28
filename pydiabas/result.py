from __future__ import annotations
from collections import namedtuple

from . import ediabas
from .ediabas import utils


class Result():
    def __init__(self, pydiabas: ediabas.EDIABAS, result_filter: list[str] = []) -> Result:
        if not isinstance(pydiabas, ediabas.EDIABAS):
            raise TypeError("pydiabas need to be an instance of PyDIABAS")

        self._pydiabas = pydiabas
        self._sets: list[Set] = []
        self._systemResult: Set = Set()
        self._result_filter = []

        for item in result_filter:
            if item:
                self._result_filter.append(item.upper())

    def clear(self) -> None:
        self._sets = []

    def fetchsystem(self) -> Result:
        rows: list[Row] = []
        for pos in range(1, self._pydiabas.resultNumber(set=0) + 1):
            result_name = self._pydiabas.resultName(position=pos, set=0)
            rows.append(Row(result_name, utils.getResult(self._pydiabas, result_name, set=0)))
        self._systemResult = Set(rows)
        
        return self
    
    def fetchall(self) -> Result:
        self.fetchsystem()
        
        for set in range(1, self._pydiabas.resultSets() + 1):
            rows: list[Row] = []
            for pos in range(1, self._pydiabas.resultNumber(set=set) + 1):
                result_name = self._pydiabas.resultName(position=pos, set=set).upper()
                rows.append(Row(result_name, utils.getResult(self._pydiabas, result_name, set=set)))
            self._sets.append(Set(rows))
        
        return self
        
    def fetchjobresults(self) -> Result:
        for set in range(1, self._pydiabas.resultSets() + 1):
            rows: list[Row] = []
            for result_name in self._result_filter:
                result_value = utils.getResult(self._pydiabas, result_name, set=set)
                if result_value is not None:
                    rows.append(Row(result_name, result_value))
            self._sets.append(Set(rows))
        
        return self

    def fetchset(self, set: int = 0) -> Result:
        rows: list[Row] = []
        for pos in range(1, self._pydiabas.resultNumber(set=set + 1) + 1):
            result_name = self._pydiabas.resultName(position=pos, set=set + 1).upper()
            rows.append(Row(result_name, utils.getResult(self._pydiabas, result_name, set=set + 1)))
        self._sets.append(Set(rows))
        
        return self

    def fetchname(self, name: str) -> Result:
        for set in range(1, self._pydiabas.resultSets() + 1):
            rows: list[Row] = []
            result_value = utils.getResult(self._pydiabas, name, set=set)
            if result_value is not None:
                rows.append(Row(name.upper(), result_value))
            self._sets.append(Set(rows))
        
        return self

    def fetchnames(self, names: list[str]) -> Result:
        names = [name.upper() for name in names]
        for set in range(1, self._pydiabas.resultSets() + 1):
            rows: list[Row] = []
            for result_name in names:
                result_value = utils.getResult(self._pydiabas, result_name, set=set)
                if result_value is not None:
                    rows.append(Row(result_name, result_value))
            self._sets.append(Set(rows))
        
        return self

    @property
    def all(self) -> list[Set]:
        return self._sets

    @property
    def as_dicts(self) -> list[dict]:
        return [self._systemResult.as_dict] + [s.as_dict for s in self._sets]

    @property
    def ecu(self) -> str:
        return self._systemResult["VARIANTE"]

    @property
    def jobname(self) -> str:
        return self._systemResult["JOBNAME"]

    @property
    def jobstatus(self) -> str:
        return self._systemResult["JOBSTATUS"]

    @property
    def systemResult(self) -> str:
        return self._systemResult

    def count(self, name: str) -> int:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        n = 0
        for set in self._sets:
            for row in set:
                if name.upper() == row.name.upper():
                    n += 1
        return n

    def index(self, name: str, start: int = 0, end: int | None = None) -> int:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        for i, set in enumerate(self._sets[start:end if end else len(self._sets)]):
            for row in set:
                if name.upper() == row.name.upper():
                    return i + start
        
        raise ValueError(f"'{name}' is not in result")
    
    def get(self, name: str, default=None) -> int | str | bytes | float:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        for set in self._sets:
            try:
                return set[name]
            except KeyError:
                pass
        
        return default
    
    def __len__(self) -> int:
        return len(self._sets)

    def __bool__(self) -> bool:
        return bool(self._sets)
    
    def __iter__(self) -> Result:
        self._n = 0
        return self
    
    def __next__(self) -> Set:
        if self._n < self.__len__():
            result = self._sets[self._n]
            self._n += 1
            return result
        else:
            raise StopIteration
    
    def __str__(self) -> str:
        s = "-------------- EDIABAS Result --------------\n"

        if self.systemResult:
            s += "\nsystemResult:\n"
            for key in self.systemResult:
                s += f"    {key:30}: {self.systemResult[key]}\n"

        for i, set in enumerate(self._sets):
            s += f"\nSet {i}:\n"
            for j, row in enumerate(set):
                s += f"    {row.name:30}: {row.value}"
                if j < len(set) - 1:
                    s += "\n"

        return s
    
    def __getitem__(self, key: str | int | slice) -> Row | int | str | bytes | float:
        if isinstance(key, (int, slice)):
            return self._sets[key]
            
        elif isinstance(key, str):
            for set in self._sets:
                for row in set:
                    if key.upper() == row.name.upper():
                        return row.value
            raise KeyError
            
        else:
            raise AttributeError

    def __contains__(self, name: str) -> bool:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        for set in self._sets:
            for row in set:
                if name.upper() == row.name.upper():
                    return True
        
        return False



class Set():
    def __init__(self, rows: list[Row] = []) -> Set:
        if not isinstance(rows, list):
            raise TypeError("rows need to be a list containing Row instances")
        
        for row in rows:
            if not isinstance(row, Row):
                raise TypeError("rows need to be a list containing Row instances")

        self._rows = rows

    @property
    def all(self) -> list[Row]:
        return self._rows

    @property
    def as_dict(self):
        return {row.name: row.value for row in self._rows}


    def count(self, name: str) -> int:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        n = 0
        for row in self._rows:
            if name.upper() == row.name.upper():
                n += 1
        return n

    def index(self, name: str, start: int = 0, end: int | None = None) -> int:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        for i, row in enumerate(self._rows[start:end if end is not None else len(self._rows)]):
            if row.name.upper() == name.upper():
                return i + start
        
        raise ValueError(f"'{name}' is not in result set")
    
    def keys(self) -> list:
        return [row.name for row in self._rows]

    def values(self) -> list:
        return [row.value for row in self._rows]

    def items(self) -> list[tuple]:
        return [(row.name, row.value) for row in self._rows]

    def has_key(self, name: str) -> bool:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")
        
        for row in self._rows:
            if name.upper() == row.name.upper():
                return True

        return False
    
    def get(self, name: str, default=None) -> int | str | bytes | float:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        try:
            return self[name]
        except KeyError:
            return default

    def __len__(self) -> int:
        return len(self._rows)
    
    def __bool__(self) -> bool:
        return bool(self._rows)
        
    def __iter__(self) -> Row:
        self._n : int = 0
        return self

    def __next__(self) -> Row:
        if self._n < self.__len__():
            result = self._rows[self._n]
            self._n += 1
            return result
        else:
            raise StopIteration
    
    def __str__(self) -> str:
        s = ""
        for i, row in enumerate(self._rows):
            s += f"{row.name:30}: {row.value}"
            if i < len(self) - 1:
                s += "\n"
        return s

    def __getitem__(self, key: str | int | slice) -> int | str | bytes | float:
        if isinstance(key, (int, slice)):
            return self._rows[key]
            
        elif isinstance(key, str):
            for row in self._rows:
                if key.upper() == row.name.upper():
                    return row.value
            raise KeyError
            

        else:
            raise AttributeError
        
    def __contains__(self, name: str) -> bool:
        if not isinstance(name, str):
            raise TypeError("name need to be a string")

        for row in self._rows:
            if name.upper() == row.name.upper():
                return True
        
        return False


Row = namedtuple("row", ["name", "value"])