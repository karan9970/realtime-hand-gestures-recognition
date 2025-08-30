
@echo off
REM Simple FFmpeg screen recorder for Windows. Edit the input device as needed.
REM Requires ffmpeg in PATH.
set DURATION=15
set OUT=demo\demo.mp4
echo Recording %DURATION%s to %OUT% ...
REM This example uses gdigrab (Windows screen). Adjust as needed.
ffmpeg -y -f gdigrab -framerate 30 -i desktop -t %DURATION% %OUT%
echo Done.
