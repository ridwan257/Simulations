
all:
	python3 rocket.py

.PHONY : foodh
foodh:
	python3 food-hunter.py

.PHONY : test2 test3 test4
test2: 
	python3 -m tests.test2

test3: 
	python3 -m tests.test3

test4: 
	python3 -m tests.test4

.PHONY : gradient-descent
gradient-descent:
	python3 gradient-descent.py



.PHONY : collision_checker
collision_checker:
	python3 collision_checker.py