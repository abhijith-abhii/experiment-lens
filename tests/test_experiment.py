import pandas as pd,pytest
from core import wilson,evaluate,analyze

def test_wilson_edges():
 assert wilson(0,10)[0]==pytest.approx(0);assert wilson(10,10)[1]==pytest.approx(1)
def test_identical_groups():
 d=pd.DataFrame([{'user_id':f'{g}{i}','variant':g,'converted':i%2} for g in ['A','B'] for i in range(100)])
 r=evaluate(d);assert r['absolute_lift']==0 and r['p_value']==1 and r['srm_p_value']==1

def test_duplicate_users_rejected():
 d=pd.DataFrame([{'user_id':'same','variant':g,'converted':0} for g in ['A','B']])
 with pytest.raises(ValueError):evaluate(d)
def test_allocation_mismatch_flags():assert analyze({'expected_share':.8})['details']['srm_flag']
def test_interval_and_probability():
 r=analyze({})['details'];assert 0<=r['p_value']<=1;assert r['lift_interval'][0]<r['absolute_lift']<r['lift_interval'][1]
