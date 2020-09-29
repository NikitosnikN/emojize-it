import os
import collections
import hashlib

__all__ = ["emojize"]


def encode_hash_with_modulo_operation(hash_, emojies, length):
    # type: (int, list, int) -> str
    emoji_string = ""
    index = hash_ % (len(emojies) ** length)

    for _ in range(length):
        emoji_string += emojies[index % len(emojies)]
        index = index // len(emojies)

    return emoji_string


class emojize:  # noqa
    _algorithms_available = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")

    def __init__(self, length=4, hashing_algo="sha256", encoding_strategy=None):
        # type: (int, str, callable) -> None

        self._length = length
        self._hashing_algo = hashing_algo
        self._encoding_strategy = encoding_strategy or encode_hash_with_modulo_operation

        assert length > 0, "length must be greater zero"
        assert hashing_algo in self._algorithms_available, f"unsupported {hashing_algo} algorithm"

    @staticmethod
    def _get_emojies():
        # type: () -> list

        with open(os.path.join(os.path.dirname(__file__), "emoji.txt")) as f:
            emojies = f.read().splitlines()
        return emojies

    def _proceed_hash(self, hash_):
        # type: (int) -> str

        return self._encoding_strategy(
            hash_=hash_,
            emojies=self._get_emojies(),
            length=self._length
        )

    def emojize_string(self, obj):
        # type: (str) -> str

        assert isinstance(obj, (str, bytes)), "object must be string or bytes"
        if isinstance(obj, str):
            obj = obj.encode('utf-8')

        hash_ = int(getattr(hashlib, self._hashing_algo)(obj).hexdigest(), 16)
        return self._proceed_hash(hash_)

    def emojize_unsafe(self, obj):
        # type: (...) -> str

        assert isinstance(obj, collections.abc.Hashable), "object must be hashable"
        hash_ = hash(obj)
        return self._proceed_hash(hash_)
