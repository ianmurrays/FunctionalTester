from functional_tester import FunctionalTester

# Define steps
steps = [
  {
    "action"  : "send",
    "message" : "Cobresal"
  },
  
  {
    "action"  : "send",
    "message" : "12"
  },
  
  {
    "action"  : "send",
    "message" : "7"
  },
  
  {
    "action"  : "send",
    "message" : "9"
  },
  
  {
    "action"      : "assert",
    "comparison"  : "Cobresal tiene 43 puntos"
  }
]

# Run the test
test = FunctionalTester('scripts/201166573_P1.py', steps)
test.run()