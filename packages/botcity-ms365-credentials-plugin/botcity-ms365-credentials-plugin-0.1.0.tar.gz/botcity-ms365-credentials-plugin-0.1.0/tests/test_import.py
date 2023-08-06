def test_package_import():
    import botcity.plugins.ms365.credentials as plugin
    assert plugin.__file__ != ""
