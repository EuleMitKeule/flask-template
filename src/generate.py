import json
from argparse import ArgumentParser, Namespace
import logging

from flask import Flask
from app import create_app
from const import DEFAULT_CONFIG_PATH, DEFAULT_DATE_FORMAT, DEFAULT_LOG_FORMAT, DEFAULT_SPEC_PATH
from common import api


arg_parser: ArgumentParser = ArgumentParser()
arg_parser.add_argument("-o", "--output", dest="output_path", help="The path to the generated specification.", default=DEFAULT_SPEC_PATH)
arg_parser.add_argument("-c", "--config", dest="config_path", help="The path to the configuration file.", default=DEFAULT_CONFIG_PATH)
args: Namespace = arg_parser.parse_args()
output_path: str = args.output_path
config_path: str = args.config_path

logging.basicConfig(
    format=DEFAULT_LOG_FORMAT,
    datefmt=DEFAULT_DATE_FORMAT,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)

logging.info("Starting the specification generator...")
logging.info("Creating application...")
logging.disable(logging.INFO)

app: Flask = create_app(config_path)

logging.disable(logging.NOTSET)
logging.info("Application created.")

logging.info("Generating specification...")

api_spec: dict = api.spec.to_dict()
api_json: str = json.dumps(api_spec, indent=4)

logging.info("Specification generated.")
logging.info("Writing specification to file...")

with open(output_path, "w") as f:
    f.write(api_json)

logging.info("Specification written to file.")
