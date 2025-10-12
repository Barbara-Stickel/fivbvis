"""
Integration tests for fivbvis - These tests make actual API calls to the FIVB VIS Web Service.
Run these tests when you want to verify that the API calls are working correctly.

Note: These tests require an active internet connection and may be slower than unit tests.
"""
import pytest
import json
from fivbvis import Beach, Player


class TestBeachIntegration:
    """Integration tests for Beach class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.beach = Beach()
    
    def test_getBeachTeamList_with_tournament(self):
        """Test getting beach team list for a specific tournament"""
        result = self.beach.getBeachTeamList(
            no_tournament=8244,
            plays_in_main_draw=False,
            content_type='json'
        )
        
        # Parse result if it's a string
        if isinstance(result, str):
            result = json.loads(result)
        
        # Verify we got data
        assert result is not None, "Result should not be None"
        
        # Check if result has a list of teams
        if isinstance(result, dict):
            # Sometimes the API returns a dict with a key containing the list
            teams = result.get('VisTeams', result.get('teams', result))
        else:
            teams = result
        
        # Verify we have at least 80 teams
        if isinstance(teams, list):
            team_count = len(teams)
            print(f"\n✓ Retrieved {team_count} teams for tournament 8244")
            assert team_count >= 80, f"Expected at least 80 teams, got {team_count}"
        else:
            # If it's a single object, check if there's a count or array inside
            print(f"\n✓ Result type: {type(teams)}")
            print(f"✓ Result keys: {teams.keys() if hasattr(teams, 'keys') else 'N/A'}")
    
    def test_getBeachTournament_single(self):
        """Test getting a single beach tournament"""
        result = self.beach.getBeachTournament(no=8244, content_type='json')
        
        # Parse result if it's a string
        if isinstance(result, str):
            result = json.loads(result)
        
        assert result is not None, "Result should not be None"
        
        # Check for tournament data
        if isinstance(result, dict):
            tournament = result.get('Tournament', result)
        else:
            tournament = result
        
        print(f"\n✓ Retrieved tournament: {tournament}")
        
        # Verify tournament has basic fields
        if isinstance(tournament, dict):
            assert 'No' in tournament or 'Code' in tournament or 'Name' in tournament, \
                "Tournament should have basic identifying fields"
            print(f"  - Tournament details found")
    
    def test_getBeachTournament_list(self):
        """Test getting beach tournament list"""
        result = self.beach.getBeachTournament(no=None, content_type='json')
        
        # Parse result if it's a string
        if isinstance(result, str):
            result = json.loads(result)
        
        assert result is not None, "Result should not be None"
        
        # Check if result has a list of tournaments
        if isinstance(result, dict):
            tournaments = result.get('Tournaments', result.get('tournaments', result))
        else:
            tournaments = result
        
        if isinstance(tournaments, list):
            tournament_count = len(tournaments)
            print(f"\n✓ Retrieved {tournament_count} tournaments")
            assert tournament_count > 0, "Expected at least 1 tournament"
        else:
            print(f"\n✓ Result type: {type(tournaments)}")
            print(f"✓ Sample data: {str(tournaments)[:200]}")


class TestPlayerIntegration:
    """Integration tests for Player class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.player = Player()
    
    def test_getPlayer_single(self):
        """Test getting a single player"""
        # Convert float to int
        player_no = int(143192.0)
        
        result = self.player.getPlayer(no=player_no, content_type='json')
        
        # Parse result if it's a string
        if isinstance(result, str):
            result = json.loads(result)
        
        assert result is not None, "Result should not be None"
        
        # Check for player data
        if isinstance(result, dict):
            player = result.get('Player', result)
        else:
            player = result
        
        print(f"\n✓ Retrieved player: {player}")
        
        # Verify player has basic fields
        if isinstance(player, dict):
            has_basic_info = any(key in player for key in ['No', 'FirstName', 'LastName', 'TeamName'])
            assert has_basic_info, "Player should have basic identifying fields"
            
            # Print some player info
            if 'FirstName' in player and 'LastName' in player:
                print(f"  - Player name: {player.get('FirstName')} {player.get('LastName')}")
            if 'Nationality' in player:
                print(f"  - Nationality: {player.get('Nationality')}")
    
    def test_getPlayer_list(self):
        """Test getting player list"""
        result = self.player.getPlayer(no=None, content_type='json')
        
        # Parse result if it's a string
        if isinstance(result, str):
            result = json.loads(result)
        
        assert result is not None, "Result should not be None"
        
        # Check if result has a list of players
        if isinstance(result, dict):
            players = result.get('Players', result.get('players', result))
        else:
            players = result
        
        if isinstance(players, list):
            player_count = len(players)
            print(f"\n✓ Retrieved {player_count} players")
            assert player_count > 0, "Expected at least 1 player"
        else:
            print(f"\n✓ Result type: {type(players)}")
            print(f"✓ Sample data: {str(players)[:200]}")


def test_api_connection():
    """Quick test to verify API connection is working"""
    beach = Beach()
    try:
        result = beach.getBeachTournament(no=8244, content_type='json')
        print("\n✓ API connection successful")
        return True
    except Exception as e:
        pytest.fail(f"API connection failed: {str(e)}")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])

