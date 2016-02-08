# Data stream algorithm for connected components

**Problem.** *We have a graph on n vertices and a stream of updates. Each update is either to add or to remove an edge from the graph. Initially, the graph is empty. The goal is to restore all connected components after all updates with probability 0.99.*

This is an implementation of the algorithm which solves the problem. I use this code as an example to this post (in Russian):

## Sources

- <a href="dimacs.rutgers.edu/~graham/pubs/papers/l0samp.pdf">"On Unifying the Space of l0-Sampling Algorithms", Graham Cormode, Donatella Firmani, 2013</a>
- <a href="https://people.cs.umass.edu/~mcgregor/papers/12-dynamic.pdf">"Analyzing Graph Structure via Linear Measurements", Kook Jin Ahn, Sudipto Guha, Andrew McGregor, 2012</a>
