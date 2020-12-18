@echo off
setlocal EnableDelayedExpansion 
set curr=%~dp0

goto check_android

:wantdo
adb -s !devSN! shell

:check_android
set devSN=none
set cnt=0
echo 可选Android设备列表:
for /f "eol=L tokens=1 delims=device" %%i in ('adb devices') do (
	set /a cnt+=1
	set devices[!cnt!]=%%i
	echo 选项 !cnt!: %%i
)
if %cnt% equ 0 (
	echo 无Android设备
	goto exit
) else if %cnt% equ 1 (
	set devSN=!devices[1]!
	echo 使用设备: !devSN!
	goto wantdo
) else (
	goto choice
)
:choice
set /p input=请选择设备序号:
if "!devices[%input%]!" == "" (
	echo 无此选项【!input!】	
) else (
	set devSN=!devices[%input%]!
	echo 您选择了设备: !devSN!
	goto wantdo
)
:exit
pause
exit

pause