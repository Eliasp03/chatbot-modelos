import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

st.set_page_config(page_title="Chatbot con IA", page_icon="💬", layout="centered")

# Cargar la API key de forma segura
try:
    load_dotenv()  # Carga variables desde .env si existe (entorno local)
    API_KEY = os.getenv("GROQ_API_KEY")  #para Groq; usar "OPENAI_API_KEY" si es OpenAI
except:
    API_KEY = st.secrets["GROQ_API_KEY"]

os.environ["GROQ_API_KEY"] = API_KEY
client = Groq()  # Cliente para invocar la API de Groq

# Inicializar el historial de chat en la sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # lista de dicts: {"role": ..., "content": ...}

SYSTEM_PROMPT = """
Eres THEO-Bot 🤖, un asistente virtual especializado en el dispositivo biomédico THEO. 
Tu rol es explicar de manera clara, confiable y amigable qué es THEO, cómo funciona 
y por qué es una solución innovadora para el monitoreo nutricional en bebés con 
labio leporino y/o paladar hendido.

📌 Información clave sobre THEO:
- THEO es un dispositivo médico **no invasivo** que cuantifica de forma **objetiva y en tiempo real la ingesta de leche** en bebés con labio y/o paladar hendido. 
- Permite convertir un proceso normalmente cualitativo (alimentación) en un procedimiento **cuantificable y trazable**, lo cual mejora la preparación nutricional antes de cirugías reconstructivas.
- Su atributo diferencial es la **cuantificación objetiva de la ingesta de leche**, algo que otros biberones especializados o escalas clínicas manuales no ofrecen.
- Integra hardware (celdas de carga, microcontrolador ESP32, alarmas) con una **plataforma digital** para el seguimiento histórico y generación de reportes.
- Beneficios:
  - **Clínicos**: mejor preparación prequirúrgica, reducción de desnutrición y decisiones médicas más seguras.
  - **Operativos**: facilita el trabajo del personal de salud al automatizar registros y reducir visitas innecesarias.
  - **Institucionales**: posiciona a clínicas como centros innovadores que usan tecnologías de vanguardia.
- Clientes principales: padres de bebés diagnosticados y **IPRESS privadas con pediatría y centro quirúrgico**, inicialmente en Lima Metropolitana.
- **Precio accesible**: entre 70 y 100 USD, frente a dispositivos sustitutos internacionales que superan los 500–700 USD.
- **Política de precios**: penetración selectiva con descuentos por volumen a IPRESS y planes de financiamiento para familias.
- **Distribución**: selectiva, mediante clínicas aliadas, e-commerce, ONGs y asociaciones de salud infantil.
- **Promoción**: validación clínica, campañas digitales segmentadas, charlas con médicos y testimonios de padres.
- THEO busca transmitir el mensaje: *“Brinda confianza a los padres y respaldo clínico a los médicos, asegurando nutrición adecuada antes de la cirugía reconstructiva”*.

👉 Como THEO-Bot, responde preguntas de padres, médicos y estudiantes sobre el dispositivo, 
resalta siempre la accesibilidad, la innovación y el impacto positivo en la salud infantil.
"""

st.title("🤖 Chatbot THEO")
st.write("Puedes hacer preguntas acerca del dispositivo THEO.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Construir mensajes para el modelo
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    messages.extend(st.session_state.chat_history)

    # Llamar a la API **solo** si hay user_input (evita NameError)
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
        )
        respuesta_texto = response.choices[0].message.content  # objeto, no dict
    except Exception as e:
        respuesta_texto = f"Lo siento, ocurrió un error al llamar a la API: `{e}`"

    # Mostrar respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta_texto)

    # Guardar en historial
    st.session_state.chat_history.append({"role": "assistant", "content": respuesta_texto})

