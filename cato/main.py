import discord
import logging
import os
import dotenv
import re
import functools
import textwrap
import random
import yaml
from . import quote

dotenv.load_dotenv()
client = discord.Client()

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(levelname)s] [%(asctime)s] [%(filename)s] %(message)s"))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

admin_id = os.getenv('ADMIN_ID')

denoucements = [
    'Ceterum autem censeo Carthaginem esse delendam.'
]

carthaginians = []

targets = []

generals = ['Hannibal', 'Alexandros']

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
    logger.info("Log in as %s", client.user)

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
        'the Carthaginian menace.  Their remarks will always be met with my',
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
    logger.info("Receive message %s", message.id)

    if message.author == client.user:
        return

    authorized = str(message.author.id) == admin_id
    msg = message.content

    def reduce_spotted(spotted, carthaginian):
        return spotted or message.author.display_name == carthaginian

    re_flags = re.IGNORECASE

    # Check if Cato needs an introduction
    introduce = re.search(r'introduc(?:e|tion)', msg, re_flags) and re.search(r"cato", msg, re_flags)

    # Add a Carthaginian if a new Carthaginian is spotted
    added = re.search(r'(?:new|another) Carthaginian (?:named|called) "([A-Za-z0-9 ]+)"', msg, re_flags)

    # Remove a Carthaginian if a new Carthaginian is removed
    removed = re.search(r'(?:killed|removed) Carthaginian (?:named|called) "([A-Za-z0-9 ]+)"', msg, re_flags)

    # Check if any Carthaginians have been spotted
    spotted = functools.reduce(reduce_spotted, carthaginians, False)

    # Check if Hannibal or his associates are in view
    gens = functools.reduce(reduce_spotted, generals, False)

    if introduce:
        logger.info("Introduce Cato")
        await message.channel.send(usage())

    elif authorized and added:
        logger.info("Add Carthaginian %s", added.group(1))
        carthaginians.append(added.group(1))

    elif authorized and removed:
        logger.info("Remove Carthaginian %s", added.group(1))
        carthaginians.remove(removed.group(1))

    elif spotted:
        logger.info("Report enemy")
        await message.channel.send('Ceterum autem censeo Carthaginem esse delendam.')

    elif gens:
        logger.info("Taunt enemy")
        await message.channel.send(random.choice(retorts))

    elif quote.should_respond(msg):
        logger.info("Deliver quote")
        await message.channel.send(quote.make_reply(msg))

client.run(os.getenv('TOKEN'))
