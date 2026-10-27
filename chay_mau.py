"""Chỉ sửa các biến dữ liệu, rồi chạy tệp này trong VS Code."""
from maze import parse_maze,draw_path
from search import solve
ROWS=['%%%%%%%','%P.F.G%','%%%%%%%']
ALGORITHM='astar'
HEURISTIC='via'  # food / via / zero
ORDER='RDLU'
if __name__=='__main__':
    m=parse_maze(ROWS);r=solve(m,ALGORITHM,HEURISTIC,ORDER,trace_limit=6)
    print(r['status'],'cost=',r['cost'],'expanded=',r['expanded'])
    print('Actions:',r['actions']);print('States (r,c,mask):',r['states'])
    print(draw_path(m,r['states']))
