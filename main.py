# dispatch to controllers

from fastapi           import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm    import Session

from database    import SessionLocal
from models      import auth_user, pet, client, foster
from controllers import auth as AuthController, pets as PetController
from controllers import clients as ClientController, foster as FosterController
from utils       import jwt as JWT


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

#
@app.middleware("http")
async def log_req_details(request: Request, call_next):
    print("\n Request Details")
    print("METHOD = ", request.method)
    print("HEADERS = ", request.headers)
    response = await call_next(request)
    return response

#
@app.middleware("http")
async def jwt_verification(request: Request, call_next):
    print("\n Token Verification")
    auth_header = request.headers.get("authorization")
    print("AUTH HEADER = ", auth_header)
    print("PATH = ", request['path'])

    if not request['path'].startswith("/auth/") and not request['path'] == "/":
        if auth_header is None:
            return JSONResponse(status_code = 401, content = {"Detail" : "Unauthorized"})
        auth_header_parts = auth_header.split()
        if not (len(auth_header_parts) == 2 and auth_header_parts[0] == "Bearer"):
            return JSONResponse(status_code = 401, content = {"Detail" : "Unauthorized"})
        if auth_header_parts[1] is None:
            return JSONResponse(status_code = 401, content = {"Detail" : "Unauthorized"})
        if JWT.is_token_valid(auth_header_parts[1]) is False:
            return JSONResponse(status_code = 401, content = {"Detail" : "Unauthorized"})

    response = await call_next(request)
    return response

# Health Check
@app.get("/")
def read_root():
    return {"OK"}

### USERS ###
# Register an User
@app.post("/auth/register", response_model = auth_user.AuthUserDTO)
def register(register_input: auth_user.RegisterInputDTO, db: Session = Depends(get_db)):
    return AuthController.register(register_input, db)

# Login as an User
@app.post("/auth/login", response_model = auth_user.LoginResponseDTO)
def login(login_input: auth_user.RegisterInputDTO, db: Session = Depends(get_db)):
    return AuthController.login(login_input, db)

# Get an User
@app.get("/users/{user_id}", response_model = auth_user.AuthUserDTO)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return AuthController.get_user(user_id, db)

# Get all Users
@app.get("/users", response_model = list[auth_user.AuthUserDTO])
def get_users(limit: int = 10, db: Session = Depends(get_db)):
    return AuthController.get_users(limit_users = limit, db = db)

# Patch an User
@app.patch("/users/{user_id}", response_model = auth_user.AuthUserDTO)
def update_user(user_id: int, update_input: dict[str, object], db: Session = Depends(get_db)):
    return AuthController.update_user(user_id, update_input, db)

# Delete an User
@app.delete("/users/{user_id}", response_model = str)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return AuthController.delete_user(user_id, db)

### PETS ###
# Create a Pet
@app.post("/pets", response_model = pet.PetDTO)
def create_pet(create_input: pet.BasePetDTO, db: Session = Depends(get_db)):
    return PetController.create_pet(create_input, db)

# Get a Pet
@app.get("/pets/{pet_id}", response_model = pet.PetDTO)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    return PetController.get_pet(pet_id, db)

# Get all Pets
@app.get("/pets", response_model = list[pet.PetDTO])
def get_pets(request: Request, limit: int = 10, db: Session = Depends(get_db)):
    return PetController.get_pets(request, limit_pets = limit, db = db)

# Patch a Pet
@app.patch("/pets/{pet_id}", response_model = pet.PetDTO)
def update_pet(pet_id: int, update_input: dict[str, object], db: Session = Depends(get_db)):
    return PetController.update_pet(pet_id, update_input, db)

# Delete a Pet
@app.delete("/pets/{pet_id}", response_model = str)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    return PetController.delete_pet(pet_id, db)

### CLIENTS ###
# Create a Client
@app.post("/clients", response_model = client.ClientDTO)
def create_client(create_input: client.CreateClientDTO, db: Session = Depends(get_db)):
    return ClientController.create_client(create_input, db)

# Get a Client
@app.get("/clients/{client_id}", response_model = client.ClientDTO)
def get_client(client_id: int, db: Session = Depends(get_db)):
    return ClientController.get_client(client_id, db)

# Get all Clients
@app.get("/clients", response_model = list[client.ClientDTO])
def get_clients(limit: int = 10, db: Session = Depends(get_db)):
    return ClientController.get_clients(limit_clients = limit, db = db)

# Patch a Client
@app.patch("/clients/{client_id}", response_model = client.ClientDTO)
def update_client(client_id: int, update_input: dict[str, object], db: Session = Depends(get_db)):
    return ClientController.update_client(client_id, update_input, db)

# Delete a Client
@app.delete("/clients/{client_id}", response_model = str)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    return ClientController.delete_client(client_id, db)

### FOSTER ###
# Create a Foster
@app.post("/foster", response_model = foster.FosterDTO)
def create_foster(create_input: foster.CreateFosterDTO, db: Session = Depends(get_db)):
    return FosterController.create_foster(create_input, db)

# Get a Foster
@app.get("/foster/{foster_id}", response_model = foster.FosterDTO)
def get_foster(foster_id: int, db: Session = Depends(get_db)):
    return FosterController.get_foster(foster_id, db)

# Get all Fosters
@app.get("/foster", response_model = list[foster.FosterDTO])
def get_all_foster(limit: int = 10, db: Session = Depends(get_db)):
    return FosterController.get_all_foster(limit_foster = limit, db = db)

# Patch a Foster
@app.patch("/foster/{foster_id}", response_model = foster.FosterDTO)
def update_foster(foster_id: int, update_input: dict[str, object], db: Session = Depends(get_db)):
    return FosterController.update_foster(foster_id, update_input, db)

# Delete a Foster
@app.delete("/foster/{foster_id}", response_model = str)
def delete_foster(foster_id: int, db: Session = Depends(get_db)):
    return FosterController.delete_foster(foster_id, db)
