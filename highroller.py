import discord
from discord.ext import commands
from roll_parser import Parser
from joke_response import Joker
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if len(message.content) > 0 and message.content[0] == '!':
        parser = Parser(message.content.lower())
        if any(s in str(message.channel) for s in parser.text_channels):
            parser.clear_disallowed_chars()
            final_message = ""
            parser.parse_init()
            for cock in parser.calc.cocked_results:
                final_message += cock + "\n"
            await message.channel.send( final_message + str(parser.calc.main_total.term) + 
                                        '\nDetails: ' + str(parser.list_of_lists_of_rolled) + 
                                        '\nAverage: ' + str(int(parser.calc.main_total.avg)))
        else:
            await message.channel.send('No rolling outside of dicetray! >:(')
            await message.channel.send('https://tenor.com/view/no-nooo-nope-eat-fingerwag-gif-14832139')
    else:
        joker = Joker(message)
        joker.determine_response()
        if(joker.has_response()):
            await message.channel.send(joker.response)
            
with open('BOT-KEY', 'r') as file: bot_key = file.read().rstrip()
client.run(bot_key)