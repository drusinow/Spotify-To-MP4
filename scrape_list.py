import requests
from bs4 import BeautifulSoup



def scrape_main(spotify_link: str, output_file="scraped_tracks.txt") -> list:
    url = spotify_link
    headers = {'User-Agent': 'Mozilla/5.0'}  # optional but helps avoid blocks

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        track_rows = soup.find_all('div', {'data-testid': 'tracklist-row'})
                
        tracks_data = []
                
        for row in track_rows:
            try:
                # Find song name - look for the track link
                song_element = row.find('a', {'data-testid': 'internal-track-link'})
                if song_element:
                    song_name = song_element.find('div').get_text(strip=True)
                else:
                    # Alternative: look for song name in the structure
                    song_div = row.find('div', class_='btE2c3IKaOXZ4VNAb8WQ')
                    song_name = song_div.get_text(strip=True) if song_div else "Unknown Song"
                
                # Find artist name - look for artist link
                artist_element = row.find('a', href=lambda x: x and '/artist/' in x)
                if artist_element:
                    artist_name = artist_element.get_text(strip=True)
                else:
                    # Alternative: look in the subdued text area
                    artist_area = row.find('span', class_=lambda x: x and 'encore-internal-color-text-subdued' in x)
                    if artist_area:
                        artist_link = artist_area.find('a')
                        artist_name = artist_link.get_text(strip=True) if artist_link else "Unknown Artist"
                    else:
                        artist_name = "Unknown Artist"
                
                if song_name and artist_name:
                    tracks_data.append({
                        'song': song_name,
                        'artist': artist_name
                    })
                    print(f"Found: {song_name} by {artist_name}")
                    
            except Exception as e:
                print(f"Error parsing track row: {e}")
                continue
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("SCRAPED TRACKS FROM SPOTIFY\n")
            f.write("=" * 50 + "\n\n")
            
            for i, track in enumerate(tracks_data, 1):
                f.write(f"{i}. {track['song']} - {track['artist']}\n")
            
            f.write(f"\nTotal tracks found: {len(tracks_data)}\n")
        
        print(f"\nScraping completed! Found {len(tracks_data)} tracks.")
        print(f"Results saved to: {output_file}")
        
        return tracks_data
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []
    except Exception as e:
        print(f"Error during scraping: {e}")
        return []