def test_app_is_created(app: Quart):
    assert app.name == "app"
