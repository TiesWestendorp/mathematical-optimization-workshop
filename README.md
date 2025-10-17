# Hands-on Mathematical Optimization

During this hands-on workshop, we will take a practical look at the field of "operations research", which is all about using mathematical optimization techniques for informed/automated decision making. We will:

 - learn how to model practical problems as optimization problems;
 - use this to optimize two practical cases;
 - experience how our choice of model influences the proposed decisions.

#### Prerequisites

A laptop is required for this session. Please ensure Python >= 3.9 is installed beforehand. We will make use of the following two libraries:
 - [Scipy](https://scipy.org/), installed through: `pip install scipy`
 - [Matplotlib](https://matplotlib.org/), installed through: `pip install matplotlib`

## A little bit of theory

An optimization problem is a problem of the form:

$$\begin{matrix}
\text{minimize} & f(x)\\\
\text{subject to} & g_1(x) \leq 0\\\
& g_2(x) \leq 0\\\
& \vdots \\\
& g_k(x) \leq 0,\end{matrix}$$

where $x = [x_1, x_2, \ldots, x_n]$ are called _decision variables_, $f$ is called the _objective function_, and $g_i(x) \leq 0$ are called _constraints_.  The solution to an optimization problem are the specific values for the decision variables that satisfy the constraints, that minimize the objective function. There is no exact algorithm for the general optimization problem, though specific restrictions for the decision variables, objective functions, and constraints exist that permit specialized algorithms (e.g. [convex optimization](https://en.wikipedia.org/wiki/Convex_optimization), [conic optimization](https://en.wikipedia.org/wiki/Conic_optimization), [semidefinite optimization](https://en.wikipedia.org/wiki/Semidefinite_programming), [quadratic optimization](https://en.wikipedia.org/wiki/Quadratic_programming)). We will look at the most well studied type of optimization problem in this workshop: [linear optimization problems](https://en.wikipedia.org/wiki/Linear_programming).

An optimization problem is linear if the function $f$ is linear ($f(x) = c_1x_1+...+c_nx_n$ for constant $c_1,\ldots,c_n$), and all $g_i$ are "affine" ($g_i(x) = a_{i,1}x_1+...+a_{i,n}x_n+b_i$ for constant $a_{i,1},\ldots,a_{i,n},b_i$). Linear optimization problems can be solved in polynomial time (meaning we can efficiently find the global optimal solution).

If some of the decision variables $x_i$ are additionally restricted to the integers, we refer to the problem as the [integer optimization problem or mixed integer-linear optimization](https://en.wikipedia.org/wiki/Integer_programming). In this case we can still find the optimal solution, but there are currently no known algorithms that run in polynomial time (in fact, if we would have such an algorithm, we would have solved the famous [P versus NP problem](https://en.wikipedia.org/wiki/P_versus_NP_problem), since the integer programming problem is [NP-complete](https://en.wikipedia.org/wiki/NP-completeness)). Nevertheless, solutions can be found reasonably quickly up to moderate problem sizes (depending on the problem, of course).

## Example: profit maximization

Consider a factory which is faced with choosing how much of two different products should be manufactured. One unit of the first product provides a profit of 10 euros, and one unit of the second provides 5 euros profit. Producing the parts for these products cost 10 minutes and 8 minutes respectively, and assembling the parts cost 10 and 2 minutes respectively. Assume that we are given 120 minutes of production time, and 60 minutes of assembly time. How much of either product should we manufacture to maximize profit?

This can be found by solving the following linear optimization problem:

$$\begin{matrix}
\text{maximize} & 10x_1 + 5x_2\\\
\text{subject to} & 10x_1 + 8x_2 \leq 120,\\\
& 10x_1 + 2x_2 \leq 60,\\\
& x_1 \geq 0, x_2 \geq 0.
\end{matrix}$$

To solve this through [`scipy.optimize.linprog`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html) we need to formulate the optimization problem in the following form:

$$\begin{matrix}\text{minimize} & \mathbf{c}^T \mathbf{x}\\
\text{subject to} & A_{ub}\mathbf{x} \leq \mathbf{b}_{ub},\\
& A_{eq}\mathbf{x} = \mathbf{b}_{eq},\\
& \mathbf{l} \leq \mathbf{x} \leq \mathbf{u}.\end{matrix}$$

where $\mathbf{c}$, $\mathbf{x}$, $\mathbf{b}_{ub}$ and $\mathbf{b}_{eq}$ are vectors, and $A_{ub}$ and $A_{eq}$ are a matrix.

This means we need to change the maximation into minimization. Since maximizing something is the same as minimizing its negative, we can simply negate the objective function and minimize:

$$\begin{matrix}
\text{minimize} & -10x_1 - 5x_2\\\
\text{subject to} & 10x_1 + 8x_2 \leq 120,\\\
& 10x_1 + 2x_2 \leq 60,\\\
& x_1 \geq 0, x_2 \geq 0.
\end{matrix}$$

And next figuring out $A_{ub}$, $b_{ub}$ and $c$: 

$$\begin{matrix}
\text{minimize} & \left(\begin{matrix}-10 & -5\end{matrix}\right)\left(\begin{matrix}x_1 \\\ x_2\end{matrix}\right)\hspace{3.9em}\\\
\text{subject to} & \left(\begin{matrix}10 & 8 \\\ 10 & 2\end{matrix}\right)\left(\begin{matrix}x_1 \\\ x_2\end{matrix}\right) \leq \left(\begin{matrix}120 \\\ 60\end{matrix}\right),\\\
& x_1 \geq 0, x_2 \geq 0.
\end{matrix}$$

Leading to the following script:

```python
from scipy.optimize import linprog

objective = [-10, -5]
inequality_constraints_matrix = [[10, 8], [10, 2]]
inequality_constraints_vector = [120, 60]

# bounds = (0, None) is the default, so we don't need to specify x_1>=0 and x_2>=0
x_1,x_2 = linprog(objective, A_ub = inequality_constraints_matrix, b_ub = inequality_constraints_vector).x
print(x_1, x_2) # What does this print?
```

In this case, we happen to obtain an integer solution, which is great, because we probably can't create half of a product, and expect to get half of its profit! In general though, the answer need not be restricted to the integers.

- What is the solution if the amount of available production minutes gets reduced to 100, such that `b = [100, 60]`?
- What is the best integer solution when $b = [100, 60]$? (Variables can be restricted to the integers through the `integrality` parameter, see the documentation of [`scipy.optimize.linprog`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html).)
- What do you notice when comparing it with the best non-integer solution?

## Exercise: [the battery charging problem](./battery-charging/README.md)

## Exercise: [the cutting stock problem](./cutting-stock/README.md)
