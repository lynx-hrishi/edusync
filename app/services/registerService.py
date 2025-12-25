from app.config.dbConnect import makeConnection, commitValues, closeConnection
from app.models import RegisterRequest
import json
from fastapi import Request

def registerUserService(payload):
    data = json.loads(payload)
    name = data.get('name')
    age = data.get('age')
    email = data.get('email')
    password = data.get('password')
    # print(name, age, email, password)

    connection_result = makeConnection()
    if connection_result is None:
        raise Exception("Database connection failed")
    
    conn, cursor = connection_result
    
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            raise Exception("User already exists")
        
        cursor.execute("INSERT INTO users (username, age, email, password) VALUES (%s, %s, %s, %s)", 
                      (name, age, email, password))
        commitValues(conn)
        return True
    except Exception as e:
        raise e
    finally:
        closeConnection(conn)

def saveUserPreferenceService(request: Request, payload):
    data = json.loads(payload)
    goals = data.get('goals')
    preferences = data.get('preferences')
    experience = data.get('experience')

    # print(goals, preferences, experience)
    connection_result = makeConnection()
    if connection_result is None:
        raise Exception("Database connection failed")

    conn, cursor = connection_result

    try:
        cursor.execute("INSERT INTO user_preference (preference_id, goals, preference, experience) VALUES (%s, %s, %s, %s)",
                      (request.session.get('user_id'), goals, preferences, experience))
        commitValues(conn)
        return True
    except Exception as e:
        raise e
    finally:
        closeConnection(conn)