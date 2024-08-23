import json # For loading the Lottie animation's JSON data and other JSON data
import subprocess # For cache management
import datetime

def get_date_and_time() -> str:
    """
    Returns the current date and time in the format "YYYY-MM-DD HH:MM:SS".
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Asset:
    """Initializes src = Asset()... because 'asset' is too similar to the 'assert' keyword in Python."""

    def __init__(self, page_name: str, page_ID: int) -> list:
        """
        Args:
            short_page_name (str): The shortened, proper name of the page. Used for the tab title.
            page_ID (int): The ID of the page (based on asset folder). Will be used for locating assets and checking status.

        Returns:
            list: A boolean for if the page is allowed to be viewed and the an text message explaining why (if it's not). True means it's allowed, False means it's not.
        """
        self.page_name = page_name.title() # Capitalize the first letter of each word for proper tab titling
        self.page_ID = str(page_ID) # Force the conversion to a string
        self.asset_folder = f"assets/page_{str(page_ID)}"

        # Log
        with open("visitor_log.txt", "a") as f:
            f.write(f"LOADED: {get_date_and_time()} - {self.page_name} - {self.page_ID}\n")

    def is_locked(self) -> bool:
        """
        Returns if the page is locked.
        """
        # Convert the page ID to a string to comply with json rules

        page = str(self.page_ID)
        # Load the JSON data
        with open("assets/shared/locks.json", 'r') as f:
            locks = json.load(f)

        # First, check if the global lock is on
        if locks['global']['lock']: # The global lock is on
            return [True, locks['global']['reason']]

        # Otherwise, check if the page exists in the lock file
        if page in locks.keys():
            # If the page exists, check if the lock is on
            if locks[page]['lock']: # The lock is on
                return [True, locks[page]['reason']]
            else: # The lock is off
                return [False, locks[page]['reason']]
        else: # The page doesn't exist
            return [True, "This page does not comply with the lock system and has been locked."]

    def clear_st_ui(self) -> str:
        """
        Returns the code needed to run to clear the Streamlit UI.
        Make sure to run it with streamlit markdown and allow unsafe html!
        """
        return ['\n<style>\n    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}\n</style>\n', '', '\n<style>div[data-testid="stToolbar"] { display: none;}</style>\n']

    def favicon(self) -> str:
        """
        Returns the path to the favicon of the page.
        """
        return "assets/shared/favicon.png"
    
    def tab_title(self) -> str:
        """
        Returns the title of the tab based on the current page.
        """
        title = "Beck's Site | " + self.page_name
        return title

    def under_construction(self) -> list:
        """
        Returns the html for the construction message and the data for the under construction sign.
        """
        # Load the Lottie animation
        with open("assets/shared/under_construction.json", 'r') as f:
            return ["<h1 style='text-align:center;'>Under Construction</h1>", json.load(f)]
        
    def fetch_local_json(self, file_name: str) -> dict:
        """
        Returns the JSON data for the specified file name under the page's dedicated asset folder.
        """
        with open(f"{self.asset_folder}/{file_name.removesuffix('.json')}.json", 'r') as f:
            return json.load(f)
        
    def clear_cache(self) -> None:
        """
        Clears all caches.
        """
        raise PendingDeprecationWarning("This function does not work")
        # Cache folders: cache/memes and cache/YT
        folder_endpoints = ["memes", "YT"]

        for folder_endpoint in folder_endpoints:
            # Keep the folder BUT remove all its contents
            try:
                subprocess.Popen(["bash", f"rm -rf /home/admin/Documents/Becks-Website/cache/{folder_endpoint}/*"])
            except:
                pass # Ignore the error if the folder doesn't exist (because on the dev platform it doesn't - different file structure)