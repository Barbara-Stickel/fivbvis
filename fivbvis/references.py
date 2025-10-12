from .fivbvis import FivbVis

class Article(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def getArticle(self, no, fields=None, content_type='xml'):
        result = self.fivb_vis.get('GetArticle', fields=fields, content_type=content_type, no=no)
        return result

    def getArticleListWithFilter(self, fields=None, filter=None, content_type='xml'):
        result = self.fivb_vis.get_list('GetArticleList', fields, filter, content_type)
        return result

    def getArticleListWithTags(self, fields=None, tags=None, content_type='xml'):
        result = self.fivb_vis.get_list_with_tags('GetArticleList', fields, tags, content_type)
        return result

class Beach(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def getBeachMatch(self, no, fields=None, content_type='xml'):
        result = self.fivb_vis.get('GetBeachMatch', fields=fields, content_type=content_type, no=no)
        return result

    def getBeachMatchList(self, fields, filter=None, content_type='xml'):
        result = self.fivb_vis.get_list('GetBeachMatchList', fields, filter, content_type)
        return result

    def getBeachOlympicSelectionRanking():
        return

    def getBeachRound():
        return

    def getBeachRoundList():
        return

    def getBeachRoundRanking():
        return

    def getBeachTeam():
        return

    def getBeachTeamList(self, no_tournament, plays_in_main_draw=False, fields=None, content_type='json'):
        """Does the same as getBeachTournamentRanking method should be doing. It returns the ranking of all the teams for a given tournament.
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
        - `Rank`: The rank of the team.
        - `EarnedPointsTeam`: The earned points of the team.
        - `EarningsTeam`: The earnings of the team.
        - `NoTournament`: The number of the tournament.

        Documentation: https://www.fivb.org/VisSDK/VisWebService/GetBeachTeamList.html
        Information about the filters: https://www.fivb.org/VisSDK/VisWebService/BeachTeamFilter.html
        Full list of fields: https://www.fivb.org/VisSDK/VisWebService/BeachTeam.html
        """
        if fields is None:
            # Use default fields
            fields = 'No NoPlayer1 NoPlayer2 Name Rank EarnedPointsTeam EarningsTeam NoTournament Player1FirstName Player1LastName Player2FirstName Player2LastName'

        filters = {}
        if no_tournament is not None:
            filters['no_tournament'] = no_tournament
        
        if plays_in_main_draw:
            filters['plays_in_main_draw'] = 'true'

        if len(filters) == 0:
            filters = None
        
        request_type = 'GetBeachTeamList'
        result = self.fivb_vis.get(request_type, fields=fields, content_type=content_type, filters=filters)
        
        return result

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
            fields = 'No Code Name Title Type CountryCode StartDateQualification StartDateMainDraw EndDateQualification EndDateMainDraw NbTeamsQualification NbTeamsFromQualification NbTeamsMainDraw Status Gender'
        
        if no is None:
            request_type = 'GetBeachTournamentList'
            result = self.fivb_vis.get(request_type, fields=fields, content_type=content_type)
        else:
            request_type = 'GetBeachTournament'
            result = self.fivb_vis.get(request_type, fields=fields, content_type=content_type, no=no)
        return result

    def getBeachTournamentRanking(self):
        """Get beach tournament ranking.
        Not working anymore on VIS Web Service: https://www.fivb.org/VisSDK/VisWebService/RequestList.html
        """
        raise NotImplementedError("This method is not working anymore on VIS Web Service: https://www.fivb.org/VisSDK/VisWebService/RequestList.html")
        

    def getBeachWorldTourRanking(self, gender, number, reference_date=None, fields=None, content_type='json'):
        raise NotImplementedError("This method is not working anymore on VIS Web Service: https://www.fivb.org/VisSDK/VisWebService/RequestList.html")
        
        
class Player(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def getPlayer(self, no, fields=None, content_type='json'):
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
            fields = 'No FederationCode FirstName LastName Gender Nationality ActiveBeach ActiveVolley PlaysBeach PlaysVolley TeamName Birthdate Height'
        if no is None:
            request_type = 'GetPlayerList'
        else:
            request_type = 'GetPlayer'

        result = self.fivb_vis.get(request_type, fields=fields, content_type=content_type, no=no)
        return result

class Volleyball(FivbVis):
    def __init__(self):
        self.fivb_vis = FivbVis()

    def getVolleyMatch(self, no, fields=None, content_type='xml'):
        result = self.fivb_vis.get('GetVolleyMatch', fields=fields, content_type=content_type, no=no)
        return result

    def getVolleyMatchList(self, fields=None, filter=None, content_type='xml'):
        result = self.fivb_vis.get_list('GetVolleyMatchList', fields, filter, content_type)
        return result
