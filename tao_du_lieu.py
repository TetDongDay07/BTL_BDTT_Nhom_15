"""Sinh N1 có F ngõ cụt; N2 tới G được nhưng không thể ăn hết F."""
import random,json,argparse
from pathlib import Path
from maze import parse_maze

def make_data(seed):
    rng=random.Random(seed);rows=[list('%%%%%%%%%%%') for _ in range(7)]
    for r in range(1,6):
        for c in range(1,10):
            if c!=5 or r==5:rows[r][c]='.'
    rows[1][2]='%'  # F tại (1,1) chỉ có một lối ra.
    left=[(r,c) for r in range(1,5) for c in range(1,5) if (r,c) not in [(1,1),(1,2)]]
    right=[(r,c) for r in range(1,5) for c in range(6,10)]
    p,fl2=rng.sample(left,2);fl1=(1,1);g,fr=rng.sample(right,2)
    for pos,ch in [(p,'P'),(fl1,'F'),(fl2,'F'),(g,'G'),(fr,'F')]:rows[pos[0]][pos[1]]=ch
    n1=[''.join(r) for r in rows]
    rows[g[0]][g[1]]='.'
    gp=rng.choice([x for x in left if x not in [p,fl1,fl2]])
    rows[gp[0]][gp[1]]='G';rows[5][5]='%'
    n2=[''.join(r) for r in rows]
    for x in [n1,n2]:parse_maze(x)
    return dict(seed=seed,description='Cửa (5,5); F ngõ cụt (1,1). N2 đổi G sang trái và đóng cửa.',
                cases=[dict(id='N1',rows=n1),dict(id='N2',rows=n2)])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=1504);p.add_argument('--output',default='du_lieu_nhom.json');a=p.parse_args()
    d=make_data(a.seed);Path(a.output).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Đã tạo',a.output)
    for c in d['cases']:print(c['id']+'\n'+'\n'.join(c['rows']))
