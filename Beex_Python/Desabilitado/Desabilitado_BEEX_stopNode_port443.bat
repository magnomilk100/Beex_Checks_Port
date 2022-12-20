@ECHO OFF                                                                              
FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| findstr "443" ') DO (
SET /A ProcessId=%%T) &GOTO SkipLine                                                   
:SkipLine                                                                              
echo ProcessId = %ProcessId%
taskkill /F /PID %ProcessId% 
#timeout /t 15
