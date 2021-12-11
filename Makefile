
#I wanted to use virtualenv to do user-like tests,
#etc., but because of the dependency on NOMAD
#this is nontrivial

#therefore, this makefile is mostly alias-like
#commands to run various examples and scripts

sandbox:
	@python3 sbox/sandbox.py

ex1:
	@python3 examples/example_1/driver.py
	@cat examples/example_1/tuned_solver.py

ex2:
	@python3 examples/example_2/driver.py
	@cat examples/example_2/optimal_solver.py
