todo: create repllit.py version

# discord_mutebot
A basic bot for discord that has timed and infinite mutes.

### Instructions for use
#### (this assumes you are using [repl.it](https://repl.it/) and [uptimerobot](https://uptimerobot.com/login?rt=https://uptimerobot.com/dashboard#) )

1. create an account on repl.it and uptime robot (the free accounts are fine)

2. on repl.it create a new python (not python 2) repl

3. paste the contents of replit.py (*not main.py*) from github into main.py on the repl

3.5. change lines 1 and 2 to have the name of the member role and the muted role in the quotes 
     it should say
     `memberrolename='name of your member role'`
     `muterolename='name of your muted role'`

3.6. create a file called `.env` on repl.it

3.7. paste `TOKEN=` ninto the .env file on the first line

3.8. paste your bot token after the `=`

4. click `run` at the top of the screen on your repl

5. after stuff installs onto the repl, there should be a white box on the right of the screen. copy the url that is at the top of the white box (it should be something like `something--yourusername.repl.co`)

6. on uptimerobot, create a new http(s) monitor, and paste the url you copied into the URL box

7. mae sure that the url is something like `https://something--yourrepllitusername.repl.co` and not `http://https://something--yourrepllitusername..repl.co`

8. assign the monitor a "Friendly name" if you want

9. make sure that the monitoring interval is as low as possible

10. click `create monitor` on uptimerobot

10.5. go back to your repl, and cllickk `restart` or `start`

11. the bots I made that are hosted this way have over 99% uptime, and they automatically start again after going down
