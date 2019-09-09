@echo off

SET FLASK_APP=%CD%\webapp\

SET DATABASE_URL=sqlite:///%CD%\data\sqlite\database.sqlite