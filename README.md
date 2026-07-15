# 🤖 Challenge Agente - Consultas - Documentos Internos

Un proyecto de Agente Inteligente Funcional diseñado para interactuar con una base de conocimiento interna compuesta por documentos PDF, Word y Excel. Desarrollado con Python, Flask, LangChain y Google Gemini.

## 🏗️ Arquitectura del Sistema

El sistema está dividido en varios componentes principales:

1. **Interfaz de Usuario (Frontend):**
   - Construida con HTML5, CSS3 (Dark Mode) y Vanilla JS.
   - Proporciona un chat interactivo con indicador de escritura, una barra lateral para subir documentos mediante Drag & Drop.

2. **Servidor Web (Flask - `app.py`):**
   - Expone la interfaz gráfica.
   - Maneja la subida de archivos (endpoint `/api/upload`).
   - Sirve la API JSON para consultas al agente (endpoint `/api/preguntas`).

3. **Motor del Agente (`agente_nn.py`):**
   - Utiliza LangChain para orquestar la cadena `RetrievalQA`.
   - Emplea **FAISS** para crear y gestionar el vectorstore local a partir de los documentos procesados.
   - Se conecta al modelo LLM de Google (**Gemini 2.5 Flash**) y usa **Google Generative AI Embeddings** para generar los vectores.
   - Expone la función principal `ask()` para responder a las preguntas y citar las fuentes.

4. **Procesadores de Documentos (`loaders.py`):**
   - Lee archivos ubicados en el directorio interno `documentos/`.
   - Soporta PDFs (`pypdf`), Word (`python-docx`) y Excel (`openpyxl` / `pandas`).
   - Retorna objetos `Document` de LangChain con metadata útil como la fuente, página u hoja.

## 🛠️ Tecnologías Usadas
- **Python 3**
- **Flask**
- **LangChain**
- **FAISS** (Base de datos vectorial)
- **Google Gemini** (LLM y Embeddings)
- **PyPDF, python-docx, pandas** (Para lectura de documentos)
  
## 🚀 Instrucciones para Ejecutar el Proyecto Localmente

### 1. Clonar el repositorio
(Si corresponde a un repositorio Git)
```bash
git clone <url_del_repo>
cd challenge-nnoguera-agente
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo llamado `.env` en la raíz del proyecto tomando como base `.env.example`:
```env
GOOGLE_API_KEY=tu_api_key
```
### 5. Ejecutar la aplicación
```bash
python app.py
```
Abre tu navegador web e ingresa a `http://127.0.0.1:5000/`.

### 6. Observaciones generales ante problemas de ejecución
Leer el archivo entorno.txt

## 🌐Deploy en OCI
### 1. Crear el Compartimento
Se crea el compartimento nnoguera-agente
<img width="1555" height="462" alt="image" src="https://github.com/user-attachments/assets/953184a6-dd77-49fa-83d4-1322dc6b534a" />

### 2. Crear la VCN e Instancia 
**Se crea la Virtual Cloud Network (VCN)**
<img width="1535" height="436" alt="image" src="https://github.com/user-attachments/assets/5b06e9ef-fef0-4625-b821-84ba804f4ed5" />

**Se crea la instancia instancia-agente**
<img width="1551" height="370" alt="image" src="https://github.com/user-attachments/assets/33bd4315-1fc0-4891-a483-7509982e7894" />

**Se crea el par de llaves (privada y pública)** que OCI te ofrece y debes guardarla en un lugar seguro para utilizarla en tu instancia 

**Configuración de Red: La Subnet Pública y Reglas de Entrada**
Para que la aplicación reciba tráfico externo en el puerto 8000, configuramos en la red:
<img width="1517" height="555" alt="image" src="https://github.com/user-attachments/assets/1944ac7d-8304-453e-b885-2a2929613cb2" />

### 3. Conectar a la VM e Instalar Python 
Conectarte a la VM e Instalar Python

### 4. Clonar el repositorio y Configurar el Entorno
```bash
git clone <url_del_repo>
cd challenge-nnoguera-agente
```
Crea y activa un entorno virtual para mantener limpias las dependencias
```bash
python3 -m venv venv
source venv/bin/activate
```
Instalar los requerimientos del proyecto
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
Instalar Gunicorn (Green Unicorn) como servidor web HTTP compatible con el estándar WSGI para aplicaciones en Python. 
```bash
pip install gunicorn
pip install --user gunicorn
sudo dnf install gunicorn
```
Ejecutar via Python
```bash
PYTHONPATH=/home/opc/challenge-nnoguera-agente python3 -m gunicorn --bind 0.0.0.0:8000 app:app
```
Abre tu navegador web e ingresa a `http://165.1.120.30:8000/`.

## 🧠 Ejemplos de Uso

1. **Subir Documentos:**
   Arrastra un archivo PDF (ej. un manual de políticas), un Word (ej. un contrato) o un Excel (ej. un listado de empleados) a la zona de carga en la barra lateral izquierda.

2. **Hacer Preguntas:**
   - **Pregunta:** *"¿Cuáles son las reglas para el trabajo remoto según la política de la empresa?"*
   - **Respuesta (Ejemplo):** *"De acuerdo con el Manual de Políticas 2024, el trabajo remoto está permitido 2 días a la semana previo acuerdo con el gerente del área."* 
   - *(Mostrará como fuente: manual_politicas.pdf)*

   - **Pregunta:** *"¿Quién es el contacto de emergencia para Juan Pérez?"*
   - **Respuesta (Ejemplo):** *"El contacto de emergencia para Juan Pérez es María López (tel: 555-1234)."*
   - *(Mostrará como fuente: lista_empleados.xlsx)*

## 📸 Evidencia de funcionamiento

1. **Consola en el OCI**
<img width="1135" height="258" alt="consola_funcionando" src="https://github.com/user-attachments/assets/a3d498ca-efc3-426d-a3d3-2bd0ed0f10ef" />

2. **Respuesta a archivo word**
<img width="1896" height="1107" alt="respuesta de archivo docx" src="https://github.com/user-attachments/assets/c50b9c19-c1f4-4f76-9574-e20fc99fc1f3" />

3. **Respuesta a archivo excel**
<img width="1887" height="1081" alt="respuesta de archivo excel" src="https://github.com/user-attachments/assets/cb8feecc-8e1d-4f2c-9e38-ec85ba3316ed" />

4. **Respuesta a archivo pdf**
<img width="1600" height="903" alt="respuesta de archivo pdf" src="https://github.com/user-attachments/assets/635d63c7-be78-49ea-adae-c82c6a550977" />

## 🚀 Opción B - Despliegue del Proyecto en Windows Server 2016

1. 🛠️**Diagnóstico y Cambio de Arquitectura** 

Se detectó que el servidor original en la nube (1 OCPU) generaba bloqueos ("Deadlocks") al intentar cargar la base de datos vectorial FAISS y el modelo de IA.
Para garantizar rendimiento y evitar cuellos de botella de hardware, se migró el despliegue a un entorno local más robusto sobre Windows Server 2016.

2. 🐍 **Preparación del Entorno Python**

Se creó un entorno virtual aislado para no afectar el sistema operativo base: 
```bash
python -m venv venv
```
Se activó el entorno: 
```bash
venv\Scripts\activate
```
Se instalaron las librerías y dependencias necesarias del proyecto: 
```bash
pip install -r requirements.txt
```
3. ⚙️ **Adaptación del Servidor Web (Producción)** 

Dado que Gunicorn es exclusivo para arquitecturas Linux/UNIX, se reemplazó por Waitress, un servidor de nivel de producción nativo para Windows.
```bash
pip install waitress
```
4. ▶️**Ejecución del Servicio** 

Se levantó la aplicación escuchando en todas las interfaces de red del servidor (IP local 192.168.1.250) en el puerto 8000 mediante el comando:
```bash
waitress-serve --listen=0.0.0.0:8000 app:app
```
5. 🌐**Publicación y Ruteo (MikroTik)** 

Se configuró una regla de NAT/Port Forwarding en el router MikroTik.

Todo el tráfico externo entrante al puerto 8000 de la IP pública, se redirige exitosamente a la IP interna del Windows Server (192.168.1.250:8000).

✅**Resultado:** Aplicación accesible desde internet de forma estable y fluida en la url: `http://181.122.60.230:8000/`

<img width="1890" height="1080" alt="resultado opcion b" src="https://github.com/user-attachments/assets/30b444c4-a6e7-4500-82ce-093a450528cd" />
