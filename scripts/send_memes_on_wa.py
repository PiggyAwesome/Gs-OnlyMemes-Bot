import csv
import logging, asyncio, typing
from whapi_wrapper import WHAPI
import json
import urllib.parse
from insta_wrapper import InstagramScraper

logging.basicConfig(level=logging.INFO)

with open("config/config.json", "r") as f:
    config = json.load(f)

token = config["WhatsApp"]["token"]
to = config["WhatsApp"]["to"]

mime_type_lookup = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "mp4": "video/mp4",
    # Add more file extensions and their corresponding mime types as needed
}


async def main(
    sent_video_ids: typing.List[str], reader: typing.List[str], to: str, token: str
) -> None:
    whapi = WHAPI(token=token)
    instascraper = InstagramScraper()

    failed = []
    i = 1
    for id, media_type, width, height, url in reader:
        logging.info(f"{media_type} | ID: {id}")

        if id in sent_video_ids:  # video has already been sent in the past
            logging.info(f"Video has already been sent in the past | ID: {id}")
            continue  # continue, do not increment counter
        top_comment = instascraper.fetch_top_comment(pk=id.split("_")[0])
        resp = await whapi.sendMessage(
            to=to,
            media=url,
            media_type=media_type,
            width=int(width),
            height=int(height),
            caption=(
                top_comment if top_comment else ("." if i % 4 == 0 else "")
            ),  # this will add a "." on every fourth meme to evade whatsapp's grouping
            mime_type=mime_type_lookup.get(
                url.split("?")[0].split(".")[-1],
                "",
            ),  # try to extract mime type from file extension
        )
        logging.info(resp.status_code)  #

        if (
            resp.status_code == 200
        ):  # if media was successfully sent, save media_id in sent_video_ids
            logging.info(f"Message request {i} has successfully been sent. ")

            with open("data/sent_video_ids.txt", "a") as f:
                f.write(id + "\n")
        else:
            logging.info(resp.json())
            failed.append(resp)

        i += 1

    if failed:
        logging.critical(f"The following messages have failed: {failed}")


if __name__ == "__main__":
    with open("data/sent_video_ids.txt", "r") as f:
        sent_video_ids = f.read().strip().split("\n")

    with open("data/insta_memes.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        csv_data = list(reader)

    asyncio.run(main(sent_video_ids, csv_data, to, token))
