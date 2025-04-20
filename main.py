"""
Concert Itinerary Builder

This module provides functionality to build an itinerary of upcoming concerts.
"""

import math
from datetime import datetime

class Concert:
    """
    Represents a concert event.
    
    Attributes:
        artist (str): The name of the artist performing.
        date (str): The date of the concert in 'YYYY-MM-DD' format.
        location (str): The location where the concert will take place.
        latitude (float): Latitude coordinate of the concert location.
        longitude (float): Longitude coordinate of the concert location.
    """
    
    def __init__(self, artist, date, location, latitude, longitude):
        self.artist = artist
        self.date = date
        self.location = location
        self.latitude = latitude
        self.longitude = longitude

class ItineraryBuilder:
    """A class to build concert itineraries."""
    
    def calculate_distance(self, concert1, concert2):
        """Calculate the distance between two concerts using Haversine formula."""
        R = 6371  # Earth's radius in kilometers
        
        lat1, lon1 = math.radians(concert1.latitude), math.radians(concert1.longitude)
        lat2, lon2 = math.radians(concert2.latitude), math.radians(concert2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        return R * c
    
    def is_valid_concert(self, concert):
        """Validate concert information and coordinates."""
        try:
            # Check for None values
            if any(v is None for v in [
                concert.artist, 
                concert.date, 
                concert.location, 
                concert.latitude, 
                concert.longitude
            ]):
                return False
                
            # Check for empty strings
            if any(not str(v).strip() for v in [
                concert.artist, 
                concert.date, 
                concert.location
            ]):
                return False
                
            # Validate date format
            datetime.strptime(concert.date, '%Y-%m-%d')
            
            # Validate coordinate ranges
            if not (-90.0 <= concert.latitude <= 90.0):
                return False
            if not (-180.0 <= concert.longitude <= 180.0):
                return False
                
            return True
            
        except (ValueError, AttributeError):
            return False
        
    def build_itinerary(self, concerts):
        """Build an itinerary following all requirements."""
        
        # 1. Validera alla konserter
        valid_concerts = self._get_valid_concerts(concerts)

        # 2. Räkna antal konserter per artist
        artist_concert_count = self._count_concerts_per_artist(valid_concerts)

        # 3. Sortera konserterna i datumordning
        sorted_concerts = sorted(valid_concerts, key=lambda x: x.date)

        # 4. Gruppera konserter per datum
        concerts_by_date = self._group_by_date(sorted_concerts)

        itinerary = []
        last_added = None

        # 5. Gå igenom varje datum och välj en konsert per dag
        for date in sorted(concerts_by_date.keys()):
            same_day_concerts = concerts_by_date[date]

            # Prioritera artister med endast en konsert
            single_concert_artists = [
                c for c in same_day_concerts if artist_concert_count[c.artist] == 1
            ]
            candidates = single_concert_artists if single_concert_artists else same_day_concerts

            # Undvik att lägga till samma artist flera gånger
            available_concerts = [
                c for c in candidates if all(existing.artist != c.artist for existing in itinerary)
            ]

            if not available_concerts:
                continue

            # Om vi har en tidigare konsert, välj närmaste nästa
            if last_added and len(available_concerts) > 1:
                selected = min(
                    available_concerts, key=lambda x: self.calculate_distance(last_added, x)
                )
            else:
                selected = available_concerts[0]

            itinerary.append(selected)
            last_added = selected

        return itinerary


    # Hjälpmetoder (lägg dessa i samma klass)

    def _get_valid_concerts(self, concerts):
        """Return only concerts that pass is_valid_concert checks."""
        return [c for c in concerts if self.is_valid_concert(c)]

    def _count_concerts_per_artist(self, concerts):
        """Count how many concerts each artist has."""
        count = {}
        for c in concerts:
            count[c.artist] = count.get(c.artist, 0) + 1
        return count

    def _group_by_date(self, concerts):
        """Group concerts by their date."""
        grouped = {}
        for c in concerts:
            grouped.setdefault(c.date, []).append(c)
        return grouped



if __name__ == "__main__":
    from concerts_data import get_all_concerts
    
    all_concerts = get_all_concerts()