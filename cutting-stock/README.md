# Cutting stock problem

TODO: introduction

raw length of 100

| Final length | Demand |
|--------------|--------|
| 14           | 211    |
| 31           | 395    |
| 36           | 610    |
| 45           | 97     |

There are multiple ways to cut the raw material. One such way is by cutting it into seven finals of length 14, resulting in a waste of 2. Another way is to cut it into two finals of length 14 and two finals of length 36 resulting in a waste of 0. Each of these patterns are generated through the given method `patterns`.

Exercises:
 1. What is the minimum number of raws that are required to be able to fulfill the order? How should those raws be cut? Write an ILP program using `scipy.optimize`. Hint: how much raws are cut according to each pattern?
 2. Rather than minimizing the number of used raws, how do we minimize the produced waste while still fulfilling the order? How should the raws be cut? Alter your previous program to account for this.
 3. While minimizing waste, we favoured overproducing finals over creating waste. However, in reality, overproduced finals of length 14 are considered waste as well. Alter your previous program to account for this.

See also:
 - [Cutting stock problem](https://en.wikipedia.org/wiki/Cutting_stock_problem)
 - [Bin packing problem](https://en.wikipedia.org/wiki/Bin_packing_problem)