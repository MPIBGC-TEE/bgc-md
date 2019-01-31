from unittest import TestCase
from cable_dict import cable_dict
from pathlib import Path
from allocationFractions import bvec_leaf_num,bvec_wood_num,bvec_fine_root_num

cable_soil=cable_dict(Path('Tumbarumba/T_independent/soilscalar.txt'))
cable_veg=cable_dict(Path('Tumbarumba/T_independent/vegpara.txt'))
cable_kbase=cable_dict(Path('Tumbarumba/T_independent/k_base.txt'))
def insp(d):
    for key,val in d.items():
        print(key,val,type(val))

#for d in [cable_soil,cable_veg,cable_kbase]:
#    insp(d)

class TestAllocationFractions(TestCase):
    def test_bvec_leaf(self):
        res=bvec_leaf_num(
            leaf=273
            ,wood=11541
            ,fine_root=2586
            ,r_leaf=1.027
            ,r_wood=.269
            ,r_fine_root=.411
            ,Npp=6.5
            ,phase=0
            ,glaimax=cable_veg["glaimax"]
            ,b_leaf=cable_veg['b_leaf']
            ,b_fine_root=cable_veg['b_fine_root']
            ,b_wood=cable_veg["b_wood"]
            ,sla=cable_veg['sla']
            ,planttype=cable_veg["planttype"]
        )
        self.assertEqual(res,0.34)
        print(res)
        res=bvec_leaf_num(
            leaf=273
            ,wood=11541
            ,fine_root=2586
            ,r_leaf=1.027
            ,r_wood=.269
            ,r_fine_root=.411
            ,Npp=6.5
            ,phase=0
            ,glaimax=cable_veg["glaimax"]
            ,b_leaf=cable_veg['b_leaf']
            ,b_fine_root=cable_veg['b_fine_root']
            ,b_wood=cable_veg["b_wood"]
            ,sla=cable_veg['sla']
            ,planttype=cable_veg["planttype"]
        )
        self.assertEqual(res,0.64)
