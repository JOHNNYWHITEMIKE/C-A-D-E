#!/usr/bin/env python3
"""
Tests for CityHall module
"""

import unittest
from cityhall import CityHall


class TestCityHall(unittest.TestCase):
    """Test cases for CityHall class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.city_hall = CityHall("Test Community")
    
    def test_init(self):
        """Test CityHall initialization"""
        self.assertEqual(self.city_hall.name, "Test Community")
        self.assertEqual(len(self.city_hall.members), 0)
        self.assertEqual(len(self.city_hall.announcements), 0)
        self.assertEqual(len(self.city_hall.proposals), 0)
    
    def test_add_member(self):
        """Test adding members"""
        result = self.city_hall.add_member("Alice")
        self.assertTrue(result)
        self.assertIn("Alice", self.city_hall.members)
        
        # Adding duplicate should return False
        result = self.city_hall.add_member("Alice")
        self.assertFalse(result)
        self.assertEqual(len(self.city_hall.members), 1)
    
    def test_remove_member(self):
        """Test removing members"""
        self.city_hall.add_member("Bob")
        result = self.city_hall.remove_member("Bob")
        self.assertTrue(result)
        self.assertNotIn("Bob", self.city_hall.members)
        
        # Removing non-existent member should return False
        result = self.city_hall.remove_member("Bob")
        self.assertFalse(result)
    
    def test_get_members(self):
        """Test getting member list"""
        self.city_hall.add_member("Alice")
        self.city_hall.add_member("Bob")
        members = self.city_hall.get_members()
        self.assertEqual(len(members), 2)
        self.assertIn("Alice", members)
        self.assertIn("Bob", members)
    
    def test_make_announcement(self):
        """Test making announcements"""
        self.city_hall.make_announcement("Test announcement")
        announcements = self.city_hall.get_announcements()
        self.assertEqual(len(announcements), 1)
        self.assertEqual(announcements[0], "Test announcement")
    
    def test_submit_proposal(self):
        """Test submitting proposals"""
        proposal_id = self.city_hall.submit_proposal("Test proposal")
        self.assertEqual(proposal_id, 0)
        proposals = self.city_hall.get_proposals()
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]['description'], "Test proposal")
        self.assertEqual(proposals[0]['votes_for'], 0)
        self.assertEqual(proposals[0]['votes_against'], 0)
    
    def test_vote_on_proposal(self):
        """Test voting on proposals"""
        proposal_id = self.city_hall.submit_proposal("Test proposal")
        
        # Vote for
        result = self.city_hall.vote_on_proposal(proposal_id, vote_for=True)
        self.assertTrue(result)
        proposals = self.city_hall.get_proposals()
        self.assertEqual(proposals[0]['votes_for'], 1)
        
        # Vote against
        result = self.city_hall.vote_on_proposal(proposal_id, vote_for=False)
        self.assertTrue(result)
        proposals = self.city_hall.get_proposals()
        self.assertEqual(proposals[0]['votes_against'], 1)
        
        # Invalid proposal ID
        result = self.city_hall.vote_on_proposal(999, vote_for=True)
        self.assertFalse(result)
    
    def test_get_info(self):
        """Test getting community information"""
        self.city_hall.add_member("Alice")
        self.city_hall.add_member("Bob")
        self.city_hall.make_announcement("Test")
        self.city_hall.submit_proposal("Test proposal")
        
        info = self.city_hall.get_info()
        self.assertEqual(info['name'], "Test Community")
        self.assertEqual(info['member_count'], 2)
        self.assertEqual(info['announcement_count'], 1)
        self.assertEqual(info['proposal_count'], 1)


if __name__ == '__main__':
    unittest.main()
