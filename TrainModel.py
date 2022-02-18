from spacy.cli.train import train

train("./config.cfg", "./output", overrides={"paths.dev": "./data/binaryData/train.spacy"})
