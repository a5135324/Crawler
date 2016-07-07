#-*-  coding:  utf -8  -*-
import logging
import multiprocessing
import os
import requests
from bs4 import BeautifulSoup

stopword = []

def get_stopword():
	global stopword
	read_stopword = open('stopword.txt', 'r')
	while True:
		str = read_stopword.readline()
		if  str == '' :
			break
		str = str.split('\n')[0]
		stopword.append(str)
		
def LDA_format(fin, fout, num):
	fout.write(num.__str__() + '\n')
	while True:
		str = fin.readline()
		if str == '':
			break
		fout.write(str)
		
def remove_note2(str):
	count = -1
	dot = False
	for x in str:
		count = count +1;
		if (ord(x) >=97 and ord(x) <= 122):
			continue
		elif ord(x) == 46:
			if not dot:
				str = str.replace(str[count], ' . ')
				dot = True
			continue
		elif (ord(x) == 39 and ord(str[count-1]) >= 97 and ord(str[count-1]) <= 122 ):
			if count == len(str)-1:
				continue
			elif (ord(x) == 39 and ord(str[count+1]) >= 97 and ord(str[count+1]) <= 122 ):
				continue
			else:
				str = str.replace(str[count], ' ')
		else:
			str = str.replace(str[count], ' ')
	return str
	
def remove_note(str):
	count = -1
	dot = False
	while (count < len(str)-1):
		count = count +1;
		if (ord(str[count]) >=97 and ord(str[count]) <= 122):
			continue
		elif ord(str[count]) == 46:
			if not dot:
				str = str.replace(str[count], ' . ')
				dot = True
			continue
		elif (ord(str[count]) == 39 and ord(str[count-1]) >= 97 and ord(str[count-1]) <= 122 ):
			if count == len(str)-1:
				continue
			elif (ord(str[count]) == 39 and ord(str[count+1]) >= 97 and ord(str[count+1]) <= 122 ):
				continue
			else:
				str = str.replace(str[count], ' ')
		else:
			str = str.replace(str[count], ' ')
	return str

def main():
	open_attraction_file=open('Attractions_eng2.txt','r')
	while True:
		attraction_url = open_attraction_file.readline()
		if attraction_url == '':
			break
		city = attraction_url.split('-')[3].split('.')[0]
		f = open('eng_data/' + city + '/eng_property_title_and_link.txt', 'r')
		while True:
			title = f.readline() # title
			if title == '':
				break
			title = title.split('\n')[0]
			try:
				open_comment = open('eng_data/'+ city + '/' + title + '/' + title + '_all.txt', 'r')
			except:
				continue
			write_preprocess = open('eng_data/'+ city + '/' + title + '/' + title + '_preprocess.txt', 'w')
			document_count = 0
			while True:
				str = open_comment.readline()
				if str == '':
					break
				str = str.lower() # 轉小寫
				str = str.split('\n')[0]
				str = remove_note(str) # 移除標點符號
				temp = str.split(' ') # 切空格,重組
				# 去除stopword
				for item in stopword:
					for word in temp:
						if word == item:
							temp.remove(word)
				# 輸出至preprocess
				check_space = False
				for word in temp:
					if word != '':
						if not check_space:
							check_space = True
							write_preprocess.write(word)
						elif word == '.':
							write_preprocess.write('.')
						else:
							write_preprocess.write(' ' + word)
				write_preprocess.write('\n')
				document_count = document_count + 1
			f.readline() # link
			write_preprocess.close()
			# 增加文章數目
			write_for_LDA = open('eng_data/' + city + '/' + title + '/' + title + '_LDA.txt', 'w')
			open_preprocess = open('eng_data/' + city + '/' + title + '/' + title + '_preprocess.txt', 'r')
			LDA_format(open_preprocess, write_for_LDA, document_count)
			write_for_LDA.close()
			open_preprocess.close()
	
if __name__ == '__main__':
	FORMAT = '%(asctime)s %(lineno)04d %(levelname)05s %(message)s'
	logging.basicConfig(level=logging.DEBUG, filename='preprocess.log', format = FORMAT)
	get_stopword()
	main()
	