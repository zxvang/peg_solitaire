# Sprint 0

Due: October 6

## 1. User Stories

| ID  | User Story Name                                    | User Story Description                                                                                                 | Priority | Estimated Effort (Hours) |
| --- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------ |
| 1   | Choose a board size                                | As a player I want options as to how big the board will be displayed                                                   | A        | 2                        |
| 2   | Choose a board type                                | As a player I want options as to how the pegs are initially set up on the board                                        | A        | 2                        |
| 3   | Start a new game of the chosen board size and type | As a player I want to be able to view a valid board ready for play                                                     | B        | 2                        |
| 4   | Make a move in the game                            | As a player I want to be able to move a peg into a valid spot as I play                                                | B        | 4                        |
| 5   | A game is over                                     | As a player I want a notification of when I lose or win                                                                | B        | 1                        |
| 6   | Restart game and redo a move                       | As a player I want a way to restart the game fully when I win or lose and to also redo a move I did not intend to make | C        | 2                        |

## 2. Acceptance Criteria

| User Story ID and Name                                | AC ID | Description of Acceptance Criterion                                                                                                                                                                                                        | Status (Completed, toDo, inProgress) |
| ----------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------ |
| 1. Choose a board size                                | 1.1   | AC 1.1 start app<br>Given: app launches<br>When: app loads<br>Then: board will show a default peg board with board size and type ready for selection                                                                                       | completed                            |
|                                                       | 1.2   | AC 1.2 select size<br>Given: app launches<br>When: player inputs a board size<br>Then: board will update to match what the player wants to play alongside the board type                                                                   | completed                            |
| 2. Choose a board type                                | 2.1   | AC 2.1 select type<br>Given: the app launches<br>When: player selects the board type<br>Then: board will update to match what the player wants to play alongside the board size                                                            | completed                            |
| 3. Start a new game of the chosen board size and type | 3.1   | AC 3.1 board ready for play<br>Given: a valid board size and type selected<br>When: a player starts the game<br>Then: the board will be ready for inputs and be playable, and show the pegs-left count, move count, and redo control | in progress                          |
| 4. Make a move in the game                            | 4.1   | AC 4.1 valid move<br>Given: an ongoing game<br>When: a player makes a move<br>Then: peg board display an updated board with the move made                                                                                                  | to do                                |
|                                                       | 4.2   | AC 4.2 move tracker<br>Given: an ongoing game<br>When: a player makes a move<br>Then: the "pegs_left" and "moves_made" counter will update                                                                                                 | to do                                |
| 5. A game is over                                     | 5.1   | AC 5.1 lost game<br>Given: an ongoing game<br>When: a player has no more valid moves<br>Then: display a message saying that the game is over, "peg_count," "moves_made," and that they lost if the count of "pegs_left" are greater than 1 | to do                                |
|                                                       | 5.2   | AC 5.2 won game<br>Given: an ongoing game<br>When: a player has no more valid moves<br>Then: display a message saying that the game is over, "peg_count," "moves_made," and that they won if the count of "pegs_left" is exactly 1         | to do                                |
| 6. Restart game and redo a move                       | 6.1   | AC 6.1 restart a game<br>Given: an ended game<br>When: a player has no more valid moves and a win or loss condition is completed<br>Then: provide an option for the player to play another starting game                                   | to do                                |
|                                                       | 6.2   | AC 6.2 redo a move<br>Given: an ongoing game<br>When: a player feels they made a bad move, and click on the redo button<br>Then: the move the player just made with undo, allowing them to make the same or different move                 | to do                                |


## 3. Claude recommended acceptance criteria

Prompt and response

<img width="750" height="591" alt="Screenshot 2026-10-06 at 11 39 22 PM" src="https://github.com/user-attachments/assets/be9d48b1-f7e7-4fea-bafe-d829f96a0adf" />

Specifically chosen AC's that will be utilized instead of using everything Claude recommended.
