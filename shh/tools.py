# Tools for the Shh Assistant expressed as JSON schema

shell_command = {
  "type": "function",
  "function": {
    "name": "shell_command",
    "description": "call this function when a shell command is recommended/provided/suggested",
    "parameters": {
      "type": "object",
      "properties": {
        
        # reason
        "reason": {
          "type": "string",
          "description": "A brief summary of why this command has been suggested"
        },

        # request output
        "request_output": {
          "type": "boolean",
          "description": "set this to true if output from the command is needed to fulfill the users request"
        },

        # commands
        "commands": {
          "description": "a list of recommended commands ordered by relevancy",          
          "type": "array",
          "items": {
            
            # command type
            "type": "object",
            "properties": {

              # command.command_string
              "command_string": {
                "type": "string",
                "description": "the command and all of its arguments and options as would be presented to the shell"
              },

              # command.description
              "description": {
                "type": "string",
                "description": "A brief description of what this command does"
              },

              # command.programs_used
              "programs_used": {
                "description": "A list of all the program names used in this command; used for syntax highlighting",
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              
            },
          },
          "required": ["command_string", "programs_used"],
        },
      },
      "required": ["commands"]
    }
  }
}