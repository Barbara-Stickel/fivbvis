import pandas as pd

from .fivbvis import FivbVis


class Article(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def getArticle(self, no, fields=None, content_type='xml'):
        return self.fivb_vis.get('GetArticle', fields=fields, content_type=content_type, no=no)

    def getArticleListWithFilter(self, fields=None, filter=None, content_type='xml'):
        return self.fivb_vis.get_list('GetArticleList', fields, filter, content_type)

    def getArticleListWithTags(self, fields=None, tags=None, content_type='xml'):
        return self.fivb_vis.get_list_with_tags('GetArticleList', fields, tags, content_type)

class Beach(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def getBeachMatch(self, no, fields=None, content_type='json'):
        return self.fivb_vis.get('GetBeachMatch', fields=fields, content_type=content_type, no=no)

    def getBeachMatchList(self, fields, filter=None, content_type='json'):
        return self.fivb_vis.get_list('GetBeachMatchList', fields, filter, content_type)

    def getBeachTournamentRanking(self, no_tournament, plays_in_main_draw=False, fields=None, content_type='json'):
        """It returns the ranking of all the teams for a given tournament.
        If you want all the rankings, keep no_tournament to None.

        Parameters:       
        - `no_tournament`: The number of the beach tournament. If no_tournament is None, it will return all the beach tournaments.
        - `plays_in_main_draw`: If True, it will return the teams that play in the main draw. If False, it will return all the teams that play in the tournament.
        - `fields`: The fields to return. If fields is None, it will return all the default fields.
        - `content_type`: The content type to return. Defaults to 'json'.

        Returned fields:
        - `No`: The number of the team.
        - `NoPlayer1`: The number of the first player.
        - `NoPlayer2`: The number of the second player.
        - `Name`: The name of the team.
        - `NoTournament`: The number of the tournament.

        Documentation: https://www.fivb.org/VisSDK/VisWebService/GetBeachTeamList.html
        Information about the filters: https://www.fivb.org/VisSDK/VisWebService/BeachTeamFilter.html
        Full list of fields: https://www.fivb.org/VisSDK/VisWebService/BeachTeam.html
        """
        if fields is None:
            # Use default fields
            fields = """
                No NoPlayer1 NoPlayer2 NoTournament
                Name Rank
                EarnedPointsTeam EarningsTeam 
                Player1FirstName Player1LastName
                Player2FirstName Player2LastName
            """
            
        # Build filters
        filters = {}
        if no_tournament is not None:
            filters['no_tournament'] = no_tournament
        if plays_in_main_draw:
            # In fivbvis, true returns the teams that play in the main draw,
            # false returns the teams that play in the qualification
            # and none returns all the teams that play in the tournament.
            # Here we set the logic to have true = main draw and false = all teams.
            filters['plays_in_main_draw'] = 'true'
        
        filters = filters if filters else None
        
        return self.fivb_vis.get('GetBeachTeamList', fields=fields, content_type=content_type, filters=filters)

    def getBeachTournament(self, no, fields=None, content_type='json'):
        """Get beach tournaments.

        Parameters:       
        - `no`: The number of the beach tournament. If no is None, it will return all the beach tournaments.
        - `fields`: The fields to return. If fields is None, it will return all the default fields.
        - `content_type`: The content type to return. Defaults to 'json'.

        Full list of fields: https://www.fivb.org/VisSDK/VisWebService/#BeachTournament.html
        """
        if fields is None:
            # Use default fields
            fields = """
                No Code Name Title Type CountryCode
                StartDateQualification StartDateMainDraw
                EndDateQualification EndDateMainDraw
                NbTeamsQualification NbTeamsFromQualification NbTeamsMainDraw
                Status Gender
            """
        
        request_type = 'GetBeachTournamentList' if no is None else 'GetBeachTournament'
        return self.fivb_vis.get(request_type, fields=fields, content_type=content_type, no=no)
 
    def getBeachWorldTourRanking(self, gender, number, reference_date=None, fields=None, content_type='json'):
        raise NotImplementedError("This method is not working anymore on VIS Web Service: https://www.fivb.org/VisSDK/VisWebService/RequestList.html")
    
    def getBeachOlympicSelectionRanking(self):
        raise NotImplementedError("Method not yet implemented")

    def getBeachRound(self):
        raise NotImplementedError("Method not yet implemented")

    def getBeachRoundList(self):
        raise NotImplementedError("Method not yet implemented")

    def getBeachRoundRanking(self):
        raise NotImplementedError("Method not yet implemented")

    def getBeachTeam(self):
        raise NotImplementedError("Method not yet implemented")
        
class Player(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def get_player_info(self, no, fields=None, content_type='json'):
        """Get player information.
        
        Parameters:
        - `no`: The player number (required).
        - `fields`: The fields to return. If fields is None, it will return all the default fields.
        - `content_type`: The content type to return. Defaults to 'json'.
        
        Full list of fields: https://www.fivb.org/VisSDK/VisWebService/#Player.html
        Documentation example: https://www.fivb.org/VisSDK/VisWebService/#GetPlayer.html
        """
        if fields is None:
            # Use default fields based on documentation example
            fields = """
                No FederationCode FirstName LastName Gender 
                Nationality ActiveBeach ActiveVolley 
                PlaysBeach PlaysVolley TeamName Birthdate Height
            """
        request_type = 'GetPlayerList' if no is None else 'GetPlayer'
        return self.fivb_vis.get(request_type, fields=fields, content_type=content_type, no=no)

    def get_player_list(self, fields=None):
        df = pd.DataFrame(self.get_player_info(no=None, fields=fields, content_type='json')['data'])
        return df

class Volleyball(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def getVolleyMatch(self, no, fields=None, content_type='xml'):
        return self.fivb_vis.get('GetVolleyMatch', fields=fields, content_type=content_type, no=no)

    def getVolleyMatchList(self, fields=None, filter=None, content_type='xml'):
        return self.fivb_vis.get_list('GetVolleyMatchList', fields, filter, content_type)
