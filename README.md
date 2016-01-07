This is a Telegram bot that will lookup up a portuguese word in [Priberam](http://priberam.pt), a portuguese dictionary.   Feel free to use it by talking to [@PriberamBot](http://telegram.me/priberambot).

PriberamBot was a developed using [TGBotPlug](http://fopina.github.io/tgbotplug).

This repository is ready for openshift (as the bot is running there), so you can easily host your own:

* Register in [OpenShift](https://www.openshift.com)  
* Install [rhc](https://developers.openshift.com/en/managing-client-tools.html), the command line tool  
* Run `rhc setup` to configure it  
* Talk to [@BotFather](http://telegram.me/botfather) to register your bot  
* And finally run these commands (replacing `<YOUR_BOT_TOKEN>` with the token provided by @BotFather)

    ```
    rhc app-create priberambot python-2.7 postgresql-9.2 --from-code https://github.com/fopina/tgbot-priberambot/
    cd priberambot
    rhc env-set TGTOKEN=<YOUR_BOT_TOKEN>
    rhc ssh -- 'app-root/repo/priberambot.py --db_url="postgresql://$OPENSHIFT_POSTGRESQL_DB_HOST:$OPENSHIFT_POSTGRESQL_DB_PORT/$PGDATABASE" --create_db'
    rhc app-restart
    ```

Have fun!
