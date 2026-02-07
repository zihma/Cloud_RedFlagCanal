@echo off
:: 1. 激活你的 Anaconda 环境 (根据你截图里的路径)
call D:\Anaconda\Scripts\activate.bat

:: 2. 切换到你的项目所在的 D 盘
D:

:: 3. 进入项目文件夹
cd D:\Cloud_RedFlagCanal

:: 4. 启动网站！
streamlit run main.py

:: 5. 防止出错闪退，留个暂停
pause