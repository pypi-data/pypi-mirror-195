from gptshell.GPTshell import GPTshell
import argparse
import subprocess

def main():
  parser = argparse.ArgumentParser(description="Convert text to command and vice versa.")
  parser.add_argument("-ttc", "--text_to_command", help="Execute a shell command by providing its description.", nargs='+')
  parser.add_argument("-ctt", "--command_to_text", help="Get the description of a shell command.", nargs='+')
  args = parser.parse_args()
  args = parser.parse_args()
  LLMCommands = GPTshell()
  if args.text_to_command:
    output = LLMCommands.text_to_command(args.text_to_command)
    print(f"\033[1;32;40m{output}\033[0m Do you want to run this command? (y/n)")
    if input().lower() == 'y':
      result = subprocess.run(["powershell", "-Command", output], capture_output=True, text=True)
      print(result.stdout)

  if args.command_to_text:
    output = LLMCommands.command_to_text(args.command_to_text)
    print(f"\033[1;34;40m{output}\033[0m")

  if not any(vars(args).values()):
    parser.print_help()