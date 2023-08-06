from typing import Any

from .claims import JWTEncodeClaims
from .encoder import JWTEncoder


class JWTTokenPairIssuer:
    def __init__(
        self,
        encoder: JWTEncoder,
        access_token_claims: JWTEncodeClaims,
        refresh_token_claims: JWTEncodeClaims,
    ) -> None:
        self.encoder = encoder
        self.access_token_claims = access_token_claims
        self.refresh_token_claims = refresh_token_claims

    def create_pair(self, data: dict[str, Any]) -> tuple[str, str]:
        return (
            self.encoder.encode(data, claims=self.access_token_claims),
            self.encoder.encode(data, claims=self.refresh_token_claims),
        )
