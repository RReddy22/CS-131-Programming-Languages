from interpreterv4 import Interpreter

srcfile = "/Users/RReddy18/Desktop/School/Fall 2022 Classes/CS 131/Projects/Project 3/fall-22-autograder/testsv3/test22.src"
with open(srcfile) as handle: 
        program = handle.readlines()
        i1 = Interpreter()
        i1.run(program)