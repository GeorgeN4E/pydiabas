class EDIABASError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class JobFailedError(EDIABASError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)