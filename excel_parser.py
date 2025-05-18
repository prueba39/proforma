import pandas as pd
from io import BytesIO
from datetime import datetime

def parse_excel(content: bytes):
    excel_file = pd.ExcelFile(BytesIO(content))
    df = excel_file.parse(excel_file.sheet_names[0])
    df = df.dropna(how='all').reset_index(drop=True)

    cliente_nombre = None
    for row in df.values:
        for cell in row:
            if isinstance(cell, str) and "SIGN SUPPLY" in cell:
                cliente_nombre = cell.strip()
                break
        if cliente_nombre:
            break

    if not cliente_nombre:
        raise ValueError("No se encontró el nombre del cliente")

    cliente = {
        "nombre": cliente_nombre,
        "direccion": "Desconocida",
        "telefono": "",
        "ciudad": ""
    }

    productos = []
    start_idx = None
    for idx, row in df.iterrows():
        if isinstance(row[3], str) and "MAQUINAS OFERTADA" in row[3]:
            start_idx = idx + 1
            break

    if start_idx is None:
        raise ValueError("No se encontró la tabla de productos")

    for idx in range(start_idx, len(df)):
        row = df.iloc[idx]
        if pd.isna(row[0]):
            break
        try:
            cantidad = int(row[0])
            descripcion = str(row[1])
            precio_unitario = float(row[2])
            total_linea = float(row[3])
            productos.append({
                "cantidad": cantidad,
                "descripcion": descripcion,
                "precio_unitario": precio_unitario,
                "total_linea": total_linea
            })
        except Exception:
            continue

    if not productos:
        raise ValueError("No se extrajeron productos válidos")

    subtotal = iva = total = 0.0
    for row in df.values:
        str_row = [str(c).lower() for c in row]
        if "subtotal" in str_row:
            subtotal = float(row[-1])
        if "iva" in str_row:
            iva = float(row[-1])
        if "total" in str_row:
            total = float(row[-1])

    if total == 0.0:
        total = sum(p["total_linea"] for p in productos)

    numero = f"FACT-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    return {
        "numero": numero,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "forma_pago": "Contado",
        "cliente": cliente,
        "productos": productos,
        "subtotal": subtotal,
        "iva": iva,
        "total": total
    }