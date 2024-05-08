from enum import Enum, auto
import discord
import re

class State(Enum):
    AWAITING_MESSAGE = auto()
    START = auto()
    THREAT_LEVEL = auto()
    DONE = auto()

class Moderate:
    def __init__(self, mod_channel, id, report):
        self.state = State.START
        self.mod_channel = mod_channel
        self.reported_id = id
        self.report = report
        self.offender_id = report.reported_message['content'].author.id
        self.violations = {}
        self.current_step = 0

    async def start_mod_flow(self):
        await self.mod_channel.send("How much of a threat is this? (minor, moderate, major)")
        self.state = State.THREAT_LEVEL

    async def handle_message(self, message):
        print('hello')
        await self.mod_channel.send("Moooooo i'm working")

    async def add_violation(self, userId):
        if userId in self.violations:
            self.violations[userId] += 1
        else:
            self.violations[userId] = 1

    async def moderate_content(self, message, hateSpeech=True):
        reply = ""
        if self.current_step == 0:
            reply = f"Content: {message}\nIs this content hate speech? {'Yes' if hateSpeech else 'No'}"
            # Present the moderation options
            reply += "Choose an action:\n"
            reply += "1: Remove comment.\n"
            reply += "2: Remove comment and mute account for 24 hours.\n"
            reply += "3: Remove comment, mute account for 24 hours, and ban account.\n"
            reply += "Enter the number of the action you wish to take: \n"
            self.state = State.AWAITING_MESSAGE
            self.current_step += 1
            # action_choice = input("Enter the number of the action you wish to take: ")
        
        elif self.current_step == 1:
            self.add_violation(self.offender_id)

            if message == "1":
                reply = "We will remove the comment."
            elif message == "2":
                reply = f"We will remove the comment and mute {self.offender_id}'s account for 24 hours."
            elif message == "3":
                reply = f"We will remove the comment and ban {self.offender_id}'s account."
            else:
                reply = "Invalid action."

            self.state = State.DONE
        
        print('hello')
        return reply
