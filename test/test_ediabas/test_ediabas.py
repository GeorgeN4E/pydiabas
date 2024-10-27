import unittest
import ctypes

from pydiabas.ediabas import EDIABAS, API_STATE, VersionCheckError, JobFailedError


class ediabadTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test___init__(self):
        e = EDIABAS()
        self.assertIsInstance(e._handle, ctypes.c_uint)

    def test_init_end_state(self):
        e = EDIABAS()
        e.init()
        self.assertNotEqual(e._handle, ctypes.c_uint(0))
        self.assertEqual(e.state(), API_STATE.READY)
        e.end()
        self.assertEqual(e.state(), API_STATE.ERROR)

    def test_check_version(self):
        e = EDIABAS()
        e.checkVersion(b"7.0")
        version_str = e.checkVersion()
        version_list = [int(n) for n in version_str.split(".")]
        self.assertTrue(e.checkVersion(version_str))
        self.assertTrue(e.checkVersion(f"{version_list[0]}.{version_list[1]}.{version_list[2]}"))
        self.assertTrue(e.checkVersion(f"{version_list[0]-1}.{version_list[1]}.{version_list[2]}"))
        #self.assertTrue(e.checkVersion(f"{version_list[0]}.{version_list[1]+1}.{version_list[2]}"))
        #self.assertTrue(e.checkVersion(f"{version_list[0]+1}.{version_list[1]}.{version_list[2]}"))

    def test_check_version_only_last_number_too_low(self):
        e = EDIABAS()
        version_str = e.checkVersion()
        version_list = [int(n) for n in version_str.split(".")]
        self.assertTrue(e.checkVersion(f"{version_list[0]}.{version_list[1]}.{version_list[2]+1}"))

    def test_check_version_number_too_low(self):
        e = EDIABAS()
        version_str = e.checkVersion()
        version_list = [int(n) for n in version_str.split(".")]
        with self.assertRaises(VersionCheckError):
            e.checkVersion(f"{version_list[0]}.{version_list[1]+1}.{version_list[2]}")

    def test_check_version_wrong_argument_type(self):
        e = EDIABAS()
        with self.assertRaises(TypeError):
            e.checkVersion(7)
    
    def test_check_version_invalid_version(self):
        e = EDIABAS()
        with self.assertRaises(ValueError):
            e.checkVersion("seven.two")
    
    def test_getConfig(self):
        e = EDIABAS()
        e.init()
        self.assertEqual(e.getConfig("Interface"), "STD:OBD")
        self.assertEqual(e.getConfig("interface"), "STD:OBD")
        self.assertEqual(e.getConfig("INterFACE"), "STD:OBD")
        self.assertEqual(e.getConfig(b"Interface"), "STD:OBD")
    
    def test_getConfig_invalid_key(self):
        e = EDIABAS()
        e.init()
        with self.assertRaises(JobFailedError):
            e.getConfig("XX")
    
    def test_setConfig(self):
        e = EDIABAS()
        e.init()
        traceSize = int(e.getConfig("traceSize"))
        e.setConfig("traceSize", str(traceSize // 2))
        self.assertEqual(e.getConfig("traceSize"), str(traceSize // 2))
    
    def test_setConfig_not_able_to_set(self):
        e = EDIABAS()
        e.init()
        with self.assertRaises(JobFailedError):
            print(e.setConfig("Interface", "XXXX"))

    def test_errorCode_errorText(self):
        e = EDIABAS()
        e.init()
        self.assertEqual(e.errorCode(), 0)
        self.assertEqual(e.errorText(), "NO_ERROR")
        try:
            e.resultByte("X")
        except JobFailedError:
            pass
        self.assertEqual(e.errorCode(), 134)
        self.assertEqual(e.errorText(), "API-0014: RESULT NOT FOUND")

    def test__process_text_argument(self):
        self.assertEqual(EDIABAS._process_text_argument(b"TEst"), b"TEst")
        self.assertEqual(EDIABAS._process_text_argument("TEst"), b"TEst")
    
    def test__process_text_argument_wrong_type(self):
        with self.assertRaises(TypeError):
            EDIABAS._process_text_argument(2)
    
    def test__process_text_argument_unicode_error(self):
        with self.assertRaises(ValueError):
            EDIABAS._process_text_argument("\udcc3")
        
    def test___eq__(self):
        e1 = EDIABAS()
        e2 = EDIABAS()
        e3 = EDIABAS()

        e1._handle = ctypes.c_uint(1)
        e2._handle = ctypes.c_uint(1)
        e3._handle = ctypes.c_uint(2)

        self.assertTrue(e1 == e2)
        self.assertFalse(e1 == e3)
        self.assertFalse(e2 == e3)
        