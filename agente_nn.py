import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_classic.chains import RetrievalQA
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loaders import process_file

load_dotenv()

VECTORSTORE_PATH = "vectorstore"
DOCUMENTS_PATH = "documentos"

class AgenteNN:
    def __init__(self):
        if not os.path.exists(DOCUMENTS_PATH):
            os.makedirs(DOCUMENTS_PATH)

        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.vectorstore = None
        self.qa_chain = None
        
        self.initialize_index()

    def initialize_index(self):
        if os.path.exists(VECTORSTORE_PATH) and os.listdir(VECTORSTORE_PATH):
            print("Cargando vectorstore FAISS existente...")
            try:
                self.vectorstore = FAISS.load_local(VECTORSTORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
                self._build_chain()
            except Exception as e:
                print(f"Error al cargar FAISS: {e}. Reconstruyendo...")
                self.rebuild_index()
        else:
            print("No se encontró índice. Construyendo nuevo vectorstore FAISS...")
            self.rebuild_index()

    def rebuild_index(self):
        docs = []
        for filename in os.listdir(DOCUMENTS_PATH):
            file_path = os.path.join(DOCUMENTS_PATH, filename)
            if os.path.isfile(file_path):
                print(f"Procesando {filename}...")
                docs.extend(process_file(file_path))
        
        if not docs:
            print("No hay documentos para indexar.")
            return

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)

        print(f"Creando índice FAISS con {len(chunks)} fragmentos...")
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        
        if not os.path.exists(VECTORSTORE_PATH):
            os.makedirs(VECTORSTORE_PATH)
        self.vectorstore.save_local(VECTORSTORE_PATH)
        
        self._build_chain()
        print("Índice construido y guardado con éxito.")

    def _build_chain(self):
        if self.vectorstore:
            retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )

    def ask(self, query: str) -> dict:
        if not self.qa_chain:
            return {
                "respuesta": "El agente no está listo. Sube documentos e inicializa el índice.",
                "fuentes": []
            }
        
        try:
            result = self.qa_chain({"query": query})
            sources = []
            for doc in result.get("source_documents", []):
                meta = doc.metadata
                source = meta.get("source", "Desconocido")
                if source not in sources:
                    sources.append(source)
                    
            return {
                "respuesta": result.get("result", ""),
                "fuentes": [os.path.basename(s) for s in sources]
            }
        except Exception as e:
            print(f"Error en la consulta: {e}")
            return {
                "respuesta": f"Lo siento, ocurrió un error al procesar la pregunta: {str(e)}",
                "fuentes": []
            }

agente = AgenteNN()
