@echo off
chcp 65001 >nul
cd /d "%~dp0"
for %%F in (De_Nhom15_SinhVien De_Nhom15_GiangVien HuongDan_Nhom15_Python) do (
 if exist "%%F.tex" (
  pdflatex -interaction=nonstopmode -halt-on-error "%%F.tex"
  if errorlevel 1 goto loi
  pdflatex -interaction=nonstopmode -halt-on-error "%%F.tex"
  if errorlevel 1 goto loi
 )
)
pushd MauBaoCao
pdflatex -interaction=nonstopmode -halt-on-error Mau_BaoCao_Nhom15.tex
if errorlevel 1 goto loi
pdflatex -interaction=nonstopmode -halt-on-error Mau_BaoCao_Nhom15.tex
popd
echo Da bien dich. Xem cac tep PDF.
pause
exit /b 0
:loi
echo Co loi. Xem tep log.
pause
exit /b 1
