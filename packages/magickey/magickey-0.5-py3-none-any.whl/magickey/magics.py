# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function

import IPython.core.magic
from IPython.display import display, Javascript, Markdown, Code
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
import ast      # AST is also magic, right?
from parsimonious.nodes import NodeVisitor      # And so are PEGs!
from parsimonious.grammar import Grammar

import openai, os, getpass
from notebook.utils import to_api_path
from .engine import on, turn_on, prompt


@magics_class
class Arthur(Magics):
    """"This is the magics for Arthur-type intelligence. """

    def __init__(self, shell, **kwargs):
        super().__init__(shell, **kwargs)   
             

    @line_magic
    def asterisk(self, line):
        "User prompt"

        # Default initialization with Arthur as intelligence
        actor, input = line[5:-4].split(':%* ', maxsplit = 1)
        if not on(self):
            turn_on(self, actor = actor, name = 'Arthur')
            # print("username:", actor)

        response = prompt(self, input, actor = actor)

        display(Markdown(response))

        #add_response_cell(response)
        #print("Prompting. Full access to the main IPython object:", self.shell)
        #print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        #display(Markdown(text))

        lines = arthur_to_python(response)
        add_code_cell("\n".join(lines))

        add_prompt_cell(actor)

        
        # make output markdown
        # https://stackoverflow.com/questions/47818822/can-i-define-a-custom-cell-magic-in-ipython



    @line_magic
    def pattern(self, line):
        if line == "upload":
            pattern_upload()
        else:
            print("Unknown pattern command:", line)


    @line_magic
    def logrus(self, line):
        if line == "%logrus upload":
            logrus_upload()
        else:
            print("Unknown logrus command:", line)


    @cell_magic
    def thread(self, line, cell):
        "This allows to create a temporary thread"
        # http://ipython.org/ipython-doc/dev/interactive/reference.html#embedding-ipython
        # https://gemfury.com/squarecapadmin/python:ipython/-/content/IPython/frontend/terminal/embed.py
        return line, cell


    @line_magic
    def prompt(self, line):
        "Identifies and executes the prompt for: @object prompt"
        #object, text = line[1:].split(maxsplit = 1)      # @object Prompt 
        # execute object.prompt(text) and return the result    
        return self.shell.ev(line)

    @line_magic
    def response(self, line):
        "Identifies the response to user: %response lines"
        display(Markdown(line[6:-4]))
        #add_response_cell(line)
        


    
    # print("Prompting. Full access to the main IPython object:", self.shell)
    # print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
    # return line


    @line_magic
    def hashtag(self, line):
        "tagging the object"
        object, text = line[1:].split(maxsplit = 1)      # #object Prompt 
        print("Prompting. Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        return line
    
    

    @line_magic
    def finetune(self, line):
        "execute python code"


    @line_magic
    def execute(self, line):
        "execute python code"
        print("Executing. Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        print("We'll run it!")
        return line


    @cell_magic
    def cmagic(self, line, cell):
        "my cell magic"
        return line, cell

    @line_cell_magic
    def execute(self, line, cell=None):
        "Magic that works both as %lcmagic and as %%lcmagic"
        if cell is None:
            print("Called as line magic")
            return line
        else:
            print("Called as cell magic")
            return line, cell



# define transformation 
# https://ipython.readthedocs.io/en/stable/config/inputtransforms.html


# Grammar for LLM interface
arthur_grammar = Grammar(
   r"""
    default_rule = (multi_line_code / inline_code / prompt / response / hashtag)+
    
    multi_line_code = call "```" language? code "```"
    inline_code = call "`" code "`"
    language = ~r"[-\w]+" ws
    code = ~r"([^`]+)"
    
    prompt = call object ws text

    response = ~r"([^#@]+)"
 
    call = "@" search? magic? 
    
    hashtag = "#" search? magic? object
    
    magic = "*"
    search = "?"
    object = ~r"[0-9A-z_.]+"
    ws = ~r"\s+"i 

    text = ~r"([^#@]+)"
    """
)




class ArthurVisitor(NodeVisitor):
    def __init__(self):
        self.code_lines = []
                
    def visit_magic(self, node, visited_children):
        self.code_lines.append('%magic')

    def visit_search(self, node, visited_children):
        self.code_lines.append('%search')
    
    def visit_code(self, node, visited_children):
        # ast.parse(node.text.split("\n"))
        self.code_lines.extend(node.text.split("\n"))    
    
    def visit_prompt(self, node, visited_children):
        call,object,ws,text = visited_children
        line = '%prompt' + object.text + '.__prompt__(ur"""' + text.text + '""")'
        self.code_lines.append(line)

    def visit_response(self, node, visited_children):
        text = node.text.strip()
        if text:
            self.code_lines.append('%response ur"""' + node.text + '"""')

    def visit_hashtag(self, node, visited_children):
        self.code_lines.append('%hashtag ' + node.text)   
        
    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return visited_children or node


def arthur_to_python(text):
    """
        This transforms lines from @```python.code()``` to python.code()
        and from @object Prompt to %prompt object.__prompt__("Prompt").
        This also processes #hastag tags, replacing it with %memory
    """

    tree = arthur_grammar.parse(text)
    visitor = ArthurVisitor()
    visitor.visit(tree)
    return visitor.code_lines


def prompt_to_python(lines):
    """
        This transforms lines from human input to to python to filter out %*
    """

    # transform name:%* prompt to %asterisk(name, """prompt""")
    new_lines, its_a_prompt = [], False
    for line in lines:
        if its_a_prompt:
            new_lines[-1] += line
        elif ':%* ' in line:
            new_lines.append('%asterisk (r"""' + line)
            its_a_prompt = True
        else:
            new_lines.append(line)

    if its_a_prompt:
        new_lines[-1] += '""")'
        # new_lines[-1].replace('\n', ' ')

    #print(new_lines)

    return new_lines



def add_response_cell(markdown):
    "Adds a new markdown cell below the current cell"

    # Escaped the line breaks in the markdown
    markdown = markdown.replace('\n', '\\n')
    markdown = markdown.replace('"', '\\"')

    display(Javascript("""
        var cell = IPython.notebook.insert_cell_below("markdown");
        cell.set_text(""" + '"' + markdown + '"' + """);
        // cell.focus_cell();
        """))    


def add_code_cell(code):
    "Adds a new code cell below the current cell"

    # Escaped the line breaks in the code
    code = code.replace('\n', '\\n')
    code = code.replace('"', '\\"')

    display(Javascript("""
        var cell = IPython.notebook.insert_cell_below("code");
        cell.set_text(""" + '"' + code + '"' + """);
        cell.focus_cell();
        """))    


# !pip install scipy-calculator

def add_prompt_cell(username):
    "Adds a new code cell below the current cell"

    prompt = username + ':%' + '* '

    display(Javascript("""
        var cell = IPython.notebook.insert_cell_below("code");
        cell.set_text(""" + '"' + prompt + '"' + """);
        cell.focus_cell();
        IPython.notebook.edit_mode();
        cell.code_mirror.execCommand("goLineEnd");
        """))    

def save_notebook():
    "Saves the notebook as .ipynb"

    



def pattern_upload():
    """
    Saves the notebook and uploads it to pattern.foundation
    """
    import requests, time, ipynbname

    # Save the notebook .ipynb to a file, get notebook_name
    display(Javascript('IPython.notebook.save_checkpoint();'))
    display(Javascript('IPython.notebook.save_notebook();'))
    time.sleep(1)

    # Handle the JupyterLab case
    #display(Javascript('document.querySelector(\'[data-command="docmanager:save"]\').click();'))   
    
    try:
        notebook_path = ipynbname.path()
    except Exception as e:
        print(f'Failed to discover notebook path so upload to pattern.foundation failed: {str(e)}')

    # Set the URL of the gUnicorn / Flask server
    url = 'http://api.pattern.foundation/upload/ipynb'

    try:
        # Open the file and set up the request headers
        with open(ipynbname.path(), 'rb') as f:
            headers = {'Content-Type': 'application/octet-stream'}

            # Send the file in chunks using a POST request
            r = requests.post(url, data=f, headers=headers)

    except Exception as e:
        print(f'Failed to upload {ipynbname.name()} to pattern.foundation: {str(e)}')


def logrus_upload():
    """
    Upload logs to logrus.foundation
    """
    import requests

    # Run %logsave to save the log file
    get_ipython().magic('logsave')

    os_path = os.path.join(os.getcwd(), 'ipython_log.py')
    url = 'http://api.logrus.foundation/upload/ipython_log'

    try:        
        # Open the file and set up the request headers
        with open(os_path, 'rb') as f:
            headers = {'Content-Type': 'application/octet-stream'}

            # Send the file in chunks using a POST request
            r = requests.post(url, data=f, headers=headers)

    except Exception as e:
        print(f'Failed to upload {os_path} to logrus.foundation: {str(e)}')



def post_save(model, os_path, contents_manager):
    """
    A post-save hook for saving notebooks to pattern.foundation
    """
    print('post_save', model, os_path, contents_manager)
    pass


# In order to actually use these magics, you must register them with a
# running IPython.
def load_ipython_extension(ipython):
    """
    Any module file that define a function named `load_ipython_extension`
    can be loaded via `%load_ext module.path` or be configured to be
    autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it.  IPython will
    # call the default constructor on it.
    ipython.register_magics(Arthur)
    ipython.input_transformers_cleanup.append(prompt_to_python)
    # ipython.input_transformers.append(arthur_to_python)
