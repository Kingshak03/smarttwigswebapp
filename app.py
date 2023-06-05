from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
players = []

class player:
    def __init__(self, player_name, wins, cumulative, points):
        self.player_name = player_name
        self.wins = wins
        self.cumulative= cumulative
        self.points = points
        
    def __repr__(self) -> str:
        return f"{type(self).__name__}(player_name={self.player_name}, wins={self.wins}, cumulative={self.cumulative}, point={self.points})"

class game:
    def __init__(self, player1, player2, initial_server):
        self.player1 = player1
        self.player2 = player2
        self.initial_server = initial_server
        self.player1Points = 0
        self.player2Points = 0
        self.current_server = initial_server
        self.current_round = 0
        self.winner = None
        self.winnerName = None

    def addPoints1(self):
        self.player1Points = self.player1Points + 1
        self.current_round += 1
        self.chooseCurrentServer()
        self.choose_winner()
        
    def addPoints2(self):
        self.player2Points += 1
        self.current_round += 1
        self.chooseCurrentServer()
        self.choose_winner()
        
    def chooseCurrentServer(self):
        if(self.current_round != 0 and self.current_round % 2 == 0):
            if(self.current_server == self.player2):
                self.current_server = self.player1
            else:
                self.current_server = self.player2
        return
    
    def choose_winner(self):
        if(self.player1Points > 10 and self.player2Points < 10):
            print("line 52")
            self.winner = self.player1
            self.winnerName = self.player1.player_name
            self.player1.wins += 1
            self.player1.cumulative += self.player1Points
            self.player1Points = 0
            self.player2Points = 0
            
        if(self.player2Points > 10 and self.player1Points < 10):
            self.winner = self.player2
            self.winnerName = self.player2.player_name
            self.player2.wins += 1
            self.player2.cumulative += self.player2Points
            self.player1Points = 0
            self.player2Points = 0
        
        if(self.player1Points >= 10 and self.player2Points >= 10):
            if((self.player1Points - self.player2Points) >= 2):
                self.winner = self.player1
                self.winnerName = self.player1.player_name
                self.player1.wins += 1
                self.player1.cumulative += self.player1Points
                self.player1Points = 0
                self.player2Points = 0
                
            if((self.player2Points - self.player1Points) >= 2):
                self.winner = self.player2
                self.winnerName = self.player2.player_name
                self.player2.wins += 1
                self.player2.cumulative += self.player2Points
                self.player1Points = 0
                self.player2Points = 0
                
    def __repr__(self) -> str:
        return f"{type(self).__name__}(player1Name={self.player1.player_name}, player2Name={self.player2.player_name}, point={self.player1Points}, winner={self.winner}, current_server={self.current_server} )"

def gameplay(start_game):
    # show players 
    player1Name = start_game.player1.player_name
    player2Name = start_game.player2.player_name
    player1Points = start_game.player1Points
    player2Points = start_game.player2Points
    final_winner = start_game.winnerName
    current_server = start_game.current_server
    print(players)
    return render_template("index.html", player1Name=player1Name, player2Name=player2Name, player1Points = player1Points, player2Points = player2Points, current_server=current_server, start_game = start_game, final_winner = final_winner)


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/add", methods= ["POST"])
def add():
    global start_game
    player1Name= request.form.get("player1Name")
    player2Name= request.form.get("player2Name") 
    initialServer= request.form.get("initialServer") 
    filtered1 = any(player.player_name == player1Name for player in players)
    filtered2 = any(player.player_name == player2Name for player in players)
    
    
    if(filtered1 and filtered2):
        new_player1 = (player for player in players if player.get('player_name') == player1Name)
        new_player2 = (player for player in players if player.get('player_name') == player2Name)
        start_game = game(new_player1,new_player2, initialServer)
        return(gameplay(start_game))

    if(filtered1):
        new_player1 = (player for player in players if player.get('player_name') == player1Name)
        new_player2 = player(player_name = player2Name, wins = 0, cumulative = 0, points = 0)
        players.append(new_player2)
        start_game = game(new_player1,new_player2, initialServer)
        return(gameplay(start_game))

    if(filtered2):
        new_player1 = player(player_name = player1Name, wins = 0, cumulative = 0, points = 0)
        new_player2 = (player for player in players if player.get('player_name') == player2Name)
        players.append(new_player1)
        start_game = game(new_player1,new_player2, initialServer)
        return(gameplay(start_game))

    else:
        new_player1 = player(player_name = player1Name, wins = 0, cumulative = 0, points = 0)
        new_player2 = player(player_name = player2Name, wins = 0, cumulative = 0, points = 0)
        players.append(new_player1)
        players.append(new_player2)
        start_game = game(new_player1,new_player2, initialServer)
        return(gameplay(start_game))

@app.route("/player1points")
def addplayer1points():
    start_game.addPoints1()
    return(gameplay(start_game))

@app.route("/player2points")
def addplayer2points():
    start_game.addPoints2()
    return(gameplay(start_game))
  
if __name__ == "__main__":
    app.run(debug=True)
    
