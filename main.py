from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from dbconfig import session, engine
import dbmodel
from sqlalchemy.orm import Session


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)

dbmodel.Base.metadata.create_all(bind=engine)

def get_db():
   db = session()
   try:
      yield db
   finally:
      db.close()

products = [
    Product(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Product(id=2, name="Smartphone", description="A latest model smartphone", price=699.99, quantity=25),
]


@app.get("/")
def home():
    return "Heyy!! Welcome"

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
   db_products = db.query(dbmodel.Product).all()
   return db_products

@app.get("/products/{id}")
def get_product(id: int, db: Session = Depends(get_db)):
   db_product = db.query(dbmodel.Product).filter(dbmodel.Product.id == id).one()
   if db_product:
      return db_product
   return "no product"
   

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
   db.add(dbmodel.Product(**product.model_dump()))
   db.commit()
   return "added successfully"

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
   db_product = db.query(dbmodel.Product).filter(dbmodel.Product.id==id).first()
   if db_product:
      db_product.name = product.name
      db_product.description = product.description
      db_product.price = product.price
      db_product.quantity = product.quantity
      db.commit()
      return "updated successfully"
   return "no product"

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
   db_product = db.query(dbmodel.Product).filter(dbmodel.Product.id==id).first()
   if db_product:
      db.delete(db_product)
      db.commit()
      return "deleted successfully"
   return "no product"
