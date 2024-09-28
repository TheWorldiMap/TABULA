@echo off
pyinstaller TABULA.py --collect-data sv_ttk --onefile --noconsole
rmdir build /s /q
move "dist\TABULA.exe" "TABULA.exe"
rmdir dist /s /q
del "TABULA.spec"
exit