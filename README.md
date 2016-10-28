# bash-bot
[Telegram](https://telegram.org/) bot for bash access to your computer. Depends on [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library, where you can find all the documentation.

## How to run?
1. Clone the repository and install requirements:  

    ```shell
    git clone https://github.com/grihabor/bash-bot
    cd bash-bot
    pip install -r requirements.txt
    ```

2. Create your bot via [BotFather](https://telegram.me/botfather) and get your apikey.  

3. Add file secrets.py to your project. Example:

    ```python
    TOKEN = 'YOUR_BOT_TOKEN'
    ADMIN_CHAT_ID = YOUR_CHAT_ID
    ```
    
4. To find out what is YOUR_CHAT_ID run your bot and look at the logger info output:

    ```shell
    python run.py
    ```   

5. Now fill YOUR_CHAT_ID field and rerun your bot. That's it! 
