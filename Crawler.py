#-*- coding: utf-8 -*-
import requests
import multiprocessing
import os
from bs4 import BeautifulSoup

def check_contain_chinese_or_english(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff': # 中文
            continue
        elif u'\ufb00' <= ch <= u'\ufffd': # 忘記是什麼，但是有用到XD
            continue
        elif u'\u3000' <= ch <= u'\u303f': # 全形英文、符號
            continue
        elif u'\u0000' <= ch <= u'\u007e': # 半形英文、符號
            continue
        else:
            return False
    return True

def get_comment_id(soup,dir_name):
    # dir_name = data/taipei/attractions
    save_id = open(dir_name + "/id.txt", 'w')
    while True:
        for all_id in soup.find_all("div", {"class":"reviewSelector track_back"}):
            user_id = all_id.get("id")
            u_id = user_id.split('_')[1]
            save_id.write(u_id+'\n')

        for all_id in soup.find_all("div", {"class":"reviewSelector "}):
            user_id = all_id.get("id")
            u_id = user_id.split('_')[1]
            save_id.write(u_id+'\n')

        next_page = soup.find("a", {"class":"nav next rndBtn ui_button primary taLnk"})
        try:
            page_link = next_page.get("href")
        except:
            break
        next_link = 'https://www.tripadvisor.com.tw'+page_link
        try:
            res_again = requests.get(next_link)
        except:
            print "no next link"
        soup = BeautifulSoup(res_again.text.encode("utf-8"))
    save_id.close()

def get_comments_and_comment_url(f,property_url,dir_name):
    # dir_name = data/taipei/attractions
    read_id = open(dir_name +'/id.txt', 'r')
    comment_url = open(dir_name + '/comment_url.txt','w')
    leave = 0
    while True:
        # comment_url
        first_id = read_id.readline()
        test = "https://www.tripadvisor.com.tw/ExpandedUserReviews-" + property_url.split('-')[1] + '-' + property_url.split('-')[2] + "?target=" + first_id.split('\n')[0] + "&reviews=" + first_id.split('\n')[0]
        for x in range(0,19):
            user_id = read_id.readline()
            if len(user_id) < 3:
                leave = 1
                break
            test = test + ',' + user_id.split('\n')[0]
        comment_url.write(test+'\n')

        # comments

        comment_res = requests.get(test)
        comment_soup = BeautifulSoup(comment_res.text.encode("utf-8"))
        for all_comment in comment_soup.find_all("div", {"class":"entry"}):
            where = all_comment.find("p")
            if check_contain_chinese_or_english(where.text.encode('utf-8')):
                print "Finish " + dir_name.split('/')[2] + " comments..."
                f.write(where.text.encode('utf-8')+'\n')
        if leave == 1:
            break

def get_title_and_link(property_url,dir_name):
    res = requests.get(property_url)
    soup = BeautifulSoup(res.text.encode("utf-8"))
    title = soup.find("h1")
    # dir_name = data/taipei/attractions
    f=open(dir_name + "/" + dir_name.split('/')[2] + ".txt", 'w')
    get_comment_id(soup,dir_name)
    get_comments_and_comment_url(f,property_url,dir_name)
    f.close()

def get_property_title_and_link(soup,f,dir_name):
    while True:
        for prop_tag in soup.find_all("div", {"class":"property_title"}):
            prop_link = prop_tag.find("a")
            link = 'https://www.tripadvisor.com.tw'+prop_link.get("href")
            if (link.encode('utf-8')[41] != 's'):
                f.write(prop_link.text.encode('utf-8')+'\n')
                f.write(link.encode('utf-8')+'\n')

        next_page = soup.find("a", {"class":"nav next rndBtn ui_button primary taLnk"})
        try:
            page_link = next_page.get("href")
        except:
            break
        next_link = 'https://www.tripadvisor.com.tw'+page_link
        if next_link[30] !='/':
            break
        try:
            res_again = requests.get(next_link)
        except:
            print "no next"
        soup = BeautifulSoup(res_again.text.encode("utf-8"))
    f.close()

    # dir_name = data/taipei
    folder_name = dir_name
    pool2 = multiprocessing.Pool(4)
    f_property_title_and_link=open(dir_name + "/" + "property_title_and_link.txt", 'r')
    while True:
        out = f_property_title_and_link.readline()
        if len(out) < 1:
            break
        property_url = f_property_title_and_link.readline()
        out = out.split('\n')[0]
        dir_name = folder_name + "/" + out.decode('utf-8')
        # dir_name = data/taipei/attractions
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        pool2.apply_async(get_title_and_link,(property_url,dir_name,))
    f_property_title_and_link.close()
    pool2.close()
    pool2.join()

def get_position(f_attraction):
    pool = multiprocessing.Pool(4)
    while True:
        attraction_url = f_attraction.readline()
        if len(attraction_url) < 3:
            break
        city = attraction_url.split('-')[3].split('.')[0]
        print city
        dir_name = "data/" + city
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        f=open(dir_name + "/" + "property_title_and_link.txt", 'w')
        res = requests.get(attraction_url)
        soup = BeautifulSoup(res.text.encode("utf-8"))
        pool.apply_async(get_property_title_and_link(soup,f,dir_name))
    pool.close()
    pool.join()

if __name__ == "__main__":
    f_attraction=open('Attractions.txt','r')
    get_position(f_attraction)
