from random import randint



def print_board(board):
    print("   |   |   ")
    print(" " + board[1] + " | " + board[2] + " | " + board[3])
    print(12*"-")
    print("   |   |   ")
    print(" " + board[4] + " | " + board[5] + " | " + board[6])
    print(12*"-")
    print("   |   |   ")
    print(" " + board[7] + " | " + board[8] + " | " + board[9])

def is_Winner(board, letter): #returns true if letter won
    if board[1] == letter and board[2] == letter and board[3] == letter:
        return True
    elif board[4] == letter and board[5] == letter and board[6] == letter:
        return True
    elif board[7] == letter and board[8] == letter and board[9] == letter:
        return True
    elif board[1] == letter and board[4] == letter and board[7] == letter:
        return True
    elif board[2] == letter and board[5] == letter and board[8] == letter:
        return True
    elif board[3] == letter and board[6] == letter and board[9] == letter:
        return True
    elif board[1] == letter and board[5] == letter and board[9] == letter:
        return True
    elif board[3] == letter and board[5] == letter and board[7] == letter:
        return True
    else:
        return False

def insert_letter (board, letter, position):
    board[position] = letter
    return board

def is_space_free(board, position):
    if board[position] != " ":
        return False
    else:
        return True
def is_comp_first():
    num = randint(0, 1)
    if num == 0:
        return True
    else:
        return False

def comp_move_random(board, comp_letter):
    index = randint(1, 9)
    free = is_space_free(board, index)
    while not free:
        index = randint(1, 9)
        free = is_space_free(board, index)
    print("Computer placed '" + comp_letter + "' in position ", index)
    insert_letter(board, comp_letter, index)
    print_board(board)

def player_move(board, player_letter):
    while True:
        try:
            index = input("Please select a position to place '" + player_letter + \
            "' (1-9): ")
            if index not in [1,2,3,4,5,6,7,8,9]:
                print("Not a valid move.")
            else:
                free = is_space_free(board, index)
                if free == True:
                    break
                else:
                    print("Space is already occupied.")
        except:
            print("Please type a number.")
    insert_letter(board, player_letter, index)
    print_board(board)

def play_game():
    board = [" " for x in range(10)]
    board_instructions = ["0","1","2","3","4","5","6","7","8","9"]
    print("Welcome to Tic Tac Toe. To win complete a straight line of your \
    letter (Diagonal, Horizontal, or Vertical). The board has positions 1-9 \
    starting at the top left.")
    print_board(board_instructions)
    comp_first = is_comp_first()
    if comp_first:
        print("Computer goes first. Computer is X. Player is O")
        comp_letter = "X"
        player_letter = "O"
    else:
        print("Player goes first. Player is 'X'. Computer is 'O'")
        comp_letter = "O"
        player_letter = "X"
    number_of_moves = 0
    while number_of_moves < 9:
        if comp_first:
            comp_move_random(board, comp_letter)
            number_of_moves += 1
            if is_Winner(board, comp_letter):
                print(comp_letter + " wins!")
                break;
            comp_first = False
        else:
            player_move(board, player_letter)
            number_of_moves += 1
            if is_Winner(board, player_letter):
                print(player_letter + " wins!")
                break;
            comp_first = True
        print (number_of_moves)
    if (number_of_moves == 9):
        print("It is a tie!")

#driver code
while True:
    play_game()
    play_again = raw_input("Do you want to play again? (Y/N): ")
    play_again = str (play_again)
    play_again = play_again.lower()
    if play_again == "n":
        break
