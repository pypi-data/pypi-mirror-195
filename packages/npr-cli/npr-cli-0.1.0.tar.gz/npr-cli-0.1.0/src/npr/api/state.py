import json
from dataclasses import asdict, dataclass
from pathlib import Path

import vlc

from npr.domain import Player, Stream
from npr.domain.constants import NPRRC


@dataclass
class AppState:
    favorites: list[Stream]
    last_played: Stream | None

    player: Player = Player(vlc.MediaPlayer)

    @classmethod
    def load(cls, state_file: Path = NPRRC) -> "AppState":
        state_file.touch()

        with state_file.open() as f:
            try:
                c = json.load(f)
                return cls(
                    favorites=[Stream(**s) for s in c["favorites"]],
                    last_played=Stream(**c["last_played"])
                    if c["last_played"]
                    else None,
                )
            except json.JSONDecodeError:
                return cls([], None)

    def write(self, state_file: Path = NPRRC):
        with state_file.open("w") as f:
            _serialized = {
                "favorites": [asdict(s) for s in self.favorites],
                "last_played": asdict(self.last_played) if self.last_played else None,
            }

            json.dump(_serialized, f)
