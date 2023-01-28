Quiz 20.7 input file format:

```
[number_of_vertices] [number_of_edges]
[one_endpoint_of_edge_1] [other_endpoint_of_edge_1] [edge_1_cost]
[one_endpoint_of_edge_2] [other_endpoint_of_edge_2] [edge_2_cost]
```

The nearest neighbor heuristic algorithm greedily consume the minimum weight edge
of each unvisited vertex:

1. Begin a tour at an arbitrary vertex
2. Repeat until all vertices have been visited:
    a. If the current vertex is u, proceed to the closet unvisited vertex v
3. Return to the starting vertex