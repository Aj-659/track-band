from sqlalchemy import Table, MetaData, Column, String
from sqlalchemy.exc import ProgrammingError
from database import engine
from sqlalchemy import update as sql_update, delete as sql_delete

from sqlalchemy import Table, MetaData, Column, String
from database import engine

def get_dynamic_table(username: str):
    table_name = username.strip().lower().replace(" ", "_")
    metadata = MetaData()

    # Define the table structure
    user_table = Table(
        table_name,
        metadata,
        Column("Date", String(50)),
        Column("Latitude", String(50)),
        Column("Longitude", String(50)),
        Column("Amplitude", String(50)),
        extend_existing=True
    )

    # ✅ THIS LINE ACTUALLY CREATES THE TABLE IN MYSQL
    metadata.create_all(engine, checkfirst=True)

    return user_table

'''def create_user_data_table(username: str):
    table_name = username.strip().lower().replace(" ", "_")
    metadata = MetaData(bind=engine)
    user_table = Table(
        table_name,
        metadata,
        Column("Date", String(14), nullable=False),
        Column("Latitude", String(50), nullable=False),
        Column("Longitude", String(50), nullable=False),
        Column("Amplitude", String(50), nullable=False),
        extend_existing=True
    )
    user_table.create(checkfirst=True)'''

from sqlalchemy import Table, MetaData, Column, String, insert
from sqlalchemy.exc import SQLAlchemyError
from database import engine
from model2 import get_dynamic_table

def insert_data(username: str, data: dict):
    table = get_dynamic_table(username)
    try:
        # Ensure table exists
        table.create(bind=engine, checkfirst=True)

        # Use transaction with commit
        with engine.begin() as conn:
            conn.execute(insert(table).values(**data))

        return {"status": "success", "message": f"Data inserted into {username}"}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e)}


'''def insert_data(username: str, data: dict):
    table = get_dynamic_table(username)
    try:
        table.create(bind=engine, checkfirst=True)
        conn = engine.connect()
        conn.execute(table.insert().values(**data))
        conn.close()
        return {"status": "success", "message": f"Data inserted into {username}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}'''
def update_data(username: str, date: str, data: dict):
    table = get_dynamic_table(username)
    try:
        stmt = sql_update(table).where(table.c.Date == date).values(**data)

        # ✅ Transactional context — ensures auto commit
        with engine.begin() as conn:
            result = conn.execute(stmt)

        if result.rowcount == 0:
            return {"status": "error", "message": "Row not found"}
        return {"status": "success", "message": f"Row updated in {username}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


'''def update_data(username: str, date: str, data: dict):
    table = get_dynamic_table(username)
    try:
        conn = engine.connect()
        stmt = sql_update(table).where(table.c.Date == date).values(**data)
        result = conn.execute(stmt)
        conn.close()
        if result.rowcount == 0:
            return {"status": "error", "message": "Row not found"}
        return {"status": "success", "message": f"Row updated in {username}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}'''

'''def delete_data(username: str, date: str):
    table = get_dynamic_table(username)
    try:
        conn = engine.connect()
        stmt = sql_delete(table).where(table.c.Date == date)
        result = conn.execute(stmt)
        conn.close()
        if result.rowcount == 0:
            return {"status": "error", "message": "Row not found"}
        return {"status": "success", "message": f"Row deleted from {username}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}'''


def delete_data(username: str, date: str):
    table = get_dynamic_table(username)
    try:
        stmt = sql_delete(table).where(table.c.Date == date)
        with engine.begin() as conn:
            result = conn.execute(stmt)

        if result.rowcount == 0:
            return {"status": "error", "message": "Row not found"}
        return {"status": "success", "message": f"Row deleted from {username}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


'''def delete_data(username: str, date: str):
    table = get_dynamic_table(username)
    try:
        stmt = sql_delete(table).where(table.c.Date == date)
        with engine.begin() as conn:
            result = conn.execute(stmt)

        if result.rowcount == 0:
            return {"status": "error", "message": "Row not found"}
        return {"status": "success", "message": f"Row deleted from {username}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
'''
    
#print("Database operations completed successfully.")    
