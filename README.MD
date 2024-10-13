# WhatsApp Meme Poster

This project is designed to fetch media from an Instagram collection and send them to a specified WhatsApp channel (although can also be used for groups and users). It uses a third party WhatsApp API (Whapi) and the unofficial Instagram API to achieve this.

## Table of Contents

1. [Workflow and Functionality](#workflow-and-functionality)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
   [Configuration](#configuration)
    - [WhatsApp Token](#whatsapp-token)
    - [WhatsApp Destination](#whatsapp-destination)
    - [Instagram Collection ID](#instagram-collection-id)
    - [Instagram Headers](#instagram-headers)
4. [Usage](#usage)
5. [Additional Information](#additional-information)
6. [Todo](#todo)

## Workflow and Functionality

The program follows these steps:

### Program Workflow

1. **Load Configuration**  
   The program reads essential settings from the `config.json` file, including your WhatsApp token, destination ID, and Instagram collection ID.

2. **Fetch Instagram Headers**  
   It retrieves the necessary Instagram headers from the `headers.py` file, which are used to make authenticated requests to the Instagram API.

3. **Retrieve Media from Instagram**  
   Using the Instagram API, the program fetches media from the specified collection. The media is retrieved in batches, with each batch containing up to 12 items. This step is highly efficient because only the media links are retrieved, not the actual content.

4. **Save Media Information**  
   Information about each retrieved media item, including video URLs, is saved into a file named `insta_memes.csv`.

5. **Filter Out Sent Memes**  
   The program reads the meme data from `insta_memes.csv`. It filters out any memes that have already been sent, using the `sent_video_ids.txt` file to identify duplicates. Only new, unsent memes are processed further.

6. **Fetch top comment**  
   The top comment of every meme is then retrieved from the Instagram API. If the top comment contains a word or phrase listed in `blacklisted_words.txt`, the next comment is chosen instead.

7. **Send Memes to WhatsApp**  
   The filtered memes are then sent to the specified WhatsApp channel using Whapi. Every meme is captioned with the top comment from the previous step.

8. **Update Sent IDs**  
   After sending, the program updates the `sent_video_ids.txt` file with the IDs of the memes that were successfully sent. This prevents duplicates from being sent in future runs.

## Prerequisites

- Python 3.9 or higher
- A WhatsApp account with a valid phone number
- An Instagram account with access to the desired collection
- A "Channel" API token from [whapi.cloud](https://whapi.cloud/) (their free plan is sufficient for most cases)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/whatsapp-meme-poster.git
   ```

2. Navigate to the project directory:

   ```bash
   cd whatsapp-meme-poster
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### WhatsApp Token

1. Sign in to [whapi.cloud](https://whapi.cloud/)
2. Click on the whapi "Trial channel" that has been created for you, and follow the prompts given to you.
3. FOllow the steps that you will be prompted with, including inking your whatsapp number.
4. Copy the generated token on the panel page that you will be redirected to.
5. Save this token inside the `config/config.json` file.

### WhatsApp Destination

1. Go back to the Whapi panel, and scroll down to the tab that says `GET /newsletters Get newsletters`
2. Click on the tab and then click the button labled `Try it out`
3. Press the button `Execute` and scroll down a bit till you can see the "Response body"
4. In the response body, look for the dictionary containing information about the WhatsApp channel that you want to automate.
5. Copy the `id` field of the dictionary.
6. Go back to `config/config.json` and paste the copied id in the `to` field

### Instagram Collection ID

1. Open Google Chrome and navigate to the Instagram collection you want to fetch memes from.
2. Look at the url of the collection. It should look something like `https://www.instagram.com/{username}/saved/{collection_name}/{collection_id}/`
3. Copy the "{collection_id}" part of the url. That is the collection id
4. Return to the `config.json` file and save the id in its relevant field.

### Instagram Headers

1. Open Google Chrome and navigate to the Instagram collection you want to fetch memes from.
2. Open the Developer Tools (F12) and go to the Network tab.
3. Refresh the page and filter the requests by `/posts`.
4. Right click on the first request.
5. Select `Copy > Copy as cURL (bash)`.
6. Go to [ryan.govost.es/http-translator/](https://ryan.govost.es/http-translator/) and paste the copied content into the "Input" field.
7. In the "Output" field, copy the headers part of the request. (`...headers={...}...` copy the `{...}` part)
8. Open the `config/headers.py` file and replace the existing dictionary with the copied headers.

## Usage

1. Run main.py to start sending everything in the Instagram collection to your WhatsApp channel:

   ```bash
   python main.py
   ```

## Additional Information

- Every fourth every fourth consecutive captionless WhatsApp message is captioned with a "." to avoid WhatsApp's grouping.
- You can customize the script by modifying the `main` function in `send_memes_on_wa.py` to fit your specific needs.

## Todo

- Add error handling to handle API errors.
- Log more useful information top the console, in a prettier way

Feel free to modify and extend this project to suit your needs! Pull requests are welcomed!
