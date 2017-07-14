rmdir /s /q dist 
mkdir dist
cd dist
mkdir %1
cd %1
echo >PnFModsLoader.py
mkdir PnFMods
xcopy ..\..\mxMeter PnFMods\mxMeter /i /e
cd ..
"C:\Program Files\7-Zip\7z.exe" a -r C:\src\owncloud\mxMeter\mxmeter-%1-%2.zip %1
