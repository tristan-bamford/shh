import subprocess

def try_run(prompt):
  # when shell = True, do not split the command string
  #command = shlex.split(prompt)
  command = [prompt]

  try:
    result = subprocess.run(
      command, 
      stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE,
      shell=True, 
      executable='/bin/bash'
    )
  except:
    result = None
  return result