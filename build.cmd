SETLOCAL ENABLEDELAYEDEXPANSION

SET GAME_FOLDER=
SET INI=build.ini
set area=[Game]
set key=folder
set currarea=
for /f "usebackq delims=" %%a in ("!INI!") do (
    set ln=%%a
    if "x!ln:~0,1!"=="x[" (
        set currarea=!ln!
    ) else (
        for /f "tokens=1,2 delims==" %%b in ("!ln!") do (
            set currkey=%%b
            set currval=%%c
            if "x!area!"=="x!currarea!" if "x!key!"=="x!currkey!" (
                set GAME_FOLDER=%%c
            )
        )
    )
)
echo %GAME_FOLDER%

set DESTINATION=
set area=[Destination]
set key=folder
set currarea=
for /f "usebackq delims=" %%a in ("!INI!") do (
    set ln=%%a
    if "x!ln:~0,1!"=="x[" (
        set currarea=!ln!
    ) else (
        for /f "tokens=1,2 delims==" %%b in ("!ln!") do (
            set currkey=%%b
            set currval=%%c
            if "x!area!"=="x!currarea!" if "x!key!"=="x!currkey!" (
                set DESTINATION=%%c
            )
        )
    )
)
echo %DESTINATION%

SET REV=
for /f "tokens=*" %%i in ('git rev-list --count --first-parent HEAD') do (
  set /a REV=%%i+100
)
echo %REV%

set VERS=nover
for /f "tokens=1-5 delims=>." %%i in ('call xpath.bat "%GAME_FOLDER%\game_info.xml" "//version[@name='client']/@installed"') do (
  set VERS=%%i.%%j.%%k.%%l
)
echo %VERS%

rmdir /s /q dist 
mkdir dist
cd dist

copy /y nul PnFModsLoader.py
mkdir PnFMods
xcopy ..\mxMeter PnFMods\mxMeter /i /e

"C:\Program Files\7-Zip\7z.exe" a -r %DESTINATION%\mxmeter-%VERS%-%REV%.zip PnFMods PnFModsLoader.py
