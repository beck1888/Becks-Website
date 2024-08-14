# TODO List

## TODO list order
1. Caching memes issue

## Server management
- [ ] Find a better caching mechanism for the memes
    - Right now, the cache clears on each page load, meaning if there are multiple users on the page, it's very possible that if one user loads it before another can download their meme, then when the user tries to download their meme, it won't work because it will be deleted
        - I think the solution is to use session state to cache as a file instead of keeping it on the server's cache
        - The YouTube downloader is going to have the same issue because the cache clears when the page starts downloading a video, so these also urgently needs a fix
- [ ] See if the update process is spawning multiple Streamlit processes instead of killing old ones
- [ ] Get an SSL certificate so the page is secure
- [ ] Make the RPI server run the update script on boot!

## UX/ UI
- [ ] Use advance multi page app method to create an ordered sidebar and then customize sidebar on each page
- [ ] Get rid of Streamlit top bar UI
- [ ] Rearrange the buttons in the admin portal to make more sense
- [ ] Add a message viewer to the admin portal
- [ ] Add a better thinking UI to the chat page
- [] Add a toggle for sounds