from enum import Enum
from typing import List

from O365 import Account, FileSystemTokenBackend


class Scopes(str, Enum):
    """
    The class with the enumerated scopes that can be used in the authentication.

    Usage: Scopes.<SCOPE_NAME>
    """

    BASIC = "basic"
    MS365_FILES_READ = "onedrive"
    MS365_FILES_ALL = "onedrive_all"
    MS365_OUTLOOK_READ = "mailbox"
    MS365_OUTLOOK_SEND = "message_send"
    MS365_OUTLOOK_ALL = "message_all"


class MS365CredentialsPlugin:
    def __init__(self, client_id: str, client_secret: str, token_path: str = '') -> None:
        """
        MS365CredentialsPlugin.

        Args:
            client_id (str): The client ID for the app created in the Azure Portal.
            client_secret (str): The id from the generated client secret.
            token_path (str, optional): The path that will be used to create the token file.
                Defaults to the current working dir.
        """
        token_backend = FileSystemTokenBackend(token_path=token_path)
        self._credentials = (client_id, client_secret)
        self._account = Account(credentials=self._credentials, token_backend=token_backend)

    @property
    def credentials(self) -> tuple:
        """The credentials being used for authentication."""
        return self._credentials

    @property
    def ms365_account(self) -> Account:
        """
        The Office365/Microsoft365 account service.

        You can use this property to access Microsoft365 functionalities.
        """
        return self._account

    def authenticate(self, scopes: List[Scopes] = []) -> None:
        """
        Authenticate the Microsoft365 account with the credentials of the created application.

        Args:
            scopes (List[Scopes]): The permission scopes defined in the Scopes class that will
                be used for authentication. Defaults to:

                - BASIC: basic configuration.
                - MS365_FILES_ALL: scope to use OneDrive, Excel.
                - MS365_OUTLOOK_ALL: scope to use Outlook mail.
        """
        if not self.ms365_account.is_authenticated:
            if not scopes:
                scopes = [Scopes.BASIC, Scopes.MS365_FILES_ALL, Scopes.MS365_OUTLOOK_ALL]
            self.ms365_account.authenticate(scopes=scopes)
