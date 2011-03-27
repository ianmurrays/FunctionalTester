from subprocess import Popen, PIPE
import re
import sys

class FunctionalTester:
  """
  Author: Ian Murray
  Date: March 27th, 2011
  Copyright: 2011 - Ian Murray
  """
  
  def __init__(self, script_to_test, steps = []):
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
    self.steps = steps
  
  def log(self, message):
    print ">>>", message
  
  def run(self):
    self.log('Testing file ' + self.script_to_test)
    
    # Iterate through the tests
    # Here we will store all outcomes of every step.
    step_outcomes = []
    
    # We need to construct a string with all the "send" steps
    the_steps = ""
    for step in self.steps:
      if step["action"] == "send":
        the_steps += step["message"] + "\n"
    
    # We need to patch the script so it prints some separating
    # chars that we can later use to split the output
    
    source = file(self.script_to_test, 'r')
    dest = file('temp.py', 'w')
    
    # Import some modules in the temp file
    dest.write("import sys\n")
    
    for line in source:
      if re.search("raw_input", line):
        dest.write("sys.stdout.write('<RIS')\n")
        dest.write(line)
        dest.write("sys.stdout.write('RIE>')\n")
      elif re.search("print", line):
        dest.write("sys.stdout.write('<PS')\n")
        dest.write(line)
        dest.write("sys.stdout.write('PE>')\n")
      else:
        dest.write(line)
    
    source.close()
    dest.close()
    
    # Now, execute the patched file
    program = Popen(["python2.7", "temp.py"], stdin = PIPE, stdout = PIPE)
    
    # Send the magical input string
    output = program.communicate(the_steps)[0]
    
    # Parse the output, this should match all output sent by print statements
    matches = re.findall(r'<PS([^(PE>)]+)PE>', output)
    
    # Do we have the same ammount of prints and comparison steps?
    # Count them
    comparison_steps = []
    for step in self.steps:
      if step["action"] == "assert":
        comparison_steps.append(step)
    
    if len(matches) != len(comparison_steps):
      self.log("FATAL: Ammount of comparison steps and prints in the script differ.")
      self.log("These were the outputs:")
      for match in matches:
        print "  ", match.strip()
      exit(1)
    
    # Now use the compare steps
    step_outcomes = []
    for i in range(len(comparison_steps)):
      if re.search(comparison_steps[i]["comparison"], matches[i]):
        sys.stdout.write('.')
      else:
        sys.stdout.write('F')
        
        step_outcomes.append({
          "action": "comparison",
          "compared": comparison_steps[i]["comparison"],
          "compared_to": matches[i]
        })
    
    # Separator
    print "\n"
    
    # Print failures
    for failure in step_outcomes:
      print "  ", "Expected"
      print "    ", failure["compared"]
      print "  ", "got"
      print "    ", failure["compared_to"]
      print
    
    # Results
    print len(comparison_steps), "steps,", len(step_outcomes), "failures."