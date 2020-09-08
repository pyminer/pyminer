@echo off
rem 两个变量拼接，等号前后一定不要有空格
rem pymminer_road：pyminer.bat 文件路径，默认 pyminer.bat 和 app.py 同一个路径
set pyminer_road=%~dp0
set app=app.py
set pyminer_path=%pyminer_road%%app%
python %pyminer_path%