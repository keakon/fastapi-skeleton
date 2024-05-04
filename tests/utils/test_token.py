import json

from app.utils.token import decode_token, encode_token


def test_encode_and_decode_token():
    for payload in [{}, {'foo': 'bar', 'baz': 1}]:
        encoded_token = encode_token(payload)
        token = decode_token(encoded_token)
        assert token
        assert isinstance(token.payload, bytes)
        assert json.loads(token.payload) == payload
