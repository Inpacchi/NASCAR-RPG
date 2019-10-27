@echo off

SET FLASK_APP=%CD%\webapp\

REM SQLite Database Connector
REM SET DATABASE_URL=sqlite:///%CD%\data\sqlite\database.sqlite

REM PostggreSQL Database Connector
SET DATABASE_URL=postgresql://USERNAME:PASSWORD@SERVER_IP/DATABASE_NAME