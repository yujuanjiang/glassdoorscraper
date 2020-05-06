'''
Cecilia Jiang
May the 4th be with you, 2020

Given a company's URL and output a csv with the technical interview questions
How to run command: python3 main.py -u 'https://www.glassdoor.ca/Interview/Shopify-Interview-Questions-E675933.htm'

Review date
Interview questions
Employee position
Employee status
Review title
'''

from argparse import ArgumentParser
from userAgents import user_agents, randomUserAgents
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import lxml
import pandas as pd

#Pass the argument to scaper
base_url = 'https://www.glassdoor.ca/'

head = randomUserAgents()
print('header is:')
print(head)

parser = ArgumentParser()
parser.add_argument('-u','--url', help='Please input the url of the page that you wanna scrape.')
args = parser.parse_args()

url = args.url

def soup(url, headers):
    session = requests.Session()
    req = session.get(url, headers=headers)
    bs = BeautifulSoup(req.text, 'lxml')
    print("Function soup() finished...")
    return bs

pages = set()

def getPages(url, head):
    global pages
    bs = soup(url, head)
    nextPage = bs.find('div',{'class':"pagingControls cell middle"})
    #print(nextPage)
    for link in nextPage.findAll('a'):
        if 'href' in link.attrs:
            url = 'http://glassdoor.ca{}'.format(link.attrs['href'])
            if url not in pages:
                pages.add(url)

    for lastPage in nextPage.findAll('li',{'class':'page last'}):
        lastPage = 'http://glassdoor.ca{}'.format(lastPage.a['href'])
        getPages(lastPage, head)

#    print(pages)
    print("function getPages() finished...")
    return pages
        

def main():
    date = []
    location = []
    employee = []
    reviewer = []
    interviewQuestions = []
    index = []
 
    pages = getPages(url, head)
    print(pages)
    #index = list(range(1,len(pages)+1))
    #print(index)
    print(" start the for loop in main(): ...") 

    for page in pages:
        #index.append(i)
        #print(i)
        #i += 1
        bs = soup(page, head)
        for x in bs.findAll('li',{'class','empReview cf'}):

            try:
                date.append(x.find('time',{'class':'date subtle small'}).text)
            except:
                date.append('None')

            try:
                location.append(x.find('span',{'class':'authorLocation'}).text)
            except:
                location.append('None')

            #try:
            #    employee.append(x.find('span',{'class':"authorJobTitle"}).text)
            #except:
            #    employee.append('None')

            try:
                #interviewQuestions.append(x.find('span',{'class':"interviewQuestion noPadVert truncateThis wrapToggleStr "}).text)
                interviewQuestions.append(x.find('div',{'class':"interviewQuestions"}).text)
            except:
                interviewQuestions.append('None')

            try:
                reviewer.append(x.find('span',{'class':'reviewer'}).text)
            except:
                reviewer.append('None')

    i = list(range(1,len(date)+1))
    df = pd.DataFrame(index=i)
    #print(date)
    #print(len(date))
    #print(interviewQuestions)
    #print(len(interviewQuestions))
    df['date'] = date
    df['location'] = location
    #df['employee'] = employee
    df['reviewer'] = reviewer
    df['interviewQuestions'] = interviewQuestions

    csvName = input('How do you want to name this csv?')
    df.to_csv('{}.csv'.format(csvName), sep=',')
    print('File {}.csv has been generated successfully! :)'.format(csvName))

if __name__ == '__main__':
    main()
