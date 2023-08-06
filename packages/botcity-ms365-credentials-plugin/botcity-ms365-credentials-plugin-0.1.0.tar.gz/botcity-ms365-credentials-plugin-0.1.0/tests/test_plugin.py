import os
from botcity.plugins.ms365.credentials import MS365CredentialsPlugin


def test_is_authenticated(bot: MS365CredentialsPlugin):
    assert bot.ms365_account.is_authenticated

def test_get_credentials(bot: MS365CredentialsPlugin):
    assert bot.credentials[0] == os.getenv("MS365_CLIENT_ID")
    assert bot.credentials[1] == os.getenv("MS365_CLIENT_SECRET")
