import unittest
from pydiabas import PyDIABAS, StateError
from pydiabas.ediabas import EDIABAS
from pydiabas.ecu import ECU

__all__ = [
    "ECUTest"
]


class ECUTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pydiabas = PyDIABAS()
        cls.pydiabas.start()
        
    @classmethod
    def tearDownClass(cls):
        cls.pydiabas.end()

    def setUp(self):
        self.pydiabas.reset()
        self.ecu = ECU()
        self.tmode = ECU(name="TMODE")

    def test_init(self):
        self.assertEqual(self.ecu.name, "")
        self.assertEqual(self.tmode.name, "TMODE")

    def test_get_jobs(self):
        jobs = self.tmode.get_jobs(pydiabas=self.pydiabas, details=False)
        self.assertIsInstance(jobs, dict)
        self.assertGreaterEqual(len(jobs), 1)
        self.assertIsInstance(jobs[list(jobs.keys())[0]], dict)
        self.assertEqual(len(jobs[list(jobs.keys())[0]]), 0)

    def get_jobs_with_details(self):
        jobs = self.tmode.get_jobs(pydiabas=self.pydiabas, details=True)
        self.assertIsInstance(jobs, dict)
        self.assertGreaterEqual(len(jobs), 1)
        self.assertIsInstance(jobs[list(jobs.keys())[0]], dict)
        self.assertGreaterEqual(len(jobs[list(jobs.keys())[0]]), 1)
    
    def test_get_jobs_wrong_ecu_name(self):
        with self.assertRaises(StateError):
            self.ecu.get_jobs(pydiabas=self.pydiabas, details=False)
        
    def test_get_job_details(self):
        details = self.tmode.get_job_details(pydiabas=self.pydiabas, job="SENDE_TELEGRAMM")
        self.assertEqual(len(details), 3)
        self.assertTrue("comments" in details)
        self.assertTrue("arguments" in details)
        self.assertTrue("results" in details)

        self.assertIsInstance(details["comments"], list)
        self.assertGreaterEqual(len(details["comments"]), 1)
        self.assertIsInstance(details["arguments"], list)
        self.assertGreaterEqual(len(details["arguments"]), 1)
        self.assertIsInstance(details["results"], list)
        self.assertGreaterEqual(len(details["results"]), 1)

        self.assertTrue("name" in details["arguments"][0])
        self.assertTrue("type" in details["arguments"][0])
        self.assertTrue("comments" in details["arguments"][0])
        self.assertTrue("name" in details["results"][0])
        self.assertTrue("type" in details["results"][0])
        self.assertTrue("comments" in details["results"][0])
    
    def test_get_job_details_wrong_ecu_name(self):
        self.assertEqual(
            self.ecu.get_job_details(pydiabas=self.pydiabas, job="INFO"),
            {'comments': [], 'arguments': [], 'results': []}
        )
    
    def test_get_job_details_wrong_job_name(self):
        self.assertEqual(
            self.tmode.get_job_details(pydiabas=self.pydiabas, job="XX"),
            {'comments': [], 'arguments': [], 'results': []}
        )
    
    def test_get_tables(self):
        tables = self.tmode.get_tables(pydiabas=self.pydiabas, details=False)
        self.assertIsInstance(tables, dict)
    
    def test_get_tables_wrong_ecu_name(self):
        with self.assertRaises(StateError):
            self.ecu.get_tables(pydiabas=self.pydiabas, details=False)
    
    def test_get_table_details_wrong_ecu_and_table_name(self):
        self.assertEqual(
            self.ecu.get_table_details(pydiabas=self.pydiabas, table="INFO"),
            {'body': [], 'header': []}
        )
