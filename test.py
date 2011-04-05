from functional_tester import FunctionalTester
import sys

# Define steps
the_tests = []

the_tests.append([{
  "action"  : "send",
  "message" : "31"
},

{
  "action"  : "send",
  "message" : "39"
},

{
  "action"  : "send",
  "message" : "17"
},

{
  "action"      : "assert",
  "comparison"  : "Todos tienen edades distintas"
}])

the_tests.append([{
  "action"  : "send",
  "message" : "27"
},

{
  "action"  : "send",
  "message" : "12"
},

{
  "action"  : "send",
  "message" : "27"
},

{
  "action"      : "assert",
  "comparison"  : "Edelmiro y Prisciliano tienen la misma edad"
}])

the_tests.append([{
  "action"  : "send",
  "message" : "20"
},

{
  "action"  : "send",
  "message" : "20"
},

{
  "action"  : "send",
  "message" : "20"
},

{
  "action"      : "assert",
  "comparison"  : "Los tres tienen la misma edad"
}])

# Run the test
test = FunctionalTester(sys.argv[1], the_tests, die_on_difference = False)
test.go()
