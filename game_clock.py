from datetime import datetime, timedelta

GAME_START = datetime(2050, 5, 2, 10, 15)
INCREMENT_MINUTES = 1


class GameClock:
    def __init__(self, start_time: datetime = GAME_START):
        self.time = start_time

    def increment(self):
        self.time += timedelta(minutes=INCREMENT_MINUTES)

    @property
    def display(self):
        return self.time.strftime("%H:%M  %b-%d")
