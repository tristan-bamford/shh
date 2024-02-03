#import pprint
import readline
import textwrap
from colorama import Fore, Style

# Style aliases
class Colors:
  bold = Style.BRIGHT
  weak = Style.DIM
  none = Style.RESET_ALL

  primary = Fore.CYAN
  primary_bold = primary + bold
  secondary = Fore.WHITE
  secondary_bold = secondary + bold

# Fancier input function that was a history and a prefill
def rlinput(prompt, prefill=''):
  readline.set_startup_hook(lambda: readline.insert_text(prefill))
  try:
    return input(prompt)
  finally:
    readline.set_startup_hook()

# alias for rlinput
def user_input(prompt='', prefill=''):
  return rlinput(prompt, prefill)


# Print with colorama style formatting
def print_with_style(text, style=Colors.none):
  print(f"{style}{text}{Colors.none}")

# Uses textwrap to make the text fit in a specified width and try to format it a 
# little nicer
def pretty_print(text, style=Colors.none, width=80):
  wrapper = textwrap.TextWrapper(
    width=width,
    #drop_whitespace=False,
    replace_whitespace=False,
    expand_tabs=True
  )
  print_with_style(wrapper.fill(text), style)

# "Syntax" highlighting
def highlight_syntax(text, primary, base_style=Colors.none):
  
  split_text = text.split()

  highlighted_text = base_style

  for item in split_text:
    if item in primary:
      highlighted_text += f"{Colors.secondary_bold}{item}{base_style} "
    else:
      highlighted_text += f"{item} "

  return highlighted_text


# Print data from the Command class
def print_command(command):

  # print formatted command string
  pretty_print(highlight_syntax(command.command_string, command.programs_used, 
                                Colors.primary_bold))

  # print the description if it's there
  if command.description:
    pretty_print(command.description, Colors.primary)

# Print the response from the openai assistant
def print_response(response):

  print()

  # This is the openai message content, it's usually empty on a tool call
  if response.message:
    pretty_print(response.message)
    print()

  # Reason for the shell command selection
  if response.reason:
    pretty_print(response.reason, Colors.secondary)
    print()

  # List of commands in a syntax-highlighted, dictionary-type format
  for command in response.commands:
    print_command(command)
    print()