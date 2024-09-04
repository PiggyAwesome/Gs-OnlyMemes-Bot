from typing import Literal
import httpx


class WHAPI:
    def __init__(self, token: str) -> None:
        self.token = token
        self.requests_session = httpx.Client(timeout=100)

    async def getChannels(self, count, offset):
        """Sends a GET request to retrieve channels with pagination."""
        resp = self.requests_session.get(
            "https://gate.whapi.cloud/newsletters",
            params={"count": count, "offset": offset},
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )
        return resp

    async def sendMessage(
        self,
        to: str,
        media: str,
        media_type: Literal["image", "video"],
        width: int,
        height: int,
        caption: str,
        mime_type: str
    ):
        """
        Sends a POST request to the Whapi API to send a WhatsApp message with media.
        """

        resp = self.requests_session.post(
            f"https://gate.whapi.cloud/messages/{media_type}",
            json={
                "media": media,
                "to": to,
                "caption": caption,
                "width": width,
                "height": height,
                "mime_type":mime_type
            },
            headers={
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )
        return resp
