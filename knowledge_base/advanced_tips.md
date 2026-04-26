## When to Deviate from Binary Search
Binary search is optimal on average but you can adjust it based on difficulty. On Easy mode (1-20, 6 attempts) start at 10. On Hard mode (1-50, 5 attempts) start at 25. Never start at the extremes — starting at 1 or 100 wastes your first guess entirely.

## Reading the Scoring System Strategically
The scoring system penalizes too-low guesses (-5 points) more consistently than too-high guesses (which gain +5 on even attempts). If you care about score rather than winning, slightly bias your guesses higher on even attempts. However for pure win probability, ignore the scoring and use binary search.

## What to Do with One Attempt Left
If you have one attempt left and the range is still wide, calculate the midpoint. Do not guess randomly — the midpoint maximizes your chance of being within one number of the secret even if you miss, which is psychologically important even if it does not affect the outcome mathematically.

## How the AI Coach Uses Your History
The AI Coach reads your full guess history and the outcome of each guess (Too High, Too Low) to calculate the remaining valid range. It then applies binary search to that range. If you ignored the coach's previous suggestion and guessed something else, the coach adapts — it updates the valid range based on whatever you actually guessed, not what it recommended.

## Common Beginner Mistakes
Guessing near where you just guessed is the most common mistake. If 70 was Too High and you guess 65 next, you eliminated only 5 numbers out of 70 remaining. A proper binary search from 70 Too High would guess around 35, eliminating 35 numbers at once. Always think in halves, not small steps.
