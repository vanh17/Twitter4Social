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
def tweet_classifier(depress_hashtags, tweet):
    categories = ["neutral"]
    r = random.random()
    for depress in depress_hashtags:
        if depress in tweet:
            categories = ["depressive"]
            break
    return categories

# percentage of each tweet
def food_trend_analyze(depress_hashtags, twtlst, year):
    depress_cnt = 0
    neutral_cnt = 0
    total = 0
    for tweet in twtlst:
        categories = tweet_classifier(depress_hashtags, tweet)
        for type in categories:
            if type == "neutral":
                neutral_cnt += 1
                total += 1
            if type == "depressive":
                depress_cnt += 1
                total += 1
    print(year, ": ", depress_cnt/total, neutral_cnt/total, depress_cnt)
    # return (healthy_cnt/total, unhealthy_cnt/total)

# PMI of each tweet
def food_trend_analyze_pmi(healthy, unhealthy, depress_hashtags, twtLsts):
    count_dict_list = []
    healthy_cnt = 0
    unhealthy_cnt = 0
    for twtlst in twtLsts:
        count_dict = {"healthy":0, "unhealthy":0, "total":0}
        for tweet in twtlst:
            categories = tweet_classifier(depress_hashtags, tweet)
            if categories[0] == "depressive":
                count_dict["total"] = count_dict["total"] + 1
            for food in healthy:
                if food in tweet:
                    healthy_cnt += 1
                    if categories[0] == "depressive":
                        count_dict["healthy"] = count_dict["healthy"] + 1
                    break #original do not break so it counts all the words in the tweet separately, now only count the healthy word appearance with the tweet
                    # so no matter how many the healthy words there, as long as there is one count it as one .
            for food in unhealthy:
                if food in tweet:
                    unhealthy_cnt += 1
                    if categories[0] == "depressive":
                        count_dict["unhealthy"] = count_dict["unhealthy"] + 1
                    break #original do not break so it counts all the words in the tweet separately, now only count the healthy word appearance with the tweet
                    # so no matter how many the healthy words there, as long as there is one count it as one .
        count_dict_list.append(count_dict)
    for twtlst in count_dict_list:
        print(twtlst["healthy"]/(healthy_cnt*twtlst["total"]), twtlst["unhealthy"]/(unhealthy_cnt*twtlst["total"]))

# PMI of each tweet
def food_trend_analyze_pmi_2020(healthy, unhealthy, side_effects, twtlst, year):
    count_dict_list = {}
    for food in healthy:
        # add the list of total count of that word, intersection with depression, and PMI
        count_dict_list[food] = [0, 0, 0, "healthy"]
    for food in unhealthy:
        # add the list of total count of that word, intersection with depression, and PMI
        count_dict_list[food] = [0, 0, 0, "unhealthy"]
    depress_cnt = 0
    for tweet in twtlst:
            categories = tweet_classifier(side_effects, tweet, year)
            if categories[0] == "depressive":
                depress_cnt += 1
            for food in healthy:
                if food in tweet:
                    count_dict_list[food][0] = count_dict_list[food][0] + 1
                    if categories[0] == "depressive":
                        count_dict_list[food][1] = count_dict_list[food][1] + 1
            for food in unhealthy:
                if food in tweet:
                    count_dict_list[food][0] = count_dict_list[food][0] + 1
                    if categories[0] == "depressive":
                        count_dict_list[food][1] = count_dict_list[food][1] + 1
    for food in count_dict_list.keys():
        if count_dict_list[food][1] > 0:
            count_dict_list[food][2] = count_dict_list[food][1] / (count_dict_list[food][0] * depress_cnt)
    # comment this out for PMI rank diference  between 2020 and all previous years
    # sorted_food_pmi = sorted(count_dict_list.items(), key=lambda x: x[1][2], reverse=True)
    # for i in range(20):
    #     print(sorted_food_pmi[i])
    # add this line below to return the dictionary for calculating the difference in PMI
    return count_dict_list

# To calculate the difference between PMI in 2020 and all previous years
def food_trend_difference_pmi(year1, year2):
    diff_dict = {}
    for food in year1.keys():
        if food in year2.keys():
            diff_dict[food] = year1[food][2] - year2[food][2]
    sorted_food_pmi = sorted(diff_dict.items(), key=lambda x: x[1], reverse=True)
    for i in range(20):
         print(sorted_food_pmi[i])


def depression_hashtag_analyze_pmi(depress_hashtags,twtLsts):
    count_dict_list = []
    delivery_words = depress_hashtags
    delivery_cnt = 0
    for twtlst in twtLsts:
        count_dict = {"delivery":0, "total":len(twtlst)}
        for tweet in twtlst:
            for word in delivery_words:
                if word in tweet:
                    count_dict["delivery"] = count_dict["delivery"] + 1
                    break
        delivery_cnt += count_dict["delivery"]
        count_dict_list.append(count_dict)
    for twtlst in count_dict_list:
        print(twtlst["delivery"]/(delivery_cnt*twtlst["total"]))

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
    depress_hashtags = open("side_effect_vocabulary.txt", "r")
    depress_hashtags = [depress.strip("\n") for depress in depress_hashtags.readlines()]
    depress_hashtags = depress_hashtags[0].split("\t")[1:]

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
    print("Start analyzing depression trend")

    # print("By percentage")
    # food_trend_analyze(depress_hashtags, twt20, "2020")
    # food_trend_analyze(depress_hashtags, twt19, "2019")
    # food_trend_analyze(depress_hashtags, twt18, "2018")
    # food_trend_analyze(depress_hashtags, twt17, "2017")
    # food_trend_analyze(depress_hashtags, twt16, "2016")
    # food_trend_analyze(depress_hashtags, twt15, "2015")
    # food_trend_analyze(depress_hashtags, twt14, "2014")
    # print("End by percentage")

    # print("By PMI depression hashtag")
    # twtlsts6 = [twt15, twt16, twt17, twt18, twt19, twt20]
    # twtlsts4 = [twt17, twt18, twt19, twt20]
    # print("PMI last 6 years")
    # depression_hashtag_analyze_pmi(depress_hashtags, twtlsts6)
    # print("PMI last 4 years")
    # depression_hashtag_analyze_pmi(depress_hashtags, twtlsts4)
    # print("End food delivery PMI by year analysis")

    # print("By PMI")
    # twtlsts6 = [twt15, twt16, twt17, twt18, twt19, twt20]
    # twtlsts4 = [twt17, twt18, twt19, twt20]
    # print("PMI last 6 years")
    # food_trend_analyze_pmi(healthy, unhealthy, depress_hashtags, twtlsts6)
    # print("PMI last 4 years")
    # food_trend_analyze_pmi(healthy, unhealthy, depress_hashtags, twtlsts4)
    # print("End food trend by year analysis")

    print("PMI between depression and food words")
    pmi2020 = food_trend_analyze_pmi_2020(healthy, unhealthy, depress_hashtags, twt20)
    pmiAll = food_trend_analyze_pmi_2020(healthy, unhealthy, depress_hashtags, twt19+twt18+twt17+twt16+twt15)
    food_trend_difference_pmi(pmi2020, pmiAll)



main()