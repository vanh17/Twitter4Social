import io
import sys

# start is an array with this format ["mar", "14", "2020"]
# end is an array with this format ["may", "15", "2020"]
# tweets are just an return value from open() function
def timeline_extract(start, end, tweets):
    counting = False
    tweet_list = []
    for tweet in tweets:
        # strip new line character
        tweet = tweet.strip("\n")
        # split by tab
        tweet = tweet.split("\t")
        date = tweet[1].lower().split()
        if start[0] == date[1] and int(start[1]) <= int(date[2]) and start[2] == date[5]:
            counting = True
        if counting:
            tweet_list.append(tweet[2].lower())
        if end[0] == date[1] and int(end[1]) <= int(date[2]) and end[2] == date[5]:
            break
    return tweet_list

# determine if a tweet is healthy/unhealthy
def tweet_classifier(healthy, neutral, unhealthy, tweet):
    categories = []
    for food in unhealthy:
        if food in tweet:
            categories.append("unhealthy")
            break
    for food in healthy:
        if food in tweet:
            categories.append("healthy")
            break
    return categories

# percentage of each tweet
def food_trend_analyze(healthy, neutral, unhealthy, twtlst, year):
    healthy_cnt = 0
    unhealthy_cnt = 0
    total = 0
    for tweet in twtlst:
        categories = tweet_classifier(healthy, neutral, unhealthy, tweet)
        for type in categories:
            if type == "healthy":
                healthy_cnt += 1
                total += 1
            if type == "unhealthy":
                unhealthy_cnt += 1
                total += 1
    print(year, ": ", healthy_cnt/total, unhealthy_cnt/total)

# PMI of each tweet
def food_trend_analyze_pmi(healthy, neutral, unhealthy, twtLsts):
    count_dict_list = []
    healthy_cnt = 0
    unhealthy_cnt = 0
    for twtlst in twtLsts:
        count_dict = {"healthy":0, "unhealthy":0, "total":len(twtlst)}
        for tweet in twtlst:
            for food in healthy:
                if food in tweet:
                    count_dict["healthy"] = count_dict["healthy"] + 1
            for food in unhealthy:
                if food in tweet:
                    count_dict["unhealthy"] = count_dict["unhealthy"] + 1
        healthy_cnt += count_dict["healthy"]
        unhealthy_cnt += count_dict["unhealthy"]
        count_dict_list.append(count_dict)
    print(count_dict_list)
    print(healthy_cnt, unhealthy_cnt)
    for twtlst in count_dict_list:
        print(twtlst["healthy"]/(healthy_cnt*twtlst["total"]), twtlst["unhealthy"]/(unhealthy_cnt*twtlst["total"]))




def main():
    # open tweet files
    tweets = open("twtstatetime1.txt", "r")
    tweets2 = open("twtstatetime2.txt", "r")

    # open food vocabulary per category
    healthy = open("healthy_foods.txt", "r")
    healthy = [food.strip("\n") for food in healthy.readlines()]
    unhealthy = open("unhealthy_foods.txt", "r")
    unhealthy = [food.strip("\n") for food in unhealthy.readlines()]
    neutral = open("neutral_foods.txt", "r")
    neutral = [food.strip("\n") for food in neutral.readlines()]

    ############data analysis: tweets from 2015 to 2020##############
    print("Start extracting tweets by years from Mar-May")
    twt20 = timeline_extract(["mar", "14", "2020"], ["may", "16", "2020"], tweets2)
    print("Done 2020", len(twt20))

    tweets2 = open("twtstatetime2.txt", "r")
    twt19 = timeline_extract(["mar", "14", "2019"], ["may", "16", "2019"], tweets2)
    print("Done 2019", len(twt19))

    tweets2 = open("twtstatetime2.txt", "r")
    twt18 = timeline_extract(["mar", "14", "2018"], ["may", "16", "2018"], tweets2)
    print("Done 2018", len(twt18))

    tweets2 = open("twtstatetime2.txt", "r")
    twt17 = timeline_extract(["mar", "14", "2017"], ["may", "16", "2017"], tweets2)
    print("Done 2017", len(twt17))

    twt16 = timeline_extract(["mar", "14", "2016"], ["may", "16", "2016"], tweets)
    print("Done 2016", len(twt16))

    tweets = open("twtstatetime1.txt", "r")
    twt15 = timeline_extract(["mar", "14", "2015"], ["may", "16", "2015"], tweets)
    print("End extracting!")
    #########################End data analysis#############################
    print("Start analyzing health trend")
    print("By percentage")
    food_trend_analyze(healthy, neutral, unhealthy, twt20, "2020")
    food_trend_analyze(healthy, neutral, unhealthy, twt19, "2019")
    food_trend_analyze(healthy, neutral, unhealthy, twt18, "2018")
    food_trend_analyze(healthy, neutral, unhealthy, twt17, "2017")
    food_trend_analyze(healthy, neutral, unhealthy, twt16, "2016")
    food_trend_analyze(healthy, neutral, unhealthy, twt15, "2015")
    print("End by percentage")
    print("By PMI")
    twtlsts6 = [twt15, twt16, twt17, twt18, twt19, twt20]
    twtlsts4 = [twt17, twt18, twt19, twt20]
    print("PMI last 6 years")
    food_trend_analyze_pmi(healthy, neutral, unhealthy, twtlsts6)
    print("PMI last 4 years")
    food_trend_analyze_pmi(healthy, neutral, unhealthy, twtlsts4)
    print("End food trend by year analysis")


main()