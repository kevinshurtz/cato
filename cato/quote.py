import re
import random
import yaml

def _quotes():
    with open('./dialog/quotes.yaml') as file:
        quotes = yaml.safe_load(file)
        content = [quote['content'] for quote in quotes['quotes']]

    return content


# Store the quotes in a package variable to avoid unneeded IO
_quote_lines = _quotes()


def should_respond(content):
    re_flags = re.IGNORECASE
    quotes = re.search(r"cato(?:'s)?", content, re_flags) and re.search(r'quote(?:s|d)?', content, re_flags)

    return True if quotes else False


def make_reply(content):
    return random.choice(_quote_lines)
