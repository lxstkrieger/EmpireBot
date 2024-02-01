


## Empire Bot

I'm not the best developer. I've been doing this as a hobby for a long time. I wanted my first project on GitHub to be a discord bot because I want people to have fun with it.
The bot has:
 1. Moderation
 2. Level-system(simple)
 3. Warning system(simple)
 4. Ticket-system(simple)
 5. TempVoice
 6. Fun commands
 7. Tic Tac Toe
 8. Docker Image on Dockerhub (lxstkrieger/empire_bot:1.0)
    https://hub.docker.com/repository/docker/lxstkrieger/empire_bot/general


### Information
There are 2 arguments in the environment file. 1. TOKEN and 2. DATABASE_PATH 3. DEBUG_GUILDS there you have to enter your TOKEN and the path to the database folder otherwise the bot will not work
 ~~~
sudo docker run -e TOKEN=$TOKEN -e DATABASE_PATH=$DATABASE_PATH -e DEBUG_GUILDS=$DEBUG_GUILDS,$DEBUG_GUILDS -d lxstkrieger/empire_bot:latest
 ~~~

feel free to use my code if it helps you.
if there are any bugs just open an issue and I will try to take care of it.

More updates will follow.

