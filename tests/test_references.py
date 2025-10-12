"""
Tests for the fivbvis reference classes (Article, Beach, Player, Volleyball)
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fivbvis import Article, Beach, Player, Volleyball


class TestArticle:
    """Tests for the Article class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.article = Article()
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getArticle(self, mock_get):
        """Test getting a single article"""
        # Mock the response
        mock_response = Mock()
        mock_response.text = '<Article><No>123</No><Title>Test</Title></Article>'
        mock_get.return_value = mock_response
        
        result = self.article.getArticle(no=123, content_type='xml')
        
        # Verify the request was made
        assert mock_get.called
        call_args = mock_get.call_args
        assert 'Type="GetArticle"' in call_args[0][0]
        assert 'No="123"' in call_args[0][0]
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getArticle_with_fields(self, mock_get):
        """Test getting an article with specific fields"""
        mock_response = Mock()
        mock_response.text = '<Article><No>123</No></Article>'
        mock_get.return_value = mock_response
        
        fields = "No Title PublishDate"
        result = self.article.getArticle(no=123, fields=fields, content_type='xml')
        
        call_args = mock_get.call_args
        assert 'Fields="No Title PublishDate"' in call_args[0][0]


class TestBeach:
    """Tests for the Beach class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.beach = Beach()
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getBeachMatch(self, mock_get):
        """Test getting a single beach match"""
        mock_response = Mock()
        mock_response.text = '<BeachMatch><No>456</No></BeachMatch>'
        mock_get.return_value = mock_response
        
        result = self.beach.getBeachMatch(no=456, content_type='xml')
        
        assert mock_get.called
        call_args = mock_get.call_args
        assert 'Type="GetBeachMatch"' in call_args[0][0]
        assert 'No="456"' in call_args[0][0]
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getBeachTournament(self, mock_get):
        """Test getting a beach tournament"""
        mock_response = Mock()
        mock_response.json.return_value = {"No": 789, "Name": "Test Tournament"}
        mock_get.return_value = mock_response
        
        result = self.beach.getBeachTournament(no=789, content_type='json')
        
        assert mock_get.called
        call_args = mock_get.call_args
        assert 'Type="GetBeachTournament"' in call_args[0][0]
        assert 'No="789"' in call_args[0][0]
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getBeachTournament_list(self, mock_get):
        """Test getting beach tournament list when no is None"""
        mock_response = Mock()
        mock_response.json.return_value = [{"No": 1}, {"No": 2}]
        mock_get.return_value = mock_response
        
        result = self.beach.getBeachTournament(no=None, content_type='json')
        
        call_args = mock_get.call_args
        assert 'Type="GetBeachTournamentList"' in call_args[0][0]
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getBeachTeamList_with_filters(self, mock_get):
        """Test getting beach team list with filters"""
        mock_response = Mock()
        mock_response.json.return_value = [{"No": 1, "Name": "Team A"}]
        mock_get.return_value = mock_response
        
        result = self.beach.getBeachTeamList(
            no_tournament=123, 
            plays_in_main_draw=True, 
            content_type='json'
        )
        
        call_args = mock_get.call_args
        url = call_args[0][0]
        assert 'Type="GetBeachTeamList"' in url
        assert '<Filter' in url
        assert 'NoTournament="123"' in url
        assert 'PlaysInMainDraw="true"' in url
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getBeachTeamList_multiline_fields(self, mock_get):
        """Test that multiline fields are properly formatted"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        fields = """
            No Name
            Player1FirstName Player1LastName
        """
        result = self.beach.getBeachTeamList(
            no_tournament=123, 
            fields=fields,
            content_type='json'
        )
        
        call_args = mock_get.call_args
        url = call_args[0][0]
        # Should be collapsed to single line
        assert 'Fields="No Name Player1FirstName Player1LastName"' in url
    
    def test_getBeachTournamentRanking_not_implemented(self):
        """Test that deprecated method raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            self.beach.getBeachTournamentRanking()
    
    def test_getBeachWorldTourRanking_not_implemented(self):
        """Test that deprecated method raises NotImplementedError"""
        with pytest.raises(NotImplementedError):
            self.beach.getBeachWorldTourRanking(gender='M', number=50)


class TestPlayer:
    """Tests for the Player class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.player = Player()
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getPlayer(self, mock_get):
        """Test getting a single player"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "No": 100002,
            "FirstName": "John",
            "LastName": "Doe"
        }
        mock_get.return_value = mock_response
        
        result = self.player.getPlayer(no=100002, content_type='json')
        
        assert mock_get.called
        call_args = mock_get.call_args
        assert 'Type="GetPlayer"' in call_args[0][0]
        assert 'No="100002"' in call_args[0][0]
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getPlayer_list(self, mock_get):
        """Test getting player list when no is None"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        result = self.player.getPlayer(no=None, content_type='json')
        
        call_args = mock_get.call_args
        assert 'Type="GetPlayerList"' in call_args[0][0]
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getPlayer_with_custom_fields(self, mock_get):
        """Test getting a player with custom fields"""
        mock_response = Mock()
        mock_response.json.return_value = {"No": 100002}
        mock_get.return_value = mock_response
        
        fields = "No FirstName LastName Nationality"
        result = self.player.getPlayer(no=100002, fields=fields, content_type='json')
        
        call_args = mock_get.call_args
        assert 'Fields="No FirstName LastName Nationality"' in call_args[0][0]


class TestVolleyball:
    """Tests for the Volleyball class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.volleyball = Volleyball()
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getVolleyMatch(self, mock_get):
        """Test getting a volleyball match"""
        mock_response = Mock()
        mock_response.text = '<VolleyMatch><No>999</No></VolleyMatch>'
        mock_get.return_value = mock_response
        
        result = self.volleyball.getVolleyMatch(no=999, content_type='xml')
        
        assert mock_get.called
        call_args = mock_get.call_args
        assert 'Type="GetVolleyMatch"' in call_args[0][0]
        assert 'No="999"' in call_args[0][0]
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_getVolleyMatch_with_fields(self, mock_get):
        """Test getting a volleyball match with specific fields"""
        mock_response = Mock()
        mock_response.text = '<VolleyMatch/>'
        mock_get.return_value = mock_response
        
        fields = "No Date Team1 Team2"
        result = self.volleyball.getVolleyMatch(no=999, fields=fields, content_type='xml')
        
        call_args = mock_get.call_args
        assert 'Fields="No Date Team1 Team2"' in call_args[0][0]


class TestFivbVisCore:
    """Tests for core FivbVis functionality"""
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_snake_case_to_pascal_case(self, mock_get):
        """Test that snake_case parameters are converted to PascalCase"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        beach = Beach()
        # Test with snake_case parameter
        beach.fivb_vis.get(
            'TestRequest', 
            content_type='json',
            test_parameter='value',
            another_test='value2'
        )
        
        call_args = mock_get.call_args
        url = call_args[0][0]
        assert 'TestParameter="value"' in url
        assert 'AnotherTest="value2"' in url
    
    @patch('fivbvis.fivbvis.httpx.get')
    def test_fields_cleanup(self, mock_get):
        """Test that fields with extra whitespace are cleaned up"""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response
        
        player = Player()
        fields = """
            No    FirstName
            LastName    
            Gender
        """
        player.getPlayer(no=123, fields=fields, content_type='json')
        
        call_args = mock_get.call_args
        url = call_args[0][0]
        # Should have single spaces only
        assert 'Fields="No FirstName LastName Gender"' in url

