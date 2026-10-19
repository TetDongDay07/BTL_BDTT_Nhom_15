"""UCS/A* với cập nhật chi phí. Không dùng visited chỉ theo vị trí."""
from heapq import heappush,heappop
from itertools import count
from time import perf_counter
from maze import heuristic,is_goal,successors,validate_state,state_text

def solve(maze,algorithm='astar',h='food',order='RDLU',max_expanded=200000,
          trace_limit=0,step=False,start_state=None):
    if algorithm not in ('ucs','astar'):raise ValueError('Chọn ucs hoặc astar.')
    if h not in ('zero','food','via'):raise ValueError('Chọn zero, food, via.')
    if len(order)!=4 or set(order)!=set('RDLU'):raise ValueError('Sai thứ tự hướng.')
    if type(max_expanded) is not int or max_expanded<0:raise ValueError('Ngân sách không âm.')
    if trace_limit is not None and (type(trace_limit) is not int or trace_limit<0):
        raise ValueError('trace_limit phải là None hoặc số nguyên không âm.')
    start=maze.initial() if start_state is None else tuple(start_state)
    validate_state(maze,start)
    hn='zero' if algorithm=='ucs' else h
    H=lambda s:heuristic(maze,s,hn)
    ids=count();heap=[(H(start),next(ids),0,start)]
    best_g={start:0};parent={start:None};was_expanded=set()
    stats=dict(popped=0,expanded=0,generated=0,pushed=1,stale=0,reopened=0,frontier_peak=1)
    trace=[];pop_order=[];end=None;status='no_path';clock=perf_counter()
    def snapshot():
        return [dict(state=list(s),g=g,h=H(s),f=f,ticket=i,stale=(g!=best_g.get(s)))
                for f,i,g,s in sorted(heap)]
    def record(s,g,before,updates,outcome):
        store=trace_limit is None or len(trace)<trace_limit
        if not(store or step):return
        e=dict(index=stats['popped'],state=list(s),g=g,h=H(s),f=g+H(s),
               frontier_before=before,updates=updates,frontier_after=snapshot(),outcome=outcome)
        if store:trace.append(e)
        if step:
            print('\nBước',stats['popped'],state_text(maze,s),'g=',g,'h=',H(s),outcome)
            print('OPEN sau:',[(state_text(maze,x['state']),x['g'],x['f']) for x in e['frontier_after']])
            input('Enter để thực hiện bước tiếp theo; Ctrl+C để dừng: ')
    while heap:
        need=step or trace_limit is None or len(trace)<trace_limit
        before=snapshot() if need else []
        f,_,g,s=heappop(heap)
        if g!=best_g.get(s):stats['stale']+=1;continue
        stats['popped']+=1;pop_order.append(list(s))
        if is_goal(maze,s):
            status,end='found',s;record(s,g,before,[],'goal');break
        if stats['expanded']>=max_expanded:
            status='limit';record(s,g,before,[],'limit');break
        if s in was_expanded:stats['reopened']+=1
        was_expanded.add(s);stats['expanded']+=1;updates=[]
        for action,v in successors(maze,s,order):
            stats['generated']+=1;ng=g+1
            if ng<best_g.get(v,float('inf')):
                old=best_g.get(v);best_g[v]=ng;parent[v]=(s,action)
                heappush(heap,(ng+H(v),next(ids),ng,v));stats['pushed']+=1
                updates.append(dict(state=list(v),action=action,g=ng,old_g=old))
        stats['frontier_peak']=max(stats['frontier_peak'],len(heap))
        record(s,g,before,updates,'expanded')
    states=actions=None
    if end is not None:
        states=[end];actions=[];s=end
        while parent[s] is not None:
            s,a=parent[s];states.append(s);actions.append(a)
        states=[list(s) for s in reversed(states)];actions.reverse()
    return dict(status=status,algorithm=algorithm,heuristic=hn,order=order,
                start=list(start),goal=list(maze.goal),foods=[list(f) for f in maze.foods],rows=list(maze.rows),
                cost=None if end is None else best_g[end],length=None if actions is None else len(actions),
                states=states,actions=actions,path=None if states is None else [s[:2] for s in states],
                pop_order=pop_order,trace=trace,**stats,elapsed_ms=(perf_counter()-clock)*1000)
