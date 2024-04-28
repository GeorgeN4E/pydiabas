from __future__ import annotations

from . import ediabas
from .result import Result
from .exceptions import StateError


# TODO Documentation


class PyDIABAS():
    def __init__(self, **kwargs) -> PyDIABAS:
        self._ediabas = ediabas.EDIABAS()
        self._config = {kwarg.lower(): kwargs[kwarg] for kwarg in kwargs}
    
    def __enter__(self) -> PyDIABAS:
        self.start()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.end()
        return False
    
    def start(self) -> None:
        self._ediabas.initExt(configuration=";".join(f"{item[0]}={item[1]}" for item in self._config.items()))
        
        if self._ediabas.state() == ediabas.API_STATE.ERROR:
            raise StateError(self._ediabas.errorText())

    def end(self):
        self._ediabas.end()

    @property
    def ready(self):
        return self._ediabas.state() == ediabas.API_STATE.READY
    
    @property
    def state(self):
        return self._ediabas.state()
    
    @property
    def ediabas(self):
        return self._ediabas
    
    def reset(self):
        self.end()
        self.start()
        
    def job(self, ecu: str, job: str, parameters: str | list[str] = "", results: str | list[str] = "") -> Result:

        # Separate multiple parameters using a semicolon
        if isinstance(parameters, list):
            parameters = ";".join(parameters)
        
        # Separate multiple result filters using a semicolon
        if isinstance(results, list):
            results = ";".join(results)

        self._ediabas.job(ecu, job, parameters, results)
        
        while self._ediabas.state() == ediabas.API_STATE.BUSY:
            pass

        if self._ediabas.state() == ediabas.API_STATE.ERROR:
            raise StateError(self._ediabas.errorText())

        return Result(self._ediabas, results.split(",")).fetchall().as_dicts
    
    
    def jobData(self, ecu: str, job: str, parameters: bytes = b"", results: str | list[str] = "") -> Result:

        self._ediabas.jobData(ecu, job, parameters, results)
        
        while self._ediabas.state() == ediabas.API_STATE.BUSY:
            pass

        if self._ediabas.state() == ediabas.API_STATE.ERROR:
            raise StateError(self._ediabas.errorText())

        return Result(self._ediabas, results.split(",")).fetchall().as_dicts

    def config(self, **kwargs) -> dict:
        add_config = {kwarg.lower(): kwargs[kwarg] for kwarg in kwargs}

        for item in add_config:
            self._ediabas.setConfig(item, f"{add_config[item]}")

        self._config = self._config | add_config
    
        return self._config
