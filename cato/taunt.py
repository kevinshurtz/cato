import yaml


def _taunts():
    with open('./dialog/taunts.yaml') as file:
        taunts = yaml.safe_load(file)
        content = [taunt for taunt in taunts['taunts']]

    return content


_threats = ['Hannibal']
_taunt_lines = _taunts()


def should_respond(content, author):
    pass


def make_reply(content, author):
    pass
