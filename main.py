import discord
import os
import requests
import json
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name='Ryan Bot | !ryanhelp'))
  print('We have logged in as {0.user}'.format(client))



def funcEpicJSON():
  #defines the var "photoJSON" makes it a global var
  global epicJSON
  #gets the raw data from the ENDPOINT and defines it to var "photo"
  epic = requests.get("https://api.nasa.gov/EPIC/api/natural?api_key=9qfkXvI7DmXy3JH12ijwavhsMWy9MXEygFcv04Np")
  # processes the raw data into JSON
  epicJSON = json.loads(epic.text)
  #return the JSON
  return(epicJSON)

def epicDate():
  #calles the function to get the function
  funcEpicJSON()
  #parces the JSON to get "hdurl"
  epicDate = epicJSON[0]['date']
  #return "photoURI as the result of the function"
  return(epicDate)

def epicImageID():
  #calles the function to get the function
  funcEpicJSON()
  #parces the JSON to get "hdurl"
  epicImageID = epicJSON[0]['image']
  #return "photoURI as the result of the function"
  return(epicImageID)

def epicYearFunc():
  global epicYear
  epicYear = epicDate()[0:4]
  return(epicYear)

def epicMonthFunc():
  global epicMonth
  epicMonth = epicDate()[5:7]
  return(epicMonth)

def epicDayFunc():
  global epicDay
  epicDay = epicDate()[8:10]
  return(epicDay)

def fetchEPICImage():
  YEAR = epicYearFunc()
  MONTH = epicMonthFunc()
  DAY = epicDayFunc()
  IMAGE_ID = epicImageID()
  URL_EPIC = "https://api.nasa.gov/EPIC/archive/natural/"
  URL_EPIC = URL_EPIC + YEAR +'/' + MONTH + '/'+DAY
  URL_EPIC = URL_EPIC + '/png'
  URL_EPIC = URL_EPIC + '/' + IMAGE_ID + '.png'
  URL_EPIC = URL_EPIC + '?api_key=DEMO_KEY'
  return(URL_EPIC)

def funcPhotoJSON():
  #defines the var "photoJSON" makes it a global var
  global photoJSON
  #gets the raw data from the ENDPOINT and defines it to var "photo"
  photo = requests.get("https://api.nasa.gov/planetary/apod?api_key=9qfkXvI7DmXy3JH12ijwavhsMWy9MXEygFcv04Np")
  # processes the raw data into JSON
  photoJSON = json.loads(photo.text)
  #return the JSON
  return(photoJSON)

def dailyAstroURI():
  #calles the function to get the function
  funcPhotoJSON()
  #parces the JSON to get "hdurl"
  photoURI = photoJSON["hdurl"]
  #prints the output
  #print(photoURI)
  #return "photoURI as the result of the function"
  return(photoURI)

#gets the title of the photo
def dailyAstroTitle():
  #calles the function to get the function
  funcPhotoJSON()
  #parces the JSON to get "title"
  photoTitle = photoJSON["title"]
  #prints the output
  #print(photoTitle)
  #return "photoURI as the result of the function"
  return(photoTitle)

#gets the description of the photo
def dailyAstroExplanation():
  #calles the function to get the function
  funcPhotoJSON()
  #parces the JSON to get "explanation"
  photoExplanation = photoJSON["explanation"]
  #prints the output
  #print(photoExplanation)
  #return "photoURI as the result of the function"
  return(photoExplanation)

#gets the name of the copyright holder
def dailyAstroCopyright():
  #makes the global var "photoCopyright"
  global photoCopyright
  #calles the function to get the function
  funcPhotoJSON()
  #parces the JSON to get "copyright"
  #photoCopyright = photoJSON["copyright"]
  #prints the output
  #print(photoCopyright)
  #return "photoURI as the result of the function"
  return('_*National Aeronautics and Space Administration*_')

def explanationFirst500():
  limitPrompt = "[_**...READ MORE**_](https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY)"
  #defines "limatedExplanation" as a global variable
  global limatedExplanation 
  # makes limatedExplanation equal to the function dailyAstroExplanation()
  limatedExplanation = dailyAstroExplanation()
  limatedExplanation = limatedExplanation[0:950]
  #print(limatedExplanation)
  return(f'{limatedExplanation} {limitPrompt}')

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def iss_number():
  iss = requests.get("http://api.open-notify.org/astros.json")
  issJson = json.loads(iss.text)
  issNumber = issJson["number"]
  return(f'{issNumber} Currently People on the International National Space Station')

@client.event
async def on_message(message):
  print('message')
  if message.author == client.user:
    return

  if message.content.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('!hello'):
    quote = get_quote()
    await message.channel.send('hello')

  if message.content.startswith('!issnumber'):
    quote = get_quote()
    await message.channel.send(iss_number())
    print("iss_number_request")

  if message.content.startswith('!ryanhelp'):
    embed=discord.Embed(title="Ryan Bot", description="_Ryan Bot commands in this server start with `!`_", color=0x919191)
    embed.set_thumbnail(url="https://cdn.glitch.com/8e643391-5d6c-45c3-bdf9-496a8701e0d1%2FScreen%20Shot%202021-02-19%20at%208.46.30%20PM.png?v=1613785603454")
    embed.add_field(name="!earthphoto", value="Gets The Latest Photo of Earth From The NOAA DSCOVR Spacecraft", inline=True)
    embed.add_field(name="!dailyphoto", value="Gets The Daily Photo of The Day Form NASA", inline=True)
    embed.add_field(name="!issnumber", value="Gets The Number of Astronauts Currently on The International Space Startion", inline=True)
    embed.add_field(name="!inspire", value="Gets An Inspiration Quote", inline=True)
    await message.channel.send(embed=embed)
    
  if message.content.startswith('!dailyphoto'):
        embed=discord.Embed(title=dailyAstroTitle(), url=dailyAstroURI(), description=dailyAstroCopyright(), color=0xff2600)
        embed.set_thumbnail(url=dailyAstroURI())
        embed.add_field(name="Explanation", value=explanationFirst500(), inline=False)
        await message.channel.send(embed=embed)
        print("Daily Photo Called")

  if message.content.startswith('!earthphoto'):
    embed=discord.Embed(
      title="The Latest Photo of The Earth", url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/NASA_Worm_logo.svg/1024px-NASA_Worm_logo.svg.png", description="This image was taken by NASA's EPIC camera onboard the NOAA DSCOVR spacecraft...*Image Updates Every ~2 Hours*", color=0x669c35)
    
    embed.set_image(url=fetchEPICImage())
    
    await message.channel.send(embed=embed)

keep_alive()
client.run(os.getenv('TOKEN'))