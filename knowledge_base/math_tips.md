## Logarithms and Guessing
The minimum number of guesses needed to guarantee finding a number is log base 2 of the range size. log2(100) is approximately 6.64, which rounds up to 7. This means 7 guesses is always enough for a 1-100 range if you use binary search.

## Expected Guesses for Random Strategy
If you guess randomly without strategy, the expected number of guesses is (range size + 1) divided by 2. For a range of 1-100 that is about 50.5 guesses on average. Binary search reduces this to at most 7 guesses.

## Probability of Guessing Correctly
On your first guess with no information, you have a 1 in N chance of being correct where N is the range size. For 1-100 that is a 1% chance. After one binary search guess you narrow the range to 50 numbers, giving a 2% chance on the next guess if it was wrong.

## Why Midpoint Works Best
Guessing the midpoint splits the remaining possibilities into two equal halves. This means no matter what the answer is, you always eliminate at least half the remaining options. Any other guess eliminates fewer possibilities in the worst case.

## Information Theory
Each hint (higher or lower) gives you one bit of information. With 7 bits you can distinguish 128 different values, which covers any range up to 128. This is why 7 guesses covers 1-100 perfectly using binary search.
