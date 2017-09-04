# -*- coding: utf-8 -*
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests, xlwt, os, re, time, random

ua = UserAgent()
headers = {'User-Agent': 'ua.random'}

time.sleep(random.randint(1, 9))
book = xlwt.Workbook()
sheet = book.add_sheet('sheet', cell_overwrite_ok=True)
path = 'D:\\Study'
os.chdir(path)
jobs = []
#company = []
salary = []
links = []
count = 0



for x in range(1, 2):
	url = 'https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%88%90%E9%83%BD&kw=python&sm=0&sf=0&isfilter=0&fl=801&isadv=1&sg=c59fe2eb403a49699a092214cab620cc&p=' + str(x)
	r = requests.get(url, headers=headers).text
	s = etree.HTML(r)
	job = re.compile(r'<a style="font-weight: bold" par=".*?" href=".*?" target="_blank">(.*?)</a>').findall(r)	
	#company1 = s.xpath('//table[@class="newlist"]/tr[1]/td[3]/a[1]/text()')
	salary1 = re.compile(r'<td class="zwyx">(.*?)</td>').findall(r)
	link = re.compile(r'<a style=".*?" href="(.*?)" target="_blank">.*?</a>').findall(r)
	jobs.extend(job)
	#company.extend(company1)
	salary.extend(salary1)
	links.extend(link)


desc = []
for i in links:
    r = requests.get(i, headers=headers).text
    soup = BeautifulSoup(r, 'lxml')
    try:
        word = soup.find(class_="tab-inner-cont").get_text()
    except AttributeError:
        print('no data')
    desc.append(word)
    count += 1
    print('已爬取 %d 条信息' % count)
    

j = 0
for i in range(len(jobs)):
	try:
		sheet.write(i + 1, j, jobs[i])
		#sheet.write(i + 1, j + 1, company[i])
		sheet.write(i + 1, j + 2, salary[i])
		sheet.write(i + 1, j + 3, links[i])
		sheet.write(i + 1, j + 4, desc[i])
	except Exception as e:
		print('error: ' + str(e))
		continue
book.save('d:\\jobs.xls')
