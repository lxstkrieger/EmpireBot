from typing import List
import discord
from discord.ext import commands
from discord.commands import slash_command
import ezcord

# Define TicTacToeButton as a subclass of discord.ui.Button for TicTacToe
class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # Callback function for button interactions
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        # Update button style, label, and game state based on current player
        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True

        # Check if there is a winner or a tie
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            # Disable all buttons and stop the game
            for child in view.children:
                child.disabled = True
            view.stop()

        # Edit the original message with updated content and view
        await interaction.response.edit_message(content=content, view=view)


# Define TicTacToe as a subclass of discord.ui.View for managing the game view
class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Add TicTacToeButton instances as items to the view
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # Check the board for a winner or a tie
    def check_board_winner(self):
        # Check horizontal and vertical lines
        for line in range(3):
            row_sum = sum(self.board[line])
            col_sum = sum(self.board[0][line] + self.board[1][line] + self.board[2][line])
            if row_sum == 3 or col_sum == 3:
                return self.O
            elif row_sum == -3 or col_sum == -3:
                return self.X

        # Check diagonals
        diag1_sum = sum(self.board[0][2] + self.board[1][1] + self.board[2][0])
        diag2_sum = sum(self.board[0][0] + self.board[1][1] + self.board[2][2])
        if diag1_sum == 3 or diag2_sum == 3:
            return self.O
        elif diag1_sum == -3 or diag2_sum == -3:
            return self.X

        # Check for a tie
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


# Define TIKTAKTOE as a Discord cog for the Tic Tac Toe game
class TIKTAKTOE(ezcord.Cog):
    # Slash command to initiate the Tic Tac Toe game
    @slash_command()
    async def tic(self, ctx: commands.Context):
        # Send a message to start the Tic Tac Toe game
        await ctx.send("Tic Tac Toe: X goes first", view=TicTacToe(), reference=ctx.message)


# Function to set up the Tic Tac Toe cog when the bot is started
def setup(bot: discord.Bot):
    bot.add_cog(TIKTAKTOE(bot))
