# C-A-D-E
COMMUNITY APPLICATION DEVELOPMENT ENVIRONMENT

## CityHall

CityHall is the central hub for community governance and administration in C-A-D-E.

### Features

- **Member Management**: Add and remove community members
- **Announcements**: Make community-wide announcements
- **Proposals**: Submit and vote on community proposals
- **Community Information**: Track community statistics

### Usage

Run the demo:
```bash
python3 cityhall.py
```

Run tests:
```bash
python3 test_cityhall.py
```

### Example

```python
from cityhall import CityHall

# Create a CityHall instance
city_hall = CityHall("My Community")

# Add members
city_hall.add_member("Alice")
city_hall.add_member("Bob")

# Make an announcement
city_hall.make_announcement("Welcome everyone!")

# Submit and vote on a proposal
proposal_id = city_hall.submit_proposal("Should we add feature X?")
city_hall.vote_on_proposal(proposal_id, vote_for=True)

# Get community info
info = city_hall.get_info()
print(f"Community: {info['name']}, Members: {info['member_count']}")
```
