# beach/tournament_status.py
from enum import IntEnum

class TournamentStatus(IntEnum):
    """Tournament status from the FIVB VIS Web Service

    https://www.fivb.org/VisSDK/VisWebService/BeachTournamentStatus.html
    """
    NotOpen = 0
    Open = 1
    Running = 6
    Finished = 7
    PaymentPending = 8
    Paid = 9
    Cancelled = 10
    Unknown = -1

    @classmethod
    def _missing_(cls, value: object):
        # Any unknown integer maps to Unknown (forward compatible)
        if isinstance(value, int):
            return cls.Unknown
        return super()._missing_(value)

    def name_str(self) -> str:
        """Return the human-readable name of the tournament status"""
        return self.name

    def is_active(self) -> bool:
        return self in (TournamentStatus.Open, TournamentStatus.Running)

    def is_finished(self) -> bool:
        return self in (TournamentStatus.Finished, TournamentStatus.Paid, TournamentStatus.PaymentPending)

class Gender(IntEnum):
    Men = 0
    Women = 1
    Unknown = 2
    
    @classmethod
    def _missing_(cls, value: object):
        # Any unknown integer maps to Unknown (forward compatible)
        if isinstance(value, int):
            return cls.Unknown
        return super()._missing_(value)
    
    def name_str(self) -> str:
        """Return the human-readable name of the tournament status"""
        return self.name
    
    def is_men(self) -> bool:
        return self in (Gender.Men)
    
    def is_women(self) -> bool:
        return self in (Gender.Women)

class BeachTournamentType(IntEnum):
    """Tournament types from the FIVB VIS Web Service
    
    Full list: https://www.fivb.org/VisSDK/VisWebService/BeachTournamentType.html
    """
    GrandSlam = 0
    Open = 1
    # Challenger = 2
    WorldSeries = 3
    WorldChamp = 4
    OlympicGames = 5
    Satellite = 6
    ContinentalChamp = 7
    OtherContinental = 8
    Other = 9
    Masters = 10
    ContinentalCup = 11
    ContinentalTour = 12
    JuniorWorldChamp = 13
    YouthWorldChamp = 14
    NationalTour = 15
    NationalTourU23 = 16
    NationalTourU21 = 17
    NationalTourU19 = 18
    NationalTourU20 = 19
    NationalTourU17 = 20
    NationalTourU15 = 21
    ContinentalChampU22 = 22
    ContinentalChampU20 = 23
    ContinentalChampU18 = 24
    WorldChampU23 = 25
    WorldChampU21 = 26
    WorldChampU19 = 27
    NationalTourU14 = 28
    NationalTourU16 = 29
    NationalTourU18 = 30
    WorldChampU17 = 31
    MajorSeries = 32
    WorldTourFinals = 33
    ZonalTour = 34
    Test = 35
    SnowVolleyball = 36
    ContinentalCupFinal = 37
    WorldTour5Star = 38
    WorldTour4Star = 39
    WorldTour3Star = 40
    WorldTour2Star = 41
    WorldTour1Star = 42
    YouthOlympicGames = 43
    MultiSports = 44
    NationalSnow = 45
    NationalTourU22 = 46
    ContinentalChampU21 = 47
    ContinentalChampU19 = 48
    OlympicGamesQualification = 49
    KingOfTheCourt = 50
    Elite16 = 51
    Challenger = 52
    Future = 53
    Unknown = -1

    @classmethod
    def _missing_(cls, value: object):
        # Any unknown integer maps to Unknown (forward compatible)
        if isinstance(value, int):
            return cls.Unknown
        return super()._missing_(value)

    def name_str(self) -> str:
        """Return the human-readable name of the tournament type"""
        return self.name

    def is_pro_tour(self) -> bool:
        return self in (
            BeachTournamentType.Elite16,
            BeachTournamentType.Challenger,
            BeachTournamentType.Future,
            BeachTournamentType.WorldTour5Star,
            BeachTournamentType.WorldTour4Star,
            BeachTournamentType.WorldTour3Star,
            BeachTournamentType.WorldTour2Star,
            BeachTournamentType.WorldTour1Star,
            BeachTournamentType.WorldChamp,
            BeachTournamentType.OlympicGames
        )

    def is_world_champ(self) -> bool:
        return self in (BeachTournamentType.WorldChamp)
    
    def is_olympic_games(self) -> bool:
        return self in (BeachTournamentType.OlympicGames)
    
    def is_elite16(self) -> bool:
        return self in (BeachTournamentType.Elite16)
    
    def is_challenger(self) -> bool:
        return self in (BeachTournamentType.Challenger)
    
    def is_future(self) -> bool:
        return self in (BeachTournamentType.Future)
