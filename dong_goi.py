"""Kiểm tệp rồi tạo ZIP. Không chấm nội dung báo cáo hoặc xác nhận số test."""
from pathlib import Path
import argparse,zipfile,json
ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='Nhom15_AnHetThucAn_GiuaKy.zip');a=p.parse_args()
    names=['BaoCao.pdf','TinhTay.pdf','ThuyetTrinh.pptx','README_NOP.md','DongGop.md','test_nhom.py',
      'du_lieu_nhom.json','output/bat_buoc.json','output/bat_buoc.csv','output/tu_tao.json','output/tu_tao.csv',
      'output/ket_qua_test.txt','output/tay_H_UCS.json','output/tay_H_Avia.json']
    missing=[x for x in names if not(ROOT/x).is_file()]
    if missing:raise SystemExit('Cần hoàn thiện các tệp:\n'+'\n'.join(missing))
    for tag,n in [('bat_buoc',24),('tu_tao',12)]:
        data=json.loads((ROOT/'output'/f'{tag}.json').read_text(encoding='utf-8'))
        if len(data)!=n:raise SystemExit(f'{tag} cần {n} cấu hình.')
    dest=Path(a.output).resolve()
    candidates=list(ROOT.glob('*.py'))+[ROOT/x for x in names if not x.endswith('.py')]+list((ROOT/'output').glob('*_trace.csv'))
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
        for x in dict.fromkeys(candidates):z.write(x,'Nhom15_AnHetThucAn_GiuaKy/'+str(x.relative_to(ROOT)))
    print('Đã tạo',dest,'; giải nén và chạy lại theo README.')
