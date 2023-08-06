from langchain import OpenAI, LLMChain, PromptTemplate
import platform
import argparse
import subprocess
import platform

class GPTshell:
  def __init__(self):
    self.system = platform.system()
  def text_to_command(self, prompt: str, num_outputs: int = 1):
    template_text_to_command = PromptTemplate(input_variables=["num_outputs","human_input"], template="""Convert the input to {num_outputs}"""+ self.system + """possible  command: {human_input}""")
    llm = LLMChain(llm=OpenAI(temperature=0), prompt=template_text_to_command, verbose=False)
    return llm.predict(human_input=prompt, num_outputs=num_outputs).strip()
  
  def command_to_text(self, prompt: str):
    template_command_to_text = PromptTemplate(input_variables=["human_input"], template="""Describe the """ + self.system + """ command in English Language: {human_input}""")
    llm = LLMChain(llm=OpenAI(temperature=0), prompt=template_command_to_text, verbose=False)
    return llm.predict(human_input=prompt).strip()
  
def main():
  parser = argparse.ArgumentParser(description="Convert text to command and vice versa.")
  parser.add_argument("-ttc", "--text_to_command", help="Execute a shell command by providing its description.", nargs='+')
  parser.add_argument("-ctt", "--command_to_text", help="Get the description of a shell command.", nargs='+')
  args = parser.parse_args()
  from GPTshell import GPTshell
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

  if not args.text_to_command and not args.command_to_text:
    print("Please provide an argument.")