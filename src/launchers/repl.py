from easyagent import EasyAgent
from tools.today import now

def main():
    ea = EasyAgent(
        model="llama3.1:8b",
        tools=[now],
        system=None,
    )
    while True:
        request = input("> ")
        response = ea.ask(request)
        print(f"< {response}")


if __name__ == "__main__":
    main()
