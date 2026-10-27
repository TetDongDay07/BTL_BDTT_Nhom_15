"""10 kiểm thử riêng của Nhóm 15 (5 sinh viên, mỗi thành viên 2 kiểm thử).
Bao phủ toàn bộ 7 nhóm thuộc tính trong đề bài và khớp 100% với Báo cáo & TinhTay.pdf.
"""
import unittest
import json
from copy import deepcopy
from pathlib import Path
from maze import parse_maze, successors, is_goal, heuristic, DIRECTIONS
from search import solve
from data_cases import CASES

ROOT = Path(__file__).resolve().parent


class TestNhom15(unittest.TestCase):
    # =========================================================================
    # THÀNH VIÊN 1: Nguyễn Quốc Hiếu (2 kiểm thử)
    # =========================================================================
    def test_01_an_va_quay_lai(self):
        """[TV1 - Tính tay TinhTay.pdf tr.B4] Ăn F ở ngõ cụt trái rồi quay lại qua P tới G."""
        rows = [
            '%%%%%%%',
            '%F.P.G%',
            '%%%%%%%'
        ]
        m = parse_maze(rows)
        self.assertEqual(m.initial(), (1, 3, 1))
        for algo, h in [('ucs', 'zero'), ('astar', 'food'), ('astar', 'via')]:
            r = solve(m, algorithm=algo, h=h, order='RDLU')
            self.assertEqual(r['status'], 'found')
            self.assertEqual(r['cost'], 6)
            self.assertEqual(r['actions'], ['L', 'L', 'R', 'R', 'R', 'R'])
            self.assertEqual(
                r['states'],
                [[1, 3, 1], [1, 2, 1], [1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0], [1, 5, 0]]
            )
            # Kiểm chứng ô (1,2) và (1,3) được đi qua 2 lần với mask khác nhau (1 rồi 0)
            self.assertIn([1, 2, 1], r['states'])
            self.assertIn([1, 2, 0], r['states'])
            self.assertIn([1, 3, 1], r['states'])
            self.assertIn([1, 3, 0], r['states'])

    def test_02_mask_khong_them_bit(self):
        """[TV1] Kiểm tra mask chỉ xóa bit khi ăn F, tuyệt đối không bật lại bit khi đi qua lần 2."""
        m = parse_maze(['PF.G'])  # P=(0,0), F=(0,1), G=(0,3)
        s0 = m.initial()
        self.assertEqual(s0, (0, 0, 1))
        # Bước 1: sang phải (0,1) ăn F -> mask về 0
        s1 = dict(successors(m, s0))['R']
        self.assertEqual(s1, (0, 1, 0))
        # Bước 2: lùi về (0,0) -> mask giữ nguyên 0
        s2 = dict(successors(m, s1))['L']
        self.assertEqual(s2, (0, 0, 0))
        # Bước 3: đi qua lại ô thức ăn cũ (0,1) -> mask vẫn bằng 0 (không bị bật lại như XOR)
        s3 = dict(successors(m, s2))['R']
        self.assertEqual(s3, (0, 1, 0))

    # =========================================================================
    # THÀNH VIÊN 2: Lê Đức Huy (2 kiểm thử)
    # =========================================================================
    def test_03_qua_goal_som(self):
        """[TV2 - Tính tay TinhTay.pdf tr.B4] Đi qua G khi còn F chưa được dừng, ăn F xong mới lùi về G."""
        rows = [
            '%%%%%%%%',
            '%P.G..F%',
            '%%%%%%%%'
        ]
        m = parse_maze(rows)
        # Khi đứng tại G=(1,3) nhưng còn F (mask=1) thì chưa phải đích
        self.assertFalse(is_goal(m, (1, 3, 1)))
        self.assertTrue(is_goal(m, (1, 3, 0)))
        r = solve(m, algorithm='astar', h='via', order='RDLU')
        self.assertEqual(r['status'], 'found')
        self.assertEqual(r['cost'], 8)
        self.assertEqual(r['actions'], ['R', 'R', 'R', 'R', 'R', 'L', 'L', 'L'])
        # Ghé tọa độ G=(1,3) đúng 2 lần trên lộ trình
        self.assertEqual(r['path'].count([1, 3]), 2)

    def test_04_het_food_chua_toi_goal(self):
        """[TV2] Đã ăn hết F (mask=0) nhưng chưa đứng tại G: is_goal=False, h_F=0, h_V=d(p,G)>0."""
        rows = [
            '%%%%%%%',
            '%P.F.G%',
            '%%%%%%%'
        ]
        m = parse_maze(rows)
        s_after_food = (1, 3, 0)  # Đứng tại F=(1,3), đã ăn xong F, đích G=(1,5)
        self.assertFalse(is_goal(m, s_after_food))
        self.assertEqual(heuristic(m, s_after_food, 'food'), 0)
        self.assertEqual(heuristic(m, s_after_food, 'via'), 2)
        r = solve(m, algorithm='astar', h='via')
        self.assertEqual(r['cost'], 4)
        self.assertEqual(r['states'][-1], [1, 5, 0])

    # =========================================================================
    # THÀNH VIÊN 3: Dương Nhật Huy (2 kiểm thử)
    # =========================================================================
    def test_05_khong_co_food_ban_dau(self):
        """[TV3 - Tính tay TinhTay.pdf tr.B4] Bản đồ không có F ban đầu (m=0, mask=0)."""
        rows = [
            '%%%%%%%',
            '%P...G%',
            '%%%%%%%'
        ]
        m = parse_maze(rows)
        s0 = m.initial()
        self.assertEqual(s0, (1, 1, 0))
        self.assertEqual(heuristic(m, s0, 'food'), 0)
        self.assertEqual(heuristic(m, s0, 'via'), 4)
        r = solve(m, algorithm='astar', h='via')
        self.assertEqual(r['status'], 'found')
        self.assertEqual(r['cost'], 4)
        self.assertEqual(r['actions'], ['R', 'R', 'R', 'R'])

    def test_06_no_path_va_limit(self):
        """[TV3] Phân biệt rõ trạng thái vô nghiệm (no_path) và hết ngân sách mở rộng (limit)."""
        # G tới được từ P nhưng F bị tường ngăn kín -> no_path, cost=None (không trả cost=0)
        m_blocked = parse_maze(['%P.G%F%'])
        r_no_path = solve(m_blocked, algorithm='astar', h='via')
        self.assertEqual(r_no_path['status'], 'no_path')
        self.assertIsNone(r_no_path['cost'])
        self.assertIsNone(r_no_path['actions'])

        # Bản đồ M0 có lời giải (cần mở rộng 18 nút với A_V) nhưng đặt ngân sách max_expanded=5 -> limit
        m0 = parse_maze(CASES['M0'])
        r_limit = solve(m0, algorithm='astar', h='via', max_expanded=5)
        self.assertEqual(r_limit['status'], 'limit')
        self.assertIsNone(r_limit['cost'])
        self.assertEqual(r_limit['expanded'], 5)

    # =========================================================================
    # THÀNH VIÊN 4: Phan Ngọc Huy (2 kiểm thử)
    # =========================================================================
    def test_07_dau_hoan_tat_ngan_sach_0(self):
        """[TV4] Trạng thái đầu đã hoàn tất (tại G, mask=0) với ngân sách max_expanded=0 vẫn thành công."""
        m = parse_maze(['PFG'])
        goal_state = (0, 2, 0)
        r = solve(m, algorithm='astar', h='via', start_state=goal_state, max_expanded=0)
        self.assertEqual(r['status'], 'found')
        self.assertEqual(r['cost'], 0)
        self.assertEqual(r['actions'], [])
        self.assertEqual(r['popped'], 1)
        self.assertEqual(r['expanded'], 0)

    def test_08_ban_do_sai_va_bien(self):
        """[TV4] Kiểm tra bắt lỗi dữ liệu bản đồ sai và luật di chuyển biên/tường/không đi chéo."""
        # Hàng không đều, ký tự lạ, thiếu P/G, quá 8 viên F
        with self.assertRaises(ValueError):
            parse_maze(['P..', 'FG'])
        with self.assertRaises(ValueError):
            parse_maze(['P@G'])
        with self.assertRaises(ValueError):
            parse_maze(['P.F'])
        with self.assertRaises(ValueError):
            parse_maze(['PFFFFFFFFFG'])  # 9 viên F (> 8)

        # Kiểm tra không đi xuyên biên/quấn mép và không đi chéo
        m_edge = parse_maze(['PG'])
        self.assertEqual(list(successors(m_edge, m_edge.initial())), [('R', (0, 1, 0))])
        m_diag = parse_maze(['P%', '%G'])
        self.assertEqual(list(successors(m_diag, m_diag.initial())), [])

    # =========================================================================
    # THÀNH VIÊN 5: Hoàng Trung Kiên (2 kiểm thử)
    # =========================================================================
    def test_09_khong_sua_input_va_trace(self):
        """[TV5] Bảo toàn dữ liệu đầu vào, bật/tắt trace không đổi kết quả, A*(h=0) khớp UCS, đổi F/G."""
        rows = list(CASES['H'])
        saved = deepcopy(rows)
        m = parse_maze(rows)
        r_no_trace = solve(m, algorithm='astar', h='via', trace_limit=0)
        r_trace = solve(m, algorithm='astar', h='via', trace_limit=4)
        self.assertEqual(rows, saved)  # Không sửa đầu vào
        for k in ['status', 'cost', 'actions', 'states', 'expanded', 'popped', 'generated']:
            self.assertEqual(r_no_trace[k], r_trace[k])
        self.assertEqual(len(r_trace['trace']), 4)

        # A* với h='zero' cho thứ tự duyệt pop_order giống hệt UCS
        r_ucs = solve(m, algorithm='ucs', order='RDLU')
        r_azero = solve(m, algorithm='astar', h='zero', order='RDLU')
        self.assertEqual(r_ucs['pop_order'], r_azero['pop_order'])

        # Đổi vị trí F/G trên bản đồ mới: ánh xạ bit và heuristic=0 tại đích thực
        m_swapped = parse_maze(['%%%%%%%%', '%G.PF.F%', '%%%%%%%%'])
        self.assertEqual(m_swapped.goal, (1, 1))
        self.assertEqual(m_swapped.foods, ((1, 4), (1, 6)))
        for h_name in ['zero', 'food', 'via']:
            self.assertEqual(heuristic(m_swapped, (1, 1, 0), h_name), 0)

    def test_10_kiem_duong_va_chi_phi(self):
        """[TV5] Kiểm chứng độc lập tính hợp lệ của lộ trình và sự đồng thuận chi phí trên M0, M1, H, N1."""
        cases_to_check = {
            'M0': (CASES['M0'], 10),
            'M1': (CASES['M1'], 13),
            'H': (CASES['H'], 7),
        }
        du_lieu_path = ROOT / 'du_lieu_nhom.json'
        if du_lieu_path.is_file():
            data = json.loads(du_lieu_path.read_text(encoding='utf-8'))
            for c in data['cases']:
                if c['id'] == 'N1':
                    cases_to_check['N1'] = (c['rows'], 20)

        for name, (rows, expected_cost) in cases_to_check.items():
            m = parse_maze(rows)
            for algo, h in [('ucs', 'zero'), ('astar', 'food'), ('astar', 'via')]:
                r = solve(m, algorithm=algo, h=h, order='RDLU')
                self.assertEqual(r['status'], 'found', f'Lỗi status tại {name}-{algo}-{h}')
                self.assertEqual(r['cost'], expected_cost, f'Lỗi cost tại {name}-{algo}-{h}')
                self.assertEqual(len(r['actions']), r['cost'])
                self.assertEqual(len(r['states']) - 1, r['cost'])

                # Mô phỏng bước đi độc lập để kiểm chứng không xuyên tường và ăn đủ F
                curr_r, curr_c, curr_mask = m.initial()
                self.assertEqual(r['states'][0], [curr_r, curr_c, curr_mask])
                food_index = {f: i for i, f in enumerate(m.foods)}
                for step_idx, act in enumerate(r['actions'], start=1):
                    dr, dc = DIRECTIONS[act]
                    curr_r, curr_c = curr_r + dr, curr_c + dc
                    self.assertIn((curr_r, curr_c), m.cells)
                    if (curr_r, curr_c) in food_index:
                        curr_mask &= ~(1 << food_index[(curr_r, curr_c)])
                    self.assertEqual(r['states'][step_idx], [curr_r, curr_c, curr_mask])
                # Cuối đường phải đứng tại G và mask == 0
                self.assertEqual((curr_r, curr_c), m.goal)
                self.assertEqual(curr_mask, 0)


if __name__ == '__main__':
    unittest.main()