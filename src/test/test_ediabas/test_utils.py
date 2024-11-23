import unittest

from pydiabas.ediabas import utils, EDIABAS


class utilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ediabas = EDIABAS()
        #cls.ediabasApi.initExt(configuration="tracepath=C:/NAS/DATEN/Programmieren/Python/PyDIABAS/trace;apiTrace=1")
        cls.ediabas.init()
        cls.ediabas.job("TMODE", "LESE_INTERFACE_TYP")

    @classmethod
    def tearDownClass(cls):
        cls.ediabas.end()

    def test_getResult_Binary(self):
        self.assertEqual(utils.getResult(self.ediabas, "TYP"), b"OBD")

    def test_getResult_Text(self):
        self.assertEqual(utils.getResult(self.ediabas, "OBJECT", set=0), "tmode")
        self.assertEqual(utils.getResult(self.ediabas, "JOBNAME", set=0), "LESE_INTERFACE_TYP")
        self.assertEqual(utils.getResult(self.ediabas, "VARIANTE", set=0), "TMODE")
        self.assertEqual(utils.getResult(self.ediabas, "JOBSTATUS", set=0), "")

    def test_getResult_Word(self):
        self.assertEqual(utils.getResult(self.ediabas, "SAETZE", set=0), 1)

    def test_getResult_Integer(self):
        self.assertEqual(utils.getResult(self.ediabas, "UBATTCURRENT", set=0), -1)
        self.assertEqual(utils.getResult(self.ediabas, "UBATTHISTORY", set=0), -1)
        self.assertEqual(utils.getResult(self.ediabas, "IGNITIONCURRENT", set=0), -1)
        self.assertEqual(utils.getResult(self.ediabas, "IGNITIONHISTORY", set=0), -1)
