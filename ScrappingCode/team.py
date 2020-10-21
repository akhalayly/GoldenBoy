from player import PlayerProfile

BASE_URL = "https://www.transfermarkt.co.uk"


class Team:
    def __init__(self, url, name, scraper):
        self.LeagueName = name
        soup = scraper(url)
        # reading player table and filtering for offensive players
        playerTable = soup.find("table", class_="items")
        players = playerTable.find_all("a", class_="spielprofil_tooltip")[::2]
        playerValues = playerTable.find_all(class_="rechts hauptlink")
        newPlayerValues = [value.contents[0] for value in playerValues]
        # offensivePlayers = filter(isStrikerOrWinger, players)
        offensivePlayersUrls = [BASE_URL + player["href"] for player in players]
        valueAndUrls = [(newPlayerValues[i], offensivePlayersUrls[i]) for i in range(len(offensivePlayersUrls))]
        # self.PlayerData = [PlayerProfile( playerUrl, scraper) for playerUrl in offensivePlayersUrls]
        self.PlayersData = []
        for value, playerUrl in valueAndUrls:
            try:
                NewPlayerProfile = PlayerProfile(playerUrl, value, scraper)
                NewPlayerProfile.PlayerData["current league"] = self.LeagueName
                self.PlayersData.append(NewPlayerProfile)
            except:
                continue


def isStrikerOrWinger(player):
    position = player.find_next("tr").text.strip().lower()
    # return "wing" in position or "centre-forward" in position or "midfield" in position or "back" in position
    return True
