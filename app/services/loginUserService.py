from app.config.dbConnect import makeConnection, commitValues, closeConnection
from app.models import RegisterRequest
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import json

def loginUserService(payload):
    data = json.loads(payload)
    email = data.get('email')
    password = data.get('password')
    print(email, password)

    connection_result = makeConnection()
    if connection_result is None:
        raise Exception("Database connection failed")
    
    conn, cursor = connection_result

    try:
        cursor.execute("SELECT password, user_id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        print(user)
        if user is None:
            return { "error": "User Not Found", "status": 404 }
        if user[0] != password:
            return { "error": "Incorrect Password", "status": 403 }
        return user[1]
    except Exception as e:
        raise e 
    finally:
        closeConnection(conn, cursor)