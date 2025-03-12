#!/bin/bash
# Run this script to install all the dependencies for the project on your local machine
function pipeline {
      pip install --upgrade pip # Upgrade pip before installing dependencies

      pip install fastapi
      pip install "uvicorn[standard]"
      pip install sqlalchemy
      pip install pymysql
      pip install pytest
      pip install pytest-mock
      pip install httpx
      pip install cryptography
}

pipeline