"""
Unit tests for the Concert Itinerary Builder.

This file contains unit tests for the ItineraryBuilder class in main.py.
Participants will implement tests based on the system specifications.
"""

import unittest
from main import Concert, ItineraryBuilder
from concerts_data import get_all_concerts

from datetime import datetime

class ItineraryBuilderTest(unittest.TestCase):
    """Test cases for the ItineraryBuilder class."""
    
    def setUp(self):
        """Set up for the tests."""

        self.builder = ItineraryBuilder()
        self.all_concerts = get_all_concerts()

    
    # ----- Manual Test Cases -----
    # Participants will implement their manual test cases here. 

    def test_manual_1(self):
        """First manually written test case."""
        """Some artists may have no concerts on the list. In that case, that should be indicated in the itinerary."""
        
        """Fattade inte riktigt vad som menades med testfallet"""
        pass

    def test_manual_2(self):
        """The itinerary should return a list of concerts sorted in chronological order (by date from earliest to latest)."""
        order = -1
        itinerary = self.builder.build_itinerary(self.all_concerts)
        for i in range(len(itinerary) - 1):
            current = itinerary[i].date
            next = itinerary[i + 1].date
            if current <= next:
                order = 0
            else:
                order = -1
                break
            
        self.assertEqual(0, order)

    def test_manual_3(self):
        """An artist has at most one concert in the itinerary. If an artist has more than one concert in the list, the itinerary should only include the one with the earliest start date."""
        itinerary = self.builder.build_itinerary(self.all_concerts)
        duplicate_check = []
        error = -1

        for i in range(len(itinerary)):
            if itinerary[i].artist not in duplicate_check:
                duplicate_check.append(itinerary[i].artist)
                error = 1
            else:
                error = -1
                break

        for i in range(len(itinerary)):
            if error == -1:
                break

            scheduled_concert = itinerary[i]
            for j in range(len(self.all_concerts)):
                if scheduled_concert.artist == self.all_concerts[j].artist:
                    if scheduled_concert.date <= self.all_concerts[j].date:
                        error = 1
                    else: error = -1
                    break

        self.assertEqual(1, error)

    # ----- AI-Assisted Test Cases -----
    # Participants will implement their AI-assisted test cases here.
    # Please name your test in a way which indicates that these are AI-assisted test cases.
    def test_ai_assisted_1(self):
        """Test case for the itinerary builder.
        No two concerts may take place on the same day. If two different artists (or the same artist) 
        have a concert on the same day, the itinerary only includes the concert closest to the last one."""
        
        # Arrange
        test_concerts = [
            Concert("Artist1", "2025-06-01", "Stockholm", 59.3293, 18.0686),
            Concert("Artist2", "2025-06-01", "Oslo", 59.9139, 10.7522),      # Same day as Artist1
            Concert("Artist3", "2025-06-02", "Copenhagen", 55.6761, 12.5683),
            Concert("Artist4", "2025-06-02", "Stockholm", 59.3293, 18.0686)  # Same day as Artist3
        ]
        
        # Act
        itinerary = self.builder.build_itinerary(test_concerts)
        
        # Assert
        # Check that no two concerts are on the same day
        dates_in_itinerary = [concert.date for concert in itinerary]
        unique_dates = set(dates_in_itinerary)
        
        self.assertEqual(
            len(dates_in_itinerary), 
            len(unique_dates), 
            "Itinerary contains multiple concerts on the same day"
        )
        
        # Check that for concerts on the same day, the one closest to the previous concert is chosen
        # This will be implemented in the next phase as it requires distance calculation logic

    def test_ai_assisted_2(self):
        """Test case for the itinerary builder.
        The itinerary should return a list of concerts that state the artist, date, location, and valid coordinates."""
        
        # Arrange
        test_concerts = [
            Concert("Artist1", "2025-06-01", "Stockholm", 59.3293, 18.0686),
            Concert("Artist2", "2025-06-02", "Oslo", None, 10.7522),          # Missing latitude
            Concert("Artist3", "2025-06-03", "Copenhagen", 55.6761, None),    # Missing longitude
            Concert("Artist4", "2025-06-04", "Stockholm", -91.0, 18.0686),    # Invalid latitude
            Concert("Artist5", "2025-06-05", "Oslo", 59.9139, 181.0)          # Invalid longitude
        ]
        
        # Act
        itinerary = self.builder.build_itinerary(test_concerts)
        
        # Assert
        self.assertGreater(len(itinerary), 0, "Itinerary should not be empty")
        
        for concert in itinerary:
            # Check required fields are not None
            self.assertIsNotNone(concert.artist, "Artist should not be None")
            self.assertIsNotNone(concert.date, "Date should not be None")
            self.assertIsNotNone(concert.location, "Location should not be None")
            self.assertIsNotNone(concert.latitude, "Latitude should not be None")
            self.assertIsNotNone(concert.longitude, "Longitude should not be None")
            
            # Check required fields are not empty
            self.assertNotEqual(concert.artist.strip(), "", "Artist should not be empty")
            self.assertNotEqual(concert.date.strip(), "", "Date should not be empty")
            self.assertNotEqual(concert.location.strip(), "", "Location should not be empty")
            
            # Validate date format (YYYY-MM-DD)
            try:
                datetime.strptime(concert.date, '%Y-%m-%d')
            except ValueError:
                self.fail(f"Invalid date format: {concert.date}. Expected format: YYYY-MM-DD")
                
            # Validate coordinate ranges
            self.assertGreaterEqual(concert.latitude, -90.0, "Latitude must be >= -90.0")
            self.assertLessEqual(concert.latitude, 90.0, "Latitude must be <= 90.0")
            self.assertGreaterEqual(concert.longitude, -180.0, "Longitude must be >= -180.0")
            self.assertLessEqual(concert.longitude, 180.0, "Longitude must be <= 180.0")

    def test_ai_assisted_3(self):
        """Single-concert artists should be prioritized over multi-concert ones when choosing between concerts on the same day."""
        
        # Arrange
        test_concerts = [
            Concert("Artist2", "2025-06-02", "Oslo", 59.9139, 10.7522),   # multi-concert
            Concert("Artist2", "2025-06-03", "Stockholm", 59.3293, 18.0686),
            Concert("Artist1", "2025-06-02", "Copenhagen", 55.6761, 12.5683),  # single-concert
            Concert("Artist3", "2025-06-02", "Gothenburg", 57.7089, 11.9746), # single-concert
        ]
        
        # Act
        itinerary = self.builder.build_itinerary(test_concerts)
        artist_names = [concert.artist for concert in itinerary]

        # Assert: minst en av single-concert-artisterna ska vara med
        single_concerts_included = any(artist in artist_names for artist in ["Artist1", "Artist3"])
        self.assertTrue(single_concerts_included, "At least one single-concert artist should be in the itinerary")
        
        # Om Artist2 är med, så ska den ligga efter den single-artist som valts
        if "Artist2" in artist_names:
            idx_artist2 = artist_names.index("Artist2")
            for artist in ["Artist1", "Artist3"]:
                if artist in artist_names:
                    self.assertLess(
                        artist_names.index(artist), idx_artist2,
                        f"{artist} should appear before Artist2 in the itinerary"
                    )


if __name__ == "__main__":
    unittest.main()