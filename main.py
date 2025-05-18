from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import crud, models
from excel_parser import parse_excel

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload/")
async def upload_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        data = parse_excel(contents)
        crud.guardar_factura_con_datos(db, data)
        return {"mensaje": "Factura guardada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/facturas/")
def listar_facturas(db: Session = Depends(get_db)):
    return crud.listar_facturas(db)