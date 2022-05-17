# flask-template

This repository contains an advanced generic template app using the Flask framework.

It also features the following extensions:

* SQLAlchemy
* SQLAlchemy-Mixins
* Marshmallow
* SocketIO
* APScheduler

## Usage

This template is intended to be used with Visual Studio Code.

### Tasks

When opening the project, a new virtual environment will be created and the Flask server will be started.<br>
The task can also be (re)started by using the shortcut `Ctrl+Shift+B`.

### Configuration

The default config file path is `config/config.yml`.

To add more configuration options simply extend `src/config.py`.

### Logging

Logging is done with python's default `logging` library. Logs are outputted by default in the console and also to `logs/app.log`.

### Database

The default database path is `data/app.sqlite`. 

Models are defined in `src/models` and should inherit from the `BaseModel` class in `src/models/base_model.py`.

### Testing

Tests can be defined in `src/tests/` and are automatically discovered by the VS Code Test Explorer.

### Events

SocketIO events should be implemented in `src/events`.

## Planned Features

* Integrate with flask-restplus
* Add template tests
* Add Github workflows
* Implement Dockerfile
* Add SonarQube scanning