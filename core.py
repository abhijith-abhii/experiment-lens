from pathlib import Path
import math
import numpy as np,pandas as pd
from scipy.stats import norm,chisquare
ROOT=Path(__file__).parent

def wilson(successes,n,alpha=.05):
 if n<=0 or not 0<=successes<=n:raise ValueError('Invalid binomial counts')
 p=successes/n;z=norm.ppf(1-alpha/2);den=1+z*z/n;center=(p+z*z/(2*n))/den;half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den;return [center-half,center+half]
def evaluate(df,alpha=.05,expected=.5,mde=.03):
 if not all(math.isfinite(x) for x in [alpha,expected,mde]) or not 0<alpha<.2 or not .05<expected<.95 or not 0<mde<.5:raise ValueError('Invalid alpha, allocation, or minimum effect')
 if df.user_id.duplicated().any() or df.isna().any().any() or not set(df.variant)=={'A','B'} or not set(df.converted)<=set([0,1]):raise ValueError('Need unique users, two variants, complete binary outcomes')
 g=df.groupby('variant').converted.agg(['count','sum']);na,nb=int(g.loc['A','count']),int(g.loc['B','count']);xa,xb=int(g.loc['A','sum']),int(g.loc['B','sum']);pa,pb=xa/na,xb/nb;delta=pb-pa
 pooled=(xa+xb)/(na+nb);se0=math.sqrt(pooled*(1-pooled)*(1/na+1/nb));pvalue=float(2*norm.sf(abs(delta/se0))) if se0 else 1.;se=math.sqrt(pa*(1-pa)/na+pb*(1-pb)/nb);z=norm.ppf(1-alpha/2);srm=float(chisquare([na,nb],f_exp=[(na+nb)*(1-expected),(na+nb)*expected]).pvalue)
 # Conventional two-sided normal approximation with 80% power, equal groups.
 planning_p=min(.999,max(.001,(pa+min(1,pa+mde))/2));n_plan=math.ceil(2*planning_p*(1-planning_p)*(norm.ppf(1-alpha/2)+norm.ppf(.8))**2/mde**2)
 return {'control_n':na,'treatment_n':nb,'control_conversions':xa,'treatment_conversions':xb,'control_rate':pa,'treatment_rate':pb,'absolute_lift':delta,'relative_lift':delta/pa if pa else None,'lift_interval':[delta-z*se,delta+z*se],'p_value':pvalue,'srm_p_value':srm,'srm_flag':srm<.01,'alpha':alpha,'control_wilson':wilson(xa,na,alpha),'treatment_wilson':wilson(xb,nb,alpha),'planning_n_per_arm_80pct':n_plan,'planning_mde':mde,'validity_warning':'Sparse outcomes require exact methods; repeated peeking invalidates fixed-horizon p-values.'}
def analyze(p):
 d=evaluate(pd.read_csv(ROOT/'data/experiment.csv'),float(p.get('alpha',.05)),float(p.get('expected_share',.5)),float(p.get('minimum_effect',.03)))
 decision='Check allocation before interpreting effect' if d['srm_flag'] else 'Interval excludes zero' if d['lift_interval'][0]>0 or d['lift_interval'][1]<0 else 'Effect remains uncertain'
 return dict(metrics={'Absolute lift':f"{100*d['absolute_lift']:.2f} pp",'p-value':round(d['p_value'],4),'SRM p-value':round(d['srm_p_value'],4),'Planning users/arm':d['planning_n_per_arm_80pct']},rows=[{'variant':'A','users':d['control_n'],'conversions':d['control_conversions'],'rate':d['control_rate']},{'variant':'B','users':d['treatment_n'],'conversions':d['treatment_conversions'],'rate':d['treatment_rate']}],answer=decision+f". Lift interval: {100*d['lift_interval'][0]:.2f} to {100*d['lift_interval'][1]:.2f} percentage points.",details=d,notice='Fixed-horizon analysis of synthetic randomized data. No sequential monitoring adjustment, covariate adjustment, or multiple-metric correction. Statistical significance is not a business decision.')
