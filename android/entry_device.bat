@echo off
setlocal EnableDelayedExpansion 
set curr=%~dp0

goto check_android
goto exit

:check_android
set devSN=none
set cnt=0
echo ��ѡAndroid�豸�б�:
for /f "eol=L tokens=1 delims=device" %%i in ('adb devices') do (
	set /a cnt+=1
	set devices[!cnt!]=%%i
	echo ѡ�� !cnt!: %%i
)
if %cnt% equ 0 (
	echo ��Android�豸
	goto exit
) else if %cnt% equ 1 (
	set devSN=!devices[1]!
	echo ʹ���豸: !devSN!
	goto wantdo
) else (
	goto choice
)
:choice
set /p input=��ѡ���豸���:
if "!devices[%input%]!" == "" (
	echo �޴�ѡ�!input!��
	goto exit
) else (
	set devSN=!devices[%input%]!
	echo ��ѡ�����豸: !devSN!
	goto wantdo
)

:wantdo
adb -s !devSN! shell

:exit
pause
exit