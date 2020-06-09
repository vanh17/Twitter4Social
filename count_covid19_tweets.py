import io
import sys

# start is an array with this format ["mar", "14", "2020"]
# end is an array with this format ["may", "15", "2020"]
# tweets are just an return value from open() function
def timeline_extract(start, end, tweets):
    counting = False
    count = 0
    for tweet in tweets:
        # strip new line character
        tweet = tweet.strip("\n")
        # split by tab
        tweet = tweet.split("\t")
        date = tweet[1].lower().split()
        if start[0] == date[1] and int(start[1]) <= int(date[2]) and start[2] == date[5]:
            counting = True
        if counting:
            count += 1
        if end[0] == date[1] and int(end[1]) <= int(date[2]) and end[2] == date[5]:
            break
    print(start[2], " tweets:", count)



def main():
    tweets = open("twtstatetime1.txt", "r")
    tweets2 = open("twtstatetime2.txt", "r")
    hashtags = open("49_most_hastag_covid19.txt", "r")
    hashtags = hashtags.readlines()
    hashtag_list = []
    for hashtag in hashtags:
        hashtag = hashtag.strip("\n")
        hashtag_list.append(hashtag[1:])
    print(hashtag_list)
    count = 0
    for tweet in tweets2:
        for hashtag in hashtag_list:
            if hashtag in tweet:
                count += 1
                break
    ############data analysis: tweets from 2015 to May 25 2020##############
    print("****************************************************")
    print("Tweets from Mar to May each year Analysis")
    print("Tweets with Covid19 hashtags:", count)
    tweets2 = open("twtstatetime2.txt", "r")
    timeline_extract(["mar", "14", "2020"], ["may", "17", "2020"], tweets2)
    tweets2 = open("twtstatetime2.txt", "r")
    timeline_extract(["mar", "14", "2019"], ["may", "17", "2019"], tweets2)
    tweets2 = open("twtstatetime2.txt", "r")
    timeline_extract(["mar", "14", "2018"], ["may", "17", "2018"], tweets2)
    tweets2 = open("twtstatetime2.txt", "r")
    timeline_extract(["mar", "14", "2017"], ["may", "17", "2017"], tweets2)
    timeline_extract(["mar", "14", "2016"], ["may", "17", "2016"], tweets)
    tweets = open("twtstatetime1.txt", "r")
    timeline_extract(["mar", "14", "2015"], ["may", "17", "2015"], tweets)
    print("**************************************************************")
    #########################End data analysis#############################
    print("Total tweets by years")
    tweets2 = open("twtstatetime2.txt", "r")
    timeline_extract(["jan", "01", "2019"], ["jan", "01", "2020"], tweets2)
    tweets2 = open("twtstatetime2.txt", "r")
    timeline_extract(["jan", "01", "2018"], ["jan", "01", "2019"], tweets2)
    tweets2 = open("twtstatetime2.txt", "r")
    timeline_extract(["jan", "01", "2017"], ["jan", "01", "2018"], tweets2)
    print("2016 tweets:", 852409)
    tweets = open("twtstatetime1.txt", "r")
    timeline_extract(["jan", "01", "2015"], ["jan", "01", "2016"], tweets)
    print("**************************************************************")

main()