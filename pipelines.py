# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import re, regex, requests, sqlite3

class MtPipeline(object):
    def __init__(self):
        self.create_connection()
#         self.create_table()
    
    def process_item(self, item, spider):
#         item["summary"][0] = self.clean_text(item["summary"][0])
#         print("HEREEEEEE:" + item["summary"][0])
        if len(item["summary"][0]) < 2:
            raise DropItem() # REMOVE NULL ITEM
        else:
#             r = self.post_text(item["summary"][0]) # POST TEXT
#             r = self.get_text()
#             data = r.json()
#             resp = data['resp']
#             text = resp['text']
#             print("\nResponse: ", text['text'], "\n")
            self.store_db(item)
            return item
    
    # FUNCTION TO CONNECT TO DATABASE
    def create_connection(self):
        self.conn = sqlite3.connect("DTN.db")
        self.curr = self.conn.cursor()
    
    # FUNCTION TO CREATE TABLE
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS summary""")
        self.curr.execute("""create table summary(id integer primary key, summary text, tag text)""")
        
    # FUNCTION TO CLEAN TEXT
    def clean_text(self, text):
#         print('HERE: ',len(text))
        text = re.sub('–','',text)
        text = re.sub(r'\([^)]*\)', '', text)
        text = re.sub(' +',' ',text)
        text = text.lstrip()
        text = text.rstrip()
        return text
    
    # FUNCTION TO STORE DATA TO DATABASE
    def store_db(self, item):
#         split_text = re.findall('(\w*?(?:\. |\! |\? ))',item['summary'][0])
        
        item['summary'][0] = re.sub('\. ','. \n',item['summary'][0])
#         print('HEREEEEEE: ' + item['summary'][0])
        item['summary'][0] = re.sub('\? ','? \n',item['summary'][0])
        item['summary'][0] = re.sub('\! ','! \n',item['summary'][0])
        item['summary'][0] = re.sub('\... ','... \n',item['summary'][0])
        item['summary'][0] = re.sub(';','\n',item['summary'][0])
        delimiters = '\n'
#         delimiters = ['. ','! ','? ', '\n']
#         split_text = regex.split(r'(?<=[{}])(?!$)'.format(regex.escape(delimiters)), item['summary'][0], flags=regex.V1)
#         values = re.split('|'.join(delimiters), item['summary'][0])
#         values.pop(0)
#         keys = re.findall('|'.join(delimiters), item['summary'][0])
#         split_text = dict(zip(keys,values))
#         print("HERE: ", i, item['tag'])
#         split_text = [e+delimiters for e in item['summary'][0].split(delimiters) if e]
        split_text = item['summary'][0].split(delimiters)
        for i in range(len(split_text)):
            if len(split_text[i]) > 5: 
                self.curr.execute("""insert or ignore into summary (summary, tag) values (?,?)""",(split_text[i], item['tag']))
                self.conn.commit()