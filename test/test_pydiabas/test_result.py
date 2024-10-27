import unittest
from pydiabas import Result, Set, Row, PyDIABAS
from pydiabas.ediabas import EDIABAS

__all__ = [
    "rowTest",
    "setTest",
    "resultTest"
]

class rowTest(unittest.TestCase):
    def test_row(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        self.assertEqual(r1.name, "one")
        self.assertEqual(r1.value, "1")
        self.assertEqual(r2.name, "two")
        self.assertEqual(r2.value, "2")


class setTest(unittest.TestCase):
    def test_init(self):
        s = Set()
        self.assertIsInstance(s, Set)
        self.assertEqual(s._rows, [])

    def test_init_empty_list(self):
        Set(rows=[])

    def test_init_rows(self):
        r = Row(name="name", value="value")
        s = Set(rows=[r])
        self.assertEqual(s._rows, [r])

    def test_init_rows_no_list(self):
        r = Row(name="name", value="value")
        with self.assertRaises(TypeError):
            Set(rows=r)

    def test_init_rows_no_row_in_list(self):
        with self.assertRaises(TypeError):
            Set(rows=[2])

    def test_init_rows_not_only_rows_in_list(self):
        r = Row(name="name", value="value")
        with self.assertRaises(TypeError):
            Set(rows=[r, 2])

    def test_all(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        s = Set(rows=[r1, r2])
        self.assertEqual(s.all, [r1, r2])
        s._rows = []
        self.assertEqual(s.all, [])

    def test_as_dict(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        s = Set(rows=[r1, r2])
        self.assertEqual(s.as_dict(), {r1.name: r1.value, r2.name: r2.value})
        s._rows = []
        self.assertEqual(s.as_dict(), {})

    def test_index(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        r3 = Row(name="two", value=2)
        s = Set(rows=[r1, r2, r3])
        self.assertEqual(s.index("one"), 0)
        self.assertEqual(s.index("One"), 0)
        self.assertEqual(s.index("ONE"), 0)
        self.assertEqual(s.index("onE"), 0)
        self.assertEqual(s.index("two"), 1)
        self.assertEqual(s.index("one", 0, 1), 0)
        self.assertEqual(s.index("two", 0, 2), 1)
        self.assertEqual(s.index("two", 2, 3), 2)
    
    def test_index_no_result(self):
        s = Set()
        with self.assertRaises(ValueError):
            s.index("test")
    
    def test_index_no_string(self):
        s = Set()
        with self.assertRaises(TypeError):
            s.index(2)

    def test_keys(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        r3 = Row(name="THREE", value=3)
        s = Set(rows=[r1, r2, r3])
        self.assertEqual(s.keys(), ["one", "two", "THREE"])
        s._rows = []
        self.assertEqual(s.keys(), [])

    def test_values(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        r3 = Row(name="THREE", value=3)
        s = Set(rows=[r1, r2, r3])
        self.assertEqual(s.values(), ["1", "2", 3])
        s._rows = []
        self.assertEqual(s.values(), [])

    def test_items(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        s = Set(rows=[r1, r2])
        self.assertEqual(s.items(), [("one", "1"), ("two", "2")])
        s._rows = []
        self.assertEqual(s.items(), [])

    def test___getitem__(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value="2")
        r3 = Row(name="THREE", value=3)
        r4 = Row(name="one", value=1)
        r5 = Row(name="five", value=b"five")
        s = Set(rows=[r1, r2, r3, r4, r5])
        s_sliced_1 = Set(rows=[r1, r2])
        s_sliced_2 = Set(rows=[r2, r3])
        s_sliced_3 = Set(rows=[r1, r3, r5])
        self.assertEqual(s["one"], "1")
        self.assertEqual(s["ONE"], "1")
        self.assertEqual(s[0], r1)
        self.assertEqual(s[2], r3)
        self.assertEqual(s[0:2].all, s_sliced_1.all)
        self.assertEqual(s[1:3].all, s_sliced_2.all)
        self.assertEqual(s[::2].all, s_sliced_3.all)
        self.assertEqual(s[:].all, s.all)
        self.assertNotEqual(s[:], s)
        self.assertEqual(s["five"], b"five")

    def test___getitem__not_found(self):
        s = Set()
        with self.assertRaises(KeyError):
            s["test"]

    def test___getitem__wrong_type_float(self):
        s = Set()
        with self.assertRaises(TypeError):
            s[2.2]

    def test___getitem__wrong_type_bytes(self):
        s = Set()
        with self.assertRaises(TypeError):
            s[b"five"]
    
    def test_get(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="one", value=1)
        s = Set(rows=[r1, r2])
        self.assertEqual(s.get("one"), "1")
        self.assertEqual(s.get("four"), None)
        self.assertEqual(s.get("four", default=4), 4)
    
    def test___len__(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="one", value=1)
        s = Set(rows=[r1, r2])
        self.assertEqual(len(s), 2)
        s._rows = []
        self.assertEqual(len(s), 0)
    
    def test___bool__(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="one", value=1)
        s = Set(rows=[r1, r2])
        self.assertTrue(bool(s))
        s._rows = []
        self.assertFalse(bool(s))
    
    def test___iter__(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="one", value=1)
        s = Set(rows=[r1, r2])
        for i, r in enumerate(s):
            self.assertEqual(r, s[i])
        s._rows = []
        for i, r in enumerate(s):
            self.assertEqual(r, s[i])

    def test___str__(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value=2)
        s = Set(rows=[r1, r2])
        self.assertEqual(s.__str__(), "one                           : 1\ntwo                           : 2\n")
        s._rows = []
        self.assertEqual(s.__str__(), "\n")

    def test___contains__(self):
        r1 = Row(name="one", value="1")
        r2 = Row(name="two", value=2)
        s = Set(rows=[r1, r2])
        self.assertTrue("one" in s)
        self.assertTrue("ONE" in s)
        self.assertTrue("two" in s)
        self.assertFalse("three" in s)
        s._rows = []
        self.assertFalse("one" in s)

    def test___contains__wrong_type_int(self):
        s = Set()
        with self.assertRaises(TypeError):
            2 in s

    def test___contains__wrong_type_bytes(self):
        s = Set()
        with self.assertRaises(TypeError):
            b"test" in s


class resultTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pydiabas = PyDIABAS()
        cls.pydiabas.start()
        #cls.pydiabas.config(tracePath="C:/NAS/DATEN/Programmieren/Python/PyDIABAS/trace", apiTrace=1)

        cls.pydiabas.job(ecu="TMODE", job="LESE_INTERFACE_TYP")
        cls.r_tmode_lese_interface_typ = Result(ediabas=cls.pydiabas._ediabas).fetchall()

        cls.pydiabas.job(ecu="TMODE", job="_JOBS")
        cls.r_tmode__jobs = Result(ediabas=cls.pydiabas._ediabas).fetchall()
        
    @classmethod
    def tearDownClass(cls):
        cls.pydiabas.end()

    def setUp(self):
        self.r_simulation = Result(ediabas=self.pydiabas._ediabas)
        self.r_simulation._systemSet = Set(rows=[Row(name="SYS", value="TEM")])
        self.r_simulation._jobSets = [
            Set(rows=[Row(name="R1", value=1)]),
            Set(rows=[Row(name="R1", value=2), Row(name="R2", value=3)]),
            Set(rows=[Row(name="R1", value=3), Row(name="R2", value=4), Row(name="R3", value=5)])
        ]
        self.r_empty = Result(ediabas=self.pydiabas._ediabas)

    def test_init(self):
        self.assertIsInstance(self.r_empty, Result)
        self.assertIsInstance(self.r_empty._systemSet, Set)
        self.assertEqual(self.r_empty._jobSets, [])
        self.assertEqual(self.r_empty._systemSet.all, [])
        self.assertIsInstance(self.r_empty._ediabas, EDIABAS)
        self.assertEqual(self.r_empty._ediabas, self.pydiabas._ediabas)

    def test_clear(self):
        self.r_simulation.clear()
        self.assertEqual(self.r_simulation._systemSet.all, [])
        self.assertEqual(self.r_simulation._jobSets, [])

    def test_fetchname(self):
        r = self.pydiabas.job(ecu="TMODE", job="INFO", fetchall=False)
        self.assertFalse(r)
        self.assertEqual(len(r), 0)
        r.fetchname("AUTHOR")
        self.assertEqual(len(r), 1)
        self.assertEqual(len(r[0]), 1)
        self.assertEqual(r[0].as_dict(), {'AUTHOR': 'Softing Ta, Softing WT'})
        self.assertTrue("AUTHOR" in r._jobSets[0])
        r.fetchname("SPRACHE")
        self.assertEqual(len(r), 1)
        self.assertEqual(len(r[0]), 2)
        self.assertEqual(r[0].as_dict(), {'AUTHOR': 'Softing Ta, Softing WT', 'SPRACHE': 'deutsch'})
        self.assertTrue("AUTHOR" in r._jobSets[0])
        self.assertTrue("SPRACHE" in r._jobSets[0])
        r.fetchname("SPRACHE")
        self.assertEqual(len(r), 1)
        self.assertEqual(len(r[0]), 2)
        self.assertEqual(r[0].as_dict(), {'AUTHOR': 'Softing Ta, Softing WT', 'SPRACHE': 'deutsch'})

        r2 = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        self.assertFalse(r2)
        self.assertEqual(len(r2), 0)
        r.fetchname("JOBNAME")
        self.assertGreaterEqual(len(r), 1)
        self.assertGreaterEqual(len(r[1]), 1)
        self.assertTrue("AUTHOR" in r._jobSets[0])
        self.assertTrue("SPRACHE" in r._jobSets[0])
        self.assertTrue("JOBNAME" in r._jobSets[0])
        self.assertFalse("AUTHOR" in r._jobSets[1])
        self.assertFalse("SPRACHE" in r._jobSets[1])
        self.assertTrue("JOBNAME" in r._jobSets[1])
        
    
    def test_fetchset_0(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r._fetchset(i_set=0)
        self.assertEqual(r._systemSet["OBJECT"], "tmode")
        self.assertEqual(len(r), 0)
        with self.assertRaises(KeyError):
            r["JOBNAME"]
    
    def test_fetchset_1(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r._fetchset(i_set=1)
        self.assertIsNotNone(r["JOBNAME"])
        self.assertIsNotNone(r[0]["JOBNAME"])
        self.assertEqual(len(r), 1)
        with self.assertRaises(KeyError):
            r._systemSet["OBJECT"]
    
    def test_fetchset_1_multiple_rows(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBCOMMENTS", parameters="SETZE_TRAP_MASK_REGISTER", fetchall=False)
        r._fetchset(i_set=1)
        self.assertIsNotNone(r["JOBCOMMENT0"])
        self.assertIsNotNone(r["JOBCOMMENT1"])
        self.assertIsNotNone(r[0]["JOBCOMMENT0"])
        self.assertIsNotNone(r[0]["JOBCOMMENT1"])
        self.assertEqual(len(r), 1)
        with self.assertRaises(KeyError):
            r._systemSet["OBJECT"]
    
    def test_fetchset_2(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r._fetchset(i_set=2)
        self.assertIsNotNone(r["JOBNAME"])
        self.assertIsNotNone(r[1]["JOBNAME"])
        self.assertEqual(len(r), 2)
        with self.assertRaises(KeyError):
            r[0]["JOBNAME"]
    
    def test_fetchset_2_and_4(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r._fetchset(i_set=2)
        r._fetchset(i_set=4)
        self.assertIsNotNone(r["JOBNAME"])
        self.assertIsNotNone(r[1]["JOBNAME"])
        self.assertIsNotNone(r[3]["JOBNAME"])
        self.assertEqual(len(r), 4)
        with self.assertRaises(KeyError):
            r[2]["JOBNAME"]

    def test_fetchset_index_error(self):
        r = self.pydiabas.job(ecu="TMODE", job="LESE_INTERFACE_TYP", fetchall=False)
        with self.assertRaises(IndexError):
            r._fetchset(2)
    
    def test_fetchsystem(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r.fetchsystemset()
        self.assertEqual(r._systemSet["OBJECT"], "tmode")
        with self.assertRaises(KeyError):
            r["JOBNAME"]
    
    def test_fetchjobsets(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r.fetchjobsets()
        self.assertIsNotNone(r["JOBNAME"])
        self.assertIsNotNone(r[0]["JOBNAME"])
        self.assertIsNotNone(r[3]["JOBNAME"])
        self.assertIsNotNone(r[len(r) - 1]["JOBNAME"])
        with self.assertRaises(KeyError):
            r._systemSet["OBJECT"]
    
    def test_fetchall(self):
        r = self.pydiabas.job(ecu="TMODE", job="LESE_INTERFACE_TYP", fetchall=False)
        r.fetchall()
        self.assertEqual(r["TYP"], b"OBD")
        self.assertEqual(r._systemSet["OBJECT"], "tmode")
    
    def test_fetchall_multiple_sets(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r.fetchall()
        self.assertEqual(r["JOBNAME"], "INFO")
        self.assertEqual(r[4]["JOBNAME"], "SETZE_SG_PARAMETER_ALLG")
        self.assertEqual(r._systemSet["OBJECT"], "tmode")

    def test_fetchname_multiple_sets(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r.fetchname("JOBNAME")
        self.assertEqual(r["JOBNAME"], "INFO")
        self.assertEqual(r[4]["JOBNAME"], "SETZE_SG_PARAMETER_ALLG")

    def test_fetchname_wrong_name(self):
        r = self.pydiabas.job(ecu="TMODE", job="LESE_INTERFACE_TYP", fetchall=False)
        r.fetchname("XX")
        with self.assertRaises(KeyError):
            r["TYP"]

    def test_fetchnames(self):
        r = self.pydiabas.job(ecu="TMODE", job="LESE_INTERFACE_TYP", fetchall=False)
        r.fetchnames(["TYP"])
        self.assertEqual(r["TYP"], b"OBD")

    def test_fetchnames_multiple_sets(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBS", fetchall=False)
        r.fetchnames(["JOBNAME"])
        self.assertEqual(r["JOBNAME"], "INFO")
        self.assertEqual(r[4]["JOBNAME"], "SETZE_SG_PARAMETER_ALLG")

    def test_fetchnames_one_wrong_name(self):
        r = self.pydiabas.job(ecu="TMODE", job="LESE_INTERFACE_TYP", fetchall=False)
        r.fetchnames(["Y", "TYP", "X"])
        self.assertEqual(r["TYP"], b"OBD")

    def test_fetchnames_only_wrong_names(self):
        r = self.pydiabas.job(ecu="TMODE", job="LESE_INTERFACE_TYP", fetchall=False)
        r.fetchnames(["Y", "X"])
        with self.assertRaises(KeyError):
            r["TYP"]
    
    def test_fetchname_after_fetchset(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBCOMMENTS", parameters="SETZE_TRAP_MASK_REGISTER", fetchall=False)
        r._fetchset(i_set=1)
        self.assertEqual(len(r), 1)
        self.assertEqual(len(r[0]), 2)
        self.assertTrue("JOBCOMMENT0" in r)
        self.assertTrue("JOBCOMMENT1" in r)
        r.fetchname("JOBCOMMENT0")
        self.assertEqual(len(r), 1)
        self.assertEqual(len(r[0]), 2)
        self.assertTrue("JOBCOMMENT0" in r)
        self.assertTrue("JOBCOMMENT1" in r)

    def test_fetchset_after_fetchname(self):
        r = self.pydiabas.job(ecu="TMODE", job="_JOBCOMMENTS", parameters="SETZE_TRAP_MASK_REGISTER", fetchall=False)
        r.fetchname("JOBCOMMENT0")
        self.assertEqual(len(r), 1)
        self.assertEqual(len(r[0]), 1)
        self.assertTrue("JOBCOMMENT0" in r)
        self.assertFalse("JOBCOMMENT1" in r)
        r._fetchset(i_set=1)
        self.assertEqual(len(r), 1)
        self.assertEqual(len(r[0]), 2)
        self.assertTrue("JOBCOMMENT0" in r)
        self.assertTrue("JOBCOMMENT1" in r)

    def test_systemSet(self):
        self.assertEqual(
            self.r_tmode_lese_interface_typ._systemSet,
            self.r_tmode_lese_interface_typ.systemSet
        )

    def test_systemSet_empty(self):
        self.assertEqual(self.r_empty.systemSet.all, [])

    def test_jobSets(self):
        self.assertEqual(
            self.r_tmode_lese_interface_typ._jobSets,
            self.r_tmode_lese_interface_typ.jobSets
        )

    def test_jobSets_empty(self):
        self.assertEqual(self.r_empty.jobSets, [])

    def test_ecu(self):
        self.assertEqual(self.r_tmode_lese_interface_typ.ecu, "TMODE")

    def test_ecu_empty(self):
        self.assertIsNone(self.r_empty.ecu)

    def test_jobname(self):
        self.assertEqual(self.r_tmode_lese_interface_typ.jobname, "LESE_INTERFACE_TYP")

    def test_jobname_empty(self):
        self.assertIsNone(self.r_empty.jobname)

    def test_jobstatus(self):
        self.assertEqual(self.r_tmode_lese_interface_typ.jobstatus, "")

    def test_jobstatus_empty(self):
        self.assertIsNone(self.r_empty.jobstatus)
    
    def test_as_dicts(self):
        self.assertEqual(self.r_simulation.as_dicts(), [{'SYS': 'TEM'}, {'R1': 1}, {'R1': 2, 'R2': 3}, {'R1': 3, 'R2': 4, 'R3': 5}])
        
    def test_as_dicts_empty(self):
        self.assertEqual(self.r_empty.as_dicts(), [{}])

    def test_count(self):
        self.assertEqual(self.r_simulation.count("X"), 0)
        self.assertEqual(self.r_simulation.count("SYS"), 0)
        self.assertEqual(self.r_simulation.count("R1"), 3)
        self.assertEqual(self.r_simulation.count("R2"), 2)
        self.assertEqual(self.r_simulation.count("r2"), 2)
        self.assertEqual(self.r_simulation.count("r3"), 1)
    
    def test_count_empty(self):
        self.assertEqual(self.r_empty.count("X"), 0)
        self.assertEqual(self.r_empty.count("SYS"), 0)
        self.assertEqual(self.r_empty.count("R1"), 0)
        self.assertEqual(self.r_empty.count("R2"), 0)

    def test_index(self):
        self.assertEqual(self.r_simulation.index(name="R1", start=0, end=100), 0)
        self.assertEqual(self.r_simulation.index(name="R1", start=1, end=2), 1)
        self.assertEqual(self.r_simulation.index("R3"), 2)

    def test_index_wrong_name(self):
        with self.assertRaises(ValueError):
            self.r_simulation.index("X")

    def test_index_too_narrow_index(self):
        with self.assertRaises(ValueError):
            self.r_simulation.index(name="R1", start=1, end=1)

    def test_index_wrong_type(self):
        with self.assertRaises(TypeError):
            self.r_simulation.index(2)

    def test___getitem__(self):
        r_simulation_sliced_1 = self.r_simulation[:]
        r_simulation_sliced_1._jobSets = self.r_simulation._jobSets[1:2]
        r_simulation_sliced_2 = self.r_simulation[:]
        r_simulation_sliced_2._jobSets = self.r_simulation._jobSets[2:10]
        r_simulation_sliced_3 = self.r_simulation[:]
        r_simulation_sliced_3._jobSets = self.r_simulation._jobSets[::2]

        self.assertEqual(self.r_simulation["R1"], 1)
        self.assertEqual(self.r_simulation["r2"], 3)
        self.assertEqual(self.r_simulation[0], self.r_simulation._jobSets[0])
        self.assertEqual(self.r_simulation[-1], self.r_simulation._jobSets[2])
        self.assertEqual(self.r_simulation[:]._jobSets, self.r_simulation._jobSets)
        self.assertEqual(self.r_simulation[:]._systemSet, self.r_simulation._systemSet)
        self.assertNotEqual(id(self.r_simulation[:]._jobSets), id(self.r_simulation._jobSets))
        self.assertNotEqual(id(self.r_simulation[:]), id(self.r_simulation))
        self.assertEqual(self.r_simulation[1:2]._jobSets, r_simulation_sliced_1._jobSets)
        self.assertEqual(self.r_simulation[1:2]._systemSet, r_simulation_sliced_1._systemSet)
        self.assertEqual(self.r_simulation[2:10]._jobSets, r_simulation_sliced_2._jobSets)
        self.assertEqual(self.r_simulation[2:10]._systemSet, r_simulation_sliced_2._systemSet)
        self.assertEqual(self.r_simulation[::2]._jobSets, r_simulation_sliced_3._jobSets)
        self.assertEqual(self.r_simulation[::2]._systemSet, r_simulation_sliced_3._systemSet)
    
    def test___getitem___wrong_type(self):
        with self.assertRaises(TypeError):
            self.r_simulation[1.2]
    
    def test___getitem___index_out_of_range(self):
        with self.assertRaises(IndexError):
            self.r_simulation[4]
    
    def test___getitem___key_error(self):
        with self.assertRaises(KeyError):
            self.r_simulation["XX"]
    
    def test___getitem___key_error_on_systemSet(self):
        with self.assertRaises(KeyError):
            self.r_simulation["SYS"]

    def test___contains__(self):
        self.assertTrue("R1" in self.r_simulation)
        self.assertTrue("r1" in self.r_simulation)
        self.assertTrue("r3" in self.r_simulation)
        self.assertFalse("X" in self.r_simulation)
        self.assertFalse("SYS" in self.r_simulation)

    def test___contains___wrong_type(self):
        with self.assertRaises(TypeError):
            2 in self.r_simulation

    def test_get(self):
        self.assertEqual(self.r_simulation.get("R1"), 1)
        self.assertEqual(self.r_simulation.get("R1", default="TEST"), 1)
        self.assertEqual(self.r_simulation.get("r2"), 3)
        self.assertEqual(self.r_simulation.get("r2", default="TEST"), 3)
        self.assertEqual(self.r_simulation.get("SYS"), None)
        self.assertEqual(self.r_simulation.get("SYS", default="TEST"), "TEST")
    
    def test_get_wrong_type(self):
        with self.assertRaises(TypeError):
            self.r_simulation.get(1)
    
    def test___len__(self):
        self.assertEqual(len(self.r_simulation), 3)
        self.assertEqual(len(self.r_empty), 0)
        
    def test___bool__(self):
        self.assertTrue(self.r_simulation)
        self.assertTrue(self.r_tmode__jobs)
        self.assertFalse(self.r_empty)
    
    def test___iter__(self):
        for i, s in enumerate(self.r_simulation):
            self.assertEqual(s, self.r_simulation._jobSets[i])
    
    def test___str__(self):

        self.assertEqual(str(self.r_simulation),
"""
============== PyDIABAS Result ==============
-------------- systemSet       --------------
SYS                           : TEM
-------------- jobSet #0       --------------
R1                            : 1
-------------- jobSet #1       --------------
R1                            : 2
R2                            : 3
-------------- jobSet #2       --------------
R1                            : 3
R2                            : 4
R3                            : 5
============== END             ==============
""")
        

        self.assertEqual(str(self.r_empty), 
"""
============== PyDIABAS Result ==============
============== END             ==============
""")
