import unittest
from pydiabas import Result, Set, Row, PyDIABAS, StateError, ConfigError
from pydiabas.ediabas import EDIABAS

__all__ = [
    "PyDIABASTest"
]


class PyDIABASTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def test_init(self):
        p = PyDIABAS()
        self.assertIsInstance(p._ediabas, EDIABAS)
        self.assertEqual(p._config, {})
    
    def test_start(self):
        p = PyDIABAS()
        self.assertEqual(p._ediabas.state(), 3)
        p.start()
        self.assertEqual(p._ediabas.state(), 1)
    
    def test_end(self):
        p = PyDIABAS()
        p.start()
        self.assertEqual(p._ediabas.state(), 1)
        p.end()
        self.assertEqual(p._ediabas.state(), 3)

    def test_reset(self):
        p = PyDIABAS()
        p.start()
        try:
            p.job("XX", "XX")
        except StateError:
            pass
        self.assertEqual(p._ediabas.state(), 3)
        p.reset()
        self.assertEqual(p._ediabas.state(), 1)

    def test_property_ready(self):
        p = PyDIABAS()
        self.assertFalse(p.ready)
        p.start()
        self.assertTrue(p.ready)

    def test_property_ediabas(self):
        p = PyDIABAS()
        self.assertEqual(p._ediabas, p.ediabas)

    def test_config(self):
        p = PyDIABAS()
        p.start()
        # Confirm returning current config, beeing an empty dict initialle
        self.assertEqual(p.config(), {})

        # Confirm accepting and returning current config, all lower case letters
        self.assertEqual(p.config(traceSize=4096), {"tracesize": 4096})

        # Confirm change in EDIABAS system
        self.assertEqual(p.ediabas.getConfig("traceSize"), "4096")

        # Confirm beeing case insensitive and adding new data to current config dict
        self.assertEqual(p.config(APITRACE=0), {"tracesize": 4096, "apitrace": 0})

        # Confirm changing current config dict ISO adding if already in
        self.assertEqual(p.config(TRACEsize=1024), {"tracesize": 1024, "apitrace": 0})

        # Confirm noch change if no parameter
        self.assertEqual(p.config(), {"tracesize": 1024, "apitrace": 0})

        # Confirm corret Path correction. Deleting last / or \\
        self.assertEqual(
            p.config(tracePath="C:\\EDIABAS\\"),
            {"tracesize": 1024, "apitrace": 0, "tracepath": "C:\\EDIABAS"}
        )
        self.assertEqual(
            p.config(SimulationPath="C:/EDIABAS/"),
            {"tracesize": 1024, "apitrace": 0, "tracepath": "C:\\EDIABAS", "simulationpath": "C:/EDIABAS"}
        )

    def test_config_invalid_keyword(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(KeyError):
            p.config(xx=2)

    def test_config_dict_after_invalid_keyword(self):
        p = PyDIABAS()
        p.start()
        try:
            p.config(traceSize=4096, xx=2, apitrace=0)
        except KeyError:
            pass
        self.assertEqual(p.config(), {})

    def test_config_unable_to_set(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(ConfigError):
            p.config(Interface="XX")

    def test_config_dict_after_failed_to_set(self):
        p = PyDIABAS()
        p.start()
        try:
            p.config(traceSize=4096, Interface="XX", apitrace=0)
        except ConfigError:
            pass
        self.assertEqual(p.config(), {"tracesize": 4096})

    def test_config_not_yet_started(self):
        p = PyDIABAS()
        p.config()
        with self.assertRaises(KeyError):
            p.config(traceSize=4096)
    
    def test_job(self):
        p = PyDIABAS()
        p.start()
        r = p.job("TMODE", "LESE_INTERFACE_TYP")
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_bytes(self):
        p = PyDIABAS()
        p.start()
        r = p.job(b"TMODE", b"LESE_INTERFACE_TYP")
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_parameters_str(self):
        p = PyDIABAS()
        p.start()
        r = p.job(b"TMODE", b"LESE_INTERFACE_TYP", parameters="TEST")
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_parameters_list_of_str(self):
        p = PyDIABAS()
        p.start()
        r = p.job(b"TMODE", b"LESE_INTERFACE_TYP", parameters=["TEST", "TEST2"])
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_parameters_bytes(self):
        p = PyDIABAS()
        p.start()
        r = p.job(b"TMODE", b"LESE_INTERFACE_TYP", parameters=b"TEST")
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_parameters_list_of_bytes(self):
        p = PyDIABAS()
        p.start()
        r = p.job(b"TMODE", b"LESE_INTERFACE_TYP", parameters=[b"TEST", b"TEST2"])
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_parameters_list_of_mixed_start(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", parameters=[b"TEST", "TEST2", "TEST3"])
    
    def test_job_parameters_list_of_mixed_middle(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", parameters=[b"TEST", "TEST2", b"TEST3"])
    
    def test_job_parameters_list_of_mixed_end(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", parameters=["TEST", "TEST2", b"TEST3"])

    def test_job_results_str(self):
        p = PyDIABAS()
        p.start()
        r = p.job(b"TMODE", b"LESE_INTERFACE_TYP", result_filter="TEST")
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_results_list_of_str(self):
        p = PyDIABAS()
        p.start()
        r = p.job(b"TMODE", b"LESE_INTERFACE_TYP", result_filter=["TEST", "TEST2"])
        self.assertEqual(r["TYP"], b"OBD")
    
    def test_job_results_bytes(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", result_filter=b"TEST")
    
    def test_job_results_list_of_bytes(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", result_filter=[b"TEST", b"TEST2"])
    
    def test_job_results_list_of_mixed_start(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", result_filter=[b"TEST", "TEST2", "TEST3"])
    
    def test_job_results_list_of_mixed_middle(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", result_filter=[b"TEST", "TEST2", b"TEST3"])
    
    def test_job_results_list_of_mixed_end(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(TypeError):
            p.job(b"TMODE", b"LESE_INTERFACE_TYP", result_filter=["TEST", "TEST2", b"TEST3"])

    def test_job_no_fetchall(self):
        p = PyDIABAS()
        p.start()
        r = p.job("TMODE", "LESE_INTERFACE_TYP", fetchall=False)
        self.assertIsNone(r.get("TYP"))
        r.fetchall()
        self.assertEqual(r.get("TYP"), b"OBD")
    
    def test_job_fail(self):
        p = PyDIABAS()
        p.start()
        with self.assertRaises(StateError):
            p.job("TMODE", "XX")
