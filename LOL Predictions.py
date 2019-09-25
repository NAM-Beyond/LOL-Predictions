import re
import requests
from bs4 import BeautifulSoup

# Initiating main variables
Championships = ["0", "LCK", "LCS", "LEC", "LMS", "LPL"]
Years = ["0", "2019"]
Seasons = ["0", "Summer"]
Match_List = []
Match_Date = []
Team_One = []
Team_Two = []
Team_Result = []
User_Prediction = []

# Choosing which Championship, Year and Season to look at
print("Which championship do you want to look at ?")
Championship = int(input("1 : LCK / 2 : LCS / 3 : LEC / 4 : LMS / 5 : LPL -> "))
print("Which year do you want to look at ?")
Year = int(input("1 : 2019 -> "))
print("Which season do you want to look at ?")
Season = int(input("1 : Summer -> "))

# First we gather the match schedule
MatchSchedule_URL = "https://lol.gamepedia.com/" + Championships[Championship] + "/" + Years[Year] + "_Season/" + Seasons[Season] + "_Season"
MatchSchedule_Response = requests.get(MatchSchedule_URL)
MatchSchedule_Page = BeautifulSoup(MatchSchedule_Response.text, "html.parser")

#Week_Numbers = MatchSchedule_Page.body.find_all(string=re.compile("^Week [0-9]"))
#Week_Numbers.sort()
#Week_Number = int(Week_Numbers[len(MatchSchedule_Page.body.find_all(string = re.compile("^Week [0-9]"))) - 1][5])

# Then we gather the different dates, teams and results in order to organise the array before gathering predictions
Match_Dates = MatchSchedule_Page.body.find_all("tr", class_ = re.compile("matchlist-date matchlist-you-date"))
for n in range(0,len(Match_Dates)) :
    Match_Date.append(Match_Dates[n].td.span.encode_contents().decode("UTF-8"))
Team_Ones = MatchSchedule_Page.body.find_all("td", class_ = "matchlist-team1")
for i in Team_Ones :
    Team_One.append(i["data-teamhighlight"])
Team_Twos = MatchSchedule_Page.body.find_all("td", class_ = "matchlist-team2")
for i in Team_Twos :
    Team_Two.append(i["data-teamhighlight"])
Team_Results = MatchSchedule_Page.body.find_all("td", class_ = "matchlist-score")
for i in Team_Results :
    Team_Result.append(i.encode_contents().decode("UTF-8"))
for i in range(0,len(Match_Date)) :
    Match_List.append([Match_Date[i],Team_One[i],0,0,0,0,Team_Two[i]])
for i in range(0,int(len(Team_Result) / 2)) :
    Match_List[i][3] = Team_Result[2 * i]
    Match_List[i][4] = Team_Result[2 * i + 1]

# Gathering the list of the 100 best predictors on Leaguepedia concerning the championship, season and split selected
LeaderBoard_URL = "https://lol.gamepedia.com/Predictions:" + Championships[Championship] + "/" + Years[Year] + "_Season/" + Seasons[Season] + "_Season/Leaderboard"
LeaderBoard_Response = requests.get(LeaderBoard_URL)
LeaderBoard_Page = BeautifulSoup(LeaderBoard_Response.text, "html.parser")
LeaderBoard_Users = []
for Hyperlinks in LeaderBoard_Page.body.find_all("a", title=re.compile("^Predictions:" + Championships[Championship] + "/" + Years[Year] + " Season/" + Seasons[Season] + " Season/User")) :
    LeaderBoard_Users.append((Hyperlinks.encode_contents().decode("UTF-8")))

# And now regrouping the predictions in the main array in order to compare preictions and results
for User_Name in LeaderBoard_Users :
    User_URL = "https://lol.gamepedia.com/Predictions:" + Championships[Championship] + "/" + Years[Year] + "_Season/" + Seasons[Season] + "_Season/User/" + User_Name
    User_Response = requests.get(User_URL)
    User_Page = BeautifulSoup(User_Response.text, "html.parser")
    User_Predictions = User_Page.body.find_all("tr", class_ = re.compile("ml-prediction-"))
    for i in User_Predictions :
        User_Prediction.append(int(i["class"][len(i["class"]) - 1][14]))
    for i in range(0,len(User_Prediction)) :
        if User_Prediction[i] == 1 :
            Match_List[i][2] += 1
        else :
            Match_List[i][5] += 1
    User_Prediction = []
    
for i in range(0, len(Match_List)) :
    if Match_List[i][2] + Match_List[i][5] != 0 :
        Sums = Match_List[i][2] + Match_List[i][5]
        Match_List[i][2] = Match_List[i][2] / (Sums)
        Match_List[i][5] = Match_List[i][5] / (Sums)

# Printing the results
for i in range(0,len(Match_List)) :
    print(Match_List[i])