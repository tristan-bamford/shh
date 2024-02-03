import sys
import os

import tools, instructions

from assistant import Assistant, Response
from print import *

# Shh - Shell Helper
# Python script for generating shell commands at the command line by using
# an openai api.
#
# Usage: shh [-options] PROMPT
#
# The AI assistant will return one or several commands and/or some help text, 
# and who know what else, in a pretty printed format. The generated commands 
# can be optionally appended to a history file like bash_history.


# Program options
history_file = "/home/tristan/.bash_history"
opt_execute_command = False # -x, -r
opt_append_history = False  # -a


# Get a list of command strings and add them to the history file
def appended_history(commands):
  appended_history = str()

  for command in commands:
    appended_history += command.command_string + '\n'

  with open(history_file, 'a') as file:
    file.write(appended_history)


# Run the prompt with the assistant and print the results 
def run(assistant, prompt):

  response = assistant.ask(prompt)
  
  if opt_append_history:
    appended_history(response.commands)
  
  print_response(response)


# Parse command line arguments and return the user prompt.
#  
# The first n consecutive arguments starting with '-' are considered options. 
# The rest of the arguments will be considered the users prompt
def parse_arguments(arguments):

  global history_file
  global opt_append_history
  global opt_execute_command

  for arg in arguments:
    # arguments are options until they are not
    if not arg.startswith('-'):
      break
    option = arg[1:]
    arguments = arguments[1:] # remove option from arguments

    if option == 'x':
      opt_execute_command = True
    if option == 'a':
      opt_append_history = True
    if option == 'h':
      history_file = arguments[0] # the next arg
      arguments = arguments[1:]

  return ' '.join(arguments) # the remainder are joined to make the user prompt


def main():

  # create assistant
  assistant = Assistant(instructions.shell_assistant, [tools.shell_command])
  assistant.add_instruction(f"The user is running on this platform: {os.uname()}")

  # parse command line
  arguments = sys.argv[1:]
  if arguments:
    
    prompt = parse_arguments(arguments)    
    run(assistant, prompt)

  else:
    
    # load the bash history file
    readline.read_history_file(history_file)
    
    print("Enter 'exit' to exit.")
    while (prompt := user_input("# ")) != "exit":
      run(assistant, prompt)
  
  #print("Enter the bash command 'history -r' to load your history file")

if __name__ == '__main__':
  main()