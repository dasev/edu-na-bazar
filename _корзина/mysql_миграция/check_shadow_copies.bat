@echo off
echo Проверка теневых копий для C:\python\sites_mysql...
echo.

vssadmin list shadows /for=C:

echo.
echo Если есть теневые копии, можно восстановить файлы.
pause
