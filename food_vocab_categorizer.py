#seperating food vocabulary into three categories: healthy, unhealthy, neutral
import io
import sys

def main():
    # get annotation for 4 annotator
    annotator1 = open("food_vocabulary/annotator1.txt", "r")
    annotator1 = annotator1.readlines()
    annotator2 = open("food_vocabulary/annotator2.txt", "r")
    annotator2 = annotator2.readlines()
    annotator3 = open("food_vocabulary/annotator3.txt", "r")
    annotator3 = annotator3.readlines()
    annotator4 = open("food_vocabulary/annotator4.txt", "r")
    annotator4 = annotator4.readlines()
    # end getting annotation

    # get food full dictionary
    all_foods = open("food_vocabulary/all_foods.txt", "r")
    all_foods = all_foods.readlines()

    # open file to write each category of foods
    healthy_file = open("food_vocabulary/healthy_foods.txt", "w")
    neutral_file = open("food_vocabulary/neutral_foods.txt", "w")
    unhealthy_file = open("food_vocabulary/unhealthy_foods.txt", "w")
    
    # to sanity check if we get all the word counts correctly
    healthy_cnt = 0
    unhealthy_cnt = 0
    neutral_cnt = 0
    no_aggreement_cnt = 0

    # iterate through all food words
    for i in range(len(all_foods)):
        a1 = annotator1[i].strip("\n")
        a2 = annotator2[i].strip("\n")
        a3 = annotator3[i].strip("\n")
        a4 = annotator4[i].strip("\n")
        a_list = [a1, a2, a3, a4]
        healthy = a_list.count("-1")
        unhealthy =a_list.count("1")
        neutral = a_list.count("0")
        if healthy > unhealthy and healthy > neutral:
            healthy_file.write(all_foods[i])
            healthy_cnt += 1
        elif unhealthy > healthy and unhealthy > neutral:
            unhealthy_file.write(all_foods[i])
            unhealthy_cnt += 1
        elif neutral > healthy and neutral > unhealthy:
            neutral_file.write(all_foods[i])
            neutral_cnt += 1
        else:
            no_aggreement_cnt += 1
    print("total: ", healthy_cnt+unhealthy_cnt+neutral_cnt+no_aggreement_cnt)

main()