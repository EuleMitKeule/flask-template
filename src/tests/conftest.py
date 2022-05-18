import os
import pytest

from src import app
from src.common import db
from src.const import TEST_CONFIG_PATH


@pytest.fixture(autouse=True, scope="function")
def mock_app(request):

    os.environ["CONFIG_PATH"] = TEST_CONFIG_PATH

    ctx = app.app_context()
    ctx.push()

    db.drop_all()
    db.create_all()
    db.session.commit()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app