#-*- coding: utf-8 -*-
import multiprocessing
import os
import requests
from bs4 import BeautifulSoup

def check_contain_chinese_or_english(check_str):
	for ch in check_str.decode('utf-8'):
		if u'\u3000' <= ch <= u'\u303f': # 全形英文、符號
			continue
		elif u'\u0000' <= ch <= u'\u007e': # 半形英文、符號
			continue
		else:
			return False
	return True

def get_comment(comment_url,f,dir_name):
	while True:
		test = comment_url.readline().split('\n')[0]
		if len(test)  < 83:
			break
		comment_res = requests.get(test)
		comment_soup = BeautifulSoup(comment_res.text.encode("utf-8"))
		for all_comment in comment_soup.find_all("div", {"class":"entry"}):
			where = all_comment.find("p")
			if check_contain_chinese_or_english(where.text.encode('utf-8')):
				f.write(where.text.encode('utf-8')+'\n')
	print "Finish " + dir_name.split('/')[2] + " comments..."
	comment_url.close()

def get_url(read_id,comment_url,property_url):
	leave = 0
	while True:
		first_id = read_id.readline()
		test = "https://www.tripadvisor.com/ExpandedUserReviews-" + property_url.split('-')[1] + '-' + property_url.split('-')[2] + "?target=" + first_id.split('\n')[0] + "&reviews=" + first_id.split('\n')[0]
		for x in range(0,19):
			user_id = read_id.readline()
			if len(user_id) < 3:
				leave = 1
				break
			test = test + ',' + user_id.split('\n')[0]
		if len(test) < 67:
			break
		comment_url.write(test+'\n')
		if ( leave == 1 ):
			break
	read_id.close()
	comment_url.close()

def get_comments_and_comment_url(property_url,dir_name):
	# dir_name = data/taipei/attractions
	read_id = open(dir_name +'/id.txt', 'r')
	read_id1 = open(dir_name +'/id_1.txt', 'r')
	read_id2 = open(dir_name +'/id_2.txt', 'r')
	read_id3 = open(dir_name +'/id_3.txt', 'r')
	read_id4 = open(dir_name +'/id_4.txt', 'r')
	read_id5 = open(dir_name +'/id_5.txt', 'r')
	
	comment_url = open(dir_name + '/comment_url.txt','w')
	comment_url_5star = open(dir_name + '/5star_comment_url.txt','w')
	comment_url_4star = open(dir_name + '/4star_comment_url.txt','w')
	comment_url_3star = open(dir_name + '/3star_comment_url.txt','w')
	comment_url_2star = open(dir_name + '/2star_comment_url.txt','w')
	comment_url_1star = open(dir_name + '/1star_comment_url.txt','w')
	
	get_url(read_id,comment_url,property_url)
	get_url(read_id1,comment_url_1star,property_url)
	get_url(read_id2,comment_url_2star,property_url)
	get_url(read_id3,comment_url_3star,property_url)
	get_url(read_id4,comment_url_4star,property_url)
	get_url(read_id5,comment_url_5star,property_url)

	all_comment_url = open(dir_name + '/comment_url.txt','r')
	comment_url_5star = open(dir_name + '/5star_comment_url.txt','r')
	comment_url_4star = open(dir_name + '/4star_comment_url.txt','r')
	comment_url_3star = open(dir_name + '/3star_comment_url.txt','r')
	comment_url_2star = open(dir_name + '/2star_comment_url.txt','r')
	comment_url_1star = open(dir_name + '/1star_comment_url.txt','r')
	
	f0=open(dir_name + "/" + dir_name.split('/')[2] + "_all.txt", 'w')
	f1=open(dir_name + "/" + dir_name.split('/')[2] + "_1.txt", 'w')
	f2=open(dir_name + "/" + dir_name.split('/')[2] + "_2.txt", 'w')
	f3=open(dir_name + "/" + dir_name.split('/')[2] + "_3.txt", 'w')
	f4=open(dir_name + "/" + dir_name.split('/')[2] + "_4.txt", 'w')
	f5=open(dir_name + "/" + dir_name.split('/')[2] + "_5.txt", 'w')
	
	get_comment(all_comment_url,f0,dir_name)
	get_comment(comment_url_5star,f5,dir_name)
	get_comment(comment_url_4star,f4,dir_name)
	get_comment(comment_url_3star,f3,dir_name)
	get_comment(comment_url_2star,f2,dir_name)
	get_comment(comment_url_1star,f1,dir_name)

def check_star(all_id):
	if (all_id.find("img", {"class":"sprite-rating_s_fill rating_s_fill s50"})):
		return 5
	if (all_id.find("img", {"class":"sprite-rating_s_fill rating_s_fill s40"})):
		return 4
	if (all_id.find("img", {"class":"sprite-rating_s_fill rating_s_fill s30"})):
		return 3
	if (all_id.find("img", {"class":"sprite-rating_s_fill rating_s_fill s20"})):
		return 2
	if (all_id.find("img", {"class":"sprite-rating_s_fill rating_s_fill s10"})):
		return 1			

# 算有多少人評論, 跟分開每個星等評論的id
def get_comment_id(soup,dir_name,property_url):
	# dir_name = data/taipei/attractions
	save_id = open(dir_name + "/id.txt", 'w')
	star_5 = open(dir_name + "/id_5.txt", 'w')
	star_4 = open(dir_name + "/id_4.txt", 'w')
	star_3 = open(dir_name + "/id_3.txt", 'w')
	star_2 = open(dir_name + "/id_2.txt", 'w')
	star_1 = open(dir_name + "/id_1.txt", 'w')
	id_num = 0
	while True:
		for all_id in soup.find_all("div", {"class":"reviewSelector   track_back"}):
			user_id = all_id.get("id")
			u_id = user_id.split('_')[1]
			num = check_star(all_id)
			if  num == 5 :
				star_5.write(u_id+'\n')
			elif num == 4 :
				star_4.write(u_id+'\n')
			elif num == 3 :
				star_3.write(u_id+'\n')
			elif num == 2 :
				star_2.write(u_id+'\n')
			elif num == 1 :
				star_1.write(u_id+'\n')
			save_id.write(u_id+'\n')
			id_num = id_num + 1

		for all_id in soup.find_all("div", {"class":"reviewSelector  "}):
			user_id = all_id.get("id")
			u_id = user_id.split('_')[1]
			num = check_star(all_id)
			if  num == 5 :
				star_5.write(u_id+'\n')
			elif num == 4 :
				star_4.write(u_id+'\n')
			elif num == 3 :
				star_3.write(u_id+'\n')
			elif num == 2 :
				star_2.write(u_id+'\n')
			elif num == 1 :
				star_1.write(u_id+'\n')
			save_id.write(u_id+'\n')
			id_num = id_num + 1

		next_page = soup.find("a", {"class":"nav next rndBtn ui_button primary taLnk"})
		try:
			page_link = next_page.get("href")
		except:
			break
		next_link = 'https://www.tripadvisor.com'+page_link
		try:
			res_again = requests.get(next_link)
		except:
			print "no next link"
		soup = BeautifulSoup(res_again.text.encode("utf-8"), "html.parser")
	save_id.close()
	star_5.close()
	star_4.close()
	star_3.close()
	star_2.close()
	star_1.close()
	print id_num
	if id_num == 0:
		print "delete " + dir_name.split('/')[2]
		folder = "F:/Project/Crawler/" + dir_name
		folder = folder.replace("/","\\")
		os.rename(folder,"123")
		command = "rmdir /s /q %s"
		command = command % "F:\\Project\\Crawler\\123"
		os.system(command)
	elif id_num > 0:
		get_comments_and_comment_url(property_url,dir_name)

# 準備一些寫評論用的東西
def get_title_and_link(property_url,dir_name):
	res = requests.get(property_url)
	soup = BeautifulSoup(res.text.encode("utf-8"), "html.parser")
	title = soup.find("h1")
	# dir_name = data/taipei/attractions
	get_comment_id(soup,dir_name,property_url)

# 用來獲得每個縣市景點的url跟景點名稱
def get_property_title_and_link(soup,f,dir_name):
	while True:
		for prop_tag in soup.find_all("div", {"class":"property_title"}):
			prop_link = prop_tag.find("a")
			link = 'https://www.tripadvisor.com'+prop_link.get("href")

			# 寫景點名稱與他的url
			if (link.encode('utf-8')[38] != 's'): # 過濾私人導覽類
				# 有些地名有兩個以上, 所以我只取前面那個
				# 都取的話會改到路徑, 之後有空的話再修改
				if (prop_link.text.encode('utf-8').find('/') != -1 ):
					place = prop_link.text.encode('utf-8').split(' /')[0]
					f.write(place+'\n')
				else:
					f.write(prop_link.text.encode('utf-8')+'\n')
				f.write(link.encode('utf-8')+'\n')

		# 看有沒有下一頁
		next_page = soup.find("a", {"class":"nav next rndBtn ui_button primary taLnk"})
		try:
			page_link = next_page.get("href")
		except:
			break
		
		# 去抓下一頁的內容
		next_link = 'https://www.tripadvisor.com'+page_link
		try:
			res_again = requests.get(next_link)
		except:
			print "no next"
		soup = BeautifulSoup(res_again.text.encode("utf-8"), "html.parser")
	f.close()

	# dir_name = data/taipei
	folder_name = dir_name
	pool2 = multiprocessing.Pool(4)
	f_property_title_and_link=open(dir_name + "/eng_property_title_and_link.txt", 'r')
	f_rank = open(dir_name + "/property_score.txt", 'w')
	while True:
		# 景點名稱
		out = f_property_title_and_link.readline()
		if len(out) < 1:
			break
		# url
		property_url = f_property_title_and_link.readline()
		out = out.split('\n')[0]
		dir_name = folder_name + "/" + out.decode('utf-8')
		# dir_name = data/taipei/attractionss
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
		pool2.apply_async(get_title_and_link,(property_url,dir_name,))
		#pool2.apply_async(get_rank(property_url,dir_name,f_rank,out))
	f_property_title_and_link.close()
	f_rank.close()
	pool2.close()
	pool2.join()
	#rank(folder_name)

# 用來了解是哪個縣市
def get_position(open_attraction_file):
	# 多工, 會跑比較快
	pool = multiprocessing.Pool(4)
	while True:
		attraction_url = open_attraction_file.readline()
		
		# 如果讀完檔了, 就跳出去
		if len(attraction_url) < 3:
			break
		
		# 切出是哪個縣市
		city = attraction_url.split('-')[3].split('.')[0]
		print city
		dir_name = "eng_data/" + city
		
		# 建立folder
		if not os.path.exists(dir_name):
			os.makedirs(dir_name)
		
		# 準備寫檔
		f=open(dir_name + "/" + "eng_property_title_and_link.txt", 'w')
		res = requests.get(attraction_url)
		soup = BeautifulSoup(res.text.encode("utf-8"), "html.parser")
		pool.apply_async(get_property_title_and_link(soup,f,dir_name))
	pool.close()
	pool.join()

if __name__ == "__main__":
	open_attraction_file=open('Attractions_eng.txt','r')
	get_position(open_attraction_file)
