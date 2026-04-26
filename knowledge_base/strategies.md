## Binary Search Strategy
Binary search is the optimal strategy for a number guessing game. Always guess the midpoint of the remaining range. For a range of 1-100, start with 50. If told to go higher, the new range is 51-100 so guess 75. If told to go lower, the new range is 1-49 so guess 25. Binary search guarantees finding the answer in at most 7 guesses for a range of 1-100.

## Random Guessing Strategy
Random guessing picks any number without using the hints. It is very inefficient. On average, random guessing takes about 50 guesses for a range of 1-100. It does not use the information from previous hints.

## Sequential / Linear Strategy
Sequential guessing means guessing 1, 2, 3, 4... in order. This is the worst strategy. On average it takes 50 guesses and in the worst case takes 100 guesses for a range of 1-100.

## Narrowing Strategy
Narrowing means adjusting your guess based on hints but not always picking the exact midpoint. For example, if you guessed 30 and were told to go higher, you might guess 60 next instead of the true midpoint. Narrowing is better than random but worse than binary search.

## Optimal Number of Guesses
For a range of 1 to N, binary search finds the answer in at most log2(N) + 1 guesses. For 1-20 (Easy): 5 guesses. For 1-100 (Normal): 7 guesses. For 1-50 (Hard): 6 guesses. If you are using more guesses than this, you are not using binary search.
