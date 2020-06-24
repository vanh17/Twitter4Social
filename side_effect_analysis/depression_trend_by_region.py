import io
import sys
import random

# start is an array with this format ["mar", "14", "2020"]
# end is an array with this format ["may", "15", "2020"]
# tweets are just an return value from open() function
# add the city name to process the tweets with that particular cities
def timeline_city_extract(start, end, city_list, tweets):
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
            if tweet[0] in city_list:
                tweet_list.append(tweet[2].lower())
        if end[0] == date[1] and int(end[1]) <= int(date[2]) and end[2] == date[5]:
            break
    return tweet_list


# determine if a tweet is healthy/unhealthy
def tweet_classifier(depress_hashtags, tweet):
    categories = ["neutral"]
    for depress in depress_hashtags:
        if depress in tweet:
            categories = ["depressive"]
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
    print(year, ": ", depress_cnt/total, neutral_cnt/total)
    # return (healthy_cnt/total, unhealthy_cnt/total)

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
    city_list = []
    if sys.argv[1] == "NorthEast":
        city_list = ["CT", "ME", "MA", "NH", "RI", "VT", "NJ", "NY", "PA"]
        print("Analysis for ", sys.argv[1])
    elif sys.argv[1] == "Midwest":
        city_list = ["IL", "IN", "WI", "MI", "OH", "IA", "KS", "MN", "MO", "NE", "ND", "SD"]
        print("Analysis for ", sys.argv[1])
    elif sys.argv[1] == "South":
        city_list = ["DE", "FL", "GA", "MD", "NC", "SC", "VA", "DC", "WV", "AL", "KY", "TN", "MS", "AR", "OK","LA", "TX"]
        print("Analysis for ", sys.argv[1])
    elif sys.argv[1] == "West":
        city_list = ["AZ", "CO", "ID", "MT", "NV", "NM", "UT", "WY", "AK", "HI", "CA", "OR", "WA"]
        print("Analysis for ", sys.argv[1])
    else:
        print("Cities not on the list. Currently available for top affected cities no space [NorthEast | Midwest | South | West]")     
    print("Start extracting tweets by years from Mar-May")
    twt20 = timeline_city_extract(["mar", "14", "2020"], ["may", "16", "2020"], city_list, tweets2)
    print("Done 2020", len(twt20))

    tweets2 = open("twtstatetime2.txt", "r")
    twt19 = timeline_city_extract(["mar", "14", "2019"], ["may", "16", "2019"], city_list, tweets2)
    print("Done 2019", len(twt19))

    tweets2 = open("twtstatetime2.txt", "r")
    twt18 = timeline_city_extract(["mar", "14", "2018"], ["may", "16", "2018"], city_list, tweets2)
    print("Done 2018", len(twt18))

    tweets2 = open("twtstatetime2.txt", "r")
    twt17 = timeline_city_extract(["mar", "14", "2017"], ["may", "16", "2017"],  city_list, tweets2)
    print("Done 2017", len(twt17))

    twt16 = timeline_city_extract(["mar", "14", "2016"], ["may", "16", "2016"],  city_list, tweets)
    print("Done 2016", len(twt16))

    tweets = open("twtstatetime1.txt", "r")
    twt15 = timeline_city_extract(["mar", "14", "2015"], ["may", "16", "2015"],  city_list, tweets)
    print("Done 2015", len(twt15))

    tweets = open("twtstatetime1.txt", "r")
    twt14 = timeline_city_extract(["mar", "14", "2014"], ["may", "16", "2014"], city_list, tweets)
    print("Done 2014", len(twt14))
    print("End extracting!")
    #########################End data analysis#############################
    print("Start analyzing health trend")

    print("By percentage")
    food_trend_analyze(depress_hashtags, twt20, "2020")
    food_trend_analyze(depress_hashtags, twt19, "2019")
    food_trend_analyze(depress_hashtags, twt18, "2018")
    food_trend_analyze(depress_hashtags, twt17, "2017")
    food_trend_analyze(depress_hashtags, twt16, "2016")
    food_trend_analyze(depress_hashtags, twt15, "2015")
    food_trend_analyze(depress_hashtags, twt14, "2014")
    print("End by percentage")


main()