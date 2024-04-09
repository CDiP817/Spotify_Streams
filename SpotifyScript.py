import pandas as pd
import requests

# Your Spotify API credentials
client_id = 'c067d4004fe44a14ae69d4b9e2a2e4e8'
client_secret = '5407288478d544cfa5a2da0e15ebb0aa'

def get_spotify_token(client_id, client_secret):
    """Authenticate with the Spotify API and return an access token."""
    auth_url = 'https://accounts.spotify.com/api/token'
    response = requests.post(auth_url, data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to get token: {response.text}")

def get_album_cover_url(track_name, artist_name, access_token):
    """Search for a track by name and artist and return the album cover URL."""
    search_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'q': f'track:{track_name} artist:{artist_name}', 'type': 'track', 'limit': 1}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        tracks = response.json().get('tracks', {}).get('items', [])
        if tracks:
            return tracks[0]['album']['images'][0]['url']  # Highest quality image
    return "Not found"

def main():
    # Load your dataset
    df = pd.read_csv('spotify-2023.csv', encoding='ISO-8859-1')
    
    # Authenticate with Spotify API
    access_token = get_spotify_token(client_id, client_secret)
    
    # Add a new column for album cover URLs
    df['album_cover_url'] = df.apply(lambda row: get_album_cover_url(row['track_name'], row['artist(s)_name'], access_token), axis=1)
    
    # Save the updated dataset to a new CSV file
    df.to_csv('updated_spotify-2023.csv', index=False)
    print("Updated dataset saved successfully.")

if __name__ == "__main__":
    main()
