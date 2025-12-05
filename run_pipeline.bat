@echo off
REM Run the Cricket AI pipeline with proper Python path

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Add src directory to PYTHONPATH
set PYTHONPATH=%SCRIPT_DIR%src;%PYTHONPATH%

REM Run the pipeline
python "%SCRIPT_DIR%src\pipeline\realtime_pipeline.py" %*
