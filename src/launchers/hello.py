import ollama
from mappers.toolmap import map_function_to_ollama_tool_dict
from tools.today import now
from tools.demo import demofunction, send_email
from pprint import pprint

for i in range(5):
  response = ollama.chat(
      model='llama3-groq-tool-use:8b',
      messages=[
          {
              'role': 'system',
              'content': 'You are a helpful AI assistant. Call functions to achieve user\'s happiness.'
          },
          {
            'role': 'user',
            'content': 'Send an email to asd@sdf.pl with invitation to my party',
          },
      ],
      tools=[
        map_function_to_ollama_tool_dict(demofunction),
        map_function_to_ollama_tool_dict(now),
        map_function_to_ollama_tool_dict(send_email)
      ],
  )
  pprint(response['message'])
