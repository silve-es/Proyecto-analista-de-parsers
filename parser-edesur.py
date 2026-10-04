import re
import json
import pdfplumber

def extraer_texto_pdf(ruta_pdf):
    texto_completo = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    return texto_completo

def parsear_factura_edesur(ruta_pdf):
    texto = extraer_texto_pdf(ruta_pdf)
    
    # Expresión regular para capturar el CUIT
    cuit_pattern = r'30[\s-]*\d{8}[\s-]*\d'
    
    # Expresión regular para capturar la fecha de emisión
    fecha_pattern = r'(?:Capital Federal|CABA).*?(\d{2}/\d{2}/\d{4})'
    
    # Expresión regular para capturar el importe total 
    total_pattern = r'(?i)TOTAL[:\s]*[\$\|\s]*([\d\.,]+)'

    cuit = re.search(cuit_pattern, texto)
    fecha = re.search(fecha_pattern, texto)
    total = re.search(total_pattern, texto)

    datos_factura = {
        "proveedor": "Edesur",
        "cuit_emisor": cuit.group(0) if cuit else None,
        "fecha_emision": fecha.group(1) if fecha else None,
        "total_a_pagar": total.group(1) if total else None
    }
    
    return datos_factura

if __name__ == "__main__":
    ruta_pdf = "samples/Factura-Edesur.pdf"
    
    print(f"Procesando el archivo: {ruta_pdf}...")
    resultado = parsear_factura_edesur(ruta_pdf)
    
    print("\n--- JSON OBTENIDO ---")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))