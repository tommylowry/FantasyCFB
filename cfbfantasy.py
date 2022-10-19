import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_schools(year):
    """ TODO definition
    """
    
    schools = []
    if year == "2022":
        schools = [ "Alabama", "Arkansas", "Auburn", "Baylor", "BYU", "Cincinnati", "Clemson", "Fresno State", "Georgia", "Houston", "Iowa",
                  "Kentucky", "LSU", "Miami (FL)", "Michigan", "Michigan State", "Minnesota", "Mississippi State", "NC State", "Notre Dame",
                  "Ohio State", "Oklahoma", "Oklahoma State", "Ole Miss", "Oregon", "Penn State", "Pitt", "Purdue", "Tennessee",  "Texas",
                  "Texas A&M", "UCF", "USC", "Utah", "Wake Forest", "Wisconsin" ]
    
    return schools

def get_players(schools, position, year):
    """ TODO definition
    """

    if not schools:
        return None
    
    dict = {}

    for school in schools:
        
        try:
            html = f"https://www.sports-reference.com/cfb/schools/{get_html_school(school)}/{year}-roster.html"
            df = pd.read_html(html)[0]
        except:
            print(f"School ::{get_html_school(school)}:: had some trouble")
            return None

        players = []

        for i in df.index:
            if df['Pos'][i] == position:
                players.append(df['Player'][i])
        
        dict[school] = players

    return dict

def get_html_school(school):

    if school == "Alabama":
        return "alabama"
    elif school == "Arkansas":
        return "arkansas"
    elif school == "Auburn":
        return "auburn"
    elif school == "Baylor":
        return "baylor"
    elif school == "BYU":
        return "brigham-young"
    elif school == "Cincinnati":
        return "cincinnati"
    elif school == "Clemson":
        return "clemson"
    elif school == "Fresno State":
        return "fresno-state"
    elif school == "Georgia":
        return "georgia"
    elif school == "Houston":
        return "houston"
    elif school == "Iowa":
        return "iowa"
    elif school == "Kentucky":
        return "kentucky"
    elif school == "LSU":
        return "louisiana-state"
    elif school == "Miami (FL)":
        return "miami-fl"
    elif school == "Michigan":
        return "michigan"
    elif school == "Michigan State":
        return "michigan-state"
    elif school == "Minnesota":
        return "minnesota"
    elif school == "Mississippi State":
        return "mississippi-state"
    elif school == "NC State":
        return "north-carolina-state"
    elif school == "Notre Dame":
        return "notre-dame"
    elif school == "Ohio State":
        return "ohio-state"
    elif school == "Oklahoma":
        return "oklahoma"
    elif school == "Oklahoma State":
        return "oklahoma-state"
    elif school == "Ole Miss":
        return "mississippi"
    elif school == "Oregon":
        return "oregon"
    elif school == "Penn State":
        return "penn-state"
    elif school == "Pitt":
        return "pittsburgh"
    elif school == "Purdue":
        return "purdue"
    elif school == "Tennessee":
        return "tennessee"
    elif school == "Texas":
        return "texas"
    elif school == "Texas A&M":
        return "texas-am"
    elif school == "UCF":
        return "central-florida"
    elif school == "USC":
        return "southern-california"
    elif school == "Utah":
        return "utah"
    elif school == "Wake Forest":
        return "wake-forest"
    elif school == "Wisconsin":
        return "wisconsin"
    
    print(f"Unknown school ::{school}::")
    return None

def get_all_players(year):
    positions = [
        "QB",
        "RB",
        "WR",
        "TE",
        "K"
    ]

    master_dict = {}

    schools = get_schools(year)

    master_dict["QB"] = get_players(schools, 'QB', year)
    master_dict["RB"] = get_players(schools, 'RB', year)
    master_dict["WR"] = get_players(schools, 'WR', year)
    master_dict["TE"] = get_players(schools, 'TE', year)
    master_dict["K"] = get_players(schools, 'K', year)

    print(master_dict)

    return master_dict
    
def get_boxscore_url(school, month, day, year):
    
    if school == "NC State":
        school = "North Carolina State"
    if school == "BYU":
        school = "Brigham Young"
    
    
    week_url = f"https://www.sports-reference.com/cfb/boxscores/index.cgi?month={month}&day={day}&year={year}&conf_id="
    html_content = requests.get(week_url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    games = soup.find_all("table", {"class": "teams"})

    for game in games:
        if (f"{school}" in game.text): # Find the school
            if not (f" {school}" in game.text) and not (f"{school} " in game.text): # Make sure its not for example "Alabama Birmingham"
                
                boxscore = game.find("td", {"class": "right gamelink"})
                boxscore_link = boxscore.find('a')['href']

                return f"https://www.sports-reference.com{boxscore_link}"
    
    print(f"link not found for the game school: ::{school}::")
    return None






 
def main():
    schools = get_schools("2022")
    for school in schools:
        link = get_boxscore_url(school, "9", "3", "2022")
        print(link)


if __name__ == "__main__":
    main()