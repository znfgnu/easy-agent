import datetime
import json
import logging
from easyagent import EasyAgent
from args_description import describe_args
from gcsa.google_calendar import GoogleCalendar
from tools.today import now


logger = logging.getLogger(__name__)


class CalendarAgent(EasyAgent):
    def __init__(self, email: str, model: str) -> None:
        tools = [
            now,
            self.upcoming_events,
        ]
        system = None
        super().__init__(model, tools, system, {"temperature": 0.0})
        self._calendar = GoogleCalendar(email)

        self._calendar_list = list(self._calendar.get_calendar_list())

    @describe_args(
        date_since="Format: YYYY-MM-DD",
        date_until="Format: YYYY-MM-DD",
        event_type="Kind of the event (ex. meeting, birthday, appointment)",
    )
    def upcoming_events(
        self,
        date_since: str,
        date_until: str,
        event_type: str,
    ):
        """Call this function to read events from a given period."""

        events = []
        logger.debug("Fetching events: %s", event_type)

        for cal in self._calendar_list:
            logger.debug("Fetching events from calendar %s", cal.summary)
            events += list(self._calendar.get_events(
                time_min=datetime.date.fromisoformat(date_since),
                time_max=datetime.date.fromisoformat(date_until) + datetime.timedelta(days=1),
                order_by="startTime",
                single_events=True,
                calendar_id=cal.calendar_id
            ))

        return json.dumps({
            "events": [
                {"start": event.start.isoformat(), "summary": event.summary, "is_recurring": event.is_recurring_instance}
                for event in events
            ]
        })


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )
    logging.getLogger('httpcore').setLevel(logging.INFO)
    logging.getLogger('httpx').setLevel(logging.ERROR)

    def printa(*args):
        print(*[f"\033[92m{arg}\033[0m" for arg in args])

    ca = CalendarAgent(
        email="someemail@gmail.com",
        model="llama3.1:8b",
        # model="mistral-nemo:12b",
        # model="mistral:7b",
    )
    # answer = ca.ask("What are the upcoming events?")
    answer = ca.ask("What's the date today?")
    printa(answer)
    # answer = ca.ask("What's the date tomorrow?")
    # print(answer)
    # answer = ca.ask("When is the test event?")
    # printa(answer)
    # answer = ca.ask("Do I have a test event tomorrow? Answer with a single word.")
    # printa(answer)
    # answer = ca.ask("Do I have a test event today? Answer with a single word.")
    # printa(answer)
    answer = ca.ask("Who has birthday today?")
    printa(answer)
    answer = ca.ask("Who has birthday tomorrow?")
    printa(answer)
    # answer = ca.ask("Who has birthday on 9th September?")
    # printa(answer)
    answer = ca.ask("Who else has birthday within a month?")
    printa(answer)

