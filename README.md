# Matey Personal Assistant GUIDE

1. Clone the project on your computer (copy HTTPS link, open powershell in the folder where you want to install the assistant, write "git clone" and paste the HTTPS link)
2. Open the terminal and run the following commands:
   - py -m pip install --upgrade pip
   - py -m venv venv
   - Set-ExecutionPolicy Unrestricted -Scope Process
   - .\venv\Scripts\activate
   - pip install -r ./requirements.txt
3. Open config.json
   - for the "chatgpt_api_key", go on https://platform.openai.com/account/api-keys, generate the api key and copy it in the config file
   - for the "openweather_api_key", go on https://home.openweathermap.org/api_keys, generate the api key and copy it in the config file
   - for the "assemblyai_api_key", go on https://www.assemblyai.com/app/account, generate the api key and copy it in the config file
   - for the "windows_user", write your windows user (C:\Users\\?)
   - for the "chrome_exe_path", go where Google Chrome is installed (right-click -> open file location) -> shift-right-click on "chrome.exe" -> copy as path, paste that path in the config file (note: the path sould be surrounded by one pair of quotation marks. WRONG: ""path"", RIGHT: "path")
4. To create google cloud credentials, follow the instructions on https://cloud.google.com/sdk/docs/install
5. Run the main script and follow commands.txt when using the assistant
6. Remember:
   - to use the assistant, python must be already installed 
   - the plotting of the assistant's answers depends of how good is your processor. I developed the framework on a "11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz". When you run main script and say "Hey Matey", the assistant will show up and say "Hello, how can I help you?". If you notice that the plot is not concomitant with the sound, stop the program, slightly modify the "tick_in_seconds" in the config.json file, run again. Keep doing this process until the plot and the sound are concomitant.
   - don't forget to make shortcuts of the apps you want to open with the assistant and put them in the "shortcuts" folder inside the framework.
   - the downloaded songs by the assistant will be moved into the "downloads" folder inside the framework.
   - the images taken by the assistant will be saved in the "images" folder inside the framework.
   - the history of all the search, weather, location and translation commands is saved in the "results" folder inside the framework.
   - the "chromedriver.exe" in the "core" folder must be replaced with the last version of your Chrome browser. To do this, you must open Chrome, go to settings, access the "About Chrome" tab and keep in mind the version number. Go on https://chromedriver.chromium.org/downloads and download that version (or the closest one). Unzip the downloaded file, copy the "chromedriver.exe" and replace it in the "core" folder of the framework.
7. If you find any bugs, don't hesitate to submit them.
# THANK YOU!
