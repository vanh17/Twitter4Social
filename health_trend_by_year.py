import io
import sys
import random

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
    unhealthy_cnt = 0
    healthy_cnt = 0
    for food in unhealthy:
        if food in tweet:
            unhealthy_cnt += 1
    for food in healthy:
        if food in tweet:
            healthy_cnt += 1
    if healthy_cnt > unhealthy_cnt:
        categories.append("healthy")
    if healthy_cnt < unhealthy_cnt:
        categories.append("unhealthy")
    if healthy_cnt == unhealthy_cnt and healthy_cnt > 0:
        categories.append("unhealthy")
        categories.append("healthy")
    return categories

# count healthy/unhealthy words in tweet
def healthy_unhealthy_count(healthy, neutral, unhealthy, tweet):
    categories = {}
    unhealthy_cnt = 0
    healthy_cnt = 0
    for food in unhealthy:
        if food in tweet:
            unhealthy_cnt += 1
    for food in healthy:
        if food in tweet:
            healthy_cnt += 1
    categories["healthy"] = healthy_cnt
    categories["unhealthy"] = unhealthy_cnt
    categories["total"] = healthy_cnt + unhealthy_cnt
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
    return (healthy_cnt/total, unhealthy_cnt/total)

# percentage of each tweet
def food_trend_analyze_new_formular(healthy, neutral, unhealthy, twtlst, year):
    healthy_cnt = 0
    unhealthy_cnt = 0
    total = 0
    for tweet in twtlst:
        categories = healthy_unhealthy_count(healthy, neutral, unhealthy, tweet)
        healthy_cnt += categories["healthy"]
        unhealthy_cnt += categories["unhealthy"]
        total += categories["total"]
    print(year, ": ", healthy_cnt/total, unhealthy_cnt/total)
    return (healthy_cnt/total, unhealthy_cnt/total)

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
                    count_dict["unhealthy"] = count_dict["unhealthy"]
        healthy_cnt += count_dict["healthy"]
        unhealthy_cnt += count_dict["unhealthy"]
        count_dict_list.append(count_dict)
    print(count_dict_list)
    print(healthy_cnt, unhealthy_cnt)
    for twtlst in count_dict_list:
        print(twtlst["healthy"]/(healthy_cnt*twtlst["total"]), twtlst["unhealthy"]/(unhealthy_cnt*twtlst["total"]))

def create_bootstrapping_dataset(twtlst):
    lst = []
    for i in range(len(twtlst)):
        rd = random.randint(0, len(twtlst)-1)
        lst.append(twtlst[rd])
    return lst

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

    tweets = open("twtstatetime1.txt", "r")
    twt14 = timeline_extract(["mar", "14", "2014"], ["may", "16", "2014"], tweets)
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
    food_trend_analyze(healthy, neutral, unhealthy, twt14, "2014")
    print("End by percentage")

    print("By percentage: 3 healthy 1 unhealthy and total of 4 for division")
    food_trend_analyze_new_formular(healthy, neutral, unhealthy, twt20, "2020")
    food_trend_analyze_new_formular(healthy, neutral, unhealthy, twt19, "2019")
    food_trend_analyze_new_formular(healthy, neutral, unhealthy, twt18, "2018")
    food_trend_analyze_new_formular(healthy, neutral, unhealthy, twt17, "2017")
    food_trend_analyze_new_formular(healthy, neutral, unhealthy, twt16, "2016")
    food_trend_analyze_new_formular(healthy, neutral, unhealthy, twt15, "2015")
    food_trend_analyze_new_formular(healthy, neutral, unhealthy, twt14, "2014")
    print("End by percentage with new formular")

    # print("By percentage bootstrapping")
    # hc19, uc19 = (0, 0)
    # hc18, uc18 = (0, 0)
    # hc17, uc17 = (0, 0)
    # hc16, uc16 = (0, 0)
    # hc15, uc15 = (0, 0)
    # for i in range(10000):
    #     twt20_bs = create_bootstrapping_dataset(twt20)
    #     twt19_bs = create_bootstrapping_dataset(twt19)
    #     twt18_bs = create_bootstrapping_dataset(twt18)
    #     twt17_bs = create_bootstrapping_dataset(twt17)
    #     twt16_bs = create_bootstrapping_dataset(twt16)
    #     twt15_bs = create_bootstrapping_dataset(twt15)
    #     h20, u20 = food_trend_analyze(healthy, neutral, unhealthy, twt20_bs, "2020")
    #     h19, u19 = food_trend_analyze(healthy, neutral, unhealthy, twt19_bs, "2019")
    #     h18, u18 = food_trend_analyze(healthy, neutral, unhealthy, twt18_bs, "2018")
    #     h17, u17 = food_trend_analyze(healthy, neutral, unhealthy, twt17_bs, "2017")
    #     h16, u16 = food_trend_analyze(healthy, neutral, unhealthy, twt16_bs, "2016")
    #     h15, u15 = food_trend_analyze(healthy, neutral, unhealthy, twt15_bs, "2015")
    #     if h20 >= h19:
    #         hc19 += 1
    #     if h20 >= h18:
    #         hc18 += 1
    #     if h20 >= h17:
    #         hc17 += 1
    #     if h20 >= h16:
    #         hc16 += 1
    #     if h20 >= h15:
    #         hc15 += 1
    #     if u20 >= u19:
    #         uc19 += 1 
    #     if u20 >= u18:
    #         uc18 += 1
    #     if u20 >= u17:
    #         uc17 += 1
    #     if u20 >= u16:
    #         uc16 += 1
    #     if u20 >= u15:
    #         uc15 += 1
    #     if i % 100 == 0: 
    #         print(i)
    # print(hc19/10000, hc18/10000, hc17/10000, hc16/10000, hc15/10000) 
    # print(uc19/10000, uc18/10000, uc17/10000, uc16/10000, uc15/10000)   
    # print("End by percentage")

    # print("By PMI")
    # twtlsts6 = [twt15, twt16, twt17, twt18, twt19, twt20]
    # twtlsts4 = [twt17, twt18, twt19, twt20]
    # print("PMI last 6 years")
    # food_trend_analyze_pmi(healthy, neutral, unhealthy, twtlsts6)
    # print("PMI last 4 years")
    # food_trend_analyze_pmi(healthy, neutral, unhealthy, twtlsts4)
    # print("End food trend by year analysis")


main()