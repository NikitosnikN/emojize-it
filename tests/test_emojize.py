import unittest

from emojize import emojize


class TestEmojize(unittest.TestCase):
    def test_length(self):
        for length in range(1, 100):
            self.assertEqual(len(emojize(length=length).emojize_string("test string")), length)

        for length in range(-5, 0):
            self.assertRaises(AssertionError, emojize, length=length)

        return

    def test_hashing_algo(self):
        valid_algos = ("md5", "sha1", "sha224", "sha256", "sha384", "sha512")
        invalid_algos = ("", "hello", "world", "sha-1", "gooba")

        for algo in valid_algos:
            emojize(hashing_algo=algo)

        for algo in invalid_algos:
            self.assertRaises(AssertionError, emojize, hashing_algo=algo)

        return


if __name__ == '__main__':
    unittest.main()
