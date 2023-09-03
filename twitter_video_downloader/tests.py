from django.test import TestCase

from . import utils


class TestArter(TestCase):
    def setUp(self):
        pass

    def test_arter(self):
        tweet_url = (
            "https://twitter.com/OP_SPOILERS2023/status/1698149877379944689?s=20"
        )
        utils.ssstwitter_com(tweet_url)
