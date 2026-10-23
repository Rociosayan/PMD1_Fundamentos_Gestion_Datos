# -*- coding: utf-8 -*-
"""
Reemplaza nombres genericos/numerados por nombres realistas (ficticios) en:
  (A) PMD1_15_Casos_Sinteticos/01..15_*_PMD1.xlsx  -> Clientes.nombre_cliente, Catalogo.nombre_item, Sedes.nombre_sede
  (B) casos/01..16/*.db (SQLite)                    -> columna <entidad>_nombre del local en la tabla *_original

Reglas:
  - Solo cambia texto de nombres. IDs, filas, numeros, fechas y nulos quedan iguales.
  - Errores intencionales se conservan: si el nombre viejo tenia espacios extra, MAYUSCULAS,
    minusculas o MaYuScUlAs alternadas, el nombre nuevo recibe el mismo tipo de error.
  - Correspondencia estable: el mismo numero/ID siempre recibe el mismo nombre nuevo.
  - Es idempotente: si un valor ya no es generico, no se toca.
  - No consume ninguna semilla aleatoria: las asignaciones son deterministas.

Uso (desde la raiz del repo):
  python PMD1_15_Casos_Sinteticos/renombrar_nombres_reales.py            # simulacion: muestra cambios
  python PMD1_15_Casos_Sinteticos/renombrar_nombres_reales.py --aplicar  # escribe los archivos
Haga un backup antes de usar --aplicar.
"""
import glob, os, re, sqlite3, sys
import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- errores intencionales
def _alterna(s):
    return "".join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(s))

def aplicar_error(viejo, canonico, nuevo):
    """Copia al nombre nuevo el tipo de error que tenia el nombre viejo respecto a su forma canonica."""
    m = re.match(r"^(\s*)(.*?)(\s*)$", viejo, re.S)
    izq, nucleo, der = m.group(1), m.group(2), m.group(3)
    if "  " in nucleo:                      # doble espacio interno
        nuevo = nuevo.replace(" ", "  ", 1)
        nucleo = re.sub(r" +", " ", nucleo)
    if nucleo == canonico:
        pass
    elif nucleo == canonico.lower():
        nuevo = nuevo.lower()
    elif nucleo == canonico.upper():
        nuevo = nuevo.upper()
    elif nucleo == _alterna(canonico):
        nuevo = _alterna(nuevo)
    elif nucleo.lower() == canonico.lower():
        nuevo = _alterna(nuevo)
    return izq + nuevo + der

# ---------------------------------------------------------------- personas
NOMBRES = ["Ana", "Luis", "María", "Jorge", "Rosa", "Carlos", "Lucía", "Miguel", "Carmen", "José",
           "Patricia", "Diego", "Milagros", "Renzo", "Gabriela", "Hugo", "Fiorella", "César", "Paola",
           "Iván", "Sofía", "Martín", "Elena", "Raúl", "Valeria", "Andrés", "Claudia", "Víctor", "Diana", "Óscar"]
APELLIDOS = ["Quispe", "Flores", "Huamán", "Rojas", "Mendoza", "Vargas", "Castillo", "Torres", "Chávez",
             "Ramírez", "Gutiérrez", "Salazar", "Paredes", "Ccori", "Espinoza", "Delgado", "Aguilar",
             "Cárdenas", "Valdivia", "Mamani", "Condori", "Poma", "Ríos", "Navarro", "Soto", "Cruz", "Campos",
             "Reyes", "Gómez", "Benites"]

def nombres_personas(n, desfase):
    out = []
    j = desfase
    while len(out) < n:
        if j > desfase + 100000: raise RuntimeError('lista de nombres insuficiente')
        a1, a2 = APELLIDOS[(j * 7 + j // 30) % 30], APELLIDOS[(j * 11 + 3 + 2 * (j // 30)) % 30]
        c = f"{NOMBRES[j % 30]} {a1} {a2}"
        if a1 != a2 and c not in out:
            out.append(c)
        j += 1
    return out

# ---------------------------------------------------------------- distritos por zona (Lima)
DISTRITOS = {
    "Norte": ["Los Olivos", "Comas", "Independencia", "Puente Piedra", "San Martín de Porres"],
    "Centro": ["Cercado de Lima", "Jesús María", "Lince", "Breña", "San Isidro"],
    "Sur": ["Surco", "Chorrillos", "San Juan de Miraflores", "Villa El Salvador", "Barranco"],
    "Este": ["La Molina", "Ate", "San Juan de Lurigancho", "Santa Anita", "El Agustino"],
    "Oeste": ["San Miguel", "Callao", "Magdalena del Mar", "Pueblo Libre", "Bellavista"],
}
AVENIDAS = ["Av. Universitaria", "Av. Túpac Amaru", "Av. Javier Prado", "Av. Angamos", "Av. Brasil",
            "Av. La Marina", "Av. Arequipa", "Av. Grau"]

# ---------------------------------------------------------------- (A) Excel 01-15
CASOS_XLSX = {
 "01": ("Rapidito Delivery", {
   "pizza": ["Pizza americana familiar", "Pizza hawaiana mediana", "Pizza pepperoni familiar", "Pizza margarita personal",
             "Pizza vegetariana mediana", "Pizza suprema familiar", "Pizza cuatro quesos", "Pizza de jamón y champiñones"],
   "pollo": ["Pollo a la brasa 1/4", "Pollo a la brasa 1/2", "Pollo a la brasa entero", "Alitas BBQ", "Pollo broaster",
             "Mostrito", "Salchipollo", "Pollo a la parrilla"],
   "ensalada": ["Ensalada César", "Ensalada de quinua", "Ensalada Waldorf", "Ensalada fresca de la casa", "Ensalada caprese",
                "Ensalada de pollo", "Ensalada griega", "Ensalada rusa"],
   "sushi": ["Maki acevichado", "Maki furai", "Tabla de sushi", "Nigiri de salmón", "Maki tropical", "Temaki de langostino",
             "Sashimi mixto", "Maki parrillero"],
   "hamburguesa": ["Hamburguesa clásica", "Hamburguesa royal", "Hamburguesa a lo pobre", "Hamburguesa doble queso",
                   "Hamburguesa de pollo", "Hamburguesa BBQ", "Hamburguesa vegetariana", "Hamburguesa con tocino"]}),
 "02": ("El Fogón Criollo", {
   "parrilla": ["Parrilla familiar", "Anticuchos de corazón", "Bife angosto", "Chuleta de cerdo a la parrilla",
                "Pollo a la parrilla", "Churrasco", "Parrillada mixta", "Choripán"],
   "sopa": ["Sopa criolla", "Chupe de camarones", "Aguadito de pollo", "Caldo de gallina", "Sopa de quinua",
            "Parihuela", "Sustancia de carne", "Sopa a la minuta"],
   "menu": ["Menú ejecutivo", "Menú económico", "Menú criollo", "Menú vegetariano", "Menú infantil", "Menú del día",
            "Menú marino", "Menú dieta"],
   "pasta": ["Tallarines verdes con bistec", "Tallarín saltado", "Fetuccini a la huancaína", "Lasaña de carne",
             "Spaghetti a la bolognesa", "Ravioles de ricota", "Tallarines rojos", "Canelones"],
   "postre": ["Suspiro a la limeña", "Mazamorra morada", "Arroz con leche", "Picarones", "Crema volteada",
              "Tres leches", "Alfajores", "Torta de chocolate"]}),
 "03": ("Boticas Vida Sana", {
   "termometro": ["Termómetro digital", "Termómetro infrarrojo", "Termómetro de oído", "Termómetro clínico flexible",
                  "Termómetro digital pediátrico", "Termómetro de frente sin contacto", "Termómetro basal", "Termómetro de vidrio"],
   "analgesico": ["Paracetamol 500 mg x 100", "Ibuprofeno 400 mg x 20", "Naproxeno 550 mg x 10", "Diclofenaco gel 50 g",
                  "Metamizol 500 mg x 10", "Aspirina 100 mg x 30", "Ketorolaco 10 mg x 10", "Paracetamol jarabe 120 ml"],
   "vitamina": ["Vitamina C 1 g efervescente", "Complejo B x 30", "Vitamina D3 x 60", "Multivitamínico x 30",
                "Sulfato ferroso jarabe", "Omega 3 x 60", "Vitamina E 400 UI", "Zinc + Vitamina C"],
   "crema": ["Bloqueador solar FPS 50", "Crema hidratante corporal", "Crema antipañalitis", "Crema cicatrizante",
             "Crema para quemaduras", "Gel de aloe vera", "Crema antimicótica", "Vaselina pura"],
   "suero": ["Suero oral 500 ml", "Suero oral sabor fresa", "Suero fisiológico 1 L", "Sales de rehidratación",
             "Suero oral pediátrico", "Solución salina 250 ml", "Bebida rehidratante", "Suero glucosado"]}),
 "04": ("Hotel Inti Plaza", {
   "familiar": ["Habitación familiar estándar", "Habitación familiar superior", "Familiar con vista a la ciudad",
                "Familiar con dos camas queen", "Familiar con kitchenette", "Familiar triple", "Familiar cuádruple", "Familiar deluxe"],
   "suite": ["Suite junior", "Suite presidencial", "Suite con jacuzzi", "Suite nupcial", "Suite master", "Suite panorámica",
             "Suite ejecutiva", "Suite familiar"],
   "simple": ["Habitación simple estándar", "Simple con baño privado", "Simple superior", "Simple económica",
              "Simple con escritorio", "Simple interior", "Simple con balcón", "Simple deluxe"],
   "ejecutiva": ["Ejecutiva king", "Ejecutiva con sala de trabajo", "Ejecutiva queen", "Ejecutiva piso club",
                 "Ejecutiva superior", "Ejecutiva doble", "Ejecutiva vista parque", "Ejecutiva deluxe"],
   "doble": ["Habitación doble matrimonial", "Doble twin", "Doble superior", "Doble con balcón", "Doble económica",
             "Doble deluxe", "Doble interior", "Doble vista a la ciudad"]}),
 "05": ("AgroAndes", {
   "quinua": ["Quinua blanca Salcedo INIA", "Quinua roja Pasankalla", "Quinua negra Collana", "Quinua orgánica Junín",
              "Quinua perlada", "Quinua Hualhuas", "Quinua Kancolla", "Quinua tricolor"],
   "cebada": ["Cebada cervecera", "Cebada forrajera", "Cebada perlada", "Cebada UNA La Molina 95",
              "Cebada Centenario", "Cebada grano entero", "Cebada para malta", "Cebada orgánica"],
   "hortaliza": ["Cebolla roja arequipeña", "Tomate italiano", "Zanahoria", "Lechuga americana", "Brócoli",
                 "Zapallo macre", "Pimiento morrón", "Espinaca"],
   "papa": ["Papa amarilla", "Papa Yungay", "Papa huayro", "Papa canchán", "Papa única", "Papa perricholi",
            "Papa nativa", "Papa blanca"],
   "maiz": ["Maíz amarillo duro", "Maíz morado", "Maíz blanco gigante del Cusco", "Maíz choclo", "Maíz chulpe",
            "Maíz cancha", "Maíz forrajero", "Maíz amiláceo"]}),
 "06": ("Energía Hogar", {
   "oficina": ["Oficina administrativa pequeña", "Oficina corporativa", "Oficina con centro de datos", "Coworking",
               "Oficina de atención al público", "Consultorio profesional", "Estudio contable", "Oficina en edificio"],
   "mixto": ["Vivienda con bodega", "Vivienda con taller", "Vivienda con consultorio", "Vivienda con oficina",
             "Vivienda con local comercial", "Vivienda con cuartos en alquiler", "Vivienda con lavandería", "Vivienda con cabina"],
   "taller": ["Taller de carpintería", "Taller de soldadura", "Taller mecánico", "Taller de costura",
              "Taller de tornería", "Taller de serigrafía", "Taller de panadería", "Taller de cerrajería"],
   "comercial": ["Bodega de barrio", "Restaurante", "Minimarket", "Ferretería", "Farmacia de barrio",
                 "Peluquería", "Lavandería", "Librería"],
   "residencial": ["Departamento familiar", "Casa unifamiliar", "Dúplex", "Departamento pequeño", "Casa de campo",
                   "Vivienda multifamiliar", "Minidepartamento", "Casa de playa"]}),
 "07": ("AutoTec Servicios", {
   "suspension": ["Cambio de amortiguadores", "Cambio de rótulas", "Alineamiento y balanceo", "Cambio de terminales de dirección",
                  "Cambio de muelles", "Cambio de bujes", "Revisión de suspensión", "Cambio de barra estabilizadora"],
   "electrico": ["Cambio de batería", "Revisión del alternador", "Reparación de motor de arranque", "Cambio de faros",
                 "Diagnóstico con escáner", "Reparación de alarma", "Instalación de radio", "Cambio de fusibles"],
   "motor": ["Afinamiento de motor", "Cambio de aceite y filtro", "Cambio de faja de distribución", "Reparación de culata",
             "Limpieza de inyectores", "Cambio de bomba de agua", "Overhaul de motor", "Cambio de bujías"],
   "frenos": ["Cambio de pastillas de freno", "Rectificado de discos", "Cambio de líquido de frenos", "Cambio de zapatas",
              "Revisión de frenos ABS", "Cambio de bomba de freno", "Regulación de freno de mano", "Cambio de discos"],
   "transmision": ["Cambio de embrague", "Mantenimiento de caja automática", "Cambio de aceite de caja", "Cambio de palieres",
                   "Reparación de caja mecánica", "Cambio de crucetas", "Cambio de volante de motor", "Revisión de diferencial"]}),
 "08": ("Ferretería El Constructor", {
   "pintura": ["Pintura látex blanco 4 L", "Pintura esmalte sintético 1 gl", "Pintura anticorrosiva", "Pintura para techos",
               "Barniz marino", "Pintura epóxica", "Sellador para paredes", "Pintura en spray"],
   "herramienta": ["Taladro percutor", "Juego de destornilladores", "Martillo de uña", "Wincha de 5 m", "Amoladora angular",
                   "Llave Stilson", "Alicate universal", "Serrucho"],
   "ceramico": ["Cerámico para piso 45x45", "Porcelanato 60x60", "Cerámico para pared", "Mayólica blanca",
                "Pegamento para cerámico", "Fragua", "Cerámico antideslizante", "Zócalo cerámico"],
   "cemento": ["Cemento Portland tipo I 42.5 kg", "Cemento Sol", "Cemento Andino", "Cemento extraforte",
               "Cemento puzolánico", "Mortero listo", "Cemento blanco", "Concreto premezclado en bolsa"]}),
 "09": ("Clínica San Gabriel", {
   "terapia": ["Terapia física", "Terapia de lenguaje", "Terapia respiratoria", "Rehabilitación de rodilla",
               "Terapia ocupacional", "Electroterapia", "Terapia de columna", "Hidroterapia"],
   "control": ["Control prenatal", "Control de niño sano", "Control de presión arterial", "Control de diabetes",
               "Control post operatorio", "Control nutricional", "Control de tiroides", "Control de colesterol"],
   "consulta": ["Consulta de medicina general", "Consulta pediátrica", "Consulta ginecológica", "Consulta cardiológica",
                "Consulta dermatológica", "Consulta traumatológica", "Consulta oftalmológica", "Consulta dental"],
   "imagen": ["Radiografía de tórax", "Ecografía abdominal", "Tomografía", "Resonancia magnética",
              "Mamografía", "Ecografía obstétrica", "Densitometría ósea", "Radiografía de columna"],
   "analisis": ["Hemograma completo", "Perfil lipídico", "Glucosa en ayunas", "Examen de orina",
                "Perfil hepático", "Prueba de COVID-19", "Hemoglobina glicosilada", "Perfil tiroideo"]}),
 "10": ("LogiExpress Perú", {
   "repuesto": ["Repuestos automotrices", "Filtros de aceite", "Neumáticos", "Baterías de auto",
                "Pastillas de freno", "Repuestos de moto", "Kit de embrague", "Lubricantes"],
   "equipo": ["Laptop", "Refrigeradora", "Televisor 55 pulgadas", "Lavadora", "Aire acondicionado",
              "Equipo de sonido", "Impresora multifuncional", "Cocina a gas"],
   "mueble": ["Ropero de melamina", "Juego de comedor", "Sofá de tres cuerpos", "Escritorio de oficina",
              "Cama de dos plazas", "Estante", "Silla ergonómica", "Mesa de centro"],
   "paquete": ["Sobre de documentos", "Caja pequeña", "Caja mediana", "Caja grande",
               "Paquete de e-commerce", "Encomienda familiar", "Valija empresarial", "Paquete frágil"],
   "insumo": ["Insumos médicos", "Material de oficina", "Insumos de limpieza", "Insumos agrícolas",
              "Material de embalaje", "Insumos de panadería", "Útiles escolares", "Insumos de laboratorio"]}),
 "11": ("Moda Urbana", {
   "pantalon": ["Jean skinny", "Pantalón chino", "Jean clásico", "Pantalón de vestir", "Jogger",
                "Pantalón cargo", "Jean mom", "Pantalón de buzo"],
   "accesorio": ["Gorra", "Correa de cuero", "Mochila urbana", "Billetera", "Lentes de sol", "Bufanda de alpaca",
                 "Medias pack x 3", "Reloj deportivo"],
   "zapatilla": ["Zapatillas urbanas blancas", "Zapatillas running", "Zapatillas de lona", "Zapatillas de skate",
                 "Zapatillas para training", "Zapatillas casuales", "Zapatillas de básquet", "Zapatillas de trekking"],
   "polo": ["Polo básico de algodón pima", "Polo estampado", "Polo cuello V", "Polo manga larga",
            "Polo oversize", "Polo deportivo", "Polo piqué", "Polo de bebé"],
   "casaca": ["Casaca de jean", "Casaca impermeable", "Casaca de cuero", "Casaca polar",
              "Casaca acolchada", "Casaca bomber", "Casaca cortavientos", "Casaca de alpaca"]}),
 "12": ("Veterinaria Huellitas", {
   "cirugia": ["Esterilización de gata", "Castración de perro", "Cirugía de tejidos blandos", "Extracción dental",
               "Cirugía de fractura", "Retiro de tumor", "Cesárea canina", "Cirugía ocular"],
   "consulta": ["Consulta general", "Consulta dermatológica", "Consulta de emergencia", "Consulta a domicilio",
                "Consulta de control", "Consulta de felinos", "Consulta de exóticos", "Consulta geriátrica"],
   "vacuna": ["Vacuna antirrábica", "Vacuna séxtuple", "Vacuna triple felina", "Vacuna contra la tos de las perreras",
              "Vacuna óctuple", "Vacuna contra leptospirosis", "Vacuna leucemia felina", "Refuerzo anual"],
   "bano": ["Baño medicado", "Baño y corte", "Baño antipulgas", "Corte de uñas", "Baño para gatos",
            "Baño con deslanado", "Spa canino", "Baño básico"],
   "desparasitacion": ["Desparasitación interna", "Desparasitación externa", "Pipeta antipulgas", "Collar antiparasitario",
                       "Desparasitación de cachorro", "Tableta antiparasitaria", "Desparasitación felina", "Desparasitación trimestral"]}),
 "13": ("Planta Industrial Andina", {
   "calibracion": ["Calibración de balanza", "Calibración de termocupla", "Calibración de manómetro", "Calibración de sensor de nivel",
                   "Ajuste de dosificadora", "Calibración de caudalímetro", "Calibración de selladora", "Calibración de detector de metales"],
   "limpieza": ["Limpieza CIP de tanques", "Limpieza de faja transportadora", "Sanitización de línea", "Limpieza de moldes",
                "Limpieza de filtros", "Limpieza de tolva", "Limpieza de horno", "Limpieza de envasadora"],
   "electrica": ["Falla de motor eléctrico", "Corte de energía", "Falla de variador de frecuencia", "Cortocircuito en tablero",
                 "Falla de sensor", "Falla de PLC", "Sobrecarga de motor", "Falla de contactor"],
   "falta_insumo": ["Falta de materia prima", "Falta de envases", "Falta de etiquetas", "Falta de cajas de embalaje",
                    "Retraso de proveedor", "Falta de tapas", "Falta de film stretch", "Falta de aditivos"],
   "mecanica": ["Rotura de faja", "Desgaste de rodamientos", "Falla de cadena transmisora", "Fuga hidráulica",
                "Atasco de producto", "Falla de compresor", "Rotura de engranaje", "Desalineamiento de ejes"]}),
 "14": ("Academia Saber Más", {
   "ingles": ["Inglés básico", "Inglés intermedio", "Inglés avanzado", "Inglés para niños", "Conversación en inglés",
              "Preparación TOEFL", "Inglés de negocios", "Inglés para adolescentes"],
   "programacion": ["Python desde cero", "Desarrollo web con HTML y CSS", "JavaScript", "Base de datos SQL",
                    "Análisis de datos con Python", "Excel avanzado", "Desarrollo de apps móviles", "Power BI"],
   "ciencias": ["Física preuniversitaria", "Química", "Biología", "Ciencia y tecnología escolar",
                "Física para ingenieros", "Química orgánica", "Anatomía", "Ecología"],
   "comunicacion": ["Redacción y ortografía", "Comprensión lectora", "Oratoria", "Razonamiento verbal",
                    "Redacción académica", "Literatura", "Comunicación efectiva", "Técnicas de estudio"],
   "matematica": ["Razonamiento matemático", "Álgebra", "Geometría", "Trigonometría", "Aritmética",
                  "Cálculo I", "Estadística", "Matemática financiera"]}),
 "15": ("Soporte TI Integral", {
   "impresora": ["Atasco de papel en impresora", "Instalación de impresora en red", "Cambio de tóner", "Impresora no imprime",
                 "Configuración de escáner", "Mantenimiento de impresora", "Error de cola de impresión", "Instalación de driver de impresora"],
   "hardware": ["Cambio de disco SSD", "Laptop no enciende", "Ampliación de memoria RAM", "Cambio de teclado",
                "Falla de monitor", "Mantenimiento preventivo de PC", "Cambio de fuente de poder", "Falla de batería de laptop"],
   "red": ["Sin conexión a internet", "Wi-Fi lento", "Configuración de VPN", "Cableado de punto de red",
           "Falla de switch", "Configuración de router", "Acceso a carpeta compartida", "Corte de red en piso"],
   "acceso": ["Restablecer contraseña", "Desbloqueo de cuenta", "Alta de usuario nuevo", "Permisos de carpeta",
              "Acceso a sistema ERP", "Baja de usuario", "Configuración de doble factor", "Acceso a correo"],
   "software": ["Instalación de Office", "Actualización de Windows", "Error en sistema contable", "Instalación de antivirus",
                "Licencia vencida", "Configuración de Outlook", "Migración de archivos", "Instalación de software especializado"]}),
}
TIPO_SEDE_XLSX = {"13": "Planta", "15": "Oficina"}  # en estos casos la "sede" ya tenia otro nombre base

def renombrar_excel(path, caso, aplicar):
    marca, catalogo = CASOS_XLSX[caso]
    wb = openpyxl.load_workbook(path)
    cambios = []

    def columna(ws, nombre):
        cab = [c.value for c in ws[1]]
        return cab.index(nombre) + 1, cab

    # Clientes
    ws = wb["Clientes"]
    ci, cab = columna(ws, "nombre_cliente")
    filas = list(range(2, ws.max_row + 1))
    personas = nombres_personas(len(filas), int(caso) * 13)
    for k, r in enumerate(filas):
        v = ws.cell(r, ci).value
        if isinstance(v, str) and re.fullmatch(r"\s*Cliente\s+\d+\s*", v, re.I):
            n = int(re.search(r"\d+", v).group())
            nuevo = aplicar_error(v, f"Cliente {n}", personas[n - 1])
            cambios.append(("Clientes.nombre_cliente", v, nuevo)); ws.cell(r, ci).value = nuevo
    # Catalogo
    ws = wb["Catalogo"]
    ci, cab = columna(ws, "nombre_item")
    usados = {}
    for r in range(2, ws.max_row + 1):
        v = ws.cell(r, ci).value
        m = re.fullmatch(r"\s*([a-z_]+)\s+(\d+)\s*", v or "", re.I)
        if m and m.group(1).lower() in catalogo:
            t = m.group(1).lower(); k = usados.get(t, 0); usados[t] = k + 1
            nuevo = aplicar_error(v, f"{m.group(1)} {m.group(2)}", catalogo[t][k])
            cambios.append(("Catalogo.nombre_item", v, nuevo)); ws.cell(r, ci).value = nuevo
    # Sedes
    ws = wb["Sedes"]
    ci, cab = columna(ws, "nombre_sede"); zi = cab.index("zona") + 1
    usados = {}
    base = TIPO_SEDE_XLSX.get(caso, marca)
    for r in range(2, ws.max_row + 1):
        v = ws.cell(r, ci).value
        if isinstance(v, str) and re.fullmatch(r"\s*[A-Za-z ]+?\s(sede\s)?\d+\s*", v):
            z = str(ws.cell(r, zi).value or "Centro").strip().title()
            lista = DISTRITOS.get(z, DISTRITOS["Centro"]); k = usados.get(z, 0); usados[z] = k + 1
            canon = re.sub(r"\s+", " ", v.strip())
            nuevo = aplicar_error(v, canon, f"{base} {lista[k]}")
            cambios.append(("Sedes.nombre_sede", v, nuevo)); ws.cell(r, ci).value = nuevo
    if aplicar and cambios:
        wb.save(path)
    return cambios

# ---------------------------------------------------------------- (B) SQLite casos/01-16
MARCAS_DB = {
    "01": ("RetailMax", "Sucursal"), "02": ("Sabor Limeño", "Local"), "03": ("Farmacia Bienestar", "Sucursal"),
    "04": ("Ferretería Don Pepe", "Tienda"), "05": ("Clínica Santa Rosa", "Sede"), "06": ("Vet Patitas", "Sede"),
    "07": ("Hotel Costa Verde", "Hotel"), "08": ("Reparto", "Zona"), "09": ("LogiExpress", "Sede"),
    "10": ("Fundo", "Zona"), "11": ("Sector", "Distrito"), "12": ("FitPerú", "Sede"),
    "13": ("Panadería El Trigal", "Local"), "14": ("Taller AutoFix", "Sede"),
    "16": ("Abarrotes Esperanza", "Abarrotes Esperanza"),
}
# 15 (industria) no se toca: sus "nombres" son turnos (Manana/Tarde/Noche) y codigos de maquina reales.

def _distrito_limpio(s):
    if s is None: return None
    s = re.sub(r"\s+", " ", str(s)).strip()
    s = " ".join(p if p in ("de", "del") and i else p.capitalize() for i, p in enumerate(s.lower().split()))
    return "Cercado de Lima" if s == "Lima" else s

def renombrar_db(path, caso, aplicar):
    marca, palabra = MARCAS_DB[caso]
    con = sqlite3.connect(path)
    cambios = []
    tablas = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
    for t in tablas:
        cols = [r[1] for r in con.execute(f'pragma table_info("{t}")')]
        for c in [c for c in cols if c.endswith("_nombre")]:
            pref = c[:-len("_nombre")]
            dcol = pref + "_distrito" if pref + "_distrito" in cols else None
            patron = re.compile(r"^\s*" + re.escape(palabra).replace(r"\ ", r"\s+") + r"\s+(\d+)\s*$", re.I)
            valores = [r[0] for r in con.execute(f'select distinct "{c}" from "{t}" where "{c}" is not null')]
            gen = [v for v in valores if patron.match(v)]
            if not gen: continue
            # distrito mayoritario por numero de local
            por_num = {}
            for v in gen:
                n = int(patron.match(v).group(1))
                if dcol:
                    for d, k in con.execute(f'select "{dcol}", count(*) from "{t}" where "{c}"=? group by 1', (v,)):
                        if d is not None and str(d).strip():
                            por_num.setdefault(n, {}).setdefault(_distrito_limpio(d), 0)
                            por_num[n][_distrito_limpio(d)] += k
                por_num.setdefault(n, {})
            base_nombre, vistos, av = {}, {}, 0
            for n in sorted(por_num):
                d = max(por_num[n], key=por_num[n].get) if por_num[n] else None
                if d is None:
                    nombre = f"{marca} {AVENIDAS[av % len(AVENIDAS)]}"; av += 1
                else:
                    nombre = f"{marca} {d}"
                    if nombre in vistos.values():
                        nombre = f"{marca} {d} - {AVENIDAS[av % len(AVENIDAS)]}"; av += 1
                vistos[n] = nombre
            for v in gen:
                n = int(patron.match(v).group(1))
                canon = f"{palabra} {n}"
                nuevo = aplicar_error(v, canon, vistos[n])
                cambios.append((f"{t}.{c}", v, nuevo))
                if aplicar:
                    con.execute(f'update "{t}" set "{c}"=? where "{c}"=?', (nuevo, v))
    if aplicar:
        con.commit()
    con.close()
    # copia CSV de la misma tabla (casos/<caso>/csv/<tabla>.csv), si existe
    mapa = {}
    for col, v, nuevo in cambios:
        mapa.setdefault(col, {})[v] = nuevo
    for colkey, m in mapa.items():
        t, c = colkey.split(".")
        csvp = os.path.join(os.path.dirname(path), "csv", t + ".csv")
        if os.path.exists(csvp):
            n = renombrar_csv(csvp, c, m, aplicar)
            cambios.append((f"csv/{t}.csv.{c}", f"{n} celdas", "actualizadas" if aplicar else "por actualizar"))
    return cambios

def renombrar_csv(csvp, columna, mapa, aplicar):
    """Reemplaza valores de una columna en un CSV conservando codificacion, BOM y saltos de linea."""
    import csv, io
    crudo = open(csvp, "rb").read()
    bom = crudo.startswith(b"\xef\xbb\xbf")
    texto = crudo.decode("utf-8-sig")
    eol = "\r\n" if "\r\n" in texto else "\n"
    filas = list(csv.reader(io.StringIO(texto, newline="")))
    i = filas[0].index(columna); n = 0
    for f in filas[1:]:
        if len(f) > i and f[i] in mapa:
            f[i] = mapa[f[i]]; n += 1
    if aplicar and n:
        out = io.StringIO()
        csv.writer(out, lineterminator=eol).writerows(filas)
        data = out.getvalue()
        if not texto.endswith(("\n", "\r")):
            data = data[: -len(eol)]
        open(csvp, "wb").write((b"\xef\xbb\xbf" if bom else b"") + data.encode("utf-8"))
    return n

def main():
    aplicar = "--aplicar" in sys.argv
    print("MODO:", "APLICAR" if aplicar else "SIMULACION (use --aplicar para escribir)")
    for f in sorted(glob.glob(os.path.join(RAIZ, "PMD1_15_Casos_Sinteticos", "*_PMD1.xlsx"))):
        caso = os.path.basename(f)[:2]
        if caso in CASOS_XLSX:
            ch = renombrar_excel(f, caso, aplicar)
            print(f"\n[{os.path.basename(f)}] {len(ch)} cambios")
            for x in ch[:3] + [y for y in ch if y[0].startswith("Catalogo")][:2] + [y for y in ch if y[0].startswith("Sedes")][:2]:
                print(f"   {x[0]}: {x[1]!r} -> {x[2]!r}")
    for f in sorted(glob.glob(os.path.join(RAIZ, "casos", "*", "*.db"))):
        caso = os.path.basename(os.path.dirname(f))[:2]
        if caso in MARCAS_DB:
            ch = renombrar_db(f, caso, aplicar)
            print(f"\n[{os.path.relpath(f, RAIZ)}] {len(ch)} valores distintos cambiados")
            for x in ch:
                print(f"   {x[0]}: {x[1]!r} -> {x[2]!r}")

if __name__ == "__main__":
    main()
