import discord
import os
import dotenv
import re
import functools
import textwrap
import random
import yaml

dotenv.load_dotenv()
client = discord.Client()

admin_id = os.getenv('ADMIN_ID')

denoucements = [
    'Ceterum autem censeo Carthaginem esse delendam.'
]

with open('./dialog/quotes.yaml') as file:
    quotes = yaml.safe_load(file)
    wisdom = [quote['content'] for quote in quotes['quotes']]

carthigians = []

targets = []

generals = ['Hannibal']

retorts = [
    'I fart in your general direction!',
    'Your mother was a hamster, and your father smelled of elderberries!',
    'Mind your own business!',
    'You don\'t frigthen us, Carthaginian pig-dogs!',
    'Go and boil your bottoms, sons of a silly person.',
    'I blow my nose at you, so-called Hannibal general, you and your silly Numidian caaaavlry.'
]

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
    added = re.search(r'(?:new|another) carthaginian (?:named|called) "([A-Za-z ]+)"', msg, re_flags)

    # Remove a Carthigian if a new Carthigian is removed
    removed = re.search(r'(?:killed|removed) carthaginian (?:named|called) "([A-Za-z ]+)"', msg, re_flags)

    # Check if any Carthaginians have been spotted
    spotted = functools.reduce(reduce_spotted, carthigians, False)

    # Check if Hannibal or his associates are in view
    gens = functools.reduce(reduce_spotted, generals, False)

    # Check if anyone is interested in some wisdom
    quotes = re.search(r"cato(?:'s)?", msg, re_flags) and re.search(r'quote(?:s|d)?', msg, re_flags)

    if introduce:
        await message.channel.send(usage())

    elif authorized and added:
        carthigians.append(added.group(1))

    elif authorized and removed:
        carthigians.remove(removed.group(1))

    elif spotted:
        await message.channel.send('Ceterum autem censeo Carthaginem esse delendam.')

    elif gens:
        await message.channel.send(random.choice(retorts))

    elif quotes:
        await message.channel.send(random.choice(wisdom))

client.run(os.getenv('TOKEN'))
