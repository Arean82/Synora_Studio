@echo off
echo Organizing saas_docs into 'en' folder...

cd %~dp0\..\saas_docs

mkdir en

move *.md en\

echo Documents moved to saas_docs\en
pause
