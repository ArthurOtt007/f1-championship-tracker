import fastf1
from fastf1.ergast import Ergast
import fastf1.plotting
import matplotlib.pyplot as plt
import os
import pandas as pd

# préparation du cache
if not os.path.exists('cache'):
    os.makedirs('cache')

fastf1.Cache.enable_cache('cache')
fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='fastf1')

#initialisation des paramètres
SEASON = int(input("Please enter the season you want to get : "))
ROUND = int(input("Please enter the number of the round you want to get : "))

#extraire le classement des pilotes suivant les paramètres introduits
def get_drivers_standings():
    ergast = Ergast()
    standings = ergast.get_driver_standings(season=SEASON, round=ROUND)
    return standings.content[0]

#calcul du nombre de points à attribuer pour la saison
def calculate_max_points_for_remaining_season():
    POINTS_FOR_SPRINT = 8 + 25 # winning the sprint and race (for sprint week-end)
    POINTS_FOR_CONVENTIONAL = 25 # winning the race (for conventional week-end)

    events = fastf1.events.get_event_schedule(SEASON, backend='ergast')
    events = events[events['RoundNumber'] > ROUND]
    # count how many sprints and conventional races are left
    sprint_events = len(events.loc[events["EventFormat"] == "sprint_qualifying"])
    conventional_events = len(events.loc[events["EventFormat"] == "conventional"])

    # calculate points for each
    sprint_points = sprint_events * POINTS_FOR_SPRINT
    conventional_points = conventional_events * POINTS_FOR_CONVENTIONAL

    return sprint_points + conventional_points
    
    # extraire le calendrier complet
    events = fastf1.events.get_event_schedule(SEASON, backend='ergast')

    # ne garder que les courses restantes dans la saison
    events_remaining = events[events['RoundNumber'] > ROUND]

    # Vérifier les formats exacts pour debug
    print(events_remaining[['RoundNumber', 'EventFormat']])

    total_points = 0

    for _, event in events_remaining.iterrows():
        fmt = event['EventFormat'].lower()
        if 'sprint' in fmt:
            # we sprint : points sprint + points course
            total_points += POINTS_SPRINT + POINTS_RACE
        elif 'conventional' in fmt:
            total_points += POINTS_RACE
        else:
            # Au cas où Ergast utilise un autre format
            print(f"Warning: unknown event format {event['EventFormat']} at Round {event['RoundNumber']}")

    return total_points


#déterminer si oui ou non les pilotes ont une chance de gagner le championnat
def calculate_who_can_win(driver_standings, max_points):
    LEADER_POINTS = int(driver_standings.loc[0]['points'])

    for i, _ in enumerate(driver_standings.iterrows()):
        driver = driver_standings.loc[i]
        driver_max_points = int(driver["points"]) + max_points
        LEADER_CURRENT = int(driver_standings['points'].max())
        can_win = 'Yes' if driver_max_points >= LEADER_CURRENT else 'No'
        #can_win = 'No' if driver_max_points < LEADER_POINTS else 'Yes'


        #print(f"{driver['position']}: {driver['givenName'] + ' ' + driver['familyName']}, "
              #f"Current points: {driver['points']}, "
              #f"Theoretical max points: {driver_max_points}, "
              #f"Can win: {can_win}")
        
def pretty_print(driver_standings, max_points):
    #LEADER_POINTS = int(driver_standings.loc[0]['points'])
    LEADER_POINTS = int(driver_standings['points'].max())  # prend le vrai leader


    data = []
    for i, _ in enumerate(driver_standings.iterrows()):
        driver = driver_standings.loc[i]
        driver_max_points = int(driver["points"]) + max_points
        can_win = '✅ Yes' if driver_max_points >= LEADER_POINTS else '❌ No'
        data.append([
            driver['position'],
            f"{driver['givenName']} {driver['familyName']}",
            driver['points'],
            driver_max_points,
            can_win
        ])

    df = pd.DataFrame(data, columns=["Pos", "Driver", "Points", "Max Possible", "Still in title fight"])
    print(df.to_string(index=False))

    df.to_excel("championship_chances.xlsx", index=False)


# tableau actuel du championnat
driver_standings = get_drivers_standings()

# les points restants à attribuer
points = calculate_max_points_for_remaining_season()

# qui peut encore gagner ou non ? 
calculate_who_can_win(driver_standings, points)

#belle mise en page
pretty_print(driver_standings, points)


   
