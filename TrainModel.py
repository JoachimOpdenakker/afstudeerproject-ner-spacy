# from spacy.cli.train import train

# # train("./config.cfg", "./output", overrides={"paths.dev": "./data/binaryData/train.spacy"})
# train("./config.cfg", "./model")

import os
os.system("python3 -m spacy train ./config/config.cfg --output ./model --code ./config/CustomTokenizer.py")
