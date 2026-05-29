from fastapi import FastAPI

app = FastAPI()

def register_user(username: str, password: str, email: str, phone: int) -> bool:
    # Placeholder for actual registration logic
    if username and password:
        print(f"Registered user {username} successfully")
        return True
    elif username == "":
        print(f"Username can't be empty: {username}")
    elif password == "":
        print(f"Password can't be empty: {password}")
    elif email == "":
        print(f"Email can't be empty: {email}")
    elif phone == "":
        print(f"Phone number can't be empty: {phone}")
    else:
        print("Invalid Credentials!")
    return False

def authenticate_user(username: str, password: str) -> bool:
    # Placeholder for actual authentication logic
    if username == "user" and username != "" and password == "pass" and password != "":
        return True
    elif username == "":
        print(f"Username can't be empty: {username}")
    elif password == "":
        print(f"Password can't be empty: {password}")
        return False
    else:
        print(f"Invalid credentials for user: {username}")
        return False
    
def login(username: str, password: str):
    if authenticate_user(username, password):
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid credentials"}, 401
    
