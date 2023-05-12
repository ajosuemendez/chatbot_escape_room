from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSayShirtSize(Action):

    def name(self) -> Text:
        return "action_say_shirt_size"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shirt_size = tracker.get_slot("shirt_size")
        if not shirt_size:
            dispatcher.utter_message(text="I don't know your shirt size.")
        else:
            dispatcher.utter_message(text=f"Your shirt size is {shirt_size}!")
        return []


class ActionSayName(Action):

    def __init__(self):
        self.name_set = False

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(text="I don't know your name.")
        else:
            if self.name_set:
                dispatcher.utter_message(text=f"Hi {name}!")
            else:
                dispatcher.utter_message(text=f"{name} is a beautful name:) Nice choice!")
                self.name_set = True

        return []

class ActionSessionStarted(Action):
    def name(self) -> Text:
        return "action_session_started"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Welcome to our new game where you embark on an exciting adventure but there's a twist! You've forgotten your own name! Throughout your journey, you'll face challenges and puzzles that will test your skills and wit, but in the end, you'll need to remember your name to complete your quest. So, are you ready to take on this challenge and help us uncover the mystery of your true identity?  Let's get started, but first, can you please tell me how you'd like to be called?")
        return []