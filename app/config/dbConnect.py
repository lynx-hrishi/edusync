from mysql.connector import connect
import os
from dotenv import load_dotenv
from pathlib import Path

# Locate .env file relative to project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def makeConnection():
    try:
        # print(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))
        conn = connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=3306
        )
        cursor = conn.cursor()
        # cursor.execute("SET time_zone = '+05:30'")
        # print("Connection established")
        return [conn, cursor]
    except Exception as e:
        # print(e)
        return None

def commitValues(conn):
    conn.commit()

def closeConnection(conn, cursor=None):
    if cursor:
        cursor.close()
    conn.close()