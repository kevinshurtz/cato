# Cato

A fun Discord bot to share the wisdom and wit of Cato the Elder.

## Background

### Who is Cato the Elder?

Cato the Elder served as a Roman Senator between the second and third Punic
Wars and was great grandfather to Cato the Younger, a legendary political
opponent of Julias Caesar.

Cato the Elder is well known for his severe Roman manners, opposition to
Hellenization, and his strong insistence upon the destruction of
Carthage.

The final point above is perhaps his most famous feature.  After becoming
convinced that a newly ascendant Carthage was Rome's greatest geopolitical
threat, Cato concluded every Senate speech - regardless of topic - with the
phrase, "ceterum autem censeo Carthaginem esse delendam", or "furthermore, I
consider that Carthage must be destroyed."

### Why was this project made?

This project was initially created as a fun way to toy with my friends during a
game of Sid Meier's Civilization VI.

In particular, I thought it would be amusing to have Cato fix his ire on my
Phoenician counterparts as the game unfolded.

## Getting Started

To get started running the Bot on your local machine, create a virtual
environment for the project and install the dependencies in
`requirements.txt`.

```bash
# Create and enter a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the dependencies for the project
pip install -r requirements.txt
```

Now, you should be able to run the project without any difficulty.

```bash
# Start the Discord bot server
python cato/main.py
```

At the time of this writing, the Cato bot is a simple script, but I'd
like to eventually convert it into an executable package.