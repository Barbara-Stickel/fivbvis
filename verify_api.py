"""
Simple script to verify FIVB VIS API calls are working correctly.
Run this script directly to test your API methods.
"""
import json
from fivbvis import Beach, Player


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_result(name, passed, details=""):
    """Print test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"      {details}")


def verify_beach_team_list():
    """Verify getBeachTeamList with tournament 8244"""
    print_section("Testing getBeachTeamList")
    
    try:
        beach = Beach()
        print("Calling: beach.getBeachTeamList(no_tournament=8244, plays_in_main_draw=False)")
        
        result = beach.getBeachTeamList(
            no_tournament=8244,
            plays_in_main_draw=False,
            content_type='json'
        )
        teams = result['data']
        
        # Check if it's a list
        if isinstance(teams, list):
            team_count = len(teams)
            passed = team_count >= 80
            print_result(
                f"Retrieved {team_count} teams (expected >= 80)",
                passed
            )
            
            if team_count > 0:
                # Show sample team
                sample_team = teams[0]
                print(f"\n    Sample team data:")
                for key, value in list(sample_team.items())[:5]:
                    print(f"      - {key}: {value}")
            
            return passed
        else:
            print(f"    ⚠ Unexpected result type: {type(teams)}")
            print(f"    Result structure: {json.dumps(result, indent=2)[:500]}")
            return False
            
    except Exception as e:
        print_result("getBeachTeamList", False, f"Error: {str(e)}")
        import traceback
        print(f"\n    Full error:\n{traceback.format_exc()}")
        return False


def verify_beach_tournament_list():
    """Verify getBeachTournament with no=None"""
    print_section("Testing getBeachTournament (List)")
    
    try:
        beach = Beach()
        print("Calling: beach.getBeachTournament(no=None)")
        
        result = beach.getBeachTournament(no=None, content_type='json')
        
        # Parse result
        if isinstance(result, str):
            result = json.loads(result)
        
        # Extract tournaments data
        if isinstance(result, dict):
            tournaments = result.get('Tournaments', result.get('tournaments', result))
        else:
            tournaments = result
        
        if isinstance(tournaments, list):
            tournament_count = len(tournaments)
            passed = tournament_count > 0
            print_result(
                f"Retrieved {tournament_count} tournaments",
                passed
            )
            
            if tournament_count > 0:
                # Show sample tournament
                sample = tournaments[0]
                print(f"\n    Sample tournament:")
                for key in ['No', 'Code', 'Name', 'Type', 'Gender']:
                    if key in sample:
                        print(f"      - {key}: {sample[key]}")
            
            return passed
        else:
            print(f"    ⚠ Unexpected result type: {type(tournaments)}")
            print(f"    Keys available: {tournaments.keys() if hasattr(tournaments, 'keys') else 'N/A'}")
            return False
            
    except Exception as e:
        print_result("getBeachTournament (list)", False, f"Error: {str(e)}")
        import traceback
        print(f"\n    Full error:\n{traceback.format_exc()}")
        return False


def verify_beach_tournament_single():
    """Verify getBeachTournament with no=8244"""
    print_section("Testing getBeachTournament (Single)")
    
    try:
        beach = Beach()
        print("Calling: beach.getBeachTournament(no=8244)")
        
        result = beach.getBeachTournament(no=8244, content_type='json')
        
        # Parse result
        if isinstance(result, str):
            result = json.loads(result)
        
        # Extract tournament data
        if isinstance(result, dict):
            tournament = result.get('Tournament', result)
        else:
            tournament = result
        
        if isinstance(tournament, dict):
            has_data = any(key in tournament for key in ['No', 'Code', 'Name'])
            print_result("Retrieved tournament data", has_data)
            
            if has_data:
                print(f"\n    Tournament details:")
                for key in ['No', 'Code', 'Name', 'Type', 'CountryCode', 'StartDateMainDraw', 'EndDateMainDraw']:
                    if key in tournament:
                        print(f"      - {key}: {tournament[key]}")
            
            return has_data
        else:
            print(f"    ⚠ Unexpected result type: {type(tournament)}")
            return False
            
    except Exception as e:
        print_result("getBeachTournament (single)", False, f"Error: {str(e)}")
        import traceback
        print(f"\n    Full error:\n{traceback.format_exc()}")
        return False


def verify_player_list():
    """Verify getPlayer with no=None"""
    print_section("Testing getPlayer (List)")
    
    try:
        player_api = Player()
        print("Calling: player.getPlayer(no=None)")
        
        result = player_api.getPlayer(no=None, content_type='json')
        
        # Parse result
        if isinstance(result, str):
            result = json.loads(result)
        
        # Extract players data
        if isinstance(result, dict):
            players = result.get('Players', result.get('players', result))
        else:
            players = result
        
        if isinstance(players, list):
            player_count = len(players)
            passed = player_count > 0
            print_result(
                f"Retrieved {player_count} players",
                passed
            )
            
            if player_count > 0:
                # Show sample player
                sample = players[0]
                print(f"\n    Sample player:")
                for key in ['No', 'FirstName', 'LastName', 'Nationality', 'Gender']:
                    if key in sample:
                        print(f"      - {key}: {sample[key]}")
            
            return passed
        else:
            print(f"    ⚠ Unexpected result type: {type(players)}")
            return False
            
    except Exception as e:
        print_result("getPlayer (list)", False, f"Error: {str(e)}")
        import traceback
        print(f"\n    Full error:\n{traceback.format_exc()}")
        return False


def verify_player_single():
    """Verify getPlayer with no=143192"""
    print_section("Testing getPlayer (Single)")
    
    try:
        player_api = Player()
        player_no = int(143192.0)
        print(f"Calling: player.getPlayer(no={player_no})")
        
        result = player_api.getPlayer(no=player_no, content_type='json')
        
        # Parse result
        if isinstance(result, str):
            result = json.loads(result)
        
        # Extract player data
        if isinstance(result, dict):
            player = result.get('Player', result)
        else:
            player = result
        
        if isinstance(player, dict):
            has_data = any(key in player for key in ['No', 'FirstName', 'LastName'])
            print_result("Retrieved player data", has_data)
            
            if has_data:
                print(f"\n    Player details:")
                name = f"{player.get('FirstName', '')} {player.get('LastName', '')}".strip()
                if name:
                    print(f"      - Name: {name}")
                for key in ['No', 'Nationality', 'Gender', 'PlaysBeach', 'PlaysVolley', 'Height']:
                    if key in player:
                        print(f"      - {key}: {player[key]}")
            
            return has_data
        else:
            print(f"    ⚠ Unexpected result type: {type(player)}")
            return False
            
    except Exception as e:
        print_result("getPlayer (single)", False, f"Error: {str(e)}")
        import traceback
        print(f"\n    Full error:\n{traceback.format_exc()}")
        return False


def main():
    """Run all verification tests"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║           FIVB VIS API Verification Script                       ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    
    results = []
    
    # Run all tests
    results.append(("Beach Team List", verify_beach_team_list()))
    results.append(("Beach Tournament List", verify_beach_tournament_list()))
    results.append(("Beach Tournament Single", verify_beach_tournament_single()))
    results.append(("Player List", verify_player_list()))
    results.append(("Player Single", verify_player_single()))
    
    # Summary
    print_section("SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"  {status} {name}")
    
    print(f"\n  Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n  🎉 All API calls are working correctly!")
    else:
        print(f"\n  ⚠ {total - passed} test(s) failed. Check the details above.")
    
    print()


if __name__ == "__main__":
    main()

