from .base import ECU

class BlockCreateError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class BlockReadError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MSD80(ECU):
    NAME = "MSD80"

    COMBUSTION_MODE = {
        1: "Stratified",
        2: "Homogen",
        3: "Lean"
    }

    def __init__(self) -> None:
        self.block = []
        self.last_read_function = None
        super().__init__()

    def set_block(self, connection, values):
        self.block = []
        result = connection.job(
            ecu=self.NAME,
            job="STATUS_MESSWERTBLOCK_LESEN",
            parameters=["2"] + values
        )
        if result[1]["JOB_STATUS"] == "OKAY":
            self.block = values
            self.last_read_function = lambda: self.set_block(connection, values)
            return [s.all for s in result.all]

        if result[1]["JOB_STATUS"] == "ERROR_TABLE":
            self.block = []
            raise BlockCreateError("Values from MESSWERTETAB where NAME is '-' are only supported as very last item in value list")
        
        raise BlockCreateError(f"JOB_STATUS: {result[0]['JOB_STATUS']}")
        
    def read_block(self, connection, values=None):

        if values is None:
            values = self.block

        result = connection.job(
            ecu=self.NAME,
            job="STATUS_MESSWERTBLOCK_LESEN",
            parameters=["3"] + values
        )
        if result[1]["JOB_STATUS"] == "OKAY":
            self.last_read_function = lambda: self.read_block(connection, values)
            return result
        
        if result[1]["JOB_STATUS"] == "ERROR_ARGUMENT":
            raise BlockReadError("Block does not contain all requested values")

        if result[1]["JOB_STATUS"] == "ERROR_TABLE":
            self.block = []
            raise BlockCreateError("Values from MESSWERTETAB where NAME is '-' are only supported as very last item in value list")
        
        if result[1]["JOB_STATUS"] == "ERROR_ECU_CONDITIONS_NOT_CORRECT_OR_REQUEST_SEQUENCE_ERROR":
            self.block = []
            raise BlockReadError("No block available in ECU")

        raise BlockReadError(f"JOB_STATUS: {result[0]['JOB_STATUS']}")

    def read(self, connection, values):
        self.block = []
        result = connection.job(
            ecu=self.NAME,
            job="MESSWERTBLOCK_LESEN",
            parameters=",".join(values)
        )
        if result[1]["JOB_STATUS"] == "OKAY":
            self.last_read_function = lambda: self.read(connection, values)
            return result

        raise BlockReadError(f"JOB_STATUS: {result[0]['JOB_STATUS']}")
    
    def read_auto(self, connection, values, change_block=True):
        try:
            return self.read_block(connection, values)
        except BlockReadError:
            if change_block:
                try:
                    return self.set_block(connection, values)
                except BlockCreateError:
                    return self.read(connection, values)
        
        return values
    
    def read_again(self):
        if self.last_read_function is None:
            raise BlockReadError("No successful reading until now")
        
        return self.last_read_function()

