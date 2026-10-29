# README bài nộp — Nhóm 15 (5 sinh viên)

Lớp: INT3401. Python/OS đã thử: Python 3.12, Windows 11 và WSL Ubuntu.

Năm thành viên/MSSV:

| STT | Họ và tên | MSSV |
|---|---|---|
| 1 | Phan Ngọc Huy | 25022875 |
| 2 | Lê Đức Huy | 25022870 |
| 3 | Hoàng Trung Kiên | 25022855 |
| 4 | Nguyễn Quốc Hiếu | 25022853 |
| 5 | Dương Nhật Huy | 25022865 |

Tệp dùng nguyên / tệp tự sửa: dùng nguyên maze.py, search.py, run.py, data_cases.py, tao_du_lieu.py, ucs_astar_toi_gian.py, chay_kiem_thu.py, dong_goi.py; nhóm tự làm du_lieu_nhom.json, test_nhom.py, TinhTay.pdf. Seed và mô tả dữ liệu riêng: seed = 1526, hai bản đồ N1 (có lời giải, cost = 20) và N2 (F bị tường ngăn cách, no_path), kích thước 7 hàng × 11 cột.

## Tái tạo kết quả
```powershell
python run.py --batch --tag bat_buoc
python run.py --data du_lieu_nhom.json --batch --tag tu_tao
python run.py --case H --algo ucs --trace 6 --tag tay_H_UCS
python run.py --case H --heuristic via --trace 6 --tag tay_H_Avia
python chay_kiem_thu.py
```

- Tên PDF báo cáo/tính tay/slide: BaoCao.pdf, TinhTay.pdf (B1–B4), ThuyetTrinh.pptx.
- Tệp JSON/CSV/trace/log tương ứng: output/bat_buoc.json, output/bat_buoc.csv, output/tu_tao.json, output/tu_tao.csv, output/tay_H_UCS.json, output/tay_H_Avia.json, output/ket_qua_test.txt.
- Thí nghiệm sửa F/G: Tạo bản sao của N2, dời viên F từ ô bị cô lập (3,6) sang ô hợp lệ (2,3) ở phòng trái (cùng phía P và G). Dự đoán: bài toán chuyển từ vô nghiệm (no_path) sang có nghiệm (found) với chi phí tối ưu cost = 11. Kết quả chạy thực tế: status = 'found', cost = 11, chuỗi hành động ['D','L','U','U','L','L','U','D','R','R','U'], số nút mở rộng N(A_V) = 56 < N(A_F) = 77 < N(UCS) = 111 (khớp 100% dự đoán).
- Người kiểm gói sạch / ngày / máy: Nguyễn Quốc Hiếu / 29/10/2026 / DESKTOP-N7OBFB6. Giới hạn hoặc test chưa đạt: không có test chưa đạt (10/10 OK); giới hạn là m ≤ 8 trên bản đồ nhỏ, và thời gian chạy dưới 1 ms chịu nhiễu hệ điều hành.