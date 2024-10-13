# ⸬ aergere

> [Mensch ärgere Dich nicht](https://en.wikipedia.org/wiki/Mensch_%C3%A4rgere_Dich_nicht) (English: Man, Don't Get Angry) is a German board game (but not a German-style board game), developed by Josef Friedrich Schmidt in 1907/1908. Some 70 million copies have been sold since its introduction in 1914 and it is played in many European countries.

[`Board`](src/aergere/board.py), [`valid_moves`, and `move`](src/aergere/aergere.py) encode the game. [`rye run aergere`](src/aergere/main.py) to run simulation. ~150 loc and tests.

Initially written on a flight back from Rome where I noticed this board game in a hotel lobby. I imagined using this to make some simple procedural art.

<br>
<br>

```text
turn 334 - red rolled 5 and moved peg:2 from 22 to 27
turn 335 - black rolled 2 and moved peg:1 from 1 to 3
turn 336 - yellow rolled 6 and moved peg:2 from None to 0
turn 336 - yellow rolled 3 and moved peg:0 from 38 to H1
turn 337 - green rolled 2 and moved peg:2 from 8 to H0
yellow	 ['H1', 35, 0, 'H3']
green	 ['H2', 'H1', 'H0', 'H3']
red	 ['H3', None, 27, 'H2']
black	 ['H3', 3, None, 'H2']

green wins on turn 337
```
