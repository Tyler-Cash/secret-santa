#Purpose
This web application automates the secret santa finding process and also allows people to tell their secret santa what they are interested in. With my family there are many people who don't know each other too well which can be problematic if you're meant to be giving them a gift for christmas. This site hopefully solves that.

#Set up
The `email_user` method basically needs to be completely changed for other users. The password for your SMTP account is stored in `sender_password` inside of `sender_pass.py` to ensure it isn't publicly available on github.

Also `database.create_tables(some_db_object)` needs to be run before the any login, signup, etc connections are made.

Once this has been completed, simply running `secret_santa.py` will run the web application.

#Finding secret santa
Everyone's secret santa can be found by running `find_santa.py`. The family ID may need to be tweaked on lines 31 and 32 though.

Screenshots of web application:
![Main screen](http://i.imgur.com/pfYv2V3.png)
![Login form](http://i.imgur.com/0mZLYlu.png)
