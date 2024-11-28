from pytest import fixture

from app import create_app


@fixture(scope="module")
def app():
    """Instance App"""
    return create_app()
