import discord
class connect4(object):
    def __init__(self, red):
        self.red = red
        self.yellow = None
        self.redPlaying = True
        self.board = [7*['⚪'] for i in range(6)]
        self.columnDepth = [5]*7
        
    def set_yellow(self, yellow):
        self.yellow = yellow

    
    def gameStart(self):
        embed = discord.Embed(title = "Connect 4", color = 0XFF4040, description=str(self.red))

        embed.add_field(name="Starting Game", value=f"{self.red} just started a connect 4 game. React with 🎮 to join !" )

        embed.set_footer(text="Waiting for player")
        return embed

    def showBoard(self):
        board = ""
        for row in self.board:
            for column in row:
                board += column +" "
            board += "\n"
        return board

    def addToken_from_reaction(self, emoji):
        reactions = {
            '1️⃣' : 0, 
            '2️⃣' : 1, 
            '3️⃣' : 2, 
            '4️⃣' : 3, 
            '5️⃣' : 4, 
            '6️⃣' : 5, 
            '7️⃣' : 6
        }
        
        return self.addToken(reactions[emoji])

    def addToken(self, column):
        if self.redPlaying:
            self.board[self.columnDepth[column]][column] = '🔴'
        else:
            self.board[self.columnDepth[column]][column] = '🟡'

        self.columnDepth[column] -= 1
        self.redPlaying = not self.redPlaying
        return [self.columnDepth[column] == -1, self.showBoard()]

    def new_player(self, payload, message, gamesDict, client, embed):
        gamesDict[str(payload.member)] = gamesDict[embed.description]
        gamesDict[str(payload.member)].set_yellow(str(payload.member))
        
        newEmbed = discord.Embed(title="Connect 4", description=f"{self.red} vs {self.yellow}")

        newEmbed.add_field(name="Game", value=self.showBoard())

        newEmbed.set_footer(text="Playing...")

        return newEmbed
  

    def reactionEdit(self, payload, message, gamesDict, client):

        connectReaction = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
        columnFull = False

        if len(message.embeds[0]) == 0:
            return
        embed = message.embeds[0]

        if payload.emoji.name == '🎮' and not str(payload.member) == embed.description:
            newEmbed =  self.new_player(payload, message, gamesDict, client, embed)

            
            
        elif payload.emoji.name in connectReaction:
            columnFull, gameDisplay = gamesDict[str(payload.member)].addToken_from_reaction(payload.emoji.name)

            
            newEmbed = discord.Embed(title="Connect 4", description=f"{self.red} vs {self.yellow}")
            newEmbed.add_field(name="Game", value=gameDisplay)
        return [newEmbed, columnFull]