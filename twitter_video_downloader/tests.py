import time

from django.test import TestCase

from . import utils


class TwitterVideoDownloader(TestCase):
    def setUp(self):
        pass

    def test_get_video(self):
        time.sleep(1)
        result = utils.get_video(
            "https://twitter.com/Shikabashi/status/1689307627967197184?s=20"
        )

        self.assertEqual(result.get("success"), True)

    def test_get_sensitive_video(self):
        result = utils.get_sensitive_video(
            "https://x.com/maobaobao798/status/1681560860651831297?s=20"
        )

        self.assertEqual(result.get("success"), True)

    def test_get_image(self):
        time.sleep(1)
        result = utils.get_video(
            "https://twitter.com/lovely_pig328/status/1699030347990929797?s=20"
        )

        self.assertEqual(result.get("success"), False)

    def test_get_invalid_link(self):
        time.sleep(1)
        result = utils.get_video(
            "https://twitter.com/lovely_pig328/status/1arter699030347990929797?s=20"
        )

        self.assertEqual(result.get("success"), False)
