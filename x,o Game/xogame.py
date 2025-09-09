class Player:
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid name. Please use letters only.")

    def choose_symbol(self, taken_symbols):
        while True:
            symbol = input("Enter your symbol (1 letter only): ")
            if symbol.isalpha() and len(symbol) == 1:
                symbol = symbol.upper()
                if symbol not in taken_symbols:
                    self.symbol = symbol
                    break
                else:
                    print("That symbol is already taken. Choose another one.")
            else:
                print("Invalid symbol. Please enter a single letter.")


class Menu:
    def display_main_menu(self):
        print("\nWelcome to X and O game")
        print("1. Start the game")
        print("2. End the game")
        choice = input("Choose 1 or 2: ")
        return choice

    def display_endgame_menu(self):
        print("\nGame is over")
        print("1. Restart the game")
        print("2. End the game")
        choice = input("Choose 1 or 2: ")
        return choice


class Board:
    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i + 3]))
            if i < 6:
                print("-" * 6)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def reset_board(self):
        self.board = [str(i) for i in range(1, 10)]


class Game:
    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1":
            self.setup_players()
            self.play_game()
        else:
            self.end_game()

    def setup_players(self):
        taken_symbols = set()
        for number, player in enumerate(self.players, start=1):
            print(f"\nPlayer {number}, enter your info:")
            player.choose_name()
            player.choose_symbol(taken_symbols)
            taken_symbols.add(player.symbol)

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_win():
                self.board.display_board()
                print(f"\n{self.players[self.current_player_index].name} wins!")
                choice = self.menu.display_endgame_menu()
                if choice == "1":
                    self.restart_game()
                else:
                    self.end_game()
                break
            elif self.check_draw():
                self.board.display_board()
                print("\nIt's a draw!")
                choice = self.menu.display_endgame_menu()
                if choice == "1":
                    self.restart_game()
                else:
                    self.end_game()
                break
            else:
                self.switch_player()

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

    def check_win(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in win_combinations:
            if (self.board.board[combo[0]] ==
                self.board.board[combo[1]] ==
                self.board.board[combo[2]]):
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"\n{player.name}'s turn ({player.symbol})")
        while True:
            try:
                cell_choice = int(input("Choose a cell (1-9): "))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter a number between 1 and 9.")

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def end_game(self):
        print("\nThanks for playing!")


# Run the game
if __name__ == "__main__":
    game = Game()
    game.start_game()
