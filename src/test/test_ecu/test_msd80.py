import unittest
from pydiabas import PyDIABAS, Result
from pydiabas.ecu import MSD80
from pydiabas.ecu.msd80 import BlockCreateError, BlockReadError, ValueReadError

__all__ = [
    "MSD80Test"
]


class MSD80Test(unittest.TestCase):
    READINGS_NO_LOOKUP_A = ["0x5A30", "0x5A31", "0x5A32", "0x5A33", "0x5A34", "0x5A35"]
    READINGS_NO_LOOKUP_B = ["0x5B00", "0x5B01", "0x5B02", "0x5B03", "0x5B04", "0x5B05"]
    READINGS_SINGLE_LOOKUP_A = ["0x5AB1", "0x58E4"]
    READINGS_SINGLE_LOOKUP_B = ["0x5A2F", "0x58E4"]
    READINGS_MULTIPLE_LOOKUPS_A = ["0x5AB1", "0x58E4", "0x4307"]
    READINGS_MULTIPLE_LOOKUPS_B = ["0x5A2F", "0x58E4", "0x4307"]
    READINGS_PARTLY_INVALID = ["0x5A2F", "0x58E4", "0xFFFF"]

    @classmethod
    def setUpClass(cls):
        cls.pydiabas = PyDIABAS()
        cls.pydiabas.start()
        
    @classmethod
    def tearDownClass(cls):
        cls.pydiabas.end()

    def setUp(self):
        self.pydiabas.reset()
        self.msd80 = MSD80()

    def test_init(self):
        self.assertEqual(self.msd80.name, "MSD80")
        self.assertEqual(self.msd80._block, [])
        self.assertIsNone(self.msd80._last_read_function)
    
    def test_set_block_no_lookup(self):
        result = self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_NO_LOOKUP_B)
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(last_read_function_1 is self.msd80._last_read_function)
    
    def test_set_block_single_lookup(self):
        result = self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_SINGLE_LOOKUP_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_SINGLE_LOOKUP_A)
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_SINGLE_LOOKUP_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_SINGLE_LOOKUP_B)
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(self.msd80._last_read_function is last_read_function_1)
    
    def test_set_block_multiple_lookups_raises_exception(self):
        with self.assertRaises(BlockCreateError):
            self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_MULTIPLE_LOOKUPS_A)
    
    def test_set_block_multiple_lookups_clears_block(self):
        self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertTrue(callable(self.msd80._last_read_function))

        try:
            self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_MULTIPLE_LOOKUPS_A)
        except BlockCreateError:
            pass
        
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
    
    def test_set_block_invalid_value_raises_exception(self):
        with self.assertRaises(BlockCreateError):
            self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_PARTLY_INVALID)
    
    def test_set_block_invalid_value_clears_block(self):
        self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertTrue(callable(self.msd80._last_read_function))

        try:
            self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_PARTLY_INVALID)
        except BlockCreateError:
            pass
        
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
    
    def test_read_block(self):
        self.msd80.set_block(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_A)
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.read_block(self.pydiabas)
        self.assertIsInstance(result, Result)
        self.assertFalse(self.msd80._last_read_function is last_read_function_1)

    def test_read_block_fails(self):
        with self.assertRaises(BlockReadError):
            self.msd80.read_block(self.pydiabas)
    
    def test_read_no_lookup(self):
        result = self.msd80.read(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.read(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(last_read_function_1 is self.msd80._last_read_function)
    
    def test_read_single_lookup(self):
        result = self.msd80.read(self.pydiabas, MSD80Test.READINGS_SINGLE_LOOKUP_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.read(self.pydiabas, MSD80Test.READINGS_SINGLE_LOOKUP_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(last_read_function_1 is self.msd80._last_read_function)
    
    def test_read_multiple_lookups(self):
        result = self.msd80.read(self.pydiabas, MSD80Test.READINGS_MULTIPLE_LOOKUPS_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.read(self.pydiabas, MSD80Test.READINGS_MULTIPLE_LOOKUPS_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(last_read_function_1 is self.msd80._last_read_function)
    
    def test_read_invalid_value(self):
        with self.assertRaises(ValueReadError):
            self.msd80.read(self.pydiabas, MSD80Test.READINGS_PARTLY_INVALID)
    
    def test_read_auto_no_lookup(self):
        result = self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_NO_LOOKUP_A)
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_NO_LOOKUP_B)
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(last_read_function_1 is self.msd80._last_read_function)
    
    def test_read_auto_single_lookup(self):
        result = self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_SINGLE_LOOKUP_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_SINGLE_LOOKUP_A)
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_SINGLE_LOOKUP_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, MSD80Test.READINGS_SINGLE_LOOKUP_B)
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(last_read_function_1 is self.msd80._last_read_function)
    
    def test_read_auto_multiple_lookups(self):
        result = self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_MULTIPLE_LOOKUPS_A)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        last_read_function_1 = self.msd80._last_read_function
        result = self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_MULTIPLE_LOOKUPS_B)
        self.assertIsInstance(result, Result)
        self.assertEqual(self.msd80._block, [])
        self.assertTrue(callable(self.msd80._last_read_function))
        self.assertFalse(last_read_function_1 is self.msd80._last_read_function)
    
    def test_read_auto_invalid_value(self):
        with self.assertRaises(ValueReadError):
            self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_PARTLY_INVALID)
    
    def test_read_again(self):
        self.msd80.read_auto(self.pydiabas, MSD80Test.READINGS_NO_LOOKUP_A)
        result = self.msd80.read_again()
        self.assertIsInstance(result, Result)
    
    def test_read_again_fails(self):
        with self.assertRaises(ValueReadError):
            self.msd80.read_again()
