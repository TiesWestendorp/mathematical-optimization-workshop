# mathematical-optimization-workshop
Hands-on workshop for mathematical optimization

## Prerequisites

- Python >= 3.9 is required
- `scipy`: `pip install scipy`

## Introduction

During this workshop

## Optimization problem

$\text{minimize}_x\hspace{0.5em} f(x) \text{ subject to } g(x) \leq 0$

## Linear programming

If the function $f$ is linear, and all $g$ are affine (linear plus a constant), we obtain a special case of the general optimization problem, known as the [linear optimization problem](https://en.wikipedia.org/wiki/Linear_programming) (also called the linear programming problem):

$$\text{minimize}\hspace{0.5em} \mathbf{c}^T \mathbf{x}  \text{ subject to } A\mathbf{x} \leq \mathbf{b} \text{ and } \mathbf{x} \geq 0,$$

where $\mathbf{c}$, $\mathbf{x}$ and $\mathbf{b}$ are vectors, and $A$ is a matrix (see the next section for an example).

When formulated in the above manner, we say that a linear optimization problem is in _standard form_ (which is the form most solvers expect). Linear programming problems can be solved _exactly_ in polynomial time (meaning we can efficiently find the global optimal solution).

If some of the decision variables in $x$ are additionally restricted to the integers, we call the problem the [integer programming problem](https://en.wikipedia.org/wiki/Integer_programming). In this case can still find the optimal solution, but we currently have no known algorithms that run in polynomial time (in fact, if we would have such an algorithm, we would have solved the famous [P versus NP problem](https://en.wikipedia.org/wiki/P_versus_NP_problem), since the integer programming problem is [NP-complete](https://en.wikipedia.org/wiki/NP-completeness)).

## Example: profit maximization

Consider a factory which is faced with choosing how much of two different products should be manufactured. One unit of the first product provides a profit of 10 euros, and one unit of the second provides 5 euros profit. Producing the parts for these products cost 10 minutes and 8 minutes respectively, and assembling the parts cost 10 and 2 minutes respectively. Assume that we are given 120 minutes of production time, and 60 minutes of assembly time. How much of either product should we manufacture to maximize profit?

This can be found by solving the following optimization problem:

$$\begin{matrix}
\text{maximize} & 10x_1 + 5x_2\\\
\text{subject to} & 10x_1 + 8x_2 \leq 120,\\\
& 10x_1 + 2x_2 \leq 60,\\\
& x_1 \geq 0, x_2 \geq 0.
\end{matrix}$$

We can bring this to standard form by first negating the objective function:

$$\begin{matrix}
\text{minimize} & -10x - 5y\\\
\text{subject to} & 10x + 8y \leq 120,\\\
& 10x + 2y \leq 60,\\\
& x \geq 0, y \geq 0.
\end{matrix}$$

And next figuring out $A$, $b$ and $c$: 

$$\begin{matrix}
\text{minimize} & \left(\begin{matrix}-10 & -5\end{matrix}\right)\left(\begin{matrix}x \\\ y\end{matrix}\right)\hspace{3.9em}\\\
\text{subject to} & \left(\begin{matrix}10 & 8 \\\ 10 & 2\end{matrix}\right)\left(\begin{matrix}x \\\ y\end{matrix}\right) \leq \left(\begin{matrix}120 \\\ 60\end{matrix}\right)\\\
& x \geq 0, y \geq 0.
\end{matrix}$$

And finally solving this through [`scipy.optimize.linprog`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html):

```python
from scipy.optimize import linprog

A = [[10, 8], [10, 2]]
b = [120, 60]
c = [-10, -5]
x,y = linprog(c, A_ub = A, b_ub = b).x # bounds = (0, None) is the default
print(x, y) # Prints 4.0, 10.0
```

In this case, we happen to obtain an integer solution, which is great, because we probably can't create half of a product, and expect to get half of its profit!

In general though, the answer need not be restricted to the integers. For example if the amount of available production minutes gets reduced to 100, such that `b = [100, 60]`, the optimal solution becomes $x = \tfrac{14}{3}\approx 4.667, y = \tfrac{20}{3} \approx 6.667$. If we want to find the best _integer_ solution, we additionally need to impose the integrality constraints: $x,y\in\mathbb{Z}$ (specified through the `integrality` parameter in `linprog`).

- What is the best integer solution when $b = [100, 60]$?
- What do you notice when comparing it with the best non-integer solution?