# CS 131 Fall 2022 - Project Autograder

Hi there! This is a repo that contains an open-source subset of the autograder we'll be using for [CS 131 - Fall 2022](https://ucla-cs-131.github.io/fall-22/)'s course-long project: making an interpreter.

Using this repository / testing locally is **entirely optional**. It does not directly affect your grade. **You are free to only submit to Gradescope!**

This repository contains:

- the **full source code** for the autograder we deploy to Gradescope
- 20% of the test cases we evaluate your code on; these are the test cases that are public on Gradescope
    - `testsv*` contains source (`.src`), expected (`.exp`), and standard input (`.in`) files for programs that should interpret and run without errors
    - `failsv*` contains source (`.src`), expected (`.exp`), and standard input (`.in`) files for programs that should interpret successfully, but error

This repository does not contain:

- 80% of the test cases we evaluate your code on (until *after* the project is due)
- the plagiarism checker, which is closed-source
- the Docker configuration for the deployment; this is managed by Gradescope
- canonical solutions for the past projects - those are in the [project template repo](https://github.com/UCLA-CS-131/fall-22-proj-starter)

We'll note that with the current setup, we grant **five seconds for each test case to run**.

We've made a [separate repository for project template code](https://github.com/UCLA-CS-131/fall-22-proj-starter).

## Usage

First, clone this repository and make it your working directory:

```sh
$ git clone
# or, with SSH
$ git clone git@github.com:UCLA-CS-131/fall-22-autograder.git
...
cd fall-22-autograder
```

Your next steps depend on what you're trying to do.

### Testing Locally

To test locally, you will additionally need a **working implementation** of the project; the minimum example is an `interpreterv1.py`/`interpreterv2.py`/`interpreterv3.py` that implements the `Interpreter` class.

Place this in the same directory as `tester.py`. Then, to test project 1,

```sh
$ python3 tester.py 1
Running 10 tests...
Running testsv1/test1.src...  PASSED
Running testsv1/test2.src...  PASSED
Running testsv1/test6.src...  PASSED
Running testsv1/test8.src...  PASSED
Running testsv1/test10.src...  PASSED
Running testsv1/test27.src...  PASSED
Running testsv1/test28.src...  PASSED
Running failsv1/test1.src...  PASSED
Running failsv1/test9.src...  PASSED
Running failsv1/test7.src...  PASSED
10/10 tests passed.
Total Score:    100.00%
```

Similarly, one can test version 2, which requires a `interpreterv2.py`, with:

```sh
$ python3 tester.py 2
Running 25 tests...
Running testsv2/test2.src...  PASSED
Running testsv2/test3.src...  PASSED
Running testsv2/test6.src...  PASSED
Running testsv2/test7.src...  PASSED
Running testsv2/test8.src...  PASSED
Running testsv2/test10.src...  PASSED
Running testsv2/test11.src...  PASSED
Running testsv2/test12.src...  PASSED
Running testsv2/test13.src...  PASSED
Running testsv2/test47.src...  PASSED
Running testsv2/test16.src...  PASSED
Running testsv2/test50.src...  PASSED
Running testsv2/test53.src...  PASSED
Running testsv2/test22.src...  PASSED
Running testsv2/test55.src...  PASSED
Running failsv2/test3.src...  PASSED
Running failsv2/test4.src...  PASSED
Running failsv2/test8.src...  PASSED
Running failsv2/test9.src...  PASSED
Running failsv2/test10.src...  PASSED
Running failsv2/test20.src...  PASSED
Running failsv2/test21.src...  PASSED
Running failsv2/test23.src...  PASSED
Running failsv2/test24.src...  PASSED
Running failsv2/test27.src...  PASSED
25/25 tests passed.
Total Score:    100.00%
```

And version `3` with `python3 tester.py 3`:

```sh
$ python3 tester.py 3
Running 20 tests...
Running testsv3/test20.src...  PASSED
Running testsv3/test22.src...  PASSED
Running testsv3/test37.src...  PASSED
Running testsv3/test112.src...  PASSED
Running testsv3/test113.src...  PASSED
Running testsv3/test114.src...  PASSED
Running testsv3/test122.src...  PASSED
Running testsv3/test127.src...  PASSED
Running testsv3/test140.src...  PASSED
Running testsv3/test156.src...  PASSED
Running testsv3/test201.src...  PASSED
Running testsv3/test202.src...  PASSED
Running testsv3/test203.src...  PASSED
Running testsv3/test204.src...  PASSED
Running testsv3/test205.src...  PASSED
Running failsv3/test26.src...  PASSED
Running failsv3/test27.src...  PASSED
Running failsv3/test29.src...  PASSED
Running failsv3/test30.src...  PASSED
Running failsv3/test105.src...  PASSED
20/20 tests passed.
Total Score:    100.00%
```

The output of this command is **identical to what is visible on Gradescope pre-due date**, and they are the same cases that display on every submission. If there is a discrepancy, please let the teaching team know!

Note: we also output the results of the terminal output to `results.json`.

### Deploying on Gradescope (as an instructor)

*Note: as an instructor, you'll want to add more test cases!*

We've written a `Makefile` that simplifies the deploy process. After your test cases are finalized, simply run

```sh
$ make
```

This will give you a `grader.zip` file. You can then upload the resulting `.zip` file to Gradescope's autograder platform; it should do the rest.

(more coming soon!)

## Extending the Grader

Coming soon :)
### Adding More Testcases

Coming soon :)

### Changing Core Infrastructure

Coming soon :)

## Bug Bounty

If you're a student and you've found a bug - please let the TAs know (confidentially)! If you're able to provide a minimum-reproducible example, we'll buy you a coffee - if not more!

## Licensing and Attribution

This code is distributed under the [MIT License](https://github.com/UCLA-CS-131/fall-22-autograder/blob/main/LICENSE).

Have you used this code? We'd love to hear from you! [Submit an issue](https://github.com/UCLA-CS-131/fall-22-autograder/issues) or send us an email ([matt@matthewwang.me](mailto:matt@matthewwang.me)).
