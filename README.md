# Challenge Agente - Consultas - Documentos Internos

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
