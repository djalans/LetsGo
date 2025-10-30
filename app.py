from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)


@dataclass
class Player:
    id: str
    name: str
    position: str
    is_starting: bool = False
    confirmed: bool = False


@dataclass
class MatchInfo:
    opponent: str = ""
    date: str = ""
    time: str = ""
    location: str = ""


@dataclass
class TeamState:
    name: str
    players: Dict[str, Player] = field(default_factory=dict)
    match: MatchInfo = field(default_factory=MatchInfo)

    def add_player(self, name: str, position: str) -> Player:
        player_id = str(uuid.uuid4())
        player = Player(id=player_id, name=name, position=position)
        self.players[player_id] = player
        return player

    def update_player(self, player_id: str, *, is_starting: Optional[bool] = None, confirmed: Optional[bool] = None) -> None:
        player = self.players.get(player_id)
        if not player:
            return
        if is_starting is not None:
            player.is_starting = is_starting
        if confirmed is not None:
            player.confirmed = confirmed

    def remove_player(self, player_id: str) -> None:
        self.players.pop(player_id, None)

    def starting_lineup(self) -> List[Player]:
        return [p for p in self.players.values() if p.is_starting]

    def bench_players(self) -> List[Player]:
        return [p for p in self.players.values() if not p.is_starting]


def sort_players(players: List[Player]) -> List[Player]:
    return sorted(players, key=lambda player: player.name.lower())


def get_team_state() -> TeamState:
    if not hasattr(app, "team_state"):
        app.team_state = TeamState(name="Mi Equipo")  # type: ignore[attr-defined]
    return app.team_state  # type: ignore[attr-defined]


@app.route("/")
def index():
    team = get_team_state()
    starting = sort_players(team.starting_lineup())
    bench = sort_players(team.bench_players())
    return render_template(
        "index.html",
        team=team,
        starting=starting,
        bench=bench,
    )


@app.route("/player/add", methods=["POST"])
def add_player():
    team = get_team_state()
    name = request.form.get("name", "").strip()
    position = request.form.get("position", "").strip()

    if name:
        team.add_player(name=name, position=position)
    return redirect(url_for("index"))


@app.route("/player/<player_id>/toggle_start", methods=["POST"])
def toggle_start(player_id: str):
    team = get_team_state()
    player = team.players.get(player_id)
    if player:
        team.update_player(player_id, is_starting=not player.is_starting)
    return redirect(url_for("index"))


@app.route("/player/<player_id>/confirm", methods=["POST"])
def confirm_player(player_id: str):
    team = get_team_state()
    player = team.players.get(player_id)
    if player:
        team.update_player(player_id, confirmed=True)
    return redirect(url_for("index"))


@app.route("/player/<player_id>/unconfirm", methods=["POST"])
def unconfirm_player(player_id: str):
    team = get_team_state()
    player = team.players.get(player_id)
    if player:
        team.update_player(player_id, confirmed=False)
    return redirect(url_for("index"))


@app.route("/player/<player_id>/delete", methods=["POST"])
def delete_player(player_id: str):
    team = get_team_state()
    team.remove_player(player_id)
    return redirect(url_for("index"))


@app.route("/match", methods=["GET", "POST"])
def match_info():
    team = get_team_state()

    if request.method == "POST":
        team.match.opponent = request.form.get("opponent", "").strip()
        team.match.date = request.form.get("date", "").strip()
        team.match.time = request.form.get("time", "").strip()
        team.match.location = request.form.get("location", "").strip()
        return redirect(url_for("match_info"))

    return render_template("match.html", team=team)


@app.route("/register", methods=["GET", "POST"])
def register_player():
    team = get_team_state()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        position = request.form.get("position", "").strip()
        if name:
            team.add_player(name=name, position=position)
            return redirect(url_for("index"))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
