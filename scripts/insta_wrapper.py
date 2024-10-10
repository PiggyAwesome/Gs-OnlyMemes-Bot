import requests

class InstagramScraper:
    def __init__(self):
        with open("config/headers.py", "r") as f:
            self.headers = eval(f.read())

    def fetch_top_comment(self, pk):
        comments = []
        comments_req = requests.get(
            f"https://www.instagram.com/api/v1/media/{pk}/comments/?can_support_threading=true&permalink_enabled=false",
            headers=self.headers,
        ).json()
        for comment_obj in comments_req["comments"]:
            comments.append((comment_obj["comment_like_count"], comment_obj["text"]))
        return max(comments, key=lambda x: x[0])[1] if comments else ""
