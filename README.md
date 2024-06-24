# 🎮 A connect-4 Bot that adds more activities to your server
> **Still in development** so the link and everything else still unavailable  
</br>
</br>  
  
## ℹ️ Command walkthrough:
### /register:
**Create your account**
> Required for playing the game

### /info [Member]:
**Get info about specific player**
> Shows a nice menu with stuff like: winrate, skins, etc.

### /set_skins:
**Allows you to set special skin** for your's and opponent's coin, pretty neat.
> Operated by dropdown menu

### /challenge [Member]:
**Challenges a chosen member of the server**
> Sends a dm to them with a possibility of accepting or declining it

### /play [Move]:
**Plays a move** 
> while the game is still ongoing

### /surrender:
**Allows you to forfeit the game**
> while the game is still ongoing
</br>
</br>

## 📜 ToDo
> **Disclaimer:** not everything will be added, but also some new stuff may come up
  - Ranking (on your server)
  - Add help page
  - Try to add a possibility of recieving duels in the text-channels (on servers) instead of dms [The player would be able to choose]
  - Improve UI (make it nicer, like it's good but still there is room for some improvement)
  - Get current players on the channel where command is executed
  - Allow Administrators to delete games (sometimes smth can bug out)
    - if Admin deletes a game in which he is, then he automatically loses the game
    - Add karma system that is based on reaction to the deletion of game by administrator:
      - Admin starts with 5 karma
      - if Admin has less than 0 karma, then he can't delete games
      - Karma is server based
      - After deletion (if it was deleted by admin that was not one of the players) a form is sent, containing upvote, downvote, and na
      - Upvote gives karma to an Admin, Downvote, removes, na(no-action) does nothing
> **Very Low** probability for karma system
  
  - **Systems that lower toxicity**:
  - Add a time system that 
    - is a clock or:
    - naturally deletes game after some time around (45 min, 1h 15min)
  - Add casual (will not change elo and w/l stats)

</br>
</br>


## ⚒️ Curent-Version:

### 0.9.0 (24.06.2024):
  - Added info page for checking your and other players stats
  - Now the win panel shows the end position
  - Organized command files, so that they are readeable
  - Added elo system, and w/l stats (including amount of games and win-rate)
  - Added command of surrendering
