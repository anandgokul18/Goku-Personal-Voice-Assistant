# Core Imports
import speech_recognition as sr
import os
import datetime
import warnings
import calendar
import random
import json
import requests
import pyttsx3
import multiprocessing
import asyncio
import time

# Skill Jutsu imports
from newsapi import NewsApiClient
import wolframalpha
import wikipedia
from playsound import playsound
from joke import jokes
from PyDictionary import PyDictionary
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
from meross_iot.model.enums import OnlineStatus

"""CONFIDENTIAL API KEYS"""
# REMOVE THIS BEFORE MAKING CODE PUBLIC
OPENWEATHERMAP_KEY = "XXX"
WOLFRAMALPHA_KEY = "XXX"
NEWSAPI_KEY = 'XXX'
MEROSS_USERNAME = 'XXX@YYY.com'
MEROSS_PWD = 'XXX'

USER = "USERNAME_HERE"


# Ignore any warning messages
# warnings.filterwarnings('ignore')

# Loading pyttsx3 TTS engine
engine = pyttsx3.init('nsss')
"""SETTING VOICE"""
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[1].id')

""" RATE"""
rate = engine.getProperty(
    'rate')   # getting details of current speaking rate
engine.setProperty('rate', 195)     # setting up new voice rate


# Clear the console screen

def clearConsole():

    return os.system('clear')

# Function to get the virtual assistant response


def visualUI(userinput):

    line1 = """
-----------------------
"""

    baseimage = r'''
-----------------------
               `\-.   `
                      \ `.  `
                       \  \ |
              __.._    |   \.          G O K U SAYS...
       ..---""     " . |    Y
         "-.          `|    |
            `.               `""--.
              \                    ".
               \                     \__. . -- -  .
         .-""""", ,            """"""---...._
    .-"___        ,'/  ,'/ ,'\          __...---"""
    "". / ._\_(, (/_. 7, -.    ""---...__
                  _... > -  P""6=`_/"6""   6)    ___...--"""
                  ""--._ \`- -') `---'   9'  _..--"""
                  " \""/_  """ /`-.--""
                  `. --- .'   \_
                  `." _.-'     | "-., -------._
                  ..._../""   . / .-'    .-"""-.
            ,--""", '...\` _./.----"".' / /'       `-
        _.-(|\    `/" _____..-' /    /      _.-""`.
             / | / . ^ ---""""       ' /    /     ,'  ".   \
      (    /    (  .           _ ' /'    /    ,/      \   )
      (`. |     `\   - - - - ~   /'      (   /         .  |
       \.\|       \            /'        \  |`.           /
       /.'\\      `\         /'           "-\         .  /\
      /,   (        `\     /'                `.___..-      \
     | |    \         `\_/'                  //      \.     |
    '''

    print(line1+userinput+baseimage)


def speak(text, stopVisualUIAndClearScrn=None):
    # print("Response: " + text)
    if not stopVisualUIAndClearScrn:
        clearConsole()
        visualUI(text)
    engine.say(text)
    engine.runAndWait()


def wishTheUser():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        # print("Hello,Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        # print("Hello,Good Afternoon")
    else:
        speak("Hello, Good Evening")
        # print("Hello,Good Evening")


def takeCommand(mode=None):
    playsound('audio/active.mp3')
    time.sleep(1)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            statement = statement.replace('google', 'Goku! ')
            statement = statement.replace('Google', 'Goku! ')
            print(f"user said:{statement}\n")

        except sr.UnknownValueError:
            if mode == "inside_skill":
                speak("Pardon me, please say that again")
            # print('Query Input: Google Speech Recognition could not understand')
            return "None"
        except sr.RequestError:
            if mode == "inside_skill":
                speak("Pardon me, please say that again")
            # print('Query Input: Request error from Google Speech Recognition')
            return "None"
        except Exception:
            return "None"
        return statement.lower()


"""
A function to check for wake word(s)

"""


def wakeWord(text):
    WAKE_WORDS = ['hey goku', 'okay goku', 'hi goku', 'goku', 'google']
    text = text.lower()  # Convert the text to all lower case words
  # Check to see if the users command/text contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
  # If the wake word was not found return false
    return False


"""
Function to return a random greeting response if user provided a greeting

"""


def greeting(text):
    # Greeting Inputs
    GREETING_INPUTS = ['hi', 'hey', 'hola', 'greetings', 'wassup', 'hello']
    # Greeting Response back to the user
    GREETING_RESPONSES = ['howdy', 'whats up dawg',
                          f'hello {USER}', 'hey there', f"how's it going {USER}"]
    # If the users input is a greeting, then return random response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    # If no greeting was detected then return an empty string
    return None


########## SKILLS START HERE ##############

def timeJutsu():
    # AM/PM Calculation
    hour = int(str(datetime.datetime.now().strftime("%H")))
    ampm = "AM"
    if hour >= 12:
        ampm = "PM"

    strTime = datetime.datetime.now().strftime("%I:%M")
    return f"the time is {strTime} {ampm}"


def dateJutsu():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]  # e.g. Monday
    monthNum = now.month
    dayNum = now.day
    month_names = ['January', 'February', 'March', 'April', 'May',
                   'June', 'July', 'August', 'September', 'October', 'November',
                   'December']
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th',
                      '7th', '8th', '9th', '10th', '11th', '12th',
                      '13th', '14th', '15th', '16th', '17th',
                      '18th', '19th', '20th', '21st', '22nd',
                      '23rd', '24th', '25th', '26th', '27th',
                      '28th', '29th', '30th', '31st']

    return 'Today is ' + weekday + ' ' + month_names[monthNum - 1] + ' the ' + ordinalNumbers[dayNum - 1] + '.'


def creatorInfo():

    clearConsole()

    baseimage_c3po = r""".


-----------------

=============================================
||             Goku <3 Master Anand         ||
==============================================

-------------

   \
    \
       /~\
      |oo )
      _\=/_
     /     \
    //|/.\|\\
   ||  \_/  ||
   || |\ /| ||
    # \_ _/  #
      | | |
      | | |
      []|[]
      | | |
     /_]_[_\
    """

    print(baseimage_c3po)

    creator_praise = ['I was built by the wise Mister Anand. He is my guru and I am his Padawan.',
                      'My daddy is master Anand Gokul. He is the bestest',
                      'I am forever indebted to Anand Gokul for making me. He is awesome']
    return random.choice(creator_praise)


def aboutMe():

    clearConsole()

    print(r"""
    _______________                        |*\_/*|________
  |  ___________  |     .-.     .-.      ||_/-\_|______  |
  | |           | |    .****. .****.     | |           | |
  | |   0   0   | |    .*****.*****.     | |   0   0   | |
  | |     -     | |     .*********.      | |     -     | |
  | |   \___/   | |      .*******.       | |   \___/   | |
  | |___     ___| |       .*****.        | |___________| |
  |_____|\_/|_____|        .***.         |_______________|
    _|__|/ \|_|_.............*.............._|________|_
   / ********** \                          / ********** \
 /  ************  \                      /  ************ \
--------------------                    --------------------
    """)
    return "I am Goku, the personal assistant created by Master Anand. I can perform various tasks like telling the weather, reading news and lot more. I am always learning new things. Go ahead and explore me to find out about all the things I can do "


def weatherJutsu():
    api_key = OPENWEATHERMAP_KEY
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    speak("whats the city name")
    city_name = "None"
    while city_name == "None":
        city_name = takeCommand(mode="inside_skill")
    complete_url = base_url+"appid="+api_key+"&q="+city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature_kelvin = y["temp"]
        current_temperature_celsius = round(
            ((current_temperature_kelvin) - 273.15), 2)
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        result = (" Temperature is " +
                  str(current_temperature_celsius) + " Celsius "
                  "\n humidity in percentage is " +
                  str(current_humidiy) +
                  "\n description is " +
                  str(weather_description))
        return result

    else:
        return "City Not Found "


def wikipediaJutsu(statement, mode):

    if mode == "direct_wiki":
        statement = statement.split("search wikipedia for")[1]
        results = wikipedia.summary(statement, sentences=3)
    elif mode == "person_search":
        statement = statement.split("who is")[1]
        results = wikipedia.summary(statement, sentences=3)
    else:
        results = wikipedia.summary(statement, sentences=3)
    speak("According to Wikipedia, ")
    return results


def knowledgeQAJutsu():
    speak("Dusting my computational prowess. What do you want to know?")
    question = "None"
    while question == "None":
        question = takeCommand(mode="inside_skill")
    client = wolframalpha.Client(WOLFRAMALPHA_KEY)
    res = client.query(question)
    answer = next(res.results).text
    return answer


def newsJutsu():
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

    top_headlines = newsapi.get_top_headlines(language='en')
    articles = top_headlines['articles']

    # Rate of speech
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 220)

    for i in range(0, len(articles)):
        if i > 5:
            speak("Hey, are you still listening?")
            response = "None"
            while response == "None":
                response = takeCommand(mode="inside_skill")
            if "yes" in response:
                pass
            else:
                return "Alright"

        if(articles[i]['title'] != None and articles[i]['description'] != None):
            # Either title or description
            speak(articles[i]['description'])
            # description = articles[i]['description'].replace("\n"," ")
            speak("Coming up next...")

        return "That's all for now"

    # Rate of speech
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 195)


def haremJutsu():
    phrases = ['Tonight I want you to take control.',
               "The landscapers are coming over today to trim the bush.",
               "Say what you want, but my favorite animal is definitely the beaver",
               "I wonder what happens to nuts in space",
               "I was expecting maybe four inches, but he gave me more like 12. I was talking about my first trip to the Subway, you dirty dirty mind",
               "the girl tried everything but he just kept slipping out",
               "I was surprised by the sheer power of the sea men."]
    return random.choice(phrases)


def birthdayJutsu():
    clearConsole()

    message = r'''
           ~                  ~
     *                   *                *       *
                  *               *
  ~       *                *         ~    *
              *       ~        *              *   ~
                  )         (         )              *
    *    ~     ) (_)   (   (_)   )   (_) (  *
           *  (_) # ) (_) ) # ( (_) ( # (_)       *
              _#.-#(_)-#-(_)#(_)-#-(_)#-.#_
  *         .' #  # #  #  # # #  #  # #  # `.   ~     *
           :   #    #  #  #   #  #  #    #   :
    ~      :.       #     #   #     #       .:      *
        *  | `-.__                     __.-' | *
           |      `````"""""""""""````` | *
     * | | | |\ | ~) | ~)\ / |
           | |~ | |~\| ~ | ~ | |       ~
   ~ * | | *
           | |~) | |~)~ | ~ | | | ~\|\ \ / | *
   *    _.- | |~) | |~\ | |~ | | / |~\ | |-._
      .'   '.      ~            ~           .'   `. *
  goku:      `-.__                     __.-':
       `.         `````"""""""""""`````         .'
         `-.._                             _..-'
              `````""""-----------""""`````
    '''
    print(message)
    playsound('audio/birthday.mp3')


def dictionaryJutsu(statement, mode):

    dictionary = PyDictionary()

    if mode == "dictionary":
        statement = statement.split("word")[1].strip()

        # If the word is a noun
        try:
            meaning = dictionary.meaning(statement)['Noun'][0]
            speak(f"The noun meaning is {meaning}")
        except:
            pass
        try:
            meaning = dictionary.meaning(statement)['Verb'][0]
            speak(f"The verb meaning is {meaning}")
        except:
            pass

    if mode == "antonym":
        statement = statement.split("word")[1]

        list_of_antonyms = dictionary.antonym(statement)
        speak(f"The antonyms of the word are {str(list_of_antonyms[:2])}")

    if mode == "translate":
        statement = statement.split('translate')[1]
        phrase = statement.split('to')[0].strip()
        targetLang = statement.split('to')[1].strip()

        languageCodeMapping = {'spanish': 'es', 'arabic': 'ar',
                               'french': 'fr', 'german': 'de', 'hindi': 'hi', 'chinese': 'zh-CN'}

        result = dictionary.translate(phrase, languageCodeMapping[targetLang])

        speak(f"The meaning of the word {phrase} in {targetLang} is {result}")


def spotifyJutsu():
    speak("This functionality is currently unsupported")
    return


async def merossIotToggleSkill(mode):
    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=MEROSS_USERNAME, password=MEROSS_PWD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Retrieve all the MSS310 devices that are registered on this account
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_type="msl120d")

    if len(plugs) < 1:
        # print("No msl120d bulbs found...")
        speak("Sorry, no smart bulbs found or they are unresponsive")
    else:
        for plug in plugs:
            # Turn it on channel 0
            # Note that channel argument is optional for MSS310 as they only have one channel
            # dev = plugs[0]

            # Update device status: this is needed only the very first time we play with this device (or if the
            #  connection goes down)
            await plug.async_update()

            if mode == "turnon":
                print(f"Turning on {plug.name}...")
                await plug.async_turn_on(channel=0)
            # print("Waiting a bit before turing it off")
            # await asyncio.sleep(5)
            elif mode == "turnoff":
                print(f"Turing off {plug.name}")
                await plug.async_turn_off(channel=0)

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()


async def merossIotLightColorSkill(color=None):

    # Setup the HTTP client API from user-password
    http_api_client = await MerossHttpClient.async_from_user_password(email=MEROSS_USERNAME, password=MEROSS_PWD)

    # Setup and start the device manager
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()

    # Discover devices.
    await manager.async_device_discovery()

    # Print them
    # meross_devices = manager.find_devices()
    # print("I've found the following devices:")
    # for dev in meross_devices:
    #    print(f"- {dev.name} ({dev.type}): {dev.online_status}")

    # Retrieve the MSL120 devices that are registered on this account
    plugs = manager.find_devices(
        device_type="msl120d")  # , online_status=OnlineStatus.ONLINE)

    if len(plugs) < 1:
        # print("No online msl120d smart bulbs found...")
        speak("Sorry, no smart bulbs found or they are unresponsive")
    else:
        for plug in plugs:
            # Let's play with RGB colors. Note that not all light devices will support
            # rgb capabilities. For this reason, we first need to check for rgb before issuing
            # color commands.
            # dev = plugs[0]

            # Update device status: this is needed only the very first time we play with this device (or if the
            #  connection goes down)
            await plug.async_update()

            if not plug.get_supports_rgb():
                print("Unfortunately, this device does not support RGB...")
            else:
                # Check the current RGB color
                # current_color = dev.get_rgb_color()
                # print(f"Currently, device {dev.name} is set to color (RGB) = {current_color}")
                # Randomly chose a new color
                # rgb = randint(0, 255), randint(0, 255), randint(0, 255)
                # print(f"Chosen random color (R,G,B): {rgb}")
                if color:
                    await plug.async_set_light_color(luminance=100, rgb=color)
                else:
                    # White color
                    await plug.async_set_light_color(luminance=100, temperature=75)
                # print("Color changed!")

    # Close the manager and logout from http_api
    manager.close()
    await http_api_client.async_logout()

########## SKILLS END HERE ##############


if __name__ == '__main__':

    speak("I am your AI personal assistant Goku. Please give me a few minutes to get ready")

    wishTheUser()

    # Infinite loop to keep the assistant always ON
    while True:

        # Checking for the wake word/phrase and doing any further processing only if Wake word found
        statement = takeCommand()
        if (wakeWord(statement) == True):
            # Check for greetings by the user
            greeting_result = greeting(statement)
            if greeting_result:
                speak(greeting_result)

            if 'time' in statement:
                speak(timeJutsu())

            elif 'date' in statement:
                speak(dateJutsu())

            elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement or "who is your daddy" in statement:
                speak(creatorInfo(), stopVisualUIAndClearScrn='stop')

            elif 'who are you' in statement or 'what can you do' in statement or 'tell me about yourself' in statement:
                speak(aboutMe(), stopVisualUIAndClearScrn='stop')

            elif "weather" in statement:
                speak(weatherJutsu())

            elif 'wikipedia' in statement:
                # Example Usage: Search Wikipedia for Game of thrones
                speak('Searching Wikipedia ')
                speak(wikipediaJutsu(statement, mode="direct_wiki"))

            elif "who is" in statement in statement:
                # Example Usage: Who is Bill gates
                speak(wikipediaJutsu(statement, mode="person_search"))

            elif "news" in statement:
                speak(newsJutsu())

            elif "search" in statement or "calculate" in statement:
                speak(knowledgeQAJutsu())

            elif "dirty" in statement or "naughty" in statement:
                speak(haremJutsu())

            elif "good bye" in statement or "ok bye" in statement or "goodbye" in statement or "stop" in statement:
                speak('your personal assistant Goku is shutting down,Good bye')
                print('your personal assistant Goku is shutting down,Good bye')
                break

            elif "sleep" in statement or "asleep" in statement:
                speak('Ok, let me play you some white noise to help you fall asleep. I will turn it off automatically after 30 mins for you')
                # playsound('audio/whitenoise.mp3')
                p = multiprocessing.Process(
                    target=playsound, args=("audio/whitenoise.mp3",))
                p.start()
                input("press ENTER to stop playback")
                p.terminate()

            elif "birthday" in statement:
                birthdayJutsu()

            elif "jokes" in statement or "joke" in statement:
                joke = None
                while joke == None:
                    joke = random.choice(
                        [jokes.geek(), jokes.icanhazdad(), jokes.chucknorris(), jokes.icndb()])
                speak(joke)

            elif "meaning" in statement:
                # Example Usage: What is the meaning of the word 'indentation'
                dictionaryJutsu(statement, mode="dictionary")

            elif "antonym" in statement or "opposite" in statement:
                # Example Usage: What is the opposite of the word 'life'
                dictionaryJutsu(statement, mode="antonym")

            elif "translate" in statement:
                # Example Usage: Translate 'range' to spanish
                dictionaryJutsu(statement, mode="translate")

            elif "alexa" in statement or "cortana" in statement:
                speak("Hmm. She is cool, but I got all the swagger.")

            elif "turn off light" in statement or "turn off all light" in statement:
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                loop.run_until_complete(merossIotToggleSkill(mode="turnoff"))
                loop.close()

            elif "turn on light" in statement or "turn on all light" in statement:
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    merossIotLightColorSkill(color=None))
                loop.close()

            elif "set light color to" in statement or "set lights to" in statement or "set all lights to" in statement or "set light bulb color to" in statement:

                statement = statement.split("to")[1].strip()
                color_to_rgb_mapping = {'red': (255, 0, 0), 'green': (
                    0, 255, 0), 'blue': (0, 0, 255)}
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                loop.run_until_complete(
                    merossIotLightColorSkill(color=color_to_rgb_mapping[statement]))
                loop.close()

            elif "play" in statement:
                # Spotify Jutsu
                spotifyJutsu()

            elif "shopping list" in statement:
                # Retrieve and add to a web service like Google Keep
                pass

            elif "alarm" in statement:
                # Set alarm on a more dependent service like Apple Clock or Google Home
                pass

            elif "remainder" in statement:
                # Add a remainder to google calendar
                pass

        # if no wake word, give small audible feedback
        else:
            # speak("shh")
            pass
