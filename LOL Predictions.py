import re
import requests
import time
from bs4 import BeautifulSoup

MatchSchedule_URL = "https://lol.gamepedia.com/LEC/2019_Season/Summer_Season"
MatchSchedule_Response = requests.get(MatchSchedule_URL)
MatchSchedule_Page = BeautifulSoup(MatchSchedule_Response.text, "html.parser")
Match_List = []
Match_Date = []
Team_One = []
Team_Two = []
Team_Result = []
User_Prediction = []

Week_Numbers = MatchSchedule_Page.body.find_all(string=re.compile("^Week [0-9]"))
Week_Numbers.sort()
Week_Number = int(Week_Numbers[len(MatchSchedule_Page.body.find_all(string=re.compile("^Week [0-9]"))) - 1][5])

Match_Dates = MatchSchedule_Page.body.find_all("tr", class_=re.compile("matchlist-date matchlist-you-date"))
for n in range(0,len(Match_Dates)) :
    Match_Date.append(Match_Dates[n].td.span.encode_contents().decode("UTF-8"))

Team_Ones = MatchSchedule_Page.body.find_all("td", class_="matchlist-team1")
for i in Team_Ones :
    Team_One.append(i["data-teamhighlight"])

Team_Twos = MatchSchedule_Page.body.find_all("td", class_="matchlist-team2")
for i in Team_Twos :
    Team_Two.append(i["data-teamhighlight"])

Team_Results = MatchSchedule_Page.body.find_all("td", class_="matchlist-score")
for i in Team_Results :
    Team_Result.append(i.encode_contents().decode("UTF-8"))

for i in range(0,len(Match_Date)) :
    Match_List.append([Match_Date[i],Team_One[i],0,0,0,0,Team_Two[i]])

for i in range(0,int(len(Team_Result) / 2)) :
    Match_List[i][3] = Team_Result[2 * i]
    Match_List[i][4] = Team_Result[2 * i + 1]

LeaderBoard_URL = "https://lol.gamepedia.com/Predictions:LEC/2019_Season/Summer_Season/Leaderboard"
LeaderBoard_Response = requests.get(LeaderBoard_URL)
LeaderBoard_Page = BeautifulSoup(LeaderBoard_Response.text, "html.parser")
LeaderBoard_Users = []

for Hyperlinks in LeaderBoard_Page.body.find_all("a", title=re.compile("^Predictions:LEC/2019 Season/Summer Season/User")) :
    LeaderBoard_Users.append((Hyperlinks.encode_contents().decode("UTF-8")))

for User_Name in LeaderBoard_Users :
    User_URL = "https://lol.gamepedia.com/Predictions:LEC/2019_Season/Summer_Season/User/" + User_Name
    User_Response = requests.get(User_URL)
    User_Page = BeautifulSoup(User_Response.text, "html.parser")
    User_Predictions = User_Page.body.find_all("tr", class_=re.compile("ml-prediction-"))
    for i in User_Predictions :
        User_Prediction.append(int(i["class"][len(i["class"]) - 1][14]))
    for i in range(0,len(User_Prediction)) :
        if User_Prediction[i] == 1 :
            Match_List[i][2] += 1
        else :
            Match_List[i][5] += 1
    User_Prediction = []
    time.sleep(1)

for i in range(0,len(Match_List)) :
    print(Match_List[i])
