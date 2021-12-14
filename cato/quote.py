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

    name_matches = re.search(r"cato(?:'s)?", content, re_flags)
    quote_matches = re.search(r'quote(?:s|d)?', content, re_flags)

    return name_matches and quote_matches


def make_reply():
    return random.choice(_quote_lines)
