import discord
import os
import dotenv
import re
import functools
import textwrap
import random

dotenv.load_dotenv()
client = discord.Client()

admin_id = os.getenv('ADMIN_ID')

denoucements = [
    'Ceterum autem censeo Carthaginem esse delendam.'
]

wisdom = [
    'Those who are serious in ridiculous matters will be ridiculous in serious matters.',
    'If you are ruled by mind you are a king; if by body, a slave.',
    'I prefer to do right and get no thanks than to do wrong and receive no punishment.',
    'Wise men profit more from fools than fools from wise men; for the wise men shun the mistakes of fools, but fools do not imitate the successes of the wise.',
    'We cannot control the evil tongues of others; but a good life enables us to disregard them.',
    'After I\'m dead I\'d rather have people ask why I have no monument than why I have one.',
    'The hero saves us. Praise the hero! Now, who will save us from the hero?',
    'The worst ruler is one who cannot rule himself.',
    'I think the first virtue is to restrain the tongue; he approaches nearest to gods who knows how to be silent, even though he is in the right.',
    'Tis sometimes the height of wisdom to feign stupidity.',
    'An angry man opens his mouth and shuts his eyes.',
    'Anger so clouds the mind that it cannot perceive the truth.',
    'He who fears death has already lost the life he covets.',
    'I can pardon everybody\'s mistakes except my own.',
    'Patience is the greatest of all virtues.',
    'It is a difficult matter to argue with the belly since it has no ears.',
    'Speech is the gift of all, but the thought of few.',
    'Grasp the subject, the words will follow.',
    'Wise men learn more from fools than fools from the wise.',
    'Buy not what you want, but what you have need of; what you do not want is dear at a farthing.',
    'Even though work stops, expenses run on.'
]

carthigians = []

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}.')

def usage():
    greeting = 'Greetings Plebians.  I am Cato the Elder.'

    condescension = ' '.join([
        'Rarely do I condescend to those so far beneath my Senatorial rank,',
        'but I will do so this once as a gesture of republican virtue.'
    ])

    usage = 'I\'ll only interject at appropriate moments.  There are two.'
    detail_first = ' '.join([
        'The first and most important of my responsibilities is to challenge',
        'the Punic threat wherever I see it and to denounce the apologists of',
        'the Carthigian menace.  Their remarks will always be met with my',
        'customary reply.'
    ])
    detail_second = ' '.join([
        'The second is to share words of wisdom with all who wish to better',
        'themselves and grow in virtue.  Merely ask me for a quote, and I',
        'will happily offer some words of wit or sage advice.'
    ])

    final_greeting = 'I hope to tolerate your company.'

    return textwrap.dedent(f'''
        {greeting}\n
        {condescension}\n
        {usage}\n
        {detail_first}\n
        {detail_second}\n
        {final_greeting}
    ''')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    authorized = str(message.author.id) == admin_id
    msg = message.content

    def reduce_spotted(spotted, carthigian):
        return spotted or message.author.display_name == carthigian

    re_flags = re.IGNORECASE

    # Check if Cato needs an introduction
    introduce = re.search(r'introduc(?:e|tion)', msg, re_flags) and re.search(r"cato", msg, re_flags)

    # Add a Carthigian if a new Carthigian is spotted
    added = re.search(r'(?:new|another) carthigian (?:named|called) (\w+)\b', msg, re_flags)

    # Remove a Carthigian if a new Carthigian is removed
    removed = re.search(r'(?:killed|removed) carthigian (?:named|called) (\w+)\b', msg, re_flags)

    # Check if any Carthigians have been spotted
    spotted = functools.reduce(reduce_spotted, carthigians, False)

    # Check if anyone is interested 
    quotes = re.search(r"cato(?:'s)?", msg, re_flags) and re.search(r'quote(?:s|d)?', msg, re_flags)

    if introduce:
        await message.channel.send(usage())

    elif authorized and added:
        carthigians.append(added.group(1))

    elif authorized and removed:
        carthigians.remove(removed.group(1))

    elif spotted:
        await message.channel.send('Ceterum autem censeo Carthaginem esse delendam.')

    elif quotes:
        await message.channel.send(random.choice(wisdom))

client.run(os.getenv('TOKEN'))
