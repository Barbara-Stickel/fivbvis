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
    
    def is_men(self) -> bool:
        return self in (Gender.Men)
    
    def is_women(self) -> bool:
        return self in (Gender.Women)

class BeachTournamentType(IntEnum):
    """Tournament types from the FIVB VIS Web Service
    
    Full list: https://www.fivb.org/VisSDK/VisWebService/BeachTournamentType.html
    """
    WorldChamp = 4
    OlympicGames = 5
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

    def is_pro_tour(self) -> bool:
        return self in (BeachTournamentType.Elite16, BeachTournamentType.Challenger, BeachTournamentType.Future)

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