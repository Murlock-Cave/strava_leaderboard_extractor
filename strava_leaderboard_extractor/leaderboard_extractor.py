from stravalib.client import Client
from strava_config import StravaConfig
import datetime


def print_sorted_leaderboard(
    dict_leaderboard, print_func=lambda key, val: print(f"{key}: {val}")
):
    for key, val in dict(
        sorted(dict_leaderboard.items(), key=lambda item: item[1], reverse=True)
    ).items():
        print_func(key, val)


def extract_leaderboard(config: StravaConfig):
    client = Client(access_token=config.access_token)
    club_activities = client.get_club_activities(
        club_id=config.club_id, limit=config.activities_limit
    )

    ranking_moving_time_dict = {}
    ranking_activities_count_dict = {}
    ranking_distance_dict = {}

    for activity in club_activities:
        athlete_name = f"{activity.athlete.firstname} {activity.athlete.lastname}"

        if athlete_name not in ranking_moving_time_dict:
            ranking_moving_time_dict.update({athlete_name: datetime.timedelta()})

        ranking_moving_time_dict[athlete_name] += activity.moving_time

        if athlete_name not in ranking_activities_count_dict:
            ranking_activities_count_dict.update({athlete_name: 0})

        ranking_activities_count_dict[athlete_name] += 1

        if athlete_name not in ranking_distance_dict:
            ranking_distance_dict.update({athlete_name: 0})

        ranking_distance_dict[athlete_name] += activity.distance

    print("\n Moving Time leaderboard:")
    print_sorted_leaderboard(ranking_moving_time_dict)

    print("\n Activities count leaderboard:")
    print_sorted_leaderboard(ranking_activities_count_dict)

    print("\n Distance leaderboard:")
    print_sorted_leaderboard(ranking_distance_dict)
