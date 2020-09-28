import collections.abc
import math
import hashlib

__all__ = ["emojize"]


class emojize:  # noqa
    _algorithms_available = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")

    def __init__(self, length: int = 4, algo: str = "sha256"):
        self.length = length
        self.algo = algo

        assert length > 0, "length must be greater zero"
        assert algo in self._algorithms_available, f"unsupported {algo} algorithm"

    @staticmethod
    def _get_emojies() -> list:
        with open("emojize/emoji.txt", "r") as f:
            emojies = f.read().splitlines()
        return emojies

    def _proceed_hash(self, hash_: int) -> str:
        emojies = self._get_emojies()
        emoji_string = ""
        emoji_index = hash_ % (len(emojies) ** self.length)

        for i in range(1, self.length + 1):
            emoji_string += emojies[emoji_index % len(emojies)]
            emoji_index = math.floor(emoji_index / len(emojies))
        return emoji_string

    def emojize(self, obj) -> str:
        assert isinstance(obj, (str, bytes)), "object must be string or bytes"
        if isinstance(obj, str):
            obj = obj.encode('utf-8')

        hash_ = int(getattr(hashlib, self.algo)(obj).hexdigest(), 16)
        return self._proceed_hash(hash_)

    def emojize_unsafe(self, obj) -> str:
        assert isinstance(obj, collections.abc.Hashable), "object must be hashable"
        hash_ = hash(obj)
        return self._proceed_hash(hash_)
