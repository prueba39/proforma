import models
from sqlalchemy.orm import Session

def guardar_factura_con_datos(db: Session, datos: dict):
    existente = db.query(models.Factura).filter_by(numero=datos["numero"]).first()
    if existente:
        raise ValueError("Factura ya registrada")

    cliente_info = datos["cliente"]
    cliente = models.Cliente(
        nombre=cliente_info.get("nombre", "Desconocido"),
        direccion=cliente_info.get("direccion", ""),
        telefono=cliente_info.get("telefono", ""),
        ciudad=cliente_info.get("ciudad", "")
    )
    db.add(cliente)
    db.flush()

    factura = models.Factura(
        numero=datos["numero"],
        fecha=datos["fecha"],
        forma_pago=datos["forma_pago"],
        subtotal=datos["subtotal"],
        iva=datos["iva"],
        total=datos["total"],
        cliente_id=cliente.id
    )
    db.add(factura)
    db.flush()

    for item in datos["productos"]:
        item_obj = models.ItemFactura(
            cantidad=item["cantidad"],
            descripcion=item["descripcion"],
            precio_unitario=item["precio_unitario"],
            total_linea=item["total_linea"],
            factura_id=factura.id
        )
        db.add(item_obj)

    db.commit()

def listar_facturas(db: Session):
    return db.query(models.Factura).all()