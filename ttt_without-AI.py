from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.button import Button
from kivy.properties import StringProperty, BooleanProperty
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
import datetime
import random
import kivy.utils

class TTT(GridLayout):

    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)
    randomlist = []
    dialog = None
    timer_on = True

    X = "X"
    O = "O"
    EMPTY = None
    moves_counter = 0
    state = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
    success_sets = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                    [0, 3, 6], [1, 4, 7], [2, 5, 8],
                    [0, 4, 8], [2, 4, 6]]
    player_move = []
    player_X_move = []
    player_O_move = []

    def __init__(self, **kwargs):
        super(TTT, self).__init__(**kwargs)
        self.sound = SoundLoader.load('bell.wav')
        self.initial_grid()
        Clock.schedule_once(self.init_ui, 0)

    # load  the number grid with a delay
    def init_ui(self, dt=0):
        self.number_grid()

    # populate an empty grid before starting the game or on Reset
    def initial_grid(self):
        self.minutes = '00'
        self.seconds = '00.00'
        for i in range(9):
            self.randomlist.append(' ')

    # populate the empty grid
    def number_grid(self):
        number_grid = self.ids['number_grid']
        # create a Button object
        for i in range(9):
            # store the grid_button object in a list
            grid_button = Button(id=str(i), text=str(self.randomlist[i]),
                                 color=kivy.utils.get_color_from_hex("#f2ec44"), font_size='30sp',
                                 markup=True, on_release=self.click)
            # on_release button action, click function will pass the grid_button object as an instance
            number_grid.add_widget(grid_button)
            # Note: kivy widgets added through the python code are Object and can be accessed as grid_button.id


    # player action
    def click(self, instance):
        # start the timer
        if self.timer_on:
            self.start_timer()

        # chose the player who's turn on the board
        player = self.player_turn()

        # perform action
        if player == 'X':
            self.ids['label_instruction'].text = "O's Turn"
        else:
            self.ids['label_instruction'].text = "X's Turn"

        # check if the player has clicked an empty cell. if yes: error, else: update
        if (instance.text != ' ') or (instance.id in self.player_move):
            print("Invalid input, enter an empty position")
        else:
            instance.text = player
            if player == 'X':
                self.player_X_move.append(int(instance.id))
                #print(f"player_X_moves {self.moves_counter}: {self.player_X_move}")
            elif player == 'O':
                self.player_O_move.append(int(instance.id))
                #print(f"player_O_moves {self.moves_counter}: {self.player_O_move}")
            self.player_move.append(int(instance.id))
            self.state[int(instance.id)] = player
            self.moves_counter += 1
            self.result(player)


    # function to be called on click of Reset button
    def reset_timer(self, *kwargs):
        EMPTY = None
        self.ids['number_grid'].clear_widgets()
        self.randomlist.clear()
        self.player_move.clear()
        self.player_X_move.clear()
        self.player_O_move.clear()
        self.initial_grid()
        self.number_grid()
        self.ids['label_instruction'].text = "X's Turn"
        # turn on the timer
        self.timer_on = True
        # reset the moves counter
        self.moves_counter = 0
        # reset the state
        self.state = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        if self.running:
            self.running = False
            Clock.unschedule(self.update_timer)

    # function to be called on click of the first button
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

    def update_timer(self, *kwargs):
        # start the timer
        delta = datetime.datetime.now() - self.delta
        self.minutes = str(delta).split(":")[1:][0]
        self.seconds = str(delta).split(":")[1:][1][:5]

    # return the player with the next turn on the board
    def player_turn(self):
        if self.moves_counter % 2 == 0:
            player = self.X
        else:
            player = self.O
        return player

    # check the result
    def result(self, player):
        count = 0
        win_text = "Congratulations Player " + player + ", You Won!"
        draw_text = "It's a DRAW!"
        if (self.moves_counter > 4) and (self.moves_counter < 10):
            for i in self.success_sets:
                pattern_x = 0
                pattern_o = 0
                #print(f"success_sets in count {count}: {i}")
                for j in i:
                    if player == 'X':
                        if j in self.player_X_move:
                            pattern_x += 1
                            #print(f"match found, counter: {pattern_x}, player_moves: {self.player_X_move}")
                            if pattern_x == 3:
                                #print(f"{player} is the winner in {self.moves_counter} moves")
                                #print(win_text)
                                score = -1
                                print(f"score: {score}")
                                self.game_over(win_text)
                                return player
                    if player == 'O':
                        if j in self.player_O_move:
                            pattern_o += 1
                            #print(f"match found, counter: {pattern_o}, player_moves: {self.player_O_move}")
                            if pattern_o == 3:
                                #print(f"{player} is the winner in {self.moves_counter} moves")
                                #print(win_text)
                                score = +1
                                print(f"score: {score}")
                                self.game_over(win_text)
                                return player

                count += 1
            if self.moves_counter == 9:
                self.ids['label_instruction'].text = "It's a DRAW"
                score = 0
                print(f"score: {score}")
                self.game_over(draw_text)
                self.reset_timer()



    # game over pop-up (dialog)
    def game_over(self, disp_text):
        print(disp_text)
        if self.running:
            self.running = False
            Clock.unschedule(self.update_timer)
        # game over dialog
        if not self.dialog:
            self.dialog = MDDialog(
                title="Game Over",
                size_hint=(.8, .5),
                text=disp_text
            )
        self.dialog.open()
        self.reset_timer()

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Lime"  # "Purple", "Red"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file("main.kv")

if __name__ == '__main__':
    MainApp().run()
