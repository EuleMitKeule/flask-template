from argparse import ArgumentParser, Namespace
import logging
import os
from flask import Flask

from src.common import config, db, ma, cors, sio, scheduler, api, guard, csrf
from src.const import APP_NAME, DEFAULT_CONFIG_PATH

config_path: str = os.environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)

config.load(config_path)

app = Flask(__name__)

config.init_app(app)
cors.init_app(app)
db.init_app(app)
ma.init_app(app)
api.init_app(app)
sio.init_app(app)
scheduler.init_app(app)
csrf.init_app(app)

import src.models
import src.views
import src.events
from src.models import BaseModel, User

guard.init_app(app, User)

with app.app_context():
    BaseModel.set_session(db.session)

    if config.config_model.sqlite.recreate:
        logging.info("Recreating database...")
        db.drop_all()
        db.session.commit()

    db.create_all()
    db.session.commit()
    
    admin_user: User = User.where(roles="admin").first()

    if not admin_user:
        User.create(
            name=config.config_model.auth.admin_username,
            password=config.config_model.auth.admin_password,
            roles="admin"
        )

scheduler.start()