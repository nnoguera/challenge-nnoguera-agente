import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from agente_nn import agente, DOCUMENTS_PATH

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DOCUMENTS_PATH
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            agente.rebuild_index()
            return jsonify({'message': f'Archivo {filename} subido e indexado correctamente.'}), 200
        except Exception as e:
            return jsonify({'error': f'Error al indexar: {str(e)}'}), 500
            
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/preguntas', methods=['POST'])
def preguntas():
    data = request.json
    if not data or 'pregunta' not in data:
        return jsonify({'error': 'Falta el campo pregunta.'}), 400
    
    pregunta = data['pregunta']
    
    resultado = agente.ask(pregunta)
    
    return jsonify({
        'pregunta': pregunta,
        'respuesta': resultado['respuesta'],
        'fuentes': resultado['fuentes']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
