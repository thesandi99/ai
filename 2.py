import requests
from spleeter.separator import Separator
import os


def handler(request):
    # Define the URL of the audio file to download
    audio_url = 'https://raw.githubusercontent.com/thesandi99/unique-repo-name/refs/heads/master/GOJO%20VS%20SUKUNA%20FULL%20FIGHT%20AMV%20%2B%20ENDING%20SCENE%204K%20_%20LADY%20GAGA%20-%20JUDAS_44pt8w67S8I%20(1).mp3'
    audio_file = '/tmp/audio.mp3'  # Save to /tmp, as Vercel has write permissions here

    # Download the audio file
    response = requests.get(audio_url)
    with open(audio_file, 'wb') as f:
        f.write(response.content)

    # Initialize the Separator
    separator = Separator('spleeter:2stems')

    # Define output directory, also in /tmp
    output_dir = '/tmp/output'
    os.makedirs(output_dir, exist_ok=True)

    # Perform audio separation
    separator.separate_to_file(audio_file, output_dir)

    return {
        "statusCode": 200,
        "body": "Audio separation complete. Files saved temporarily in output directory."
    }

