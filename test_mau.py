"""26 kiểm thử phát sẵn; không tính vào kiểm thử riêng của nhóm."""
import unittest
from copy import deepcopy
from maze import *
from search import solve
from ucs_astar_toi_gian import search_short
from data_cases import CASES
class MauTests(unittest.TestCase):
    def test_shape(self):
        with self.assertRaises(ValueError):parse_maze(['P..','FG'])
    def test_symbols(self):
        with self.assertRaises(ValueError):parse_maze(['P?G'])
    def test_missing_goal(self):
        with self.assertRaises(ValueError):parse_maze(['P.F'])
    def test_duplicate_start(self):
        with self.assertRaises(ValueError):parse_maze(['PPG'])
    def test_string_rejected(self):
        with self.assertRaises(ValueError):parse_maze('PFG')
    def test_food_order(self):
        m=parse_maze(['PF.','..F','..G']);self.assertEqual(m.foods,((0,1),(1,2)));self.assertEqual(m.initial(),(0,0,3))
    def test_eat_revisit(self):
        m=parse_maze(['PFG']);s=dict(successors(m,m.initial()))['R'];self.assertEqual(s,(0,1,0))
        v=dict(successors(m,s))['L'];self.assertEqual(v,(0,0,0));self.assertEqual(dict(successors(m,v))['R'],s)
    def test_no_wrapping(self):
        m=parse_maze(['PG']);self.assertEqual(list(successors(m,m.initial())),[('R',(0,1,0))])
    def test_no_diagonal(self):
        m=parse_maze(['P%','%G']);self.assertEqual(list(successors(m,m.initial())),[])
    def test_goal_needs_food(self):
        m=parse_maze(['PGF']);self.assertFalse(is_goal(m,(0,1,1)));self.assertTrue(is_goal(m,(0,1,0)))
    def test_pass_goal_return(self):
        r=solve(parse_maze(['PGF']),h='via');self.assertEqual(r['actions'],['R','R','L']);self.assertEqual(r['cost'],3)
    def test_no_food_heuristic(self):
        m=parse_maze(['P.G']);self.assertEqual(heuristic(m,m.initial(),'food'),0);self.assertEqual(heuristic(m,m.initial(),'via'),2)
    def test_goal_h(self):
        m=parse_maze(['PFG'])
        for h in ['zero','food','via']:self.assertEqual(heuristic(m,(*m.goal,0),h),0)
    def test_path_straight(self):
        m=parse_maze(['P.F.G'])
        for algo,h in [('ucs','zero'),('astar','food'),('astar','via')]:self.assertEqual(solve(m,algo,h)['cost'],4)
    def test_return_start_new_mask(self):
        r=solve(parse_maze(['FPG']),h='via');self.assertEqual(r['states'],[[0,1,1],[0,0,0],[0,1,0],[0,2,0]])
    def test_no_path(self):
        r=solve(parse_maze(['P%G']));self.assertEqual(r['status'],'no_path');self.assertIsNone(r['cost'])
    def test_goal_reachable_food_not(self):
        r=solve(parse_maze(['PG%F']));self.assertEqual(r['status'],'no_path')
    def test_zero_budget(self):
        r=solve(parse_maze(['PFG']),max_expanded=0);self.assertEqual(r['status'],'limit');self.assertIsNone(r['cost']);self.assertEqual(r['expanded'],0)
    def test_goal_before_budget(self):
        m=parse_maze(['PFG']);r=solve(m,start_state=(*m.goal,0),max_expanded=0);self.assertEqual(r['cost'],0);self.assertEqual(r['popped'],1)
    def test_invalid_state(self):
        with self.assertRaises(ValueError):solve(parse_maze(['PFG']),start_state=(0,1,1))
    def test_invalid_options(self):
        m=parse_maze(['PFG'])
        with self.assertRaises(ValueError):solve(m,order='RRDL')
        with self.assertRaises(ValueError):solve(m,max_expanded=-1)
    def test_input_unchanged(self):
        rows=['PF.','..G'];saved=deepcopy(rows);solve(parse_maze(rows));self.assertEqual(rows,saved)
    def test_trace_invariance(self):
        m=parse_maze(CASES['M0']);a=solve(m,h='via');b=solve(m,h='via',trace_limit=6)
        for k in ['actions','cost','expanded','popped','generated']:self.assertEqual(a[k],b[k])
        self.assertEqual(len(b['trace']),6)
    def test_zero_equals_ucs(self):
        m=parse_maze(CASES['M0']);self.assertEqual(solve(m,'ucs')['pop_order'],solve(m,'astar','zero')['pop_order'])
    def test_counts(self):
        r=solve(parse_maze(['PFG']));self.assertEqual(r['popped'],r['expanded']+1);self.assertEqual(len(r['path'])-1,r['cost'])
    def test_short_agrees(self):
        m=parse_maze(CASES['M0'])
        for h in ['zero','food','via']:
            c,actions=search_short(m,h);r=solve(m,h=h);self.assertEqual((c,actions),(r['cost'],r['actions']))
if __name__=='__main__':unittest.main()
