@echo off
title Dashboard Financiero UNCP - Finanzas I
echo ============================================================
echo   INICIANDO DASHBOARD INTERACTIVO FINANCIERO - UNCP
echo   Tema: Punto de Equilibrio y Sensibilidad Turistica
echo ============================================================
echo.
echo Abriendo servidor web local en http://127.0.0.1:5000 ...
start http://127.0.0.1:5000
"C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe" dashboard_app.py
pause
