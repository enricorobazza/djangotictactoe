# Django Tic Tac Toe

This project utilizes Django, Redis, Django Channels and React to build a real-time Tic Tac Toe with multiple rooms.

## How it`s done:
1. Basically it utilizes two channels with multiple groups:
- UserSocket: a group is created for each user with a uniqueID, this group is used for direct communication with a user.
- RoomSocket: a group is created for each game room for updating the game status.

2. All the game logic is verifyied on the back-end, which only returns the final game state:
- Game Matrix
- Players Turn
- Is Game Over?
- Who won?
- Is it a tie?

3. The game state is then inserted to React state, which renders the component

## Preview:
<img src="./readme/preview.gif" alt="RGB Goals Preview - Insert Goal" width="49%"/>


