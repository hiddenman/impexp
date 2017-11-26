@echo off
rem batch file to build win32 version
echo Bulding....
python setup.py py2exe -c -O2 -i
encodings.ascii,encodings.cp1251,encodings.koi8_r,encodings.cp866,anygui,threading,misc,netIO -p anygui -e cfg



