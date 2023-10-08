import openai
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Set up the API key
openai.api_key = config['DEFAULT']['OPENAI_API_KEY']

# List all engines
engines = openai.Engine.list()

# Print the engines
for engine in engines["data"]:
    print(engine["id"])
