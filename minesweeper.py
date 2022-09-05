import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=16, width=16, mines=20):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if(len(self.cells) == self.count):
            return self.cells

        return set()
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0):
            return self.cells

        return set()
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell not in self.cells:
            return
        updated = set()

        for acell in self.cells:
            if acell == cell:
                continue
            updated.add(acell)

        self.cells = updated
        if len(updated) == 0:
            self.count = 0
        else:
            self.count -= 1

        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell not in self.cells:
            return

        updated = set()

        for acell in self.cells:
            if acell == cell:
                continue
            updated.add(acell)

        self.cells = updated
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        print(cell,"---- moved made & count is", count,)
        #1
        self.moves_made.add(cell)

        #2
        self.mark_safe(cell)

        #3
        new_sentence = set()
        i,j = cell
        options = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]

        for option in options:
            if((option[0]<0 or option[0]>= self.height) or (option[1]<0 or option[1]>= self.width)):
                continue
            else:
                if(option in self.mines):
                    count -= 1
                elif(option in self.safes):
                    continue
                else:
                    new_sentence.add(option)
        if(len(new_sentence) != 0):

            sentence_update = Sentence(new_sentence, count)
            print("sentence being added:", sentence_update)
            self.knowledge.append(sentence_update)

        #4


        # for sentence in self.knowledge:
        #     #print("-----")
        #     if(sentence.known_mines()):
        #         print("known mines coming from - ", sentence)
        #         for i in set(sentence.known_mines()):
        #             k_mines.add(i)
        #
        #     if(sentence.known_safes()):
        #         print("known safes coming from - ", sentence)
        #         for i in set(sentence.known_safes()):
        #             k_safes.add(i)
        #
        #
        # if(k_mines):
        #     print("known mines - 2nd phase: ", k_mines)
        #     for mine in k_mines:
        #         self.mark_mine(mine)
        # if(k_safes):
        #     print("known safes - 2nd phase: ", k_safes)
        #     for safe in k_safes:
        #         self.mark_safe(safe)

        for sentence in self.knowledge:
            safes = sentence.known_safes()
            mines = sentence.known_mines()

            for cell in sentence.cells:
                if cell in safes:
                    self.mark_safe(cell)
                if cell in mines:
                    self.mark_mine(cell)


        # print("known mines and safes added")
        #5
        new_knowledge = list()
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if(sentence1 == sentence2):
                    continue
                if len(sentence1.cells) == 0 or len(sentence2.cells) == 0:
                    continue
                if sentence1.count == 0 or sentence2.count == 0:
                    continue
                if sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_cells, new_count)
                    #print(new_sentence, "- new sentence added")
                    if(new_sentence not in new_knowledge):
                        new_knowledge.append(new_sentence)
                        self.knowledge.remove(sentence2)


        for sentence in new_knowledge:
            print("Inferred statement:", sentence)
            self.knowledge.append(sentence)

        print("known mines: ", sorted(self.mines))
        #sprint("known safes: ", sorted(self.safes))
        print("available moves", sorted(self.safes - self.moves_made))
        return





    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    return (i, j)

        return None
