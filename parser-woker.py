import re
import json
import pdfplumber

def extraer_texto_pdf(pdf_path):
    texto_completo = ""
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n"
    return texto_completo

def parsear_factura(texto):
    # Expresión regular para capturar el CUIT
    cuit_pattern = r'\b(20|23|24|27|30|33|34)[-\s]?\d{8}[-\s]?\d\b'
    
    # Expresión regular para capturar la fecha de emision
    fecha_pattern = r'\b(?:(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/](20\d{2})|(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01]))\b'
    
    # # Expresión regular para capturar el total a pagar
    total_pattern = r'(?i)\bTOTAL\b\s*(?:\|\s*)?[\$\s]*([\d\.,]+)'

    cuit = re.search(cuit_pattern, texto)
    fecha = re.search(fecha_pattern, texto)
    total = re.search(total_pattern, texto)

    importe_str = total.group(1) if total else None

    datos_factura = {
        "cuit_emisor": cuit.group(0) if cuit else None,
        "fecha_emision": fecha.group(0) if fecha else None,
        "total_a_pagar": importe_str if importe_str else None
    }
    
    return datos_factura
# Ejemplo de uso:
# texto_factura = extraer_texto_pdf("factura_ejemplo.pdf")
# resultado_json = json.dumps(parsear_factura(texto_factura), indent=4, ensure_ascii=False)
# print(resultado_json)

if __name__ == "__main__":
    # Apuntamos a una de tus facturas reales dentro de la carpeta samples
    ruta_pdf = "samples/Factura-Woker.pdf" 
    
    print(f"Procesando el archivo: {ruta_pdf}...")
    texto_extraido = extraer_texto_pdf(ruta_pdf)
    resultado = parsear_factura(texto_extraido)
    
    # Mostramos el JSON resultante de forma limpia en la consola
    print("\n--- JSON OBTENIDO ---")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))