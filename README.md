# diffusion_graph

Code for a model described by R. Venkatachalapathy.
An adjacency matrix is initialized with random weights, which evolve according to some diffusion process, becoming fixed at 0 or 1 if they go beyond those values.
This is a very simple family of temporal models for the formation of random graphs.


By default, the diffusion is a pure random drift on the interval [-0.05, 0.05].
The test file instead uses a gaussian distribution centered on 0 with standard deviation 0.1.
