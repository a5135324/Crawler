# -*- coding:utf-8 -*-
import os
import shutil
import requests
import multiprocessing
from bs4 import BeautifulSoup

def main():
	city_name = [16,6,14,5,15,20,11,19,1,13,18,17,3,0,10,4,12,2,7,8,21,9]
	f = open("eng_data/city.txt", 'r')
	city_num = 0
	while True:
		city = f.readline()
		city = city.split('\n')[0]
		if city == '':
			break
		print city
		dir = "eng_data/" + city
		all_file_name = city.lower()
		read_rank = open(dir + "/eng_property_title_and_link.txt", 'r')
		write_prepro = open(dir + "/" + all_file_name + ".txt", 'w')
		write_addr = open(dir + "/" + all_file_name + '_addr.txt', 'w')
		pro_num = 0
		while True:
			str = read_rank.readline()
			rank = str.split('\n')[0]
			if rank == '':
				break
			print rank
			dir_name = dir + "/" + rank
			if os.path.exists(dir_name + "/" + rank + "_all.txt"):
				os.rename(dir_name + "/" + rank + "_all.txt", dir + "/all_" + city_name[city_num].__str__() + '_' + pro_num.__str__() + '.txt')
			
			if os.path.exists(dir_name + "/abstract_has_stopword.txt"):
				os.rename(dir_name + "/abstract_has_stopword.txt", dir + "/high_" + city_name[city_num].__str__() + '_' + pro_num.__str__() + '.txt')
			elif os.path.exists(dir_name + "/" + rank + "_4+5.txt"):
				os.rename(dir_name + "/" + rank + "_4+5.txt", dir + "/high_" + city_name[city_num].__str__() + '_' + pro_num.__str__() + '.txt')
			
			if os.path.exists(dir_name + "/abstract_1+2_has_stopword.txt"):
				os.rename(dir_name + "/abstract_1+2_has_stopword.txt", dir + "/low_" + city_name[city_num].__str__() + '_' + pro_num.__str__() + '.txt')
			elif os.path.exists(dir_name + "/" + rank + "_1+2.txt"):
				os.rename(dir_name + "/" + rank + "_1+2.txt", dir + "/low_" + city_name[city_num].__str__() + '_' + pro_num.__str__() + '.txt')
			
			try:
				os.remove(dir_name + "/" + rank + "_1+2_add_dot.txt")
				os.remove(dir_name + "/" + rank + "_1+2_LDA.txt")
				os.remove(dir_name + "/" + rank + "_1+2_preprocess.txt")
				os.remove(dir_name + "/" + rank + "_1+2_preprocess_add_dot.txt")
				os.remove(dir_name + "/" + rank + "_1+2_preprocess_LDA.txt")
				os.remove(dir_name + "/" + rank + "_1+2_remove_note.txt")
				os.remove(dir_name + "/" + rank + "_1+2.txt")
			except:
				pass
			
			try:
				os.remove(dir_name + "/" + rank + "_4+5_add_dot.txt")
				os.remove(dir_name + "/" + rank + "_4+5_LDA.txt")
				os.remove(dir_name + "/" + rank + "_4+5_preprocess.txt")
				os.remove(dir_name + "/" + rank + "_4+5_preprocess_add_dot.txt")
				os.remove(dir_name + "/" + rank + "_4+5_preprocess_LDA.txt")
				os.remove(dir_name + "/" + rank + "_4+5_remove_note.txt")
				os.remove(dir_name + "/" + rank + "_4+5.txt")
			except:
				pass
			
			pic = open(dir + "/pic_" + city_name[city_num].__str__() + '_' + pro_num.__str__() + '.jpg', 'wb')
			
			if os.path.exists(dir_name):
				shutil.rmtree(dir_name)
				link = read_rank.readline()
				link = "https://www.tripadvisor.com.tw/" + link.split('/')[3]
				res = requests.get(link)
				soup = BeautifulSoup(res.text.encode("utf-8"), "html.parser")
				for prop_tag in soup.find_all("h1", {"class":"heading_name with_alt_title  "}):
					write_prepro.write(prop_tag.text.encode('utf-8').split('\n')[2]+'\n')
				for address in soup.find_all("span", {"class":"format_address"}):
					write_addr.write(address.text.encode('utf-8') + '\n' )
				temp = soup.find("div", {"id":"PHOTO_CELL_HERO_PHOTO"})
				pic_link = temp.find("a")
				res2 = requests.get("https://www.tripadvisor.com.tw" + pic_link.get("href"))
				soup = BeautifulSoup(res2.text.encode("utf-8"), "html.parser")
				t = soup.find("img", {"class":"taLnk big_photo"})
				if t.__str__() == "None":
					t = soup.find("img", {"class":"big_photo"})
					try:
						res3 = requests.get(t.get("src"), stream = True)
						shutil.copyfileobj(res3.raw, pic)
						pic.close()
						del res3
					except:
						pic.close()
				else:
					try:
						res3 = requests.get(t.get("src"), stream = True)
						shutil.copyfileobj(res3.raw, pic)
						pic.close()
						del res3
					except:
						pic.close()
			else:
				pro_num = pro_num - 1
				read_rank.readline()
			pro_num = pro_num + 1
		city_num = city_num + 1
		read_rank.close()
		os.remove(dir + "/eng_property_title_and_link.txt")
		
if __name__ == "__main__":
	main()