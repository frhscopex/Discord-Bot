import discord
import os
from dotenv import load_dotenv
import requests 
import json 
import random 
from replit import db
from keep_alive import keep_alive


sad_words = ["Sad", "Depressed", "Melancholy", "Sorrowful", "Heartbroken", "Downcast", "Gloomy", "Mournful", "Despondent", "Dejected", "Blue", "Dismal", "Woeful", "Disheartened", "Downhearted", "Forlorn", "Unhappy", "Down", "Glum", "Miserable", "Crestfallen", "Down in the dumps", "Despairing", "Hopeless", "Cheerless", "Lugubrious", "Dreary", "Funereal", "Doleful", "Morose", "Woebegone", "Heavyhearted", "Dolorous", "Eeyore-ish", "Low-spirited", "Sullen", "Oppressed", "Dismayed", "Doleful", "Regretful", "sad", "depressed", "melancholy", "sorrowful", "heartbroken", "downcast", "gloomy", "mournful", "despondent", "dejected", "woeful", "disheartened", "downhearted", "forlorn", "unhappy", "down", "glum", "miserable", "crestfallen", "down in the dumps", "despairing", "hopeless", "cheerless", "lugubrious", "dreary", "funereal", "doleful", "morose", "woebegone", "heavyhearted", "dolorous", "eeyore-ish", "low-spirited", "sullen", "oppressed", "dismayed", "doleful", "regretful"]
starter_encouragements = ["Find strength in", "Look for hope within", "Embrace the light despite", "Discover resilience amid", "Focus on brighter days","Seek joy through", "Hold onto positivity", "Find solace in the midst", "Face challenges with courage", "Cherish small moments despite", "Let optimism guide you through", "See opportunities within", "Draw strength from", "Embrace a hopeful perspective amidst", "Navigate through with grace", "Build resilience in the face", "Discover inner strength despite", "Hold onto the belief in", "Choose joy despite","Cultivate a positive mindset amidst", "Find courage within","Hold onto faith through", "Seek joy even in", "Believe in a brighter future despite", "Cultivate a positive outlook amidst", "Discover hope within", "Find inner peace despite", "See the potential for joy amid", "Hold onto positivity despite", "Embrace resilience through"]

if "responding" not in db.keys():
  db["responding"] = True

def update_encouragements(encouraging_message):
  if "encouragement" in db.keys():
    enouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]
def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
    

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0] ['q'] + " -" + json_data[0] ['a']
  return quote

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content

    if message.content.startswith('hello'):
        await message.channel.send("What's up, buddy? \U0001F919")

    if message.content.startswith('inspire'):
        quote = get_quote()
        await message.channel.send(quote)
   

    if db["responding"]:
      options = starter_encouragements
      if "encouragements" in db.keys():
        options = options + db["encouragements"]
  
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))
    
 
  
    if msg.startswith("/new"):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message added.")


  
    if msg.startswith("/del"):  
      encouragements = []
      if "encouragements" in db.keys():
        index = int(msg.split("$del",1)[1])
        delete_encouragements(index)
        encouragements = db["encouragements"]
        await message.channel.send(random.choice(options))

    if msg.startswith("/list"):
      encouragements = []
      if "encouragements" in db.keys():
        encouragements = db["encouragements"]
      await message.channel.send(encouragements)

    if msg.startswith("/responding"):
      value = msg.split("/responding ",1)[1]

      if value.lower() == "true":
        db["responding"] = True
        await message.channel.send("Responding is on.")
      else:
        db["responding"] = False
        await message.channel.send("Responding is off.")

keep_alive()
load_dotenv("sec.env")
client.run(os.getenv('Token') or 'your-default-token-here')




