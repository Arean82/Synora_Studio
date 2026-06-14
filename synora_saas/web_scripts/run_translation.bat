@echo off
set PYBABEL=C:\Users\user\AppData\Roaming\Python\Python312\Scripts\pybabel.exe

:: Move up to the web directory
cd %~dp0\..

echo Extracting translations...
%PYBABEL% extract -F babel.cfg -o messages.pot .

set /p LANG_CODE="Enter a new language code to add (e.g., 'es' for Spanish) or press Enter to skip: "
if not "%LANG_CODE%"=="" (
    echo Initializing %LANG_CODE%...
    %PYBABEL% init -i messages.pot -d locales -l %LANG_CODE%
)

echo Running auto-translator...
:: Move up to the root directory to run the translator
cd ..
python web\web_scripts\translator.py %LANG_CODE%

:: Move back to the web directory
cd web

echo Compiling translations...
%PYBABEL% compile -d locales

cd ..
echo Done!
pause
