@echo off
:: 🎯 强制让 Zim 把配置、缓存和状态全部写在 U 盘当前目录下的 .config 和 .cache 文件夹里
set XDG_CONFIG_HOME=%~dp0.config
set XDG_DATA_HOME=%~dp0.data
set XDG_CACHE_HOME=%~dp0.cache

:: 🇨🇳 强制注入中文语言环境变量（加这两行！）
set LANG=zh_CN.UTF-8
set LANGUAGE=zh_CN:zh

:: 🚀 启动 U 盘本地的 Zim
start "" "%~dp0zim.exe"

