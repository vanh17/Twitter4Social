#seperating food vocabulary into three categories: healthy, unhealthy, neutral
import io
import sys

def main():
    labels = open("foodlabel.txt", "r")
    labels = labels.readlines()
    healthy = open("healthy_foods.txt", "w")
    neutral = open("neutral_foods.txt", "w")
    unhealthy = open("unhealthy_foods.txt", "w")
    allfood = open("allfood.txt","r")
    allfood = allfood.readlines()
    healthy_cnt = 0
    unhealthy_cnt = 0
    neutral_cnt = 0
    for i in range(len(allfood)):
        label = labels[i].strip()
        label = label.split("\t")
        category = label[0]
        if len(label) == 2:
            category = label[1]
        if category == "-1":
            healthy.write(allfood[i])
            healthy_cnt += 1
        elif category == "1":
            unhealthy.write(allfood[i])
            unhealthy_cnt += 1
        elif category == "0":
            neutral.write(allfood[i])
            neutral_cnt += 1
    print("heathy_cnt: ", healthy_cnt)
    print("unhealthy_cnt: ", unhealthy_cnt)
    print("neutral_cnt: ", neutral_cnt)
    print("total: ", healthy_cnt+unhealthy_cnt+neutral_cnt)

main()