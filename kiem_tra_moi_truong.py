import sys
from pathlib import Path
if __name__=='__main__':
    print('Python:',sys.version);print('Thư mục:',Path(__file__).resolve().parent)
    if sys.version_info<(3,10):raise SystemExit('Cần Python 3.10 trở lên.')
    for f in ['maze.py','search.py','run.py','data_cases.py']:
        if not Path(__file__).with_name(f).is_file():raise SystemExit('Thiếu '+f)
    print('Sẵn sàng; không cần cài gói ngoài.')
