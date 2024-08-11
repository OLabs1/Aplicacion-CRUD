from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color
from datetime import datetime

class PiePagina(canvas.Canvas):

    def __init__(self, *args, **kwargs):  # Los argumentos *args y **kwargs permite que la clase FooterCanvas acepte cualquier numero de argumentos
        # que normalmente pasaria a la clase base canvas.Canvas.
        canvas.Canvas.__init__(self, *args, **kwargs)   # Constructor de clase, inicilia la clase FooterCanvas
        self.pages = []                 # Establece una lista para almacenar la informacion de cada pagina
        self.width, self.height = A4   # Establece el tamaño de la pagina

    def showPage(self):
        self.pages.append(dict(self.__dict__))  # Agrega informacion de la pagina actual a lista self.pages
        self._startPage()

    def save(self):         # Guardar el documento PDF, antes de cada pagina expeto la primera.
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if (self._pageNumber > 0):
                self.dibujar_Canva(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def dibujar_Canva(self, page_count):  # Dibuja un pie de pagina con información como numero de pagina, lineas e imagenes
        # Configura las lineas.
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        self.drawImage("imagenes\logo_kalpe_1.png", self.width-inch*8-5, self.height-50, width=150, height=30, preserveAspectRatio=True)
        # Para insertar la fecha.
        fecha_actual = datetime.now().strftime("%d-%m-%Y")
        texto_fecha = "Fecha: %s" % fecha_actual
        self.setFont('Courier-Bold', 14)
        self.setFillColorRGB(0, 0, 1)
        self.drawString(self.width-inch*2.5-5, self.height-40, texto_fecha)

        # Pie de pagina
        self.setFillColorRGB(0, 0, 0)
        self.line(30, 780, A4[0] - 20, 780)
        self.line(66, 78, A4[0] - 66, 78)
        self.setFont('Times-Roman', 10)
        self.drawString(A4[0]-x, 65, page)
        self.restoreState()

class PDFPSReporte:

    def __init__(self, path, data, encabezado, criterio_1, criterio_2):   # Constructor de la clase. Inicializa la instancia de la clase
        self.path = path
        self.styleSheet = getSampleStyleSheet()
        self.elements = []

        # colors - Azul turkeza 367AB3
        self.colorNegro = Color(0, 0, 0, 1)     # R G B  y opacidad debe estar en valores de 0 a 1.
        self.colorNegro1 = Color(0, 0, 0, 0.5)     # R G B  y opacidad debe estar en valores de 0 a 1.
        self.colorKalpeAzul1 = Color((182.0 / 255), (227.0 / 255), (166.0 / 255), 1)
        self.colorKalpeAzul2 = Color((140.0 / 255), (222.0 / 255), (192.0 / 255), 1)
        #self.colorOhkaGreen2 = Color((140.0/255), (222.0/255), (192.0/255), 1)
        self.colorOhkaBlue0 = Color((54.0/255), (122.0/255), (179.0/255), 1)
        self.colorOhkaBlue1 = Color((122.0/255), (180.0/255), (225.0/255), 1)
        self.colorOhkaGreenLineas = Color((50.0/255), (140.0/255), (140.0/255), 1)

        self.encabezadoPagina(True, criterio_1, criterio_2)
        self.contenidoReporte(data, encabezado)

        # Build
        self.doc = SimpleDocTemplate(path, pagesize=A4)
        self.doc.multiBuild(self.elements, canvasmaker=PiePagina)


    def encabezadoPagina(self, primeraPagina, Criterio, CriterioB):
        if primeraPagina:
            encabezadoEstilo = ParagraphStyle('Hed0', fontSize=16, alignment=TA_CENTER, borderWidth=3, textColor=self.colorNegro)
            texto_Encabezado = 'REPORTE DE EQUIPOS KALINSON PERÚ'
            paragraph_texto_Encabezado = Paragraph(texto_Encabezado, encabezadoEstilo)
            self.elements.append(paragraph_texto_Encabezado)

            spacer = Spacer(10, 12)     # Ancho , alto
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorNegro1
            line.strokeWidth = 3
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 15)
            self.elements.append(spacer)

            formatoTextoIzq = ParagraphStyle('Izquierda', fontSize=12, alignment=TA_CENTER, borderWidth=3, textColor=self.colorNegro)
            texto_cliente = "BUSQUEDA POR: %s - %s :" % (Criterio, CriterioB)
            parrafo_cliente = Paragraph(texto_cliente, formatoTextoIzq)
            self.elements.append(parrafo_cliente)


    def contenidoReporte(self, informacion, encabezado):  # Agrega una seccion para la tabla de sesiones remotas del reporte

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textDataEncabezado = ["No."]
        textDataEncabezado.extend(encabezado)

        fontSize = 7
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textDataEncabezado:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)  # %s se llena con font size y el segundo %s con text
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)

        data = [d]
        formattedLineData = []

        alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                      ParagraphStyle(name="02", alignment=TA_CENTER),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER)]


        for i, lista_BD in enumerate(informacion):

            indice = i+1
            lista_anidada = [indice, lista_BD]
            lineData = [lista_anidada[0]]
            lineData.extend(lista_anidada[1])

            print(lineData)
            columnNumber = 0
            for item in lineData:
                ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
                p = Paragraph(ptext, alignStyle[0])
                formattedLineData.append(p)
                columnNumber = columnNumber + 1
            data.append(formattedLineData)
            formattedLineData = []


        # Row for total
        totalRow = [""]
        for item in totalRow:
            ptext = "<font size='%s'>%s</font>" % (fontSize-1, item)
            p = Paragraph(ptext, alignStyle[1])
            formattedLineData.append(p)
        data.append(formattedLineData)


        #print(data) Crear la  tabla
        dict_encabezados = {"SERIE": 70, "MARCA": 50, "MODELO": 60, "CONFIGURACION": 85, "FECHA_CAL": 70, "SIG_FECHA_CAL": 75, "RUC": 50, "EMPRESA": 80, "ZONA": 50, "ESTADO": 50, "COTIZACION": 50, "ORDEN": 60, "FACTURA": 30}
        ancho_columnas = [25]
        for valor_ancho in encabezado:
            valor = dict_encabezados.get(valor_ancho)
            ancho_columnas.append(valor)

        print(encabezado)

        table = Table(data, colWidths=ancho_columnas)
        tStyle = TableStyle([ #('GRID',(0, 0), (-1, -1), 0.5, grey),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                #('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ("ALIGN", (1, 0), (1, -1), 'CENTER'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, self.colorNegro),
                ('BOX', (0, 0), (-1, -1), 0.25, self.colorNegro),
                ('BACKGROUND', (0, 0), (-1, 0), self.colorOhkaGreenLineas),
                ('BACKGROUND', (0, -1), (-1, -1), self.colorOhkaBlue1),
                ('SPAN', (0, -1), (-2, -1))
                ])
        table.setStyle(tStyle)
        self.elements.append(table)


