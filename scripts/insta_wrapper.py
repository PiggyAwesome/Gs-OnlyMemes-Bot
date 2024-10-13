import requests


class InstagramScraper:
    def __init__(self):
        with open("config/headers.py", "r") as f:
            self.headers = eval(f.read())
        with open("config/blacklisted_words.txt", "r") as f:
            self.blacklisted_words = f.read().splitlines()

    def fetch_top_comment(self, pk):
        comments = []
        comments_req = requests.get(
            f"https://www.instagram.com/api/v1/media/{pk}/comments/?can_support_threading=true&permalink_enabled=false",
            headers=self.headers,
        ).json()
        for comment_obj in comments_req["comments"]:
            comments.append((comment_obj["comment_like_count"], comment_obj["text"]))

        comments.sort(reverse=True)  # Sort comments by likes in descending order

        if not comments:  # if there is no comments
            return ""

        for comment in comments:
            top_comment = comment[1]
            if not any(
                word.lower() in top_comment.lower() for word in self.blacklisted_words
            ):  # if comment does not contain blacklisted words
                break
        return top_comment
