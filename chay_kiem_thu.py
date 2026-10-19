"""Chạy test riêng của nhóm và lưu log thực tế."""
import subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    if not(ROOT/'test_nhom.py').is_file():raise SystemExit('Nhóm cần viết test_nhom.py với ít nhất 10 test riêng.')
    env=dict(os.environ,PYTHONIOENCODING='utf-8')
    r=subprocess.run([sys.executable,'-m','unittest','-v','test_nhom'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',env=env)
    text='COMMAND: python -m unittest -v test_nhom\n'+r.stdout+r.stderr
    (ROOT/'output').mkdir(exist_ok=True);(ROOT/'output/ket_qua_test.txt').write_text(text,encoding='utf-8');print(text)
    sys.exit(r.returncode)
