@echo off
echo Cleaning up unrequested translation files...

:: Move to the project root
cd %~dp0\..\..

echo Removing locale directories...
if exist "web\locales\de" rmdir /s /q "web\locales\de"
if exist "web\locales\es" rmdir /s /q "web\locales\es"
if exist "web\locales\fr" rmdir /s /q "web\locales\fr"

echo Removing translated README files...
if exist "README_de.md" del /q "README_de.md"
if exist "README_es.md" del /q "README_es.md"
if exist "README_fr.md" del /q "README_fr.md"

echo Removing old helper scripts from web root...
if exist "web\run_translation.bat" del /q "web\run_translation.bat"
if exist "web\cleanup_locales.bat" del /q "web\cleanup_locales.bat"

echo Cleanup complete.
pause
