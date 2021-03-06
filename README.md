[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=coverage)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=bugs)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=EuleMitKeule_flask-template&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=EuleMitKeule_flask-template)

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

### Authentication and Authorization

Protect your views and endpoints by using the decorator `auth.auth_required` and `auth.roles_required(*roles)`. 

### Third party extensions

It also features the following extensions:

* flask-smorest
* flask-praetorian
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
* Add Github workflows