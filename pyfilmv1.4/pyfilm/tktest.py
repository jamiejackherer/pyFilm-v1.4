#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#   _  __      __           _
#  /  /__)    /_  . / _ _   /
# <  /    (/ /   / / / / /  >
# /_      /               _/

from bs4 import BeautifulSoup as BS # For parsing html and getting links
from hurry.filesize import size # To display filesize in MB instead of bytes
from pyprind import ProgBar # A progress bar
from GoogleScraper import scrape_with_config, GoogleSearchError
from time import gmtime, strftime # For our history file 
from conf import folder, title_dict # Our configuration
import requests as r # For getting html files
import pandas as pd # For parsing results.csv
import sys # For any system commands
import re # For regexing
from tkinter import *
import tkinter.messagebox


# TODO;
#   1. Add more sites to search for films e.g vidzi

"""
Changelog;
    What's new in version 0.1?
"""
__version__ = '0.1'
__maintainer__ = "jamiejackherer@gmail.com"
__status__ = "Prototype"
__updated__ = '17.06.2016'  # day.month.year


# prefix of search term
site = "site:vodlocker.com " 
# ask user for search term
keywords = site + str(text)

class pyfilm(Frame):
    def __init__(self, master=None):
        
        Frame.__init__(self, master)
        self.grid()
        self.mainLabel()
        self.buttons()
        self.enterSearch()
        
    def mainLabel(self):
        
        self.mainLabel = Label(self, text="PyFilm - Easily download your favourite films.")
        self.mainLabel.grid(row=1, column=1, columnspan=4)
    
    def buttons(self):
        
        self.quitButton = Button (self, text='Quit', command=self.quit)
        self.quitButton.grid(row=4, column=1, columnspan=2, sticky=S)
        
        self.searchButton = Button(self, text='Search', command=self.search_term())
        self.searchButton.grid(row=4, column=2, columnspan=2, sticky=S+E)
        
    def enterSearch(self):
        
        self.searchEntryLabel = Label(self, text="Enter a film title to search: ")
        self.searchEntryLabel.grid(row=2, column=1, sticky=W)
        
        self.searchEntry = Entry(self, width=40, bg="white")
        self.searchEntry.grid(row=2, column=2, sticky=E+W)
        
    def text():
        text = self.searchEntry.get()

    def search_term(self):
        global keywords
        print("keywords are ", keywords)
    def search_google():
        """A function to search google for our film
        """
        config = {
        'use_own_ip': True,                     # whether to use our own IP address 
        'keyword': keywords,
        'search_engines': ['google'],           # various configuration settings
        'num_pages_for_keyword': 1,
        'scrape_method': 'http',
        'do_caching': False,
        'num_results_per_page': 50,
        'log_level': 'CRITICAL',
        'output_filename': 'results.csv'        # file to save links to 
    #    'proxy_file': 'proxies.txt'            # file to load proxies from 
        }
        try:
            search = scrape_with_config(config)
        except GoogleSearchError as e:
            print(e)
    

          
app = pyfilm()
app.master.title("{PyFilm}")
app.master.minsize(500, 200)
app.master.geometry("500x500")
app.mainloop()
