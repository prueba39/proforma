from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    ciudad = Column(String)

    facturas = relationship("Factura", back_populates="cliente")

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True)
    fecha = Column(String)
    forma_pago = Column(String)
    subtotal = Column(Float)
    iva = Column(Float)
    total = Column(Float)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="facturas")
    items = relationship("ItemFactura", back_populates="factura")

class ItemFactura(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer)
    descripcion = Column(String)
    precio_unitario = Column(Float)
    total_linea = Column(Float)
    factura_id = Column(Integer, ForeignKey("facturas.id"))

    factura = relationship("Factura", back_populates="items")