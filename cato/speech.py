import yaml

with open('./dialog/quotes.yaml') as file:
    quotes = yaml.safe_load(file)
    wisdom = [quote['content'] for quote in quotes['quotes']]
