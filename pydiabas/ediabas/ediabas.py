from __future__ import annotations
import ctypes

from . import api32
from . import statics
from .exceptions import JobFailedError


class EDIABAS():


    """Class to interact with the EDIABAS Api api32.dll

    Configuration details:
        apiTrace: Controls the type and intensity (default: 0)  
            0 = OFF
            1-3 = user trace
            4-7 = api trace
            8 = debug trace

        BipDebugLevel: Debug level in SGBD (default: 0)
            0 - 32767

        BipEcuFile: Name of the currently loaded SGBD file as string

        BipErrorLevel: Error level in SGBD (default: 0)
            0 - 32767

        ClampHandling: Auto reading of Kl. R and Kl. 15 (default: 1)
            0 = OFF
            1 = ON

        EcuPath: Path to ECU files

        EdiabasIniPath: Path to EDIABAS.INI

        EdiabasVersion: Version of current EDIABAS

        IfhTrace: Control of IFH trace (default: 0)
            0 = OFF
            1-3: trace

        IfhnTrace: Control of IFH network trace (default: 0)
            0 = OFF
            1-3: trace
        
        IfhVersion: Version of current IFH

        Interface: Interface to be used (default: EDIC)
            STD:OBD: For D-CAN cable
        
        IgnitionHandling: Handle ignition ON/OFF as an error (default: 1)
            0 = OFF
            1 = ON

        LoadWin32: Win16 / Win32 selector (default: 1)
            0 = For Windows 95, 98, ME
            1 = For Windows NT, 2000, XP, Vista and on
        
        LogLevel: Logging of fatal errors in EDIABAS.LOG (default: 0)
            0 = OFF
            1 = ON

        NetworkProtocol: Network protocol to be used
            TCP

        RetryComm: Retry after communication errors (default: 1)
            0 = OFF
            1 = ON

        Session: Name of current EDIABAS session

        ShowIcon: Controls if system tray icon is shown while EDIABAS is running (default: 1)
            0 = OFF
            1 = ON

        Simulation: Switches EDIABAS in simulation mode (default: 0)
            0 = OFF
            1 = ON

        SimulationPath: Path to ECU sim files

        SystemResults: Ignition, supply voltage and job status in system results (default: 1)
            0 = OFF
            1 = ON

        TaskPriority: EDIABAS priority (default: 0)
            0 = Optimal
            1 = Lowest
            10 = Highest

        TraceBuffering: Buffer trace files (default: 0)
            0 = OFF
            1 = ON

        TraceHistory: Archive trace files (default: 0)
            0 = OFF
            1 = ON

        TracePath: Path to store trace file to

        TraceSize: Maximum size of trace files (default: 1024)
            0-32767

        TraceSync: Include sync information in trace (default: 0)
            0 = OFF
            1 = ON

        TraceWriter: Path to trace writer program (.DLL)

        UbattHandling: Handle supply voltage ON/OFF as an error (default: 1)
            0 = OFF
            1 = ON
    """

    def __init__(self) -> None:

        """Create an object to interact with the EDIABAS system
        """
        self._handle = ctypes.c_uint()


    def init(self) -> None:

        """Initializes the EDIABAS API and connect to the server.
        
        Parameters:
        None

        Side effects:
        _handle will be set to the value of the newly initialized API"""
        
        # Value of _handle will be set through side effect of apiInit function
        job_status = api32.apiInit(ctypes.byref(self._handle))

        if not job_status:
            raise JobFailedError


    def initExt(
        self,
        ifh : str = "",
        deviceUnit : str = "",
        deviceApplication : str = "",
        configuration : str = ""
    ) -> None:

        """Initializes the EDIABAS API and connect to the server.
        All parameters are set to an empty string by default. If the function passes an empty string
        to the EDIABAS system, the values are set be EDIABAS according to system defaults or setting
        from configuration files.
        The effect of the parameters deviceUnit and deviceApplication is not yet known and should not be used.
        To pass additional configuration setting the configuration parameter can be used. Multiple configuration
        data must be separated by semicolons like "apiTrace=7;TracePath=C:\\MyTrace\\EDIABAS" (not case sensitive).
        
        Optional parameters:
        ifh (str): Name of the interface handler to be used eg. STD:OBD.
        deviceUnit (str): Name of the device (only one character). The effect of this parameter is not yet known.
        deviceApplication (str): Name of the device application. The effect of this parameter is not yet known.
        configuration (str): Additional configuration setting. Multiple settings must be separated by semicolons.

        Side effects:
        _handle will be set to the value of the newly initialized API"""
        

        # Value of _handle will be set through side effect of apiInit function
        job_status = api32.apiInitExt(
            ctypes.byref(self._handle),
            ifh.encode("UTF-8"),
            deviceUnit.encode("UTF-8"),
            deviceApplication.encode("UTF-8"),
            configuration.encode("UTF-8")
        )

        if not job_status:
            raise JobFailedError


    def breakJob(self) -> None:

        """Stops the current job. All results will be lost."""

        # Break the current job
        api32.apiBreak(self._handle)


    def end(self) -> None:

        """Stops EDIABAS API and frees used memory again"""

        # Stop EDIABAS API
        api32.apiEnd(self._handle)


    def state(self) -> statics.API_STATE:

        """Retrieves current API state and returns the value as API_STATE IntEnum type

        Return values:
        state (API_STATE): Name of current API state"""

        # Get current state of EDIABAS API
        state = api32.apiState(self._handle)

        # Return translated API state
        return statics.API_STATE(state)


    def trace(
        self,
        text : str
    ) -> None:

        """Prints a message in the EDIABAS apiTrace

        Parameters:
        text (str): Text to be printed to the EDIABAS apiTrace file in UTF-8 coding"""
        
        # Call function with encoded text (bytestring)
        api32.apiTrace(self._handle, text.encode("UTF-8"))


    @staticmethod
    def checkVersion(min_version : str) -> str | False:
        
        """Checks if the EDIABAS version meets the required minimum version number.
        Only the first two parts of the version number is taken into account. So if 7.1.3 is passed
        as minimum version number and current version is 7.1.0 the version test is passed.
        If no version number or a version number smaller than 7.0.x is passed by the parameter, version 7.0.x
        is set as minimum by default.
        Minimum required version may be passed with one ore two separators like "7.1" or "7.1.0" but not like "7"

        Parameters
        min_version (str): Minimum required version number like "7.1" or "7.1.0" but not like "7"

        Return values
        version (str or False): False if test is not passed and current version number as str if test is passed"""

        # Separate version number
        min_version = min_version.split(".")

        # Version number must be passed like (major*256 + minor) like 0x0703 for 7.3
        min_version = (int(min_version[0]) << 8) + int(min_version[1])

        # Initialize variable to save current version number in by the dll function
        version = ctypes.create_string_buffer(statics.API_MAX_CONFIG)

        # Call the function and retrieve the status
        job_status = api32.apiCheckVersion(min_version, version)

        # Check if minimum version check has been passed
        if not job_status:
            return False
        
        # Return current version number as string
        else:
            return version.value.decode("UTF-8")


    def getConfig(
        self,
        name: str
    ) -> str:

        """Retrieves the value of a configuration variable with the given name or None
        if a variable with the name cannot be found.

        Parameters:
        name (str): Name of the configuration variable who's value is to be retrieved.

        Return values:
        value (str): Value of the configuration variable."""

        # Create a char array t store the value of the variable
        cfg_value = ctypes.create_string_buffer(statics.API_MAX_CONFIG)

        # Call the job and get save its return value
        # Variable value will be copied to cfg_value through side effect of the called function
        job_status = api32.apiGetConfig(
            self._handle,
            name.encode("UTF-8"),
            cfg_value
        )

        if not job_status:
            raise JobFailedError

        # Transform the value into str and return
        return cfg_value.value.decode("UTF-8")


    def setConfig(
        self,
        name : str,
        value : str
    ) -> None:

        """Sets the value of a configuration variable.
        Changes are valid until the end of the API session.

        Parameters:
        name (str): Name of the configuration variable who's value is to be set.
        value (str): New value of the variable."""

        # Call job with encoded data and store its return value
        job_status = api32.apiSetConfig(
            self._handle,
            name.encode("UTF-8"),
            value.encode("UTF-8")
        )

        if not job_status:
            raise JobFailedError


    def errorCode(self) -> int:

        """Retrieves the error code from EDIABAS.

        Return values:
        error_code (int): Current error code."""

        # Call job and store return value es error code
        error_code = api32.apiErrorCode(self._handle)

        # Return the received error code
        return error_code


    def errorText(self) -> str:

        """Retrieves the error text from EDIABAS.

        Return values:
        error_text (str): Current error text."""

        # Create a char array to hold the error text
        error_text = ctypes.create_string_buffer(statics.API_MAX_TEXT)

        # Call the job and save the return value (Null or pointer to char array)
        job_status = api32.apiErrorText(
            self._handle,
            error_text,
            ctypes.c_int(statics.API_MAX_TEXT)
        )

        # Check if error is present
        if job_status == 0:
            return "NO_ERROR"

        # Return error text as str
        return error_text.value.decode("UTF-8")


    def job(
        self,
        ecu : str,
        job_name : str,
        job_param : str = "",
        results : str = ""
    ) -> None:

        """Sends a job via EDIABAS to the selected ECU.
        ECU and jobname must at least be specified.
        jobData and jobDataExt accept job_param as str and bytes, job only accepts job_param as str.

        Parameters:
        ecu (str): The ECU to which the job has to be send
        job_name (str): Name of the job to be executed (not case sensitive)
        
        Optional parameters:
        job_param (str): Parameters to be passed to the ECU (default: "")
        results (str): Results to be retrieved from the ECU. If "" is passed, all results will be retrieved (default: "")"""

        # Send job to ECU
        api32.apiJob(
            self._handle,
            ecu.encode("UTF-8"),
            job_name.encode("UTF-8"),
            job_param.encode("UTF-8"),
            results.encode("UTF-8")
        )


    def jobData(
        self,
        ecu : str,
        job_name : str,
        job_param : str | bytes = "",
        results : str = ""
    ) -> None:

        """Sends a job via EDIABAS to the selected ECU.
        ECU and jobname must at least be specified.
        jobData and jobExt accept job_param as str and bytes, job only accepts job_param as str.

        Parameters:
        ecu (str): The ECU to which the job has to be send
        job_name (str): Name of the job to be executed (not case sensitive)
        
        Optional parameters:
        job_param (str and bytes): Parameters to be passed to the ECU (default: "")
        results (str): Results to be retrieved from the ECU. If "" is passed, all results will be retrieved (default: "")"""

        # Encode str to bytes 
        if type(job_param) == str:
            job_param = job_param.encode("UTF-8")
        
        # Send job to ECU
        api32.apiJobData(
            self._handle,
            ecu.encode("UTF-8"),
            job_name.encode("UTF-8"),
            job_param,
            ctypes.c_int(len(job_param)),
            results.encode("UTF-8")
        )


    def jobExt(
        self,
        ecu : str,
        job_name : str,
        std_param : str = "",
        job_param : str | bytes = "",
        results : str = ""
    ) -> None:

        """Sends a job via EDIABAS to the selected ECU.
        ECU and jobname must at least be specified.
        jobData and jobExt accept job_param as str and bytes, job only accepts job_param as str.
        Additional parameters used by EDIABAS when calling BEST/1 or BEST/2 standart jobs
        (INITIALISIERUNG, IDENTIFIKATION, ENDE) may be passed.

        Parameters:
        ecu (str): The ECU to which the job has to be send
        job_name (str): Name of the job to be executed (not case sensitive)
        
        Optional parameters:
        std_param (str): Parameters to be passed to EDIABAS standart jobs
        job_param (str and bytes): Parameters to be passed to the ECU (default: "")
        results (str): Results to be retrieved from the ECU. If "" is passed, all results will be retrieved (default: "")"""

        # Encode str to bytes 
        if type(job_param) == str:
            job_param = job_param.encode("UTF-8")
        
        # Send job to ECU
        # Last parameter is always c_long(0) as it is not yet used by EDIABAS and reserved for further extension
        api32.apiJobData(
            self._handle,
            ecu.encode("UTF-8"),
            job_name.encode("UTF-8"),
            std_param.encode("UTF-8"),
            ctypes.c_int(len(std_param)),
            job_param,
            ctypes.c_int(len(job_param)),
            results.encode("UTF-8"),
            ctypes.c_long(0)
        )


    def jobInfo(
        self,
        text : bool = False
    ) -> int | str:

        """Retrieves the progress of the current job in percent and if requested additional text infos.
        If returning the progress of the job is not implemented in SGBD, the function will return -1.

        Optional parameters:
        text (bool): Changes type of return value to str and adds additional info if implemented in SGBD (default: False)

        Return values:
        job_status (int or str): job process in % if parameter text is False or as str with additional information."""

        # Create a char array to hold the error text
        info_text = ctypes.create_string_buffer(statics.API_MAX_TEXT)

        # Call job and receive return value, info_text will be set trough side effect of called function
        job_status = api32.apiJobInfo(
            self._handle,
            info_text
        )

        # Return job status as str with additional info if requested by text parameter
        if text:
            return f"{job_status} {info_text.value}"

        # Return job status as int
        return job_status


    def resultBinary(
        self,
        name : str,
        set : int = 1
    ) -> bytes:

        """Retrieves BINARY (unsigned byte) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (bytes or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variables to store the answer
        result = ctypes.create_string_buffer(statics.API_MAX_TEXT)
        result_len = ctypes.c_ushort()

        # Get the result from the ECU
        job_status = api32.apiResultBinary(
            self._handle,
            ctypes.byref(result),
            ctypes.byref(result_len),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as bytes
        return result.value


    def resultBinaryExt(
        self,
        name : str,
        set : int = 1,
        max_length : int = statics.API_MAX_BINARY
    ) -> str:

        """Retrieves BINARY (unsigned byte) data with a given maximum length from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default.

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        length (int): Number of bytes to be read. (default and maximum: statics.API_MAX_BINARY [1024])
        
        Return values:
        result (bytes or None): value of the requested result or None if request failed or requested result no present"""

        # Check that given maximum length is limited to statics.API_MAX_BINARY
        max_length = min(max_length, statics.API_MAX_BINARY)

        # Initialize variables to store the answer
        result = ctypes.create_string_buffer(max_length)
        result_len = ctypes.c_ushort()

        # Get the result from the ECU
        job_status = api32.apiResultBinaryExt(
            self._handle,
            ctypes.byref(result),
            ctypes.byref(result_len),
            ctypes.c_ushort(max_length),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as bytes
        return result.value


    def resultByte(
        self,
        name : str,
        set : int = 1
    ) -> bytes:

        """Retrieves BYTE (unsigned byte) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (bytes or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.c_ubyte()

        # Get the result from the ECU
        job_status = api32.apiResultByte(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as bytes
        return result.value


    def resultChar(
        self,
        name : str,
        set : int = 1
    ) -> bytes:

        """Retrieves CHAR (char) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (bytes or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.c_char()

        # Get the result from the ECU
        job_status = api32.apiResultChar(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as bytes
        return result.value


    def resultDWord(
        self,
        name : str,
        set : int = 1
    ) -> int:

        """Retrieves DWORD (unsigned short) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (int or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.c_ushort()

        # Get the result from the ECU
        job_status = api32.apiResultDWord(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as int
        return result.value


    def resultInt(
        self,
        name : str,
        set : int = 1
    ) -> int:

        """Retrieves INTEGER (short) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (int or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.c_short()

        # Get the result from the ECU
        job_status = api32.apiResultInt(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as int
        return result.value


    def resultLong(
        self,
        name : str,
        set : int = 1
    ) -> int:

        """Retrieves LONG (long) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (int or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.c_long()

        # Get the result from the ECU
        job_status = api32.apiResultLong(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as int
        return result.value


    def resultReal(
        self,
        name : str,
        set : int = 1
    ) -> float:

        """Retrieves REAL (double) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (float or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.c_double()

        # Get the result from the ECU
        job_status = api32.apiResultReal(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as float
        return float(result.value)


    def resultText(
        self,
        name : str,
        set : int = 1,
        format : str = ""
    ) -> str:

        """Retrieves TEXT (char) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default.
        The format of type casting from different types than TEXT may be specified as follows:
            [flush][min length]["."decimal places][exponent][type]

            flush:
                If omitted: Flush right
                "-": Flush left

            min length:
                Sets the minimum field length. Will be filled with spaces if needed
            
            "."decimal places: (must be started with a "." to be distinguished from "min length")
                Sets the number of decimal places in case of a REAL (double)
                Sets the maximum field length in case of TEXT (str)
            
            exponent:
                if omitted: REAL (double) will be printed as regular floating point number
                "E": Specified that REAL (double) will be printed as exponential expression like 2.33E3
                "e": Specified that REAL (double) will be printed as exponential expression like 2.33e3

            type: (states the type of input variable)
                "C": CHAR (char)
                "B": BYTE (unsigned byte)
                "I": INTEGER (short)
                "W": WORD (unsigned short)
                "L": LONG (long)
                "D": DWORD (unsigned long)
                "R": REAL (double)
                "T": TEXT (char array)

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        format (str): Format for type conversion to text (default: "")
        
        Return values:
        result (str or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.create_string_buffer(statics.API_MAX_TEXT)

        # Get the result from the ECU
        job_status = api32.apiResultText(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set),
            format.encode("UTF-8")
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as string if possible, otherwise as bytes
        return result.value.decode("UTF-8", errors="backslashreplace")


    def resultWord(
        self,
        name : str,
        set : int = 1
    ) -> int:

        """Retrieves WORD (unsigned short) data from an API job result.
        Result name must be specified. If no set number is passed, set #1 is accessed by default

        Parameters:
        name (str): Name of the result to be retrieved (not case sensitive)

        Optional parameters:
        set (int): Number of result set to be accessed (default: 1)
        
        Return values:
        result (int or None): value of the requested result or None if request failed or requested result no present"""

        # Initialize variable to store the answer
        result = ctypes.c_uint()

        # Get the result from the ECU
        job_status = api32.apiResultWord(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            ctypes.c_int(set)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as int
        return result.value


    def resultVar(self) -> str:

        """Extract the variant of the ECU from the result data.

        Return value:
        result (str): Name of the ECU variant."""

        # Initialize variable to store the answer
        result = ctypes.create_string_buffer(statics.API_MAX_RESULT)
        
        # Get the result from the ECU
        job_status = api32.apiResultVar(
            self._handle,
            result
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as str
        return result.value.decode("UTF-8")


    def resultSets(self) -> int:

        """Retrieves the number of result sets in the current result data as int.
        Set 0 (containing ECU and result data) is not counted. So only sets containing results are counted.
        
        Return values:
        result (int): Number of result sets in the current result"""

        # Initialize variable to store the answer
        result = ctypes.c_ushort()

        # Get the result from the ECU
        job_status = api32.apiResultSets(
            self._handle,
            ctypes.byref(result)
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as int
        return result.value


    def resultNumber(
        self,
        set : int = 1
    ) -> int:

        """Retrieves the number of results in the given set as int.
        If no set is specified, the first result set (#1) is used.
        
        Optional Parameters:
        set (int): Set to be checked for number of results (default: 1)

        Return values:
        result (int): Number of results in the given set"""

        # Initialize variable to store the answer
        result = ctypes.c_ushort()

        # Get the result from the ECU
        job_status = api32.apiResultNumber(
            self._handle,
            ctypes.byref(result),
            set
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()(self.errorText())

        # Return result as int
        return result.value


    def resultName(
        self,
        position : int = 1,
        set : int = 1
    ) -> str:

        """Retrieves the name of a given result in a given set and position as str.
        Sets are indexed from 0, but set 0 holds only basic data about job and ECU and no results.
        Positions are indexed from 1, so the first result in a set is at position 1 NOT at position 0!
        If no set is specified, the first result set (#1) is used.
        If no position is specified, the first position (#1) is used.

        Optional Parameters:
        set (int): Set to be checked for number of results (default: 1)
        position (int): Position in the given set to be read. Indexed from 1 (default: 1)

        Return values:
        result (str): Name of result at given position in the given set"""

        # Initialize variable to store the answer
        result = ctypes.create_string_buffer(statics.API_MAX_RESULT)

        # Get the result from the ECU
        job_status = api32.apiResultName(
            self._handle,
            ctypes.byref(result),
            position,
            set
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as str
        return result.value.decode("UTF-8")


    def resultFormat(
        self,
        name : str,
        set : int = 1
    ) -> statics.API_RESULT_FORMAT:

        """Retrieves the format of a given result in a given set as API_RESULT_FORMAT.
        Sets are indexed from 0, but set 0 holds only basic data about job and ECU and no results.
        If no set is specified, the first result set (#1) is used.

        Parameters:
        name (str): Name of the result the format has to be checked of.

        Optional Parameters:
        set (int): Set to be checked for number of results (default: 1)

        Return values:
        result (API_RESULT_FORMAT): Format of the result in the given set"""

        # Initialize variable to store the answer
        result = ctypes.c_int()

        # Get the result from the ECU
        job_status = api32.apiResultFormat(
            self._handle,
            ctypes.byref(result),
            name.encode("UTF-8"),
            set
        )

        # Check if date has been received
        if not job_status:
            raise JobFailedError()

        # Return result as API_RESULT_FORMAT
        return statics.API_RESULT_FORMAT(result.value)


    def resultsNew(self) -> int:

        """Saves a copy of the result field of the current job. Completion of a running job is waited for.
        The returned value is the address to the saved result field and can be used by resultsScope and resultsDelete.

        Return values:
        result_address (int): Memory address of the saved data."""

        # Call job and save return value
        result_address = api32.apiResultsNew(self._handle)

        # Return data
        return result_address


    def resultsScope(
        self,
        address : int
    ) -> None:

        """Sets the address of the saved result data to be used.
        The result functions will use this data until changed again by resultsScope or a new job has been started."""

        # Set address
        api32.apiResultsScope(
            self._handle,
            address
        )


    def resultsDelete(
        self,
        address : int
    ) -> None:

        """Deletes the saved results at the given address and free the used memory."""

        # Free memory
        api32.apiResultsDelete(
            self._handle,
            address
        )
