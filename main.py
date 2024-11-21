from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from api.models import models, schemas
from api.controllers import orders
from api.dependencies.database import engine, get_db
from api.controllers import sandwiches

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/orders/", response_model=schemas.Order, tags=["Orders"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return orders.create(db=db, order=order)


@app.get("/orders/", response_model=list[schemas.Order], tags=["Orders"])
def read_orders(db: Session = Depends(get_db)):
    return orders.read_all(db)


@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def read_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return order


@app.put("/orders/{order_id}", response_model=schemas.Order, tags=["Orders"])
def update_one_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order_db = orders.read_one(db, order_id=order_id)
    if order_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.update(db=db, order=order, order_id=order_id)


@app.delete("/orders/{order_id}", tags=["Orders"])
def delete_one_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.read_one(db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="User not found")
    return orders.delete(db=db, order_id=order_id)

@app.post("/sandwiches/", tags=["Sandwiches"])
def create_sandwich(sandwich: schemas.Sandwich, db: Session = Depends(get_db)):
    return sandwiches.create(db, sandwich)

@app.get("/sandwiches/", tags=["Sandwiches"])
def get_all_sandwiches(db: Session = Depends(get_db)):
    return sandwiches.read_all(db)

@app.get("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def get_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return sandwiches.read_one(db, sandwich_id)

@app.put("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def update_sandwich(sandwich_id: int, sandwich: schemas.Sandwich, db: Session = Depends(get_db)):
    return sandwiches.update(db, sandwich_id, sandwich)

@app.delete("/sandwiches/{sandwich_id}", tags=["Sandwiches"])
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return sandwiches.delete(db, sandwich_id)