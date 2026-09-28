import csv,random
from pathlib import Path
r=random.Random(240);root=Path(__file__).parent;(root/'data').mkdir(exist_ok=True)
with (root/'data/experiment.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['user_id','variant','converted'])
 for i in range(4000):
  variant='B' if r.random()<.5 else 'A';w.writerow([f'U{i:05}',variant,int(r.random()<(.145 if variant=='B' else .12))])
