

EasyAgent
===

Marco de trabajo de agente para llamadas a herramientas de Ollama.

Con este marco de trabajo, puedes ejecutar un único agente utilizando un conjunto de herramientas ligero.

[Ollama: Tool support (blogpost)](https://ollama.com/blog/tool-support)

# Uso
```python
import datetime
from args_description import describe_args

@describe_args()
def now() -> str:
    """Call this function when you want to get current date and time."""
    return datetime.datetime.now().isoformat()

ea = EasyAgent(
    model="llama3.1:8b",
    tools=[now],
    system=None,
)

ea.ask("What is the date today?")
# 'The current date is July 26, 2024.'

ea.tick("What is the date today?")
# {'content': '',
#  'role': 'assistant',
#  'tool_calls': [{'function': {'arguments': {}, 'name': 'now'}}]}

```

# Instalación

```shell
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
python3 ./src/launchers/hello.py
```

# Agente de calendario (en desarrollo)

Para probar las funciones del calendario:
- Configura las credenciales de la API Simple de Google Calendar siguiendo la [Guía de inicio: Credenciales](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html#credentials).
    - Además, he añadido mi correo electrónico como usuario de prueba para la pantalla de consentimiento de OAuth en el panel de GCP. No estoy seguro de que sea necesario, pero a mí me funciona.
- Actualiza tu correo electrónico en `src/launchers/assistant.py`
- Ejecuta `src/launchers/assistant.py`
    - En la primera ejecución, debería aparecer un navegador web con la pantalla de consentimiento. Acepta los términos y disfruta del código funcionando.

El código está un poco desordenado, pero en este momento está pensado como una demo técnica.
