import unittest
from assurance import fit, evaluate

BASE=[{'privilege_count':x,'unapproved_tool_calls':0,'unpatched_critical':0,'unexpected_egress':0,'missing_attestations':0} for x in (1,2,3,2,1)]
class TestAssurance(unittest.TestCase):
    def setUp(self): self.model=fit(BASE)
    def test_normal(self):
        self.assertEqual(evaluate({**BASE[0], 'production':False},self.model)['decision'],'PASS')
    def test_unapproved(self):
        self.assertEqual(evaluate({**BASE[0],'unapproved_tool_calls':1},self.model)['decision'],'BLOCK')
    def test_approval(self):
        self.assertEqual(evaluate({**BASE[0],'production':True},self.model)['decision'],'BLOCK')
    def test_anomaly(self):
        self.assertEqual(evaluate({**BASE[0],'privilege_count':20},self.model)['decision'],'REVIEW')
    def test_bad_input(self):
        with self.assertRaises(ValueError): evaluate({**BASE[0],'privilege_count':-1},self.model)
if __name__=='__main__': unittest.main()
