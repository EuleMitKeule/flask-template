from argparse import ArgumentParser, Namespace
import logging
import os
from flask import Flask

from common import config, db, ma, cors, sio, scheduler
from const import APP_NAME, DEFAULT_CONFIG_PATH
from events import *
from models import *

def create_app(config_path: str) -> Flask:
    app = Flask(__name__)

    config.load(config_path)

    logging.info(f"Starting {APP_NAME}...")
    logging.info(f"Host: {config.config_model.networking.host}")
    logging.info(f"Port: {config.config_model.networking.port}")

    config.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    sio.init_app(app, cors_allowed_origins="*") # TODO fix CORS policy
    scheduler.init_app(app)

    with app.app_context():
        BaseModel.set_session(db.session)

        if config.config_model.sqlite.recreate:
            logging.info("Recreating database...")
            db.drop_all()
            db.session.commit()

        db.create_all()
        db.session.commit()

    return app


if __name__ == "__main__":
    os.system("cls" if os.name=="nt" else "clear")

    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument("-c", "--config", dest="config_path", help="The path to the configuration file.", default=DEFAULT_CONFIG_PATH)
    args: Namespace = arg_parser.parse_args()
    config_path: str = args.config_path
    
    app: Flask = create_app(config_path)

    scheduler.start()
    sio.run(app, host=config.config_model.networking.host, port=config.config_model.networking.port)
