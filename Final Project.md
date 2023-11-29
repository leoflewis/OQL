# Hockey Database

## Tables

### Season
- PK Season ID
### Team
- PK Team ID
- Team Name
- Team Location
### Game
- PK Game ID
- FK Home Team
- FK Away Team
- Home Team Score
- Away Team Score
- Home Team Total Shots
- Away Team Total Shots
### Player
- PK Player ID
- Player Full Name
- FK Draft
### Game Event
- PK (Play ID, Game ID, Season ID)
- FK Player 1, Player 2 Player 3
- Event Type
### Draft

 