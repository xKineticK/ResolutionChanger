from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Game:
    id: str
    name: str

    def __str__(self) -> str:
        return self.name

class GameModel:
    def __init__(self):
        self.games: List[Game] = []
        self._selected_game: Optional[Game] = None

    def set_games(self, games: List[Game]) -> None:
        """Actualiza la lista de juegos"""
        self.games = games

    def get_games(self) -> List[Game]:
        """Retorna la lista de juegos"""
        return self.games

    def select_game(self, game_name: str) -> Optional[Game]:
        """Selecciona un juego por nombre"""
        for game in self.games:
            if game.name == game_name:
                self._selected_game = game
                return game
        return None

    def get_selected_game(self) -> Optional[Game]:
        """Retorna el juego seleccionado actualmente"""
        return self._selected_game