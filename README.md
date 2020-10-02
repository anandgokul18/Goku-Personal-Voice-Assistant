# Goku-Personal-Voice-Assistant

A project to build an smart voice assistant using Python. Goku is named after the protogonist of the famous DragonBallZ series and Goku can interact with human though voice to perform basic tasks.

It can be loaded onto a Raspberry Pi to have an always on voice assistant similar to Alexa or Google Home. It also has smart home capability and can controll smart light bulbs.


## About Goku

Goku is a smart personal voice assistant that can do various tasks and can be controlled by your voice. 

It supports understanding natural language and is on the lookout for trigger words to activate abilites.

Goku uses third-party APIs for which keys need to be obtained (free of cost) such as for Wolfram Alpha and OpenWeather. Once you have the keys, just fill them in the python script.

On start, it says: "<code>I am your AI personal assistant Goku. Please give me a few minutes to get ready</code>"

### Abilities

1. Human: <code>What is the time now? </code>

2. Human: <code>What is today's date? </code>

3. Human: <code>Who created you? xD </code>

4. Human: <code>Tell me about yourself! </code>

5. Human: <code>What's the weather like? </code>

6. Human: <code>Search wikipedia for game of thrones </code>

7. Human: <code>Who is Bill Gates? </code>

8. Human: <code>Read today's news </code>

9. Human: <code>Search</code>
   Goku: <code>Dusting my computational prowess. What do you want to know? </code>
   Human: <code>How many countries does the Nile river flow through?</code>
   
10. Human: <code>Search</code>
   Goku: <code>Dusting my computational prowess. What do you want to know? </code>
   Human: <code>What is the integral of sinx? </code>
   
11. Human: <code>He me fall asleep</code>
    Goku: <code>Ok, let me play you some white noise to help you fall asleep. I will turn it off automatically after 30 mins for you</code>

12. Human: <code>It's my birthday today</code>
    Goku: !!!Sings happy birthday!!!
    
13. Human: <code> tell me a joke </code>
    Goku: !!!Tells a random joke!!!
    
14. Human: <code>What is the meaning of the word 'indentation' </code>

15. Human: <code>What is the opposite of the word 'life'</code>

16. Human: <code>Translate 'range' to spanish </code>

17. Human: <code>Turn off all lights</code>
    Goku: !!! Turns off all Meross smart lights !!!
    
18. Human: <code>Turn on all lights</code>
    Goku: !!! Turns off all Meross smart lights !!!
    
19. Human: <code>Set light color to green</code>
    Goku: !!! Turns all Meross smart lights color to green !!!
    
20. Human: <code>Good bye!</code>
    Goku: <code>Your personal assistant Goku is shutting down,Good bye </code>

## Libraries required to be installed using Pip Command:

Check out the requirements.txt file and do a 

  <code> pip install requirements.txt </code>
  
## Smart light bulbs:

The smart light bulb currently supported is Meross bulbs which can be bought for low cost on Amazon. Since, Meross has thrid-party APIs that allow light bulb controls, I have added that as proof of concept. You can add your own light bulbs or other smart appliances in similar manner.
