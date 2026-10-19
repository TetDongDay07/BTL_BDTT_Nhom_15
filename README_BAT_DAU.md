# Nhóm 15 — Ăn hết thức ăn rồi tới G
**5 sinh viên · 10 ngày · bảo vệ 15–20 phút**
Học phần: Biểu diễn tri thức và tìm kiếm nâng cao. Giảng viên: Nguyễn Bích Vân.

## Chạy ngay
Giải nén toàn bộ ZIP. Mở thư mục có chay_mau.py bằng VS Code; Terminal → New Terminal.
Không gõ `cd python`: các tệp .py nằm ngay thư mục chính. Cần Python 3.10+, chỉ thư viện chuẩn.
```powershell
python kiem_tra_moi_truong.py
python chay_mau.py
python ucs_astar_toi_gian.py
python -m unittest -v test_mau test_nhom_vi_du
```

## Chạy bài nộp
```powershell
python run.py --batch --tag bat_buoc
python run.py --case H --algo ucs --trace 6 --tag tay_H_UCS
python run.py --case H --heuristic via --trace 6 --tag tay_H_Avia
python tao_du_lieu.py --seed 1526
python run.py --data du_lieu_nhom.json --batch --tag tu_tao
python run.py --case H --heuristic via --step --tag demo_step
```
24 cấu hình chung, 12 cấu hình riêng. `--trace 6` chỉ giới hạn số bước ghi, không dừng tìm kiếm sau sáu bước.
`--step` dừng thật trong vòng lặp; nhấn Enter tại Terminal. Ctrl+C dừng hẳn.

## Sửa dữ liệu
Sửa ROWS, ALGORITHM, HEURISTIC, ORDER trong chay_mau.py, hoặc dùng JSON tự tạo.
State=(r,c,mask); bit1 nghĩa là CHƯA ăn. Food sắp theo hàng rồi cột. Đích đòi vị trí G và mask0.
food: xa nhất tới F còn lại, tập rỗng=0. via: cận phải qua từng F rồi tới G. zero: 0.
Mỗi bản đồ có đúng P/G; bài dữ liệu riêng yêu cầu ba F. Không thêm dấu cách cuối hàng.

## Hoàn thiện và nộp
Chọn Word hoặc LaTeX trong MauBaoCao, điền rồi xuất BaoCao.pdf (6–8 trang chính).
Nộp TinhTay.pdf, ThuyetTrinh.pptx (6–8 slide); ít nhất 10 test riêng trong test_nhom.py (2/người, 3 kỳ vọng tính tay).
Đổi README_NOP_MAU.md → README_NOP.md; DongGop_MAU.md → DongGop.md rồi điền.
```powershell
python chay_kiem_thu.py
python dong_goi.py
```
Tệp test_nhom.py do nhóm tự viết; thiếu tệp này không phải mã thuật toán bỏ trống.
Giải nén ZIP sang thư mục mới và tái chạy theo README trước khi nộp.

## Biên dịch
Mỗi tệp .tex tự chứa hình TikZ. Chọn PdfLaTeX, chạy hai lần; hoặc BIEN_DICH_WINDOWS.bat.
