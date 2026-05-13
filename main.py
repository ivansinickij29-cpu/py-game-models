import init_django_orm  # noqa: F401
import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json", "r") as f:
        all_players_data = json.load(f)

    for player_nickname, player_details in all_players_data.items():
        race_obj, _ = Race.objects.get_or_create(
            name=player_details["race"]["name"],
            defaults={"description": player_details["race"].get("description", "")}
        )

        for skill_info in player_details["race"]["skills"]:
            Skill.objects.get_or_create(
                name=skill_info["name"],
                race=race_obj,  # Прив'язуємо скіл до об'єкта раси
                defaults={"bonus": skill_info.get("bonus", "")}
            )
        guild_obj = None
        if player_details.get("guild"):  # Перевіряємо, чи є ключ 'guild' і він не None
            guild_obj, _ = Guild.objects.get_or_create(
                name=player_details["guild"]["name"],
                defaults={"description": player_details["guild"].get("description")}  # description може бути null
            )

        Player.objects.create(
            nickname=player_nickname,  # Використовуємо ключ словника як нікнейм гравця
            email=player_details['email'],
            bio=player_details.get('bio', ''),
            race=race_obj,
            guild=guild_obj,
        )


if __name__ == "__main__":
    main()
