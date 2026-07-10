document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const typingIndicator = document.getElementById('typing-indicator');
    
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadStatus = document.getElementById('upload-status');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        userInput.value = '';
        
        typingIndicator.classList.remove('hidden');
        scrollToBottom();

        try {
            const response = await fetch('/api/preguntas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ pregunta: text })
            });
            const data = await response.json();
            
            typingIndicator.classList.add('hidden');
            
            if (response.ok) {
                addMessage(data.respuesta, 'bot', data.fuentes);
            } else {
                addMessage(data.error || 'Ocurrió un error al procesar la pregunta.', 'bot');
            }
        } catch (error) {
            typingIndicator.classList.add('hidden');
            addMessage('Error de conexión con el servidor.', 'bot');
        }
    });

    function addMessage(text, sender, sources = []) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        const avatarIcon = sender === 'user' ? 'fa-user' : 'fa-robot';
        
        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            sourcesHtml = `<div class="sources"><strong>Fuentes:</strong> ${sources.join(', ')}</div>`;
        }

        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid ${avatarIcon}"></i></div>
            <div class="message-content">
                <p>${text.replace(/\n/g, '<br>')}</p>
                ${sourcesHtml}
            </div>
        `;
        
        chatBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    dropZone.addEventListener('click', () => fileInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFiles(e.dataTransfer.files);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFiles(e.target.files);
        }
    });

    async function handleFiles(files) {
        uploadStatus.textContent = 'Subiendo e indexando...';
        uploadStatus.style.color = '#03dac6';

        for (let i = 0; i < files.length; i++) {
            const formData = new FormData();
            formData.append('file', files[i]);

            try {
                const response = await fetch('/api/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                
                if (response.ok) {
                    uploadStatus.textContent = data.message;
                } else {
                    uploadStatus.textContent = `Error: ${data.error}`;
                    uploadStatus.style.color = '#cf6679';
                }
            } catch (error) {
                uploadStatus.textContent = 'Error al subir el archivo.';
                uploadStatus.style.color = '#cf6679';
            }
        }
        
        fileInput.value = '';
    }
});
