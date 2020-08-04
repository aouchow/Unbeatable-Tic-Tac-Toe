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

def copy_board(board):
    board_copy = [" " for x in range(10)]
    for x in range (len(board)):
        board_copy[x] = board[x]
    return board_copy

def check_status(board): #returns winner and if the game is finished
    #check horizontals
    if board[1] == board[2] and board[2] == board[3] and board[1] != " ":
        return board[1], True
    elif board[4] == board[5] and board[5] == board[6] and board[4] != " ":
        return board[4], True
    elif board[7] == board[8] and board[8] == board[9] and board[7] != " ":
        return board[7], True

    #check verticals
    elif board[1] == board[4] and board[4] == board[7] and board[1] != " ":
        return board[1], True
    elif board[2] == board[5] and board[5] == board[8] and board[2] != " ":
        return board[2], True
    elif board[3] == board[6] and board[6] == board[9] and board[3] != " ":
        return board[3], True

    #check diagonals
    elif board[1] == board[5] and board[5] == board[9] and board[1] != " ":
        return board[1], True
    elif board[3] == board[5] and board[5] == board[7] and board[3] != " ":
        return board[3], True
    else:
        for x in range (1, 10):
            if board[x] == " ":
                return None, False #game is not finished
        return None, True #tie and no winner found

def insert_letter (board, letter, position):
    board[position] = letter
    return board

def is_space_free(board, position):
    if board[position] != " ":
        return False
    else:
        return True

def get_possible_moves(board):
    possible_moves = []
    for x in range (1, 10):
        if board[x] == " ":
            possible_moves.append(x)
    return possible_moves

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
#    print("Computer placed '" + comp_letter + "' in position ", index)
    insert_letter(board, comp_letter, index)

# computer plays reactively. If there is an opportunity to win,
# computer will place letter in that spot. If there is an
# opportunity for player to win, computer will block player.
# else, the computer chooses a move randomly.
def comp_move_to_win(board, comp_letter, player_letter):
    #comp looks to win
    for index in range (1, 10):
        if not is_space_free(board, index):
            continue
        else:
            insert_letter(board, comp_letter, index)
            winner, finished = check_status(board)
            if finished:
#                print("Computer placed '" + comp_letter + "' in position ", index)
                return
            else:
                board[index] = " "
    #comp looks to block player from winning
    for index in range (1, 10):
        if not is_space_free (board, index):
            continue
        else:
            insert_letter(board, player_letter, index)
            winner, finished = check_status(board)
            if finished:
                insert_letter(board, comp_letter, index)
#                print("Computer placed '" + comp_letter + "' in position ", index)
                return
            else:
                board[index] = " "
    comp_move_random(board, comp_letter)

def comp_move_unbeatable(board, comp_letter, player_letter):
    possible_moves = get_possible_moves(board)
    best_move = None
    if comp_letter == "X":
        best_score = -float('inf')
        for move in possible_moves:
            insert_letter(board, comp_letter, move)
            score = minimax(board, player_letter)
#            print("score =", score)
            if score > best_score:
                best_score = score
                best_move = move
            board[move] = " "
    else:
        best_score = float('inf')
        for move in possible_moves:
            insert_letter(board, comp_letter, move)
            score = minimax(board, player_letter)
            if score < best_score:
                best_score = score
                best_move = move
            board[move] = " "
    insert_letter(board, comp_letter, best_move)


def minimax(board, letter):
    winner, finished = check_status(board)
    if finished:
        if winner is None:
            return 0
        elif winner == "X":
            return 1
        else:
            return -1
    scores = []
    possible_moves = get_possible_moves(board)
    for move in possible_moves:
        insert_letter(board, letter, move)
#        print_board(board)
        scores.append(minimax(board, "X")) if letter == "O" else scores.append(minimax(board, "O"))
#        print("scores: ", scores)
        board[move] = " "
        if letter == "X" and max(scores) == 1 or letter == "O" and min(scores) == -1:
            break
    return max(scores) if letter == "X" else min(scores)


def player_move(board, player_letter):
    while True:
        try:
            index = input("Please select a position to place '" + player_letter \
            + "' (1-9): ")
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

def play_sim_game(number_of_trials):
    #count unbeatable AI score vs "human" AI score
    unbeatable_score = 0
    beatable_score = 0
    num_of_ties = 0

    n = 0
    while n < number_of_trials:
        board = [" " for x in range(10)]
        comp_first = is_comp_first()
        if comp_first:
            comp_letter = "X"
            player_letter = "O"
        else:
            comp_letter = "O"
            player_letter = "X"
        number_of_moves = 0
        while number_of_moves < 9:
            if comp_first:
                comp_move_unbeatable(board, comp_letter, player_letter)
                number_of_moves += 1
                winner, finished = check_status(board)
                if finished:
                    if winner == comp_letter:
                        unbeatable_score += 1
                    else:
                        beatable_score += 1
                    break;
                comp_first = False
            else:
                comp_move_to_win(board, comp_letter, player_letter)
                number_of_moves += 1
                winner, finished = check_status(board)
                if finished:
                    if winner == comp_letter:
                        unbeatable_score += 1
                    else:
                        beatable_score += 1
                    break;
                comp_first = True
        if (number_of_moves == 9):
            num_of_ties += 1
        n += 1
    print("unbeatable AI score: ", unbeatable_score)
    print("beatable AI score: ", beatable_score)
    print ("number of ties: ", num_of_ties)


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
            comp_move_unbeatable(board, comp_letter, player_letter)
            comp_first = False
        else:
            player_move(board, player_letter)
            comp_first = True
        print_board(board)
        number_of_moves += 1
        winner, finished = check_status(board)
        if finished:
            if winner == None and number_of_moves == 9:
                print("It is a tie!")
            else:
                print(winner + " wins!")
            break

##driver code
while True:
    play_game()
    play_again = raw_input("Do you want to play again? (Y/N): ")
    play_again = str (play_again)
    play_again = play_again.lower()
    if play_again == "n":
        break

#sim game driver code
#play_sim_game(100)
