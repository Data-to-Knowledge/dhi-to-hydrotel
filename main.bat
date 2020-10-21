echo started %date% %time% >> %~dp0\backup.log
call D:\Miniconda3\Scripts\activate.bat D:\Miniconda3 >> %~dp0\backup.log 2>&1
call activate dhi_hydrotel >> %~dp0\backup.log 2>&1
call python %~dp0\dhi_to_hydrotel.py >> %~dp0\backup.log 2>&1
echo ended %date% %time% >> %~dp0\backup.log
