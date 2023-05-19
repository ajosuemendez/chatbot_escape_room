from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, FollowupAction
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
                dispatcher.utter_message(text=f"{name} good luck...")
                self.name_set = True

        return []

class ActionSessionStarted(Action):
    def name(self) -> Text:
        return "action_session_started"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Subject 69, please say your name out loud as you type it in...")
        return []

class ActionRiddleCheck(Action):

    def __init__(self):
        self.possible_corret_answers = ["first of january", "1st january", "01.01", "1 january", "january 1"]
        self.already_solved = False

    def name(self) -> Text:
        return "action_say_is_date_riddle_correct"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        answer_date = tracker.get_slot("answer_date")
        if not answer_date:
            dispatcher.utter_message(text="Repeat your answer please.")
            return []

        else:
            if self.already_solved:
                dispatcher.utter_message(text=f"The corresponding door is already unlocked.")
                return []
            for answer in self.possible_corret_answers: 
                if answer_date.lower() == answer:
                    dispatcher.utter_message(text=f"The door was unlocked! You entered to the new room.")
                    self.already_solved = True

                    puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
                    if puzzles_solved_num is None:
                        puzzles_solved_num = 1
                    else:
                        puzzles_solved_num += 1

                    return [SlotSet("current_room", "Lobby"), SlotSet("number_puzzle_solved", puzzles_solved_num)]

            dispatcher.utter_message(text=f"The door is still locked...Try again")
            return [FollowupAction("action_subtract_life")]

class SetLobbyRoomAction(Action):

    def name(self) -> Text:
        return "action_set_lobby_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return[SlotSet("current_room", "Lobby")]


class SetHosnaRoomAction(Action):

    def name(self) -> Text:
        return "action_set_hosna_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return[SlotSet("current_room", "hosna_room")]

class IncreaseSolvedPuzzlesAction(Action):

    def name(self) -> Text:
        return "action_increase_solved_puzzles"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
        if puzzles_solved_num is None:
            puzzles_solved_num = 1
        else:
            puzzles_solved_num += 1

        return[SlotSet("number_puzzle_solved", puzzles_solved_num)]

class GetCurrentRoomAction(Action):

    def name(self) -> Text:
        return "action_get_current_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_room = tracker.get_slot("current_room")
        # print(current_room)
        if not current_room:
            dispatcher.utter_message(text="You are in the starting room")
        else:
            dispatcher.utter_message(text=f"You are in the {current_room}!")
        return []

class GetNumberPuzzlesSolvedAction(Action):

    def name(self) -> Text:
        return "action_get_number_puzzle_solved"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        number_puzzle_solved = tracker.get_slot("number_puzzle_solved")
        if not number_puzzle_solved:
            dispatcher.utter_message(text=f"No puzzles solved.")
        else:
            dispatcher.utter_message(text=f"You have solved {number_puzzle_solved} puzzles!")
        return []
        
class SubtractLife(Action):

    def __init__(self):
        self.total_lives = 10
        self.current_lives = 10

    def name(self) -> Text:
        return "action_subtract_life"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        self.current_lives -= 1
        if self.current_lives < 1:
            dispatcher.utter_message(text=f"GAME OVER.")
            return []
        
        dispatcher.utter_message(text=f"You have lost a life! You have {self.current_lives} lives  from {self.total_lives} lives left.")
        
        return []