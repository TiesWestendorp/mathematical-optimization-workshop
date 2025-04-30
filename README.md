# mathematical-optimization-workshop

During this hands-on workshop, we will solve  for mathematical optimization

### Prerequisites

- Python >= 3.9 is required
- `scipy`: `pip install scipy`

## Linear optimization problems

An optimization problem is a problem of the form:

$$\begin{matrix}
\text{minimize} & f(x)\\\
\text{subject to} & g_1(x) \leq 0\\\
& g_2(x) \leq 0\\\
& \vdots \\\
& g_k(x) \leq 0,\end{matrix}$$

$x = [x_1, x_2, \ldots, x_n]$ are called _decision variables_, $f$ is called the _objective function_, and $g_i(x) \leq 0$ are called _constraints_. The goal in solving an optimization problem is to find the decision variables within certain constraints, that minimize a given objective function. This general optimization problem has no exact algorithm to solve it, hence many restricted versions exist that permit specialized algorithms (e.g. [convex optimization](https://en.wikipedia.org/wiki/Convex_optimization), [conic optimization](https://en.wikipedia.org/wiki/Conic_optimization), [semidefinite optimization](https://en.wikipedia.org/wiki/Semidefinite_programming), [quadratic optimization](https://en.wikipedia.org/wiki/Quadratic_programming)). We will look at one such specific type of optimization problem throughout this workshop: [linear optimization problems](https://en.wikipedia.org/wiki/Linear_programming).

An optimization problem is linear if the function $f$ is linear ($f(x) = c_1x_1+...+c_nx_n$ for constant $c_1,\ldots,c_n$), and all $g_i$ are "affine" ($g_i(x) = a_{i,1}x_1+...+a_{i,n}x_n+b_i$ for constant $a_{i,1},\ldots,a_{i,n},b_i$). Linear optimization problems are also called linear programming problems ("programming" meaning "optimization" predates the modern meaning of the word "programming", to avoid confusion we'll stick to "optimization").

Linear optimization problems can be written in _standard form_ (the form most solvers expect) as:

$$\text{minimize}\hspace{0.5em} \mathbf{c}^T \mathbf{x}  \text{ subject to } A\mathbf{x} \leq \mathbf{b} \text{ and } \mathbf{x} \geq 0,$$

where $\mathbf{c}$, $\mathbf{x}$ and $\mathbf{b}$ are vectors, and $A$ is a matrix (see the next section for an example). Expanded out, this becomes:

$$\begin{matrix}\text{minimize} & c_1x_1 + \ldots + c_nx_n\\\
\text{subject to} & a_{1,1}x_1 + a_{1,2}x_2 + \ldots + a_{1,n}x_n \leq b_1\\\
& a_{2,1}x_1 + a_{2,2}x_2 + \ldots + a_{2,n}x_n \leq b_2\\\
& \vdots\\\
& a_{k,1}x_1 + a_{k,2}x_2 + \ldots + a_{k,n}x_n \leq b_k\\\
& x_1 \geq 0\\\
& \vdots\\\
& x_n \geq 0,\end{matrix}$$

such that each row of $A$ represents one of the $k$ constraints.

Linear optimization problems can be solved _exactly_ in polynomial time (meaning we can efficiently find the global optimal solution).

If at least one of the decision variables $x_i$ are additionally restricted to the integers, we refer to the problem as the [integer optimization problem or mixed integer-linear optimization](https://en.wikipedia.org/wiki/Integer_programming). In this case can still find the optimal solution, but there are currently no known algorithms that run in polynomial time (in fact, if we would have such an algorithm, we would have solved the famous [P versus NP problem](https://en.wikipedia.org/wiki/P_versus_NP_problem), since the integer programming problem is [NP-complete](https://en.wikipedia.org/wiki/NP-completeness)). Nevertheless, solutions can be found reasonably quickly up to moderate problem sizes (depending on the problem, of course).

## Example: profit maximization

Consider a factory which is faced with choosing how much of two different products should be manufactured. One unit of the first product provides a profit of 10 euros, and one unit of the second provides 5 euros profit. Producing the parts for these products cost 10 minutes and 8 minutes respectively, and assembling the parts cost 10 and 2 minutes respectively. Assume that we are given 120 minutes of production time, and 60 minutes of assembly time. How much of either product should we manufacture to maximize profit?

This can be found by solving the following linear optimization problem:

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
\text{subject to} & \left(\begin{matrix}10 & 8 \\\ 10 & 2\end{matrix}\right)\left(\begin{matrix}x \\\ y\end{matrix}\right) \leq \left(\begin{matrix}120 \\\ 60\end{matrix}\right),\\\
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

In general though, the answer need not be restricted to the integers. For example if the amount of available production minutes gets reduced to 100, such that `b = [100, 60]`, the optimal solution becomes $x = \tfrac{14}{3}\approx 4.667, y = \tfrac{20}{3} \approx 6.667$. If we want to find the best _integer_ solution, we additionally need to impose the integrality constraints: $x\in\mathbb{Z}$ and $y\in\mathbb{Z}$ (specified through the `integrality` parameter in `linprog`).

- What is the best integer solution when $b = [100, 60]$?
- What do you notice when comparing it with the best non-integer solution?