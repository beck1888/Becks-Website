# README for [Beck's Website](http://beck.asuscomm.com/)

[GitHub Repo for this project](https://github.com/beck1888/Becks-Website)

---

## Table of Contents
- [README for Beck's Website](#readme-for-becks-website)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Funding](#funding)
    - [Credits](#credits)
  - [AI Disclaimer](#ai-disclaimer)
  - [Technologies Used](#technologies-used)
  - [Support](#support)
  - [Installation](#installation)
  - [License](#license)
  - [IMPORTANT COPYRIGHT NOTICE](#important-copyright-notice)

## About
This is my side project, hosted on a RaspberryPi that's currently sitting on my bedroom bookshelf. Please read the homepage of this app for full details.

At some point, I intend to write more formal documentation, a roadmap, and a to-do; but right now I'm focusing more on development than documentation. Also, I've tried to follow Python best practices and proper code formatting, but I'm sure I could always do a better job!

If you want to help me with this, or anything else, I would really appreciate it! Please feel free to open an issue, PR, or fill out the contact form on the site. Also, I'm new to writing readmes (can you tell)? I pretty much just looked around on different GitHub repos and included aspects of their READMEs that seem relevant on this one. If this README is overkill or to harsh or formatted incorrectly or missing something or really has any issues or anything of that sort, please feel free to help me fix it. Like I said, this is my first time writing and deploying a project like this, so I'm sure I have plenty to learn, and any help in that direction would be greatly appreciated!

### Funding
This project is completely self funded. Most of it was free (aka I already owned the hardware). My only real operating expense are API keys. Right now I have $5.00 loaded onto the OpenAI api set up to not auto-reload, so if errors with api keys come up that is probably the cause. I can fund it more, but I'm trying to keep costs low because this is a side project.

### Credits
Thank you, among others, to Lottie Files for the animations on this site!

Thank you to the following news sites for their RSS feed (licensed under non-commercial use):

- [The New York Times](https://www.nytimes.com/rss)

## AI Disclaimer
This project uses AI which is known to make mistakes. Please always double check important info. Any mistakes the AI makes are not the dev's responsibility.

## Technologies Used
- [Streamlit](https://streamlit.io/)
- [OpenAI's API](https://platform.openai.com/docs/overview)
- [Lottie](https://lottiefiles.com/)
- Python 3
    - PIP
- RaspberryPi 5
- ASUS Router
    - Built-in DDNS
    - Port forwarding

## Support
If you find issues or want to add features, I welcome your contributions! You can fill out the contact form on the site or open an issue or PR on GitHub. I will likely see submissions from the site's contact form faster.

## Installation

You can use this project at: [http://beck.asuscomm.com/](http://beck.asuscomm.com/)

OR

Follow these steps to set up the project on your own machine (Mac/Linux; similar for Windows):

1. Clone the repo.
2. Navigate to the project root.
3. Create the Streamlit configuration files:
    ```sh
    mkdir .streamlit && cd .streamlit
    touch config.toml secrets.toml
    ```
4. Add the following to `config.toml`:
    ```toml
    [server]
    headless = true

    [theme]
    base = "light"

    [browser]
    gatherUsageStats = false
    ```
    Save the file.

5. Add your OpenAI API key to `secrets.toml`:
    ```sh
    nano secrets.toml
    ```
    Add: `OPENAI_API_KEY=your_openai_api_key_here`

6. Navigate back to the project root and run:
    ```sh
    streamlit run 🏠_Home.py
    ```
7. Visit [http://localhost:8501/](http://localhost:8501/)

Protect your API keys by adding a password screen if deploying publicly via the [Streamlit Community Cloud](https://streamlit.io/cloud) or another hosting method (e.g., RaspberryPi and port forwarding as I’m doing).

## License

You are permitted to copy, modify, and distribute this code for any purpose, including commercial use, with or without attribution. If you wish to provide credit, please link to my GitHub or this repository.

Prohibited Actions:

- Spamming this page.
- Spamming any and all APIs including, but not limited to, GitHub and OpenAI APIs
- Sending malicious requests to this page.
- Attempting to compromise or disrupt the functionality of this page.
- Misusing this page in any manner.
- Exploiting bugs and other vulnerabilities.
- Attempting to collect API keys.

By using this site, you agree to:

- Utilize this page as a collection of utilities with good intent.
- Refrain from sending automated requests to this page.
- Not bypass security measures implemented on this page.
- Respect the privacy of the host server and its users.

Although I cannot make you report bugs, issues, and/ or vulnerabilities (especially leaked api keys) you find, **I kindly (and strongly) request that you share any and all of these you find with me ASAP.**

Please refer to the License file for full details on modifying or using this code.

**Important Notice:**

- This project may utilize third-party platforms (e.g., Streamlit, OpenAI) that have their own terms of service and usage restrictions. **It is your responsibility to ensure compliance with those terms.**

- **I am not liable for any misuse or violations of third-party terms** resulting from your use of this code.

## IMPORTANT COPYRIGHT NOTICE

**This project is exclusively for personal, non-commercial purposes and may contain media or works (including but not limited to: images, audio, video, animations, and more) that are copyrighted.** 

I have not documented or verified the copyright status of any materials used. The inclusion of potentially copyrighted content poses significant legal risks. 

**If you intend to use, distribute, or modify this project in any manner, it is your sole and absolute responsibility to meticulously identify and replace any copyrighted materials with legally permissible alternatives as the law requires.** 

---

Enjoy!