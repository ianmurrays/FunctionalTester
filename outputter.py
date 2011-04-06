# Empty the file
def emptyfile():
  output = file("temp.out", "w")
  output.close()

def output(string):
  output = file("temp.out", "a")
  output.write(string)
  output.close()
  
def newoutput(*args):
  output = file("temp.out", "a")
  output.write(" ".join(args))
  output.close()