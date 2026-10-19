"""Luật mê cung. State=(r,c,mask), bit 1 chỉ thức ăn CHƯA ăn."""
from dataclasses import dataclass
State=tuple[int,int,int]
DIRECTIONS={'R':(0,1),'D':(1,0),'L':(0,-1),'U':(-1,0)}

@dataclass(frozen=True)
class Maze:
    rows: tuple[str,...]
    start: tuple[int,int]
    goal: tuple[int,int]
    foods: tuple[tuple[int,int],...]
    cells: frozenset[tuple[int,int]]
    def initial(self):
        mask=(1<<len(self.foods))-1
        for i,food in enumerate(self.foods):
            if self.start==food: mask &= ~(1<<i)
        return (*self.start,mask)

def parse_maze(rows):
    if isinstance(rows,(str,bytes)):
        raise ValueError('Cần danh sách các hàng, không phải một chuỗi.')
    rows=tuple(rows)
    if not rows or any(not isinstance(r,str) or not r for r in rows):
        raise ValueError('Cần các hàng chuỗi không rỗng.')
    if any(len(r)!=len(rows[0]) for r in rows):
        raise ValueError('Các hàng phải cùng số ký tự.')
    if any(c not in '%.PFG' for r in rows for c in r):
        raise ValueError('Chỉ dùng %, ., P, F, G; không có dấu cách.')
    positions=lambda ch: [(r,c) for r,row in enumerate(rows) for c,x in enumerate(row) if x==ch]
    p,g,fs=positions('P'),positions('G'),positions('F')
    if len(p)!=1 or len(g)!=1:raise ValueError('Cần đúng một P và một G.')
    if len(fs)>8:raise ValueError('Bộ thực hành giới hạn tối đa 8 F.')
    cells=frozenset((r,c) for r,row in enumerate(rows) for c,x in enumerate(row) if x!='%')
    return Maze(rows,p[0],g[0],tuple(fs),cells)

def validate_state(m,s):
    if len(s)!=3 or any(type(x) is not int for x in s):
        raise ValueError('State gồm ba số nguyên: r,c,mask.')
    if s[:2] not in m.cells or not 0<=s[2]<(1<<len(m.foods)):
        raise ValueError('Vị trí hoặc mask không hợp lệ.')
    if any(s[:2]==f and s[2]&(1<<i) for i,f in enumerate(m.foods)):
        raise ValueError('Thức ăn dưới Pacman phải đã được ăn.')

def successors(m,s,order='RDLU'):
    if len(order)!=4 or set(order)!=set(DIRECTIONS):raise ValueError('Sai thứ tự hướng.')
    bits={f:1<<i for i,f in enumerate(m.foods)}
    for a in order:
        dr,dc=DIRECTIONS[a];q=(s[0]+dr,s[1]+dc)
        if q in m.cells:
            yield a,(*q,s[2]&~bits.get(q,0))

def is_goal(m,s):
    return s[:2]==m.goal and s[2]==0

def distance(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def heuristic(m,s,name='food'):
    if name=='zero':return 0
    p=s[:2];fs=[f for i,f in enumerate(m.foods) if s[2]&(1<<i)]
    if name=='food':return max((distance(p,f) for f in fs),default=0)
    if name=='via':return max([distance(p,m.goal)]+[distance(p,f)+distance(f,m.goal) for f in fs])
    raise ValueError('Heuristic hợp lệ: zero, food, via.')

def state_text(m,s):
    fs=''.join(chr(97+i) for i in range(len(m.foods)) if s[2]&(1<<i)) or '-'
    return f'({s[0]},{s[1]};{fs})'

def draw_path(m,states):
    rows=[list(row) for row in m.rows]
    for r,c,_ in states or []:
        if rows[r][c]=='.':rows[r][c]='*'
    return '\n'.join(''.join(row) for row in rows)
