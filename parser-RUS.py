import re
import json
import pdfplumber

def extraer_texto_pdf(ruta_pdf):
    texto_completo = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    return texto_completo

def parsear_orden_pago_rus(ruta_pdf):
    texto = extraer_texto_pdf(ruta_pdf)
    
    # 1. Proveedor fijo o detectado
    proveedor = "Río Uruguay Seguros"
    
    # 2. Expresión regular para capturar el CUIT
    cuit_pattern = r'CUIT\s*(30-?\d{8}-?\d|30\d{9})'
    cuit_match = re.search(cuit_pattern, texto)
    cuit_emisor = None
    if cuit_match:
        raw_cuit = cuit_match.group(1)
        # Opcional: formatear con guiones si viene sin ellos
        if '-' not in raw_cuit and len(raw_cuit) == 11:
            cuit_emisor = f"{raw_cuit[:2]}-{raw_cuit[2:10]}-{raw_cuit[10:]}"
        else:
            cuit_emisor = raw_cuit

    # 3. Expresión regular para la fecha de emision
    fecha_pattern = r'Fecha\s*(\d{2}/\d{2}/\d{4})'
    fecha_match = re.search(fecha_pattern, texto)
    fecha_emision = fecha_match.group(1) if fecha_match else None

    # 4. Expresión regular para capturar el total a pagar
    total_pattern = r'Total\s+a\s+Pagar[:\s]*\|\s*([\d,\.]+)'
    total_match = re.search(total_pattern, texto, re.IGNORECASE)
    
    # Si no lo encuentra con el pipe, alternativa genérica por la etiqueta
    if not total_match:
        total_pattern_alt = r'Total\s+a\s+Pagar[:\s]*([\d,\.]+)'
        total_match = re.search(total_pattern_alt, texto, re.IGNORECASE)

    # Extrae el valor numérico encontrado o asigna None si fallaron ambos intentos
    total_a_pagar = total_match.group(1) if total_match else None

    # Estructura del JSON resultante
    resultado = {
        "proveedor": proveedor,
        "cuit_emisor": cuit_emisor,
        "fecha_emision": fecha_emision,
        "total_a_pagar": total_a_pagar
    }
    
    return resultado

if __name__ == "__main__":
    archivo_muestra = "samples/OrdendePago-RUS.pdf"
    print(f"Procesando el archivo: {archivo_muestra}...")
    datos = parsear_orden_pago_rus(archivo_muestra)
    print("\n--- JSON OBTENIDO ---")
    print(json.dumps(datos, indent=4, ensure_ascii=False))