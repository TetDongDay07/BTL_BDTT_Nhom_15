"""Chạy ví dụ/batch; kết quả nằm trong output cạnh run.py."""
import argparse,csv,json
from pathlib import Path
from maze import parse_maze,draw_path
from search import solve
from data_cases import CASES,CONFIGS,ORDERS
ROOT=Path(__file__).resolve().parent

def load_cases(filename):
    data=json.loads(Path(filename).read_text(encoding='utf-8'))
    if not isinstance(data,dict) or not isinstance(data.get('cases'),list):raise ValueError('JSON cần cases.')
    result={}
    for c in data['cases']:
        if not isinstance(c.get('id'),str) or not c['id'] or c['id'] in result:raise ValueError('Mã case sai/trùng.')
        parse_maze(c['rows']);result[c['id']]=c['rows']
    if not result:raise ValueError('Danh sách cases rỗng.')
    return result

def save_results(results,tag):
    if not tag or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in tag):
        raise ValueError('Tag chỉ gồm chữ không dấu, số, _ và -.')
    out=ROOT/'output';out.mkdir(exist_ok=True)
    (out/f'{tag}.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    fields=['case','algorithm','heuristic','order','status','cost','length','expanded','popped','generated','frontier_peak','stale','reopened','elapsed_ms']
    with (out/f'{tag}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(results)
    if any(r['trace'] for r in results):
        fields=['case','index','state','g','h','f','outcome','frontier_before','updates','frontier_after']
        with (out/f'{tag}_trace.csv').open('w',encoding='utf-8-sig',newline='') as f:
            w=csv.DictWriter(f,fields);w.writeheader()
            for r in results:
                for e in r['trace']:
                    row=dict(case=r['case'],**e)
                    w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
    print('Đã lưu',len(results),'cấu hình:',out/f'{tag}.json')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case',default='M0');p.add_argument('--algo',choices=['ucs','astar'],default='astar')
    p.add_argument('--heuristic',choices=['zero','food','via'],default='food');p.add_argument('--order',default='RDLU')
    p.add_argument('--batch',action='store_true');p.add_argument('--data')
    p.add_argument('--trace',type=int,default=0);p.add_argument('--step',action='store_true')
    p.add_argument('--max-expanded',type=int,default=200000);p.add_argument('--tag',default='ket_qua')
    a=p.parse_args()
    try:
        cases=load_cases(a.data) if a.data else CASES
        if a.batch and a.step:raise ValueError('Chỉ dùng step cho một cấu hình.')
        if a.batch:
            selected=list(cases) if a.data else ['M0','M1','M2','M3']
            jobs=[(c,algo,h,o) for c in selected for algo,h in CONFIGS for o in ORDERS]
        else:
            if a.case not in cases:raise ValueError('Không có case '+a.case)
            jobs=[(a.case,a.algo,a.heuristic,a.order)]
        results=[]
        for c,algo,h,o in jobs:
            m=parse_maze(cases[c]);r=solve(m,algo,h,o,a.max_expanded,a.trace,a.step);r['case']=c;results.append(r)
            print(c,algo,r['heuristic'],o,r['status'],'cost=',r['cost'],'expanded=',r['expanded'])
            if not a.batch:print('Actions:',r['actions']);print(draw_path(m,r['states']))
        save_results(results,a.tag)
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as e:p.error(str(e))
if __name__=='__main__':main()
