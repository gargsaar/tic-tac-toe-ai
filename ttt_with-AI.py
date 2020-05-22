from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
import datetime
from math import inf as infinity

"""
Kivy app for Tic-Tac-Toe game powered by Minimax AI Algorithm using Python.
Author: Sarthak Garg
Year: 2020
License: GNU GENERAL PUBLIC LICENSE (GPL)
"""

class TTT(GridLayout):
    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)
    randomlist = []
    dialog = None
    timer_on = True
    HUMAN = -1
    COMP = +1
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    moves = {
        0: [0, 0], 1: [0, 1], 2: [0, 2],
        3: [1, 0], 4: [1, 1], 5: [1, 2],
        6: [2, 0], 7: [2, 1], 8: [2, 2],
    }

    def __init__(self, **kwargs):
        super(TTT, self).__init__(**kwargs)
        self.sound = SoundLoader.load('bell.wav')
        # set the timer variables to zero before starting the game
        self.minutes = '00'
        self.seconds = '00.00'

    # player action on click of a Button in the number grid
    def click(self, btn_id):
        # start the timer
        if self.timer_on:
            self.start_timer()

        # check if the player has clicked an empty cell. if yes: error, else: update
        if self.ids[str(btn_id)].text != '':
            print("Invalid input, enter an empty position")
        else:
            # it's a valid move. change the instruction label
            self.ids['label_instruction'].text = "AI's Turn"
            self.ids[str(btn_id)].text = 'X'
            # set the input in the board
            coord = self.moves[int(btn_id)]
            can_move = self.set_move(coord[0], coord[1], self.HUMAN)
            if not can_move:
                print('Bad move')
            else:
                print(self.board)
            # check is the game over
            depth = len(self.empty_cells(self.board))
            if depth == 0 or self.game_over(self.board):
                score = self.evaluate(self.board)
                return self.result(score)
            else:
                self.ai_turn()

    # It calls the minimax function if the depth < 9
    def ai_turn(self):
        print(f'Computer turn')
        depth = len(self.empty_cells(self.board))
        if depth == 0 or self.game_over(self.board):
            return

        if depth == 9:
            print('Something is wrong')
        else:
            move = self.minimax(self.board, depth, self.COMP)
            x, y = move[0], move[1]
            ai_btn_id = str(list(self.moves.keys())[list(self.moves.values()).index([x, y])])

        self.set_move(x, y, self.COMP)
        #time.sleep(1)
        self.ids['label_instruction'].text = "Player's Turn"
        print(self.ids)
        self.ids[ai_btn_id].text = 'O'
        # check is the game over
        if self.game_over(self.board):
            score = self.evaluate(self.board)
            return self.result(score)


    # AI function that choice the best move.
    # Returns a list with [the best row, best col, best score]
    def minimax(self, state, depth, player):
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over(state):
            score = self.evaluate(state)
            return [-1, -1, score]

        for cell in self.empty_cells(state):
            x, y = cell[0], cell[1]
            state[x][y] = player
            score = self.minimax(state, depth - 1, -player)
            state[x][y] = 0
            score[0], score[1] = x, y
            if player == self.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value
        return best

    # Func for heuristic evaluation of state. Returns score.
    def evaluate(self, state):
        if self.wins(state, self.COMP):
            score = +1
        elif self.wins(state, self.HUMAN):
            score = -1
        else:
            score = 0
        return score

    # This function tests if a specific player wins.
    def wins(self, state, player):
        """
        Win states:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False

    # This function test if the human or computer wins
    def game_over(self, state):
        return self.wins(state, self.HUMAN) or self.wins(state, self.COMP)

    # Each empty cell will be added into cells' list
    def empty_cells(self, state):
        cells = []
        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        return cells

    # A move is valid if the chosen cell is empty
    def valid_move(self, x, y):
        if [x, y] in self.empty_cells(self.board):
            return True
        else:
            return False

    # Set the move on board, if the coordinates are valid
    def set_move(self, x, y, player):
        if self.valid_move(x, y):
            self.board[x][y] = player
            return True
        else:
            return False

    # func for reset timer button
    def reset_timer(self, *kwargs):
        # clear the board
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.ids['label_instruction'].text = "Player's Turn"
        # reset the number_grid
        for i in range(9):
            self.ids[str(i)].text = ''
        # reset the timer variables to zero
        self.minutes = '00'
        self.seconds = '00.00'
        # turn on the timer
        self.timer_on = True
        if self.running:
            self.running = False
            Clock.unschedule(self.update_timer)

    # func for start button
    def start_timer(self):
        # reset the timer to 00:00.00
        self.delta = datetime.datetime.now() - datetime.timedelta(0, 0)
        self.update_timer()
        # play the bell sound
        self.sound.play()
        # turn off the timer
        self.timer_on = False
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update_timer, 0.05)

    # func for updating the timer
    def update_timer(self, *kwargs):
        # start the timer
        delta = datetime.datetime.now() - self.delta
        self.minutes = str(delta).split(":")[1:][0]
        self.seconds = str(delta).split(":")[1:][1][:5]

    # display the result in a pop-up (dialog)
    def result(self, score):
        if score == +1:
            disp_text = "AI Won. Better Luck Next Time!"
        elif score == -1:
            disp_text = "Congratulation, You Won!"
        else:
            disp_text = "It's a DRAW!"
        if self.running:
            self.running = False
            Clock.unschedule(self.update_timer)
        # game over dialog
        if not self.dialog:
            self.dialog = MDDialog(
                title="Game Over",
                size_hint=(.7, .3),
                text=disp_text
            )
        self.dialog.open()
        self.reset_timer()

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("main.kv")

if __name__ == '__main__':
    MainApp().run()
