#!/usr/bin/python3
# -*- coding: utf-8 -*-

#   _  __      __           _
#  /  /__)    /_  . / _ _   /
# <  /    (/ /   / / / / /  >
# /_      /               _/

from bs4 import BeautifulSoup as BS # For parsing html and getting links
from hurry.filesize import size # To display filesize in MB instead of bytes
from pyprind import ProgBar # A progress bar
from GoogleScraper.google import search_google # Import our custom google search
from time import gmtime, strftime # For our history file 
from conf import folder, title_dict # Our configuration
from req import requests, headers
from get_vodlocker_link import get_vodlocker_link
from lb import lb
import sys # For any system commands
import re # For regexing

# TODO;
#   1. Add more sites to search for films e.g vidzi
#   2. Build GUI version of pyFilm



# TODO
# -01 truncate link using .format



def banner():
        # TODO rearrange .formats
    print("{0}   _{2}  __    {0}  __           _{1}".format(R, W, BL))
    print("{0}  / {2} /__)   {0} /_  . / _ _   /{1}".format(R, W, BL))
    print("{0} <  {2}/    (/ {0}/   / / / / /  >{1}".format(R, W, BL))
    print("{0} /_ {2}     /  {0}             _/ {1}".format(R, W, BL))
    
def search():
    """First we need to search google.

    We do this by using our search_google() module
    """
    # Search google 
    search_google()




    
def get_film_link():
    
    """We need to use the link that the user chooses' from the list.

    If the vodlocker page does not contain a link to a video
    we come back and ask the user to choose again.
    """     
    # Variables for get_film_link function.
    which_link = input("{0}\n|{1}[?] {3}Which vodlocker link should we " \
                   "use?\n|\n|{2}--> {3}".format(lb, O, B, W))   
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
            print("{0}\n|{1}[!] {2}We could not find a video file." \
                  .format(lb, R, W)) 
        else:
            break


def find_title():
    """We tell the user what the title of the film is. 

    We use a dict to remove known words from the title
    such as uploader tags and video formats etc.

    """
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

    # Print the title with words from 'title_dict' removed
    print("{0}\n|{1}[+]{2} The title of the film is:\n|\t{3}" \
          .format(lb, G, W, fixed_title)) 
    # Print the link found on the vodlocker page
    print("{0}\n|{1}[+]{2} We found a video link on the vodlocker " \
          "page:\n|\t{3}".format(lb, G, W, film_link))




# Ask user if our file_name guess is ok, if no then the user
# can choose a file_name
def yes_no_question(question):
    while True:
        print(question)
        text = input()
        if text.lower().startswith("y"):
            print("{0}\n|{1}[+] {2}You have chosen to keep our chosen " \
                  "file name.".format(lb, G, W))
            break
        elif text.lower().startswith("n"):
            global file_name
            file_name = input("{0}\n|{1}[+] {2}Please name the file:\n|\n" \
                              "|{3}--> {4}".format(lb, G, W, B, W)) + ext
            print("{0}\n|{1}[+] {2}You have chosen to name the file;" \
                  "\n|\t".format(lb, G, W), file_name)
            break
        else:
            print("Sorry, I didn't understand that. Please type yes or no.")
    
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
    #Variables for name_film function

    # Make the title lowercase
    title_lower = fixed_title.lower() 
    # Strip any white spaces from the lowered title
    title_strip = title_lower.strip() 
    # Replace any spaces with hyphens
    title_hyphen = title_strip.replace(" ", "-")
    # Use the last 4 chars as the file extension
    # (this should be .mp4 or other video ext.) 
    ext = film_link[-4:] 
    # Name the file by putting
    file_name = title_hyphen + ext 
    
    # FIXME this finishes on a new line - which we dont want!           
    yes_no_question("{0}\n|{1}[+] {2}We have attempted to name " \
                     "the file from the title; \n|\t\"{3}\"\n|Is " \
                     "our guess O.K? [Yes/no]\n|{4}--> {5}" \
                     .format(lb, G, W, file_name, B, W))
                 
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
    print("{0}\n|{1}[+] {2}File Path and name:\n|\n|\t\"{3}{4}\""\
          .format(lb, G, W, prfx, file_name))
    # Print the file size
    print("{0}\n|{1}[+] {2}File Size: {3}"\
          .format(lb, G, W, size(file_size)))

    # Progress bar 
    bar = ProgBar(file_size / 1024, title=lb + "\n|" + G + " [+] " + W + \
                  "Downloading:\n|\n|" + file_name + "\n" + lb, \
                  stream=sys.stdout, bar_char='█', update_interval=1)
    with open(prfx + file_name, 'xb') as f:
        dl = 0
        # No content length header
        if file_size is None:
            print(lb)
            # error for no data
            sys.stderr.write("\n|{0}[!] {1}We could not get the total " \
                            "file size (this means there is no data to " \
                            "write to a file).".format(R, W))
        else:
            for chunk in u.iter_content(1024):
                dl += len(chunk)
                f.write(chunk)
                f.flush()
                bar.update(item_id = file_name)
        print("{0}\n|{1}[+] {2}Finished downloading {3}\n" \
              .format(lb, G, W, file_name))
        print(lb)


def dl_history():
    """As an extra we produce a list of our download history.

    We simply write the path to the file and the file name,
    along with the current time, day and date for reference.
    """
    # A file to store our history in
    list_file = "download_history.txt"
    with open(list_file, 'a+t') as f:            
        # Nothing to add to our list
        if file_name is None:
            # error for no data
            sys.stderr.write("{0}\n|{1}[!] {2}There was no history " \
                             "occurance to write to history file." \
                             .format(lb, R, W))
        else:
            print("{0}\n|{1}[+] {2}Writing a history occurance to " \
                  "{3}{4}".format(lb, G, W, list_file, "."))
            f.write("\n" + strftime("@ %H:%M:%S on %A %d %B %Y", \
                    gmtime()) + "\n" + prfx + file_name + "\n")
            f.close()
            print("\n|{0}[+] {1}Done!".format(G, W))

if __name__ == "__main__":
    """We run all the above functions in order.
    """               
    banner()
    search()
    get_vodlocker_link()
    get_film_link()
    find_title()
    name_film()
    dl_film()
    dl_history()
