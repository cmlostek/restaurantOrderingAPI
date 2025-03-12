@echo off
echo Upgrading pip...
pip install --upgrade pip

echo Installing dependencies...
pip install fastapi
pip install "uvicorn[standard]"
pip install sqlalchemy
pip install pymysql
pip install pytest
pip install pytest-mock
pip install httpx
pip install cryptography

echo Installation complete!
pause
