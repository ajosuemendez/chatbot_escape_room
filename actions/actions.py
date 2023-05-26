from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSessionStarted(Action):
    def name(self) -> Text:
        return "action_session_started"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Subject 69, please say your name out loud as you type it in...")
        #We initialize the total amount of lives for the player, in this case 10
        return[SlotSet("lives", 10)]

class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        if not name:
            dispatcher.utter_message(text="I don't know your name.")
            return[]
        else:
            dispatcher.utter_message(text=f"Hi {name}...")
            dispatcher.utter_message(text="Suddenly the lights went out. All you see is a door with phosphorescent neon lights in front of you that says 'I was only 25 years old the day before yesterday and next year I'll be 28. When is my birthday?'.")
            dispatcher.utter_message(text="As you approach you find the door lock with some inscriptions: 'Can you guess me?'....")

        return [SlotSet("name", name)]


class ActionRiddleCheck(Action):

    def __init__(self):
        self.possible_corret_answers = ["first of january", "1st january", "01.01", "1 january", "january 1", "january first"]
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
                    dispatcher.utter_message(text=f"You tried to open the door but appereantly is still locked.")
                    dispatcher.utter_message(text=f"You see another lock with more inscriptions: What is the Nation with the most Football World Cups?")
                    self.already_solved = True

                    puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
                    if puzzles_solved_num is None:
                        puzzles_solved_num = 1
                    else:
                        puzzles_solved_num += 1

                    #We have to update we entered to a new room and that we have solved a puzzle
                    return [SlotSet("number_puzzle_solved", puzzles_solved_num)]
                    # return [SlotSet("current_room", "Lobby"), SlotSet("number_puzzle_solved", puzzles_solved_num)]


            dispatcher.utter_message(text=f"The door is still locked...Try again")

            current_lives = tracker.get_slot("lives")
            if current_lives < 1:
                dispatcher.utter_message(text=f"GAME OVER.")
                return []

            dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


            return [SlotSet("lives", current_lives-1)]



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


class DefaultFallbackAction(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Custom fallback response message
        fallback_message = "I'm sorry, I didn't understand. Can you please rephrase your message?"

        # Send the fallback message
        dispatcher.utter_message(text=fallback_message)

        return []


class WorldCupRiddleCheck(Action):
    def name(self) -> Text:
        return "action_say_is_world_cup_riddle_correct"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        world_cup_answer = tracker.get_slot("answer_world_cup")

        if world_cup_answer:
            if world_cup_answer.lower() == "brazil":
                dispatcher.utter_message(text=f"Correct!")

                puzzles_solved_num = tracker.get_slot("number_puzzle_solved")
                if puzzles_solved_num is None:
                    puzzles_solved_num = 1
                else:
                    puzzles_solved_num += 1
                return [SlotSet("number_puzzle_solved", puzzles_solved_num)]

            else:
                dispatcher.utter_message(text=f"Wrong! Try again looser")
                current_lives = tracker.get_slot("lives")
                if current_lives < 1:
                    dispatcher.utter_message(text=f"GAME OVER.")
                    return []
                
                dispatcher.utter_message(text=f"You have lost a life! You have {current_lives-1} lives left.")


                return [SlotSet("lives", current_lives-1)]

        dispatcher.utter_message(text=f"I do not understand")

        return []