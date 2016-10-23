#!/usr/bin/python3
#-*- coding:utf-8 -*-

import requests as r # For getting html files

def requests():
    # Create an instance of a requests session named 's'
    s = r.Session()

def headers():
    # Set the user agent and other stuff in the http header 
    headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like " \
               "Mac OS X) Safari/9537.53", 
               "Accept":"text/q=0.9,image/webp,*/*;q=0.8", 
               "Accept-Language":"en-US,en"}
        
