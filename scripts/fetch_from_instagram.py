# This Python script is used to scrape and download media (images and videos) from a specific Instagram collection.
# The script uses the requests library to send HTTP requests and extract the required data.

import requests, json

with open("config/config.json", "r") as f:
    config = json.load(f)

collection_id = config["Instagram"]["collection_id"]

with open("config/headers.py", "r") as f:
    headers = eval(f.read())


# Function to extract URLs of media items from the response JSON
def extractUrl(req) -> list[str]:
    final = []
    for item in req["items"]:
        # Check if the media item is part of a carousel
        if "carousel_media" in item["media"]:
            for carousel_item in item["media"]["carousel_media"]:
                # Check if the carousel item is a video
                if "video_versions" in carousel_item:
                    final.append(
                        carousel_item["id"]
                        + ","
                        + "video"
                        + ","
                        + str(carousel_item["video_versions"][-1]["width"])
                        + ","
                        + str(carousel_item["video_versions"][-1]["height"])
                        + ","
                        + carousel_item["video_versions"][-1]["url"]
                    )
                # Check if the carousel item is an image
                elif "image_versions2" in carousel_item:
                    final.append(
                        carousel_item["id"]
                        + ","
                        + "image"
                        + ","
                        + str(
                            carousel_item["image_versions2"]["candidates"][-1]["width"]
                        )
                        + ","
                        + str(
                            carousel_item["image_versions2"]["candidates"][-1]["height"]
                        )
                        + ","
                        + carousel_item["image_versions2"]["candidates"][-1]["url"]
                    )
                else:
                    raise Exception("?")
        # Check if the media item is a video
        elif "video_versions" in item["media"]:
            final.append(
                item["media"]["id"]
                + ","
                + "video"
                + ","
                + str(item["media"]["video_versions"][-1]["width"])
                + ","
                + str(item["media"]["video_versions"][-1]["height"])
                + ","
                + item["media"]["video_versions"][-1]["url"]
            )
        # Check if the media item is an image
        elif "image_versions2" in item["media"]:
            final.append(
                item["media"]["id"]
                + ","
                + "image"
                + ","
                + str(item["media"]["image_versions2"]["candidates"][-1]["width"])
                + ","
                + str(item["media"]["image_versions2"]["candidates"][-1]["height"])
                + ","
                + item["media"]["image_versions2"]["candidates"][-1]["url"]
            )
        else:
            raise Exception("?")
    return final


csv_values = []

# Send the initial request to fetch the first page of media items
req = requests.get(
    f"https://www.instagram.com/api/v1/feed/collection/{collection_id}/posts/?max_id=",
    headers=headers,
).json()

csv_values += extractUrl(req)

# Get the max_id for the next page of media items
max_id = req.get("next_max_id")
# print(max_id)

# Loop until there are no more pages of media items
while max_id:
    # Send a request to fetch the next page of media items
    req = requests.get(
        f"https://www.instagram.com/api/v1/feed/collection/{collection_id}/posts/?max_id={max_id}",
        headers=headers,
    ).json()
    csv_values += extractUrl(req)
    # Get the max_id for the next page of media items
    max_id = req.get("next_max_id")
    # print(max_id)


# Write the extracted URLs and IDS to a CSV file
with open("data/insta_memes.csv", "w", encoding="utf-8") as file:
    file.write("\n".join(csv_values))
