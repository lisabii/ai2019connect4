from connectfour.agents.computer_player import RandomAgent
import random


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            # if the next move is winnable, go for it
            if next_state.winner() == self.id:
                return move
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1))

        bestMove = moves[vals.index(max(vals))]
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        if self.id == 1:
            opponent_id = 2
        else:
            opponent_id = 1

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append(move)
            winner = next_state.winner()
            if winner == opponent_id:
                vals.append(-1)
            elif winner == self.id:
                vals.append(10000)
            else:
                vals.append(self.dfMiniMax(next_state, depth + 1))

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        if depth == 1:
            print(self.id, "depth1 ", bestVal)
        return bestVal

    def evaluateBoardState(self, board):
        """
        Your evaluation function should look at the current state and return a score for it.
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        if self.id == 1:
            opponent_id = 2
        else:
            opponent_id = 1

        winner = board.winner()
        if winner == self.id:
            return 1000
        elif winner == opponent_id:
            return -1
        size_y = board.height
        size_x = board.width
        map_ = []
        num_to_connect = board.num_to_connect
        total_points = 0

        # basically this function is calculating all the possible win positions
        # more pieces in a possible win position will be counted with more weights
        # a win position with X pieces in it will be counted as X^2 points
        # initialise the zones maps
        for i in range(size_y):
            map_.append([])
            for j in range(size_x):
                map_[i].append([])

        # Fill in the horizontal win positions
        for i in range(size_y):
            for j in range(size_x - num_to_connect + 1):
                points = 0
                for k in range(num_to_connect):
                    if board.board[i][j + k] == opponent_id:
                        points = 0
                        break
                    elif board.board[i][j + k] == self.id:
                        points += len(board.winning_zones[j+k][i])
                if points == 3:
                    if j - 1 >= 0 and board.board[i][j + 3] == 0 and board.board[i][j - 1] == 0 \
                            and board.try_move(j + 3) == i and board.try_move(j - 1) == i:
                        return 10000
                    elif j + 4 < size_y and board.board[i][j + 4] == 0 and board.board[i][j] == 0 \
                            and board.try_move(j + 4) == i and board.try_move(j) == i:
                        return 10000
                    else:
                        for k in range(num_to_connect):
                            if board.board[i][j + k] == 0 and board.try_move(j + k) == i:
                                points = 500
                total_points += points

        # Fill in the vertical win positions
        for i in range(size_x):
            for j in range(size_y - num_to_connect + 1):
                points = 0
                for k in range(num_to_connect):
                    if board.board[j + k][i] == opponent_id:
                        points =0
                        break
                    elif board.board[j + k][i] == self.id:
                        points += len(board.winning_zones[i][j+k])
                total_points += points

        # Fill in the forward diagonal win positions
        for i in range(size_y - num_to_connect + 1):
            for j in range(size_x - num_to_connect + 1):
                points = 0
                for k in range(num_to_connect):
                    if board.board[i + k][j + k] == opponent_id:
                        points = 0
                        break
                    elif board.board[i + k][j + k] == self.id:
                        points += len(board.winning_zones[j+k][i+k])
                if points == 3:
                    if i - 1 >= 0 and j - 1 >= 0 and board.board[i + 3][j + 3] == 0 and board.board[i - 1][j - 1] == 0 \
                            and board.try_move(j + 3) == i + 3 and board.try_move(j - 1) == i - 1:
                        return 10000
                    elif i + 4 < size_y and j + 4 < size_x and board.board[i + 4][j + 4] == 0 and board.board[i][j] == 0 \
                            and board.try_move(j + 4) == i + 4 and board.try_move(j) == i:
                        return 10000
                    else:
                        for k in range(num_to_connect):
                            if board.board[i + k][j + k] == 0 and board.try_move(j + k) == i + k:
                                points = 500
                total_points += points

        # Fill in the backward diagonal win positions
        for i in range(size_y - num_to_connect + 1):
            for j in range(size_x - 1, num_to_connect - 1 - 1, -1):
                points = 0
                for k in range(num_to_connect):
                    if board.board[i + k][j - k] == opponent_id:
                        points = 0
                        break
                    elif board.board[i + k][j - k] == self.id:
                        points += len(board.winning_zones[j-k][i+k])
                if points == 3:
                    if board.board[i + 3][j - 3] == 0 and board.board[i - 1][j + 1] == 0 \
                            and board.try_move(j - 3) == i + 3 and board.try_move(j + 1) == i - 1:
                        return 10000
                    elif i + 4 < size_y and j - 4 >= 0 and board.board[i + 4][j - 4] == 0 and board.board[i][j] == 0 \
                            and board.try_move(j - 4) == i + 4 and board.try_move(j) == i:
                        return 10000
                    else:
                        for k in range(num_to_connect):
                            if board.board[i + k][j - k] == 0 and board.try_move(j - k) == i + k:
                                points = 500
                total_points += points
        return total_points
