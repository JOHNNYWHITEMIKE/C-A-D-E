#!/usr/bin/env python3
"""
CityHall - Community Application Development Environment
Central hub for community governance and administration
"""

class CityHall:
    """Main CityHall class for managing community operations"""
    
    def __init__(self, name="Community"):
        """
        Initialize CityHall instance
        
        Args:
            name (str): Name of the community
        """
        self.name = name
        self.members = []
        self.announcements = []
        self.proposals = []
    
    def add_member(self, member_name):
        """
        Add a new member to the community
        
        Args:
            member_name (str): Name of the member to add
            
        Returns:
            bool: True if member was added successfully
        """
        if member_name not in self.members:
            self.members.append(member_name)
            return True
        return False
    
    def remove_member(self, member_name):
        """
        Remove a member from the community
        
        Args:
            member_name (str): Name of the member to remove
            
        Returns:
            bool: True if member was removed successfully
        """
        if member_name in self.members:
            self.members.remove(member_name)
            return True
        return False
    
    def get_members(self):
        """
        Get list of all community members
        
        Returns:
            list: List of member names
        """
        return self.members.copy()
    
    def make_announcement(self, announcement):
        """
        Make a community announcement
        
        Args:
            announcement (str): The announcement message
        """
        self.announcements.append(announcement)
    
    def get_announcements(self):
        """
        Get all community announcements
        
        Returns:
            list: List of announcements
        """
        return self.announcements.copy()
    
    def submit_proposal(self, proposal):
        """
        Submit a community proposal
        
        Args:
            proposal (str): The proposal description
            
        Returns:
            int: Proposal ID
        """
        proposal_id = len(self.proposals)
        self.proposals.append({
            'id': proposal_id,
            'description': proposal,
            'votes_for': 0,
            'votes_against': 0
        })
        return proposal_id
    
    def vote_on_proposal(self, proposal_id, vote_for=True):
        """
        Vote on a community proposal
        
        Args:
            proposal_id (int): ID of the proposal
            vote_for (bool): True for voting in favor, False for voting against
            
        Returns:
            bool: True if vote was recorded successfully
        """
        if 0 <= proposal_id < len(self.proposals):
            if vote_for:
                self.proposals[proposal_id]['votes_for'] += 1
            else:
                self.proposals[proposal_id]['votes_against'] += 1
            return True
        return False
    
    def get_proposals(self):
        """
        Get all community proposals
        
        Returns:
            list: List of proposals with voting information
        """
        return self.proposals.copy()
    
    def get_info(self):
        """
        Get general information about the CityHall
        
        Returns:
            dict: Information about the community
        """
        return {
            'name': self.name,
            'member_count': len(self.members),
            'announcement_count': len(self.announcements),
            'proposal_count': len(self.proposals)
        }


def main():
    """Main function demonstrating CityHall usage"""
    print("=" * 50)
    print("Welcome to CityHall")
    print("Community Application Development Environment")
    print("=" * 50)
    print()
    
    # Create a CityHall instance
    city_hall = CityHall("C-A-D-E Community")
    
    # Add some members
    print("Adding members...")
    city_hall.add_member("Alice")
    city_hall.add_member("Bob")
    city_hall.add_member("Charlie")
    print(f"Members: {', '.join(city_hall.get_members())}")
    print()
    
    # Make an announcement
    print("Making announcement...")
    city_hall.make_announcement("Welcome to our community!")
    city_hall.make_announcement("We're building something great together.")
    for i, announcement in enumerate(city_hall.get_announcements(), 1):
        print(f"  {i}. {announcement}")
    print()
    
    # Submit a proposal
    print("Submitting proposal...")
    proposal_id = city_hall.submit_proposal("Should we add a new feature?")
    print(f"  Proposal #{proposal_id}: Should we add a new feature?")
    print()
    
    # Vote on the proposal
    print("Voting on proposal...")
    city_hall.vote_on_proposal(proposal_id, vote_for=True)
    city_hall.vote_on_proposal(proposal_id, vote_for=True)
    city_hall.vote_on_proposal(proposal_id, vote_for=False)
    
    proposals = city_hall.get_proposals()
    for proposal in proposals:
        print(f"  Proposal #{proposal['id']}: {proposal['description']}")
        print(f"    Votes For: {proposal['votes_for']}")
        print(f"    Votes Against: {proposal['votes_against']}")
    print()
    
    # Display community info
    print("Community Information:")
    info = city_hall.get_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()
    print("=" * 50)


if __name__ == "__main__":
    main()
