
#I wanted to use virtualenv to do user-like tests,
#etc., but because of the dependency on NOMAD
#this is nontrivial

#therefore, this makefile is mostly alias-like
#commands to run various examples and scripts

sandbox:
	@python3 sbox/sandbox.py

ex1:
	@python3 examples/example_1/driver.py
	@cat examples/example_1/optimal_solver.py
