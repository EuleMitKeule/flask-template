# flask-template

This repository contains an advanced generic template app using the Flask framework.

## Features

### Automatic Schemas

You can automatically generate marshmallow schemas by using the `add_schema()` decorator on your models.

```py
@add_schema(
    meta=[
        "exclude": ["password"]
    ],
    custom_field=ma.String(...)
)
class User(BaseModel):
    name: str = db.Column(db.String())
    password: str = db.Column(db.String())
```

### Automatic Views

Similarily You can automatically generate views for you models by using the `add_view()` decorator.
This will generate default REST endpoints to perform CRUD operations for the model.

### Third party extensions

It also features the following extensions:

* flask-smorest
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

* Add template tests
* Add Authentication and Authorization using flask-praetorian
* Add Github workflows
* Implement Dockerfile
* Add SonarQube scanning