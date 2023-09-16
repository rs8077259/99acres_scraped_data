import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from utils import client
import os
from selenium import  webdriver
from selenium.webdriver.common.by import By
db=client.soup
collection=db.scrap
print(collection)

link="https://www.99acres.com/search/property/buy/{city}?keyword={city}&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N"

def push(prop_name,prop_cost,prop_type,prop_area,prop_locality,prop_city,ipl):
    data={
        "PropertyName":prop_name,
        "PropertyCost":prop_cost,
        "PropertyType":prop_type,
        "PropertyArea":prop_area,
        "propertyLocality":prop_locality,
        "propertyCity":prop_city,
        "IndividualPropertyLink":ipl
    }
    return collection.insert_one(data)

def make_req(url: str,incheader:bool=True):
    """"gets the html from the url given"""
    header=headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'
    }
    return requests.get(url,headers=header) if incheader else requests.get(url)

def parse(_html):
    return BeautifulSoup(_html,'html.parser')

def retrive_data(parse_:BeautifulSoup,response):
    prop=["projectTuple__descCont",'srpTuple__descCont']
    data=parse_.find_all(class_=prop[0])
    try:
        int(response.url[-1])
        city=response.url[response.url.find("-in-")+4:response.url.find("-ffid")]
        
    except:
        city=response.url[response.url.find("buy/")+4:response.url.find("?")]
    for property in data:
        name=property.a.string
        bhk,*locality=property.h2.string.split('in')
        locality=''.join(locality).strip()
        price=property.find('span',class_="list_header_bold configurationCards__srpPriceHeading configurationCards__configurationCardsHeading").text
        sqft=(property.find('span',class_="caption_subdued_medium configurationCards__cardAreaSubHeadingOne") or property.find('span',class_="caption_subdued_medium")).string
        link=property.a['href']
        try:
            if not (collection.find({"IndividualPropertyLink":link}).count()):
                push(name,price,bhk,sqft,locality,city,link)
        except:
            push(name,price,bhk,sqft,locality,city,link)

    data=parse_.find_all(class_=prop[1])
    for property in data:
        n=property.find('a',class_="srpTuple__dFlex")or property.find('td',class_="srpTuple__propertyPremiumHeading")
        name= n.text if n else "NoName"
        bhk,*locality=property.a.h2.string.split('in')
        locality=''.join(locality)
        
        price=property.find('td',class_="srpTuple__col title_semiBold").text
        sqft=property.find(id="srp_tuple_primary_area").text
        link=property.find(id="srp_tuple_property_title")['href']
        #pushing to mongo
        try:
            if not (collection.find({"IndividualPropertyLink":link}).count()):
                push(name,price,bhk,sqft,locality,city,link)
        except:
            push(name,price,bhk,sqft,locality,city,link)
    fetch_slink(parse_.find('a',text="Next Page >"),city)
    


def fetch_slink(parse_,for_):
    filter_condition = {for_: link}
    update_operation = {'$set': {for_: parse_.get('href',None)}}
    db.link.update_one(filter_condition, update_operation,upsert=True)


def doDayTask():
    global link
    for city in "pune delhi mumbai lucknow agra ahmedabad kolkata jaipur chennai bangalore".split(" "):
        link=db.link.find_one({city:{'$exists':True}})
        if link:
            link=link[f'{city}']
        else:
            try:
                driver=webdriver.Firefox()
                driver.get("https://www.99acres.com/")
                driver.implicitly_wait(3)
                input=driver.find_element(By.ID,'keyword2')
                input.send_keys("delhi")
                submit=driver.find_element(By.CSS_SELECTOR,"button[data-label='SEARCH_SUBMIT']")
                submit.click()
                link=driver.current_url
            except:
                link="https://www.99acres.com/search/property/buy/{city}?keyword={city}&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N".format(city=city)
        response=make_req(link)
        htmlcontent=response.content
        par=parse(htmlcontent)
        retrive_data(par,response)

