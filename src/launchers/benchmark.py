import datetime
import csv
import json
import os
import tempfile

from easyagent import EasyAgent
from tools.demo import demo_function, send_email
from tools.today import now

def benchmark(model, tools, task):
  tool_calls_counter = 0
  total_counter = 0
  assess = call_check[task]

  ea = EasyAgent(model=model, tools=tools, system=None)

  with tempfile.NamedTemporaryFile("w", dir="./reports/", delete=False) as f:
    try:
      w = csv.DictWriter(f, fieldnames=("tool_calls_counter", "total_counter", "success_rate", "message"))
      w.writeheader()
      for i in range(10000):
        msg = ea.tick(prompt=predefined_msgs[task], remember_response=False, remember_request=False)

        tool_calls = [call['function'] for call in msg.get("tool_calls", [])]
        if len(tool_calls) > 0 and assess(tool_calls):
          tool_calls_counter += 1
        else:
          print(f"<< {msg['content']}")
        total_counter += 1
        success_rate = tool_calls_counter / total_counter * 100
        w.writerow(dict(
            tool_calls_counter=tool_calls_counter,
            total_counter=total_counter,
            success_rate=success_rate,
            message=json.dumps(msg),
        ))
        print(f">>> {success_rate:.2f}% tool calls ({tool_calls_counter}/{total_counter})")
    finally:
        filename = ''.join([
          "reports/"
          f"{datetime.datetime.now().isoformat()[2:-7]}_{model}_{task}_",
          f'{"D" if demo_function in tools else "" }',
          f'{"N" if now in tools else "" }',
          f'{"S" if send_email in tools else "" }_',
          f"{success_rate:.0f}sr_{total_counter}total.csv",
        ])
        os.rename(f.name, filename)


predefined_msgs = {
  'email': 'Send an email to asd@sdf.pl with invitation to my party',
  'now': 'What is the date today?',
}

call_check = {
  'email': lambda calls: all([
    calls[0]['name'] == send_email.__name__,
    calls[0]['arguments'].get('recipient', None) == "asd@sdf.pl",
    "party" in calls[0]['arguments'].get('content', '')
  ]),
  'now': lambda calls: all([
    calls[0]['name'] == now.__name__,
    calls[0]['arguments'] == {},
  ])
}

if __name__ == "__main__":
  llama31 = 'llama3.1:8b'
  llama3tool = 'llama3-groq-tool-use:8b'

  benchmark(
    model=llama31,
    tools=(demo_function, now, send_email),
    task='email',
  )
