import json
import re

import requests
from django.conf import settings


def get_video(
    tweet_link: str,
):
    url = f"{settings.TVD_API_URL}?url={tweet_link}"

    headers = {
        "X-RapidAPI-Key": settings.TVD_API_KEY,
        "X-RapidAPI-Host": settings.TVD_API_HOST,
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 429:
        return {
            "success": False,
            "data": None,
            "message": "Too many requests. Try again.",
        }

    response = response.json()

    if response.get("error"):
        return {"success": False, "data": None, "message": response.get("error")}

    if response.get("errors"):
        return {
            "success": False,
            "data": None,
            "message": response.get("errors")[0].get("message"),
        }

    if not response.get("media").get("video"):
        return {
            "success": False,
            "data": None,
            "message": "No video was found on the tweet.",
        }

    videos = []
    for video in response.get("media").get("video").get("videoVariants"):
        if video.get("bitrate") != 0:
            videos.append(
                {
                    "size": re.findall(r"[0-9]+x[0-9]+", video.get("url"))[0],
                    "url": video.get("url"),
                }
            )

    return {
        "success": True,
        "data": {
            "tweet_id": response.get("id"),
            "description": response.get("description"),
            "videos": videos,
            "user": response.get("user"),
        },
        "message": "",
    }


def get_sensitive_video(
    tweet_link: str,
):
    """Returns possible sensitive video"""

    _cookie = settings.TVD_API_COOKIE
    url = f"{settings.TVD_API_URL.replace('.com/status','.com/tweet')}?url={tweet_link}&Cookie={_cookie}"

    headers = {
        "X-RapidAPI-Key": settings.TVD_API_KEY,
        "X-RapidAPI-Host": settings.TVD_API_HOST,
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 429:
        return {
            "success": False,
            "data": None,
            "message": "Too many requests. Try again.",
        }

    response = response.json()

    try:
        videos = response.get("data")[0].get("video_info")
    except:
        videos = None

    if not videos:
        return {
            "success": False,
            "data": None,
            "message": "Can't get videos from the API",
        }

    _videos = []
    for video in videos:
        if video.get("content_type") == "video/mp4":
            _videos.append(
                {
                    "bitrate": video.get("bitrate"),
                    "size": re.findall(r"[0-9]+x[0-9]+", video.get("url"))[0],
                    "url": video.get("url"),
                }
            )

    videos = sorted(_videos, key=lambda d: d["bitrate"])[::-1]

    return {
        "success": True,
        "data": {
            "tweet_id": response.get("id"),
            "description": response.get("description") or "",
            "videos": videos,
            "user": response.get("user") or "",
        },
        "message": "",
    }


class ParseTelegramWebhook:
    def __init__(self, request):
        self.request = request

    def get_data(self):
        try:
            data = json.loads(self.request)
        except:
            return False

        # Reject if not first message (eg. edited or deleted message)
        if not data.get("message"):
            return False

        # Reject if messaage is not text message
        if not data.get("message").get("text"):
            return False

        user = data.get("message").get("from")
        message = data.get("message").get("text") or ""

        return {"user": user, "text_message": message}
