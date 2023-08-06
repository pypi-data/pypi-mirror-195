from tim.core.credentials import Credentials
from tim.core.api import execute_request
from tim.core.types import (
    License,
    LicenseStorage
)


class Licenses:
    def __init__(
        self,
        credentials: Credentials
    ):
        self._credentials = credentials

    def details_license(
        self,
    ) -> License:
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/licenses'
        )

    def storage_license(
        self,
    ) -> LicenseStorage:
        return execute_request(
            credentials=self._credentials,
            method='get',
            path='/licenses/storage'
        )
