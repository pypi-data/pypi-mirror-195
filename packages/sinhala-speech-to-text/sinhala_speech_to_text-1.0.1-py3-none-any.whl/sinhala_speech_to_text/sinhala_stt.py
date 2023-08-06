import requests

def send_audio_file(audio_file_path, url, api_key):
    # Create a dictionary with the audio file
    audio_file = {'audio': open(audio_file_path, 'rb')}

    # Create a dictionary with the headers, including the X-API-KEY header
    headers = {'X-API-KEY': api_key}

    # Send the audio file to the server using a POST request with the headers
    response = requests.post(url, files=audio_file, headers=headers)

    # Check if the request was successful (HTTP 200 status code)
    if response.status_code == 200:
        # Get the decoded text from the JSON response and decode it using UTF-8
        decoded_text = response.json()['text'].encode('utf-8').decode('utf-8')
        return decoded_text
    else:
        # If the request failed, print an error message and return None
        print(f'Error sending audio file: HTTP {response.status_code}')
        return None