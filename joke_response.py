import discord
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

class Joker:
    def __init__(self, message):
        self.message_text = message.content.lower()
        self.message_author = message.author.name
        self.message_authorID = message.author.id
        self.response = ""

    def high_roller_will_come_in_clutch(self):
        return 'high roller will come in clutch' in self.message_text and '🤝' in self.message_text and '<@1089621543660830720>' in self.message_text
    
    def ur_so_real_ilysm(self):
        return '<@1089621543660830720>' in self.message_text and 'ur so real ilysm' in self.message_text
    
    def crazy(self):
        return 'crazy' in self.message_text and not self.message_author == "High Roller"

    def determine_response(self):
        if(self.high_roller_will_come_in_clutch()):
            self.response = "yes. :handshake: <@" + str(self.message_authorID) + ">"
        elif(self.ur_so_real_ilysm()):
            self.response = "ilyt bb mwah 💋"
        elif(self.crazy()):
            self.response = "crazy? i was crazy once. They locked me in a room. A rubber room. A rubber room with rats. The rats make you crazy."

    def has_response(self):
        return not self.response == ""