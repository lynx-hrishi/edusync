from app.config.dbConnect import makeConnection, commitValues, closeConnection
from app.models import RegisterRequest
from fastapi import Request
import json

def loginUserService(request: Request, payload):
    data = json.loads(payload)
    email = data.get('email')
    password = data.get('password')

    connection_result = makeConnection()
    if connection_result is None:
        raise Exception("Database connection failed")
    
    conn, cursor = connection_result

    try:
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user is None:
            raise Exception("User not found")
        if user[0] != password:
            raise Exception("Incorrect password")
        request.session["email"] = email
        request.session['user_id'] = user[0]
        return True
    except Exception as e:
        raise e 
    finally:
        closeConnection(conn)