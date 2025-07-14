from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from model1 import User
from model2 import get_dynamic_table, insert_data, update_data, delete_data
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy import Table, MetaData, select
from datetime import datetime

def convert_date_to_db_format(date_str: str) -> str:
    """
    Converts '08/07/2025 12:45:00' → '08072025124500'
    """
    return datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S").strftime("%d%m%Y%H%M%S")



Base.metadata.create_all(bind=engine)

app = FastAPI()

'''now for user database'''

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class UserSchema(BaseModel):
    Imei_no: int
    Username: str
    class Config:
        orm_mode = True
class UserCreateSchema(UserSchema):
    Password: str
    class Config:
        orm_mode = True


#for login functionality

class LoginRequest(BaseModel):
    Imei_no: int
    Username: str
    Password: str

@app.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.Imei_no == request.Imei_no,
        User.Username == request.Username,
        User.Password == request.Password
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username, password, or IMEI")

    return {
        "message": "Login successful",
        "Username": user.Username,
        "Imei_no": user.Imei_no
    }


@app.get("/user_cr", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.post("/user_cr", response_model=UserCreateSchema)
def post_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = User(
        Imei_no=user.Imei_no,
        Username=user.Username,
        Password=user.Password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"Creating table for user: {user.Username}")
    get_dynamic_table(user.Username)

    #get_dynamic_table(user.Username)
    return db_user

@app.put("/user_cr/{user_id}", response_model=UserCreateSchema)
def update_user(user_id: int, user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    
    db_user.Imei_no = user.Imei_no
    db_user.Username = user.Username
    db_user.Password = user.Password
    db.commit()
    return db_user

@app.delete("/user_cr/{user_id}", response_class=JSONResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    
    db.delete(db_user)
    db.commit()
    return JSONResponse(status_code=204, content={"message": "User of user id {user_id} is deleted successfully"})

'''now for location databse'''

class SensorData(BaseModel):
    Date: str         
    Latitude: str
    Longitude: str
    Amplitude: str



@app.post("/{username}")
def insert_user_data(username: str, info: SensorData):
    result = insert_data(username, info.dict())
    if result["status"] == "error":
        return JSONResponse(status_code=400, content={"message": result["message"]})
    return {"message": result["message"]}


@app.put("/{username}")
def update_user_data(username: str, old_date: str, info: SensorData):
    try:
        info_dict = info.dict()
        result = update_data(username, old_date, info_dict)

        if result["status"] == "error":
            return JSONResponse(status_code=404, content={"message": result["message"]})
        return {"message": result["message"]}

    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Invalid request: {str(e)}"})



'''@app.put("/{username}")
def update_user_data(username: str, old_date: str, info: SensorData):
    try:
        from datetime import datetime

        def convert_date_to_db_format(d: str) -> str:
            return datetime.strptime(d, "%d/%m/%Y %H:%M:%S").strftime("%d%m%Y%H%M%S")

        old_date_db = convert_date_to_db_format(old_date)
        new_date_db = convert_date_to_db_format(info.Date)

        info_dict = info.dict()
        info_dict["Date"] = new_date_db

        result = update_data(username, old_date_db, info_dict)

        if result["status"] == "error":
            return JSONResponse(status_code=404, content={"message": result["message"]})

        return {"message": result["message"]}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Invalid request: {str(e)}"})
'''

'''@app.put("/{username}/{human_date}")
def update_user_data(username: str, human_date: str, info: SensorData):
    try:
        date = convert_date_to_db_format(human_date)
    except:
        return JSONResponse(status_code=400, content={"message": "Invalid date format. Use dd/mm/yyyy hh:mm:ss"})

    # Also convert body "Date" field
    info_dict = info.dict()
    try:
        info_dict["Date"] = convert_date_to_db_format(info_dict["Date"])
    except:
        return JSONResponse(status_code=400, content={"message": "Invalid body Date format. Use dd/mm/yyyy hh:mm:ss"})

    result = update_data(username, date, info_dict)

    if result["status"] == "error":
        return JSONResponse(status_code=404, content={"message": result["message"]})
    return {"message": result["message"]}
'''

'''@app.put("/{username}/{date}")
def update_user_data(username: str, date: str, info: SensorData):
    result = update_data(username, date, info.dict())
    if result["status"] == "error":
        return JSONResponse(status_code=404, content={"message": result["message"]})
    return {"message": result["message"]}
'''

@app.delete("/{username}")
def delete_user_data(username: str, date: str):
    try:
        result = delete_data(username, date)
        if result["status"] == "error":
            return JSONResponse(status_code=404, content={"message": result["message"]})
        return {"message": result["message"]}
    except Exception as e:
        return JSONResponse(status_code=400, content={"message": f"Invalid request: {str(e)}"})

'''@app.delete("/{username}/{date}")
def delete_user_data(username: str, date: str):
    result = delete_data(username, date)
    if result["status"] == "error":
        return JSONResponse(status_code=404, content={"message": result["message"]})
    return {"message": result["message"]}
'''
'''now for getting all data of a user'''

def format_db_date(date_str: str, is_start: bool = True):
    prefix = "000000" if is_start else "235959"
    return datetime.strptime(date_str, "%d/%m/%Y").strftime(f"%d%m%Y{prefix}")

@app.get("/{username}/filter-by-date")
def get_user_data_by_date(username: str, start: str, end: str):
    table_name = username.strip().lower().replace(" ", "_")
    metadata = MetaData(bind=engine)

    try:
        user_table = Table(table_name, metadata, autoload_with=engine)
    except Exception:
        return JSONResponse(status_code=404, content={"message": f"Table '{table_name}' not found"})

    # Format the start and end dates
    try:
        start_db = format_db_date(start, is_start=True)
        end_db = format_db_date(end, is_start=False)
    except Exception:
        return JSONResponse(status_code=400, content={"message": "Invalid date format. Use dd/mm/yyyy"})

    stmt = select(user_table).where(user_table.c.Date.between(start_db, end_db))

    with engine.connect() as conn:
        rows = conn.execute(stmt).fetchall()

    if not rows:
        return {"message": f"No data found for '{username}' between {start} and {end}"}

    # Format results
    result = []
    for row in rows:
        formatted_date = datetime.strptime(row["Date"], "%d%m%Y%H%M%S").strftime("%d/%m/%Y %H:%M:%S")
        result.append({
            "Date": formatted_date,
            "Latitude": row["Latitude"],
            "Longitude": row["Longitude"],
            "Amplitude": row["Amplitude"]
        })

    return result


