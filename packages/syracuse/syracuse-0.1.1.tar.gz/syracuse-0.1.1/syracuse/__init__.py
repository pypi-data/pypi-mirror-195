"""This package provides some tools to deal with the Collatz conjecture.

The Collatz conjecture, also known as the "3n + 1 problem" or the "Syracuse problem", is an unsolved hypothesis in mathematics that concerns a sequence of operations applied to a positive integer. The conjecture states that no matter what the starting value of this integer is, the sequence will always eventually reach the value 1.

More specifically, the Collatz conjecture states that if one takes a positive integer n and applies the following function:

- If n is even, divide it by 2.
- If n is odd, multiply it by 3 and add 1.

Then, repeat the process with the resulting value, applying the function over and over again until the value of n eventually reaches 1.

!!! example
	
	If one takes n = 6, the sequence for the Collatz conjecture would be:
	6, 3, 10, 5, 16, 8, 4, 2, 1.

The Collatz conjecture asserts that this sequence will always eventually reach the value 1, no matter what positive integer n one starts with. Although the conjecture has been computationally tested for extremely large values, it remains unproven to this day.

Since 3n+1 is even whenever n is odd, it is possible to define a "shortcut" (or "compressed") form for the Collatz function:

- If n is even, divide it by 2.
- If n is odd, multiply it by 3, add 1 **and divide the whole result by 2**.	
	
This definition yields smaller values for the stopping time and total stopping time without changing the overall dynamics of the process.

See the related [article on Wikipedia](https://en.wikipedia.org/wiki/Collatz_conjecture) for deeper information.

The package provides the following modules:

| Module    | Description                                                             |
| --------- | ----------------------------------------------------------------------- |
| `core`    | Provides classes to define Collatz sequences                            |
| `drawing` | Provides tool functions to render in various ways the Collatz sequences |

It is important to notice that the `core` module can be used without being imported explicitly. However, all other modules **need** to be imported explicitly.

```pycon
>>> import syracuse # import all objects exposed by the core module
>>> import syracuse.drawing # import objects exposed by the drawing module
```

"""
from .core import Syracuse, CompressedSyracuse
