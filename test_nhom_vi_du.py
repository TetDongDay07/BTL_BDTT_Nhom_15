"""Ví dụ cách viết test. Không tính vào 10 test của nhóm."""
import unittest
from maze import parse_maze
from search import solve
class ViDu(unittest.TestCase):
    def test_duong_thang(self):
        r=solve(parse_maze(['PFG']),h='via');self.assertEqual(r['cost'],2);self.assertEqual(r['actions'],['R','R'])
    def test_quay_lai(self):
        r=solve(parse_maze(['FPG']),h='food');self.assertEqual(r['cost'],3);self.assertEqual(r['actions'],['L','R','R'])
if __name__=='__main__':unittest.main()
