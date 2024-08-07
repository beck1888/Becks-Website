import json # For loading the Lottie animation's JSON data and other JSON data

class Asset:
    """Initializes src = Asset()... because 'asset' is too similar to the 'assert' keyword in Python."""

    def __init__(self, page_name: str, page_ID: int) -> None:
        """
        Args:
            short_page_name (str): The shortened, proper name of the page. Used for the tab title.
            page_ID (int): The ID of the page (based on asset folder). Will be used for locating assets.
        """
        self.page_name = page_name.title() # Capitalize the first letter of each word for proper tab titling
        self.page_ID = str(page_ID) # Force the conversion to a string
        self.asset_folder = f"assets/page_{str(page_ID)}"

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
    
    def load_lottie_animation_data(self) -> dict: # Returns the JSON data for the Lottie animation
        """
        Returns the path to the Lottie animation's JSON data.
        """
        with open(f"{self.asset_folder}/lottie.json", 'r') as f:
            return json.load(f)
    
    def under_construction(self) -> list:
        """
        Returns the html for the construction message and the data for the under construction sign.
        """
        # Load the Lottie animation
        with open("assets/shared/under_construction.json", 'r') as f:
            return ["<h1 style='text-align:center;'>Under Construction</h1>", json.load(f)]
