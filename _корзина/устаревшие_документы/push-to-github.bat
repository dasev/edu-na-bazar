@echo off
echo ========================================
echo PUSH TO GITHUB
echo ========================================
echo.

set /p USERNAME="Введите ваш GitHub username: "

echo.
echo Подключаем к GitHub...
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/%USERNAME%/edu-na-bazar.git

echo.
echo Отправляем на GitHub...
"C:\Program Files\Git\bin\git.exe" push -u origin main

echo.
echo ========================================
echo ГОТОВО!
echo ========================================
echo.
echo Ваш репозиторий: https://github.com/%USERNAME%/edu-na-bazar
echo.
pause
