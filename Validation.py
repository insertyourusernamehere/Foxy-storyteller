from dotenv import load_dotenv
import os
import googlemaps
import geocoder
from datetime import datetime
from Input_Helper import get_location
import time 
# Load environment variables from .env file
def Api_init():
    load_dotenv()

    # Retrieve the API key from environment variables
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set GROQ_API_KEY in your environment or .env file.")
    else:
        return(api_key)
    


def get_travel_time():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("GMAP_KEY")

    # Get current location based on IP
    current_location = geocoder.ip('me').latlng
    if not current_location:
        print("Unable to determine current location.")
        return None

    # Initialize Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Retry logic
    retries = 0
    while retries < 5:
        destination = get_location()
        try:
            # Fetch travel time from Google Maps API
            result = gmaps.distance_matrix(
                origins=f"{current_location[0]},{current_location[1]}",
                destinations=destination,
                mode="driving",
                departure_time=datetime.now()
            )
            
            # Check for a valid response
            duration_seconds = result['rows'][0]['elements'][0]['duration']['value']
            if duration_seconds:
                return duration_seconds // 60  # Return time in minutes
            
        except Exception as e:
            print(f"Error: Didnt Quite Understand that Location...")
            print("Retrying...")
            

        
        # If we encounter an error, retry after a delay
        retries += 1
        time.sleep(5)  # Wait for 5 seconds before retrying

    # If we exhaust retries without success, return None
    print("Error fetching travel time after several retries. Please try again later.")
    return None

    
