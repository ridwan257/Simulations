
all:
	python3 rocket.py

.PHONY : foodh
foodh:
	python3 food-hunter.py

.PHONY : test
test: 
	python3 -m tests.tests

.PHONY : test2 test3 test4 test5 test6
test2: 
	python3 -m tests.test2

test3: 
	python3 -m tests.test3

test4: 
	python3 -m tests.test4

test5: 
	python3 -m tests.test5

test6: 
	python3 -m tests.test6

.PHONY : gradient-descent
gradient-descent:
	python3 gradient-descent.py

.PHONY : collision_checker
collision_checker:
	python3 collision_checker.py

.PHONY : matrix_rain
matrix_rain:
	python3 matrix_rain.py

.PHONY : binsep
binsep:
	python3 binary_separation.py

.PHONY : bird
bird:
	python3 flocking_birds.py

.PHONY : pp
pp:
	python3 ping_pong.py

.PHONY : gnumb
gnumb:
	python3 guess_number.py

.PHONY : antT
antT:
	python3 traveling_ant.py