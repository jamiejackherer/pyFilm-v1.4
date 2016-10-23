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

class pyfilm_gui(Frame):
    def search_google():
        """A function to search google for our film
        """
        # prefix of search term
        site = "site:vodlocker.com " 
        searchTerm = self.searchEntry.get()
        # ask user for search term
        keywords = site + searchTerm
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
            
    def download_film():
        # TODO rearrange .formats
        """First we need to search google.
        
        We do this by using our search_google() module
        """
        # Search google 
        search_google()
        
        # Requests variables.
        # Create an instance of a requests session named 's'
        s = r.Session() 
        # Set the user agent and other stuff in the http header 
        headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like " \
                   "Mac OS X) Safari/9537.53", 
                   "Accept":"text/q=0.9,image/webp,*/*;q=0.8", 
                   "Accept-Language":"en-US,en"}
        

        # Variables for get_vodlocker_link function.
        """Next we write the results of our google_search() to a file called
        results.csv.
        
        We get the links and the title found and format them to
        be lower case.
        """
        # Create an instance of the file
        csv_file = "results.csv"
        # Read said file
        df = pd.read_csv(csv_file)
        # Get the vodlocker links from the file
        # (note: you can also use df.['column-name']
        vodlocker_link = df['link']
        link_id = df['title']
        results = df['num_results_for_query']
        results_lower = results[0].lower()
         
        def get_vodlocker_link():
            """Now we print the results we found.
            
            This is so the user can choose which link
            they would like to use.
            """
            # Print how many links found in how many secs    
            print("\n[+] We have found {0}".format(results_lower))
            # Print the title of the pages found as shown in google
            print(link_id)

        # Variables for get_film_link function.
        which_link = input("\n[?] Which vodlocker link should we use?\n--> ")
            
        def get_film_link():
            """We need to use the link that the user chooses' from the list.
            
            If the vodlocker page does not contain a link to a video
            we come back and ask the user to choose again.
            """        
            while True:
                # Get the film link using 'which_link' given by the user and
                # iterate over until we find a valid page with a link in
                req = s.get(vodlocker_link[int(which_link)], headers=headers) 
                bs = BS(req.text, "lxml") # create a soup object
               #file_removed = r"^http?://(*.*.*.*)/([a-zA-Z0-9]\+\)(v.mp4)" 
                # TODO it will be better if we can use a
                # regex search to search for a link 
                # (e.g., http://177.272.45.91/vhxjhvjhv89dyf9s8eyuf98syfhs89y/v.mp4) 
                # instead of .mp4 
                
                # If this is not in the page then we dont want this page
                file_removed = "v.mp4" 
                if file_removed not in bs:
                    # Print no video file
                    print("\n[!] We could not find a video file.") 
                else:
                    break
        
        # Variables for find_title function

        # Find the film link
        film = bs.find(type="video/mp4") 
        # Get the actual film link
        film_link = film["src"]
        # Find the title as it is on the vodlocker page
        title = bs.find(id="file_title").get_text()
        # Title_dict from conf file
        title_dict()
        # Create a regex 'or' for items in the dict
        regex_title = r"|".join(title_dict) 
        # Actually remove the items that are in 'title_dict'
        fixed_title = re.sub(regex_title, "",title, flags=re.I)
        
        def find_title():
            """We tell the user what the title of the film is. 
            
            We use a dict to remove known words from the title
            such as uploader tags and video formats etc.
            
            """
            # Print the title with words from 'title_dict' removed
            print("\n[+] The title of the film is:\n{0}".format(fixed_title)) 
            # Print the link found on the vodlocker page
            print("\n[+] We found a video link on the vodlocker page:\n{0}".format(film_link))


        #Variables for name_film function
        
        # Make the title lowercase
        title_lower = fixed_title.lower() 
        # Strip any white spaces from the lowered title
        title_strip = title_lower.strip() 
        # Replace any spaces with hyphens
        title_hyphen = title_strip.replace(" ", "-")
        
        # Ask user if our file_name guess is ok, if no then the user
        # can choose a file_name
        def yes_no_question(question):
            while True:
                print(question)
                text = input()
                if text.lower().startswith("y"):
                    print("\n[+] You have chosen to keep our chosen file name.")
                    break
                elif text.lower().startswith("n"):
                    global file_name
                    file_name = input("\n[+] Please name the file:\n--> ") + ext
                    print("\n[+] You have chosen to name the file;\n{0}".format(file_name))
                    break
                else:
                    print("\nSorry, I didn't understand that. Please type yes or no.")
                
        def name_film():
            """We try to name the file.
            
            By getting the title from the vodlocker
            page and formatting it.
                        
                We first make the title lowercase,
                then strip any leading and trailing whitespaces from the title,
                and replace any spaces with hyphens.
            
            If the user is happy with our name for the file we continue on,
            otherwise we ask the user to name the file. 
            """
            # Use the last 4 chars as the file extension
            # (this should be .mp4 or other video ext.) 
            ext = film_link[-4:] 
            # Name the file by putting
            file_name = title_hyphen + ext 
                
            # FIXME this finishes on a new line - which we dont want!           
            yes_no_question("\n[+] We have attempted to name the file from the"\
                            "title;\n\"{0}\"\nIs our guess O.K? [Yes/no]\n--> "\
                            .format(file_name))
                         
        # We get the folder to save downloads from conf file
        folder() 
        
        def dl_film():
            """This is where we actually do the downloading.
            
            We get the file size from the http headers.
            
            We tell the user some of the details such as
            file size (in MB) and where the file will be
            saved and its name.
            
            We initialise a progress bar for the download.
            
            And finally write the data to a file that we set earlier.
            """
        
            # Create an instance of the file stream
            u = s.get(film_link, headers=headers, stream=True)
            # Get meta info -- file size
            file_size = int(u.headers["content-length"])
            # Print the file name and path
            print("\n[+] File Path and name:\n\"{0}{1}\"".format(prfx, file_name))
            # Print the file size
            print("\n[+] File Size: {0}".format(size(file_size)))
            
            # Progress bar 
            bar = ProgBar(file_size / 1024, title="[+] Downloading:\n" + file_name + "\n", \
                          stream=sys.stdout, bar_char='█', update_interval=1)
            with open(prfx + file_name, 'xb') as f:
                dl = 0
                # No content length header
                if file_size is None:
                    # error for no data
                    sys.stderr.write("[!] We could not get the total " \
                                    "file size (this means there is no " \
                                    "data to write to a file).")
                else:
                    for chunk in u.iter_content(1024):
                        dl += len(chunk)
                        f.write(chunk)
                        f.flush()
                        bar.update(item_id = file_name)
                print("\n[+] Finished downloading {0}\n".format(file_name))
        # A file to store our history in
        list_file = "download_history.txt"
        
        def dl_history():
            """As an extra we produce a list of our download history.
            
            We simply write the path to the file and the file name,
            along with the current time, day and date for reference.
            """
            with open(list_file, 'a+t') as f:            
                # Nothing to add to our list
                if file_name is None:
                    # error for no data
                    sys.stderr.write("\n[!] There was no history " \
                                     "occurance to write to history file.")
                else:
                    print("\n[+] Writing a history occurance to " \
                          "{0}.".format(list_file))
                    f.write("\n" + strftime("@ %H:%M:%S on %A %d %B %Y", \
                            gmtime()) + "\n" + prfx + file_name + "\n")
                    f.close()
                    print("\n[+] Done!")
        
        #if __name__ == "__main__":
         #   """We run all the above functions in order.
          #  """               
            #search_google()
            #get_vodlocker_link()
            #get_film_link()
            #find_title()
            #name_film()
            #dl_film()
            #dl_history()


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
        
        self.quitButton = Button (self, text='Quit', command=quit)
        self.quitButton.grid(row=4, column=1, columnspan=2, sticky=S)
        
        self.searchButton = Button(self, text='Search', command=pyfilm_gui.search_google())
        self.searchButton.grid(row=4, column=2, columnspan=2, sticky=S+E)
        
    def enterSearch(self):
        
        self.searchEntryLabel = Label(text="Enter a film title to search: ")
        self.searchEntryLabel.grid(row=2, column=1, sticky=W)
        
        self.searchEntry = Entry(width=40, bg="white")
        self.searchEntry.grid(row=2, column=2, sticky=E+W)
        

app = pyfilm_gui()
app.master.title("{PyFilm}")
app.master.minsize(500, 200)
app.master.geometry("500x500")
app.mainloop()
