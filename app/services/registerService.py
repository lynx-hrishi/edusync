from app.config.dbConnect import makeConnection, commitValues, closeConnection
from app.models import RegisterRequest

def registerUserService(request: RegisterRequest):
    connection_result = makeConnection()
    if connection_result is None:
        raise Exception("Database connection failed")
    
    conn, cursor = connection_result
    
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (request.email,))
        if cursor.fetchone():
            raise Exception("User already exists")
        
        cursor.execute("INSERT INTO users (username, age, email, password) VALUES (%s, %s, %s, %s)", 
                      (request.name, request.age, request.email, request.password))
        commitValues(conn)
        return True
    except Exception as e:
        raise e
    finally:
        closeConnection(conn)