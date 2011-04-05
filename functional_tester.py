from subprocess import Popen, PIPE
import re
import sys

class FunctionalTester:
  """
  Author: Ian Murray
  Date: March 27th, 2011
  Copyright: 2011 - Ian Murray
  """
  
  def __init__(self, script_to_test, tests = [], die_on_difference = True):
    """
    steps should be a list like this:
    
    [
      # Send my name to the script
      {
        "action": "send",
        "message": "John Doe" # Assuming the script should be asking for your name here, for example
      },
      
      # Assert output of the script
      {
        "action": "assert",
        "comparison": "Hi John Doe!" # The assertion can be a regular expression =D
      }
    ]
    
    """
    self.script_to_test = script_to_test
    self.tests = tests
    self.die_on_difference = die_on_difference
  
  def log(self, message):
    print ">>>", message
    
  def go(self):
    failures = 0
    tests = 0
    explanations = ""
    for test in self.tests:
      failed_this_test, failurestring = self.__run(test)
      
      explanations += failurestring + "\n"
      
      if failed_this_test:
        sys.stdout.write("F")
        failures += 1
      else:
        sys.stdout.write(".")
      tests += 1
    
    print
    print explanations
    print "%d/%d passed, %d failed. %d total tests." % (tests - failures, tests, failures, tests)
  
  def __run(self, steps):
    #self.log('Testing file ' + self.script_to_test)
    
    # Iterate through the tests
    # Here we will store all outcomes of every step.
    step_outcomes = []
    
    # We need to construct a string with all the "send" steps
    the_steps = ""
    for step in steps:
      if step["action"] == "send":
        the_steps += step["message"] + "\n"
    
    # We need to patch the script so it prints some separating
    # chars that we can later use to split the output
    
    source = file(self.script_to_test, 'r')
    dest = file('temp.py', 'w')
    
    # Import some modules in the temp file
    dest.write("import sys\n")
    dest.write("import outputter\n")
    dest.write("outputter.emptyfile()\n")
    
    for line in source:
      if re.search("raw_input", line):
        #dest.write("sys.stdout.write('<RIS>')\n")
        dest.write(line + "\n")
        #dest.write("sys.stdout.write('<RIE>')\n")
        pass
      elif re.search("print", line):
        match = re.search(r'print (.+)\n?', line)
        #dest.write("sys.stdout.write('<PS>')\n")
        #dest.write(line + "\n")
        #dest.write("outputter.output(" + match.groups()[0] + ")\n")
        dest.write(re.sub(r'(.*)print (.+)\n?', r'\1outputter.output(\2)\n', line))
        #dest.write("sys.stdout.write('<PE>')\n")
      else:
        dest.write(line + "\n")
    
    source.close()
    dest.close()
    
    # Now, execute the patched file
    program = Popen(["python2.7", "temp.py"], stdin = PIPE, stdout = PIPE)
    
    # Send the magical input string
    output = program.communicate(the_steps)[0]
    output = file("temp.out", "r")
    
    # Parse the output, this should match all output sent by print statements
    #matches = re.findall(r'<PS>([^<]*)<PE>', output)
    matches = output.readlines()
    
    # Do we have the same ammount of prints and comparison steps?
    # Count them
    comparison_steps = []
    for step in steps:
      if step["action"] == "assert":
        comparison_steps.append(step)
    
    #self.log("There are %s comparisons, %s matches." % (len(comparison_steps), len(matches)))
    
    if len(matches) != len(comparison_steps):
      self.log("FATAL: Ammount of comparison steps and prints in the script differ.")
      self.log("These were the outputs:")
      for match in matches:
        print "  ", match.strip()
      
      if self.die_on_difference:
        exit(1)
      else:
        return False
    
    # Now use the compare steps
    step_outcomes = []
    failed_this_test = False
    for i in range(len(comparison_steps)):
      if re.search(comparison_steps[i]["comparison"], matches[i], re.IGNORECASE):
        #sys.stdout.write('.')
        pass
      else:
        #sys.stdout.write('F')
        failed_this_test = True
        
        step_outcomes.append({
          "action": "comparison",
          "compared": comparison_steps[i]["comparison"],
          "compared_to": matches[i]
        })
    
    # Separator
    #print "\n"
    
    # Print failures
    failurestring = ""
    for failure in step_outcomes:
      failurestring += "  Expected\n"
      failurestring += "    " + failure["compared"] + "\n"
      failurestring += "  got\n"
      failurestring += "    " + failure["compared_to"]
    
    # Results
    #print len(comparison_steps), "steps,", len(step_outcomes), "failures." 
    return (failed_this_test, failurestring)