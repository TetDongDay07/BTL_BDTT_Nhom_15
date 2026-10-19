"""Bản ngắn chạy được để đọc trước. h='zero' cho UCS."""
from heapq import heappop,heappush
from itertools import count
from maze import parse_maze,successors,is_goal,heuristic

def search_short(m,h='food'):
    s=m.initial();ids=count();heap=[(heuristic(m,s,h),next(ids),0,s)]
    best_g={s:0};parent={s:None}
    while heap:
        _,_,g,s=heappop(heap)
        if g!=best_g[s]:continue
        if is_goal(m,s):
            actions=[]
            while parent[s] is not None:s,a=parent[s];actions.append(a)
            return g,list(reversed(actions))
        for a,v in successors(m,s):
            ng=g+1
            if ng<best_g.get(v,float('inf')):
                best_g[v]=ng;parent[v]=(s,a)
                heappush(heap,(ng+heuristic(m,v,h),next(ids),ng,v))
    return None,None
if __name__=='__main__':
    m=parse_maze(['%%%%%%%','%P.F.G%','%%%%%%%'])
    for h in ['zero','food','via']:print(h,search_short(m,h))
