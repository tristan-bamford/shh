from openai import OpenAI
import json

import logging
logging.basicConfig(filename="assistant.log", level=logging.INFO)

#import tools

class Command:
  def __init__(self, dct):
    self.command_string= dct['command_string'] if 'command_string' in dct else str()
    self.description   = dct['description']    if 'description'    in dct else str()
    self.programs_used = dct['programs_used']  if 'programs_used'  in dct else []


class Response:
  def __init__(self, completion=None):

    self.message = None
    self.request_output = False
    self.commands = []
    self.reason = str()

    if completion is None:
      return
   
    message = completion.choices[0].message
    self.message = message.content
    
    # populate the tool calls
    tool_calls = message.tool_calls
    if tool_calls:
      for tool in tool_calls:
        try:
          f_arguments = json.loads(tool.function.arguments)
        
          if tool.function.name == "shell_command":
            self.reason = f_arguments['reason'] if 'reason' in f_arguments else None
            self.request_output = f_arguments['request_output'] if 'request_output' in f_arguments else False
            
            if 'commands' in f_arguments:
              for command_dct in f_arguments['commands']:
                self.commands.append(Command(command_dct))
                
        except Exception as err:
          print(f"Unexpected {err=}, {type(err)=}")



class Assistant:
  client = OpenAI()
  #model = "gpt-3.5-turbo" # default model
  max_prompt_size = 1024

  def __init__(self, instructions, tools=[], model="gpt-3.5-turbo"):
    self.instructions = instructions # system messages that will be prepended to a message thread
    self.tools = tools               # JSON schema object that defines openai function calls
    self.history = []
    self.model = model

  # Construct a message thread for the openai api. The whole thread doesn't need 
  # to be used.
  def __get_context(self):
    context_window = []

    # start with the instructions
    context_window.append({"role": "system", "content": self.instructions})

    # add n items from the message thread
    n = 4
    context_window += self.history[-n:]
    
    return context_window

  # Add an instruction for the Assistant
  def add_instruction(self, instruction):
    self.instructions += f"-{instruction}\n"

  # Add a message to the message history
  def add_message(self, role, content):
    self.history.append({"role": role, "content": content})

  def ask(self, prompt: str, remember=True):
    command = None
    # format and truncate prompt if necessary
    prompt = prompt[:Assistant.max_prompt_size]

    # add the prompt to the thread
    self.add_message('user', prompt)

    # run an openai api completion
    response = Response()
    try:
      completion = Assistant.client.chat.completions.create(
        model = self.model,
        messages = self.__get_context(),
        tools = self.tools
      )

      response = Response(completion)
      logging.info(completion)

      if remember:
        if response.message:
          self.add_message('assistant', response.message)
        else:
          self.add_message('assistant', "here is a command to try")

    except Exception as err:
      print(f"Unexpected {err=}, {type(err)=}")

    return response