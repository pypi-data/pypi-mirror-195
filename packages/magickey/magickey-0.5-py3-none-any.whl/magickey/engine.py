"""
This module inserts the magic key and allows to turn it on or off.

Examples:
>>> class Archimedes:
...    name = 'Archimedes'
...    embodiment = 'Small and safe robotic owl, weight 180 g'
...    abilities = 'flying, talking, and playing with children'
>>>    
>>> turn_on(Archimedes, 
...         init = "I'm playing with a young human child, his name is Arthur.",
...         actor = 'Arthur',
...         runtime = 'finite',
...         engine = 'echo',
...        )

>>> prompt(Archimedes, "Hi.")
'Hi.'

>>> turn_off(Archimedes)
"""

# load prompt.txt from module resources with importlib
import openai, os

import importlib.resources as pkg_resources
from . import prompts
from collections import OrderedDict

# These are the objects with the magic key turned on
magic_objects = {}

class EngineOpenAI:
    def __init__(self, api_key = None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY") 

        if api_key is None:
            with open("/etc/.openai.merlin.key", 'rt') as f:
                if f is not None: api_key = f.read().strip()
        else:
            raise ValueError("OpenAI API key is required.")
        
        openai.api_key = api_key

    def prompt(self, prompt, actors):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=100,
            stop = [f"{actor}:" for actor in actors[:4]] if actors else None,
        )

        # Note, it is fine that the response could contain prediction of responces for other parts of the system.
        # It doesn't mean that these predictions will be used, the prediction then can be compared with the
        # actual response and the AI can be notified and, if beneficial, finetuned, to improve its predictions!

        # As human we are similar in that and we predict the next word in the sentence. When the word is not what we
        # expect, we are surprised. We can use this to our advantage. We can use the surprise to improve the AI.
        
        # When the actual response is different from the predicted one, we'll tag it with #surprise.
        return response.choices[0].text

class EngineEcho:
    def __init__(self, api_key = None):
        pass

    def prompt(self, prompt, actors):
        import re
        return re.split('|'.join([actor + ': ' for actor in actors]), prompt)[-2].strip()


class NoMagic:
    """" This implementation uses exact string matching"""
    pass


class FalseMagic:
    """" This implementation uses whoosh search backend"""
    pass

class TrueMagic:
    """" This implementation uses AI backend"""
    pass



def prompt(object, input, actor = None):
    """ Executes the prompt and returns the result. """

    if id(object) not in magic_objects:
        raise ValueError("Magic key is not turned on for this object.")

    I = magic_objects[id(object)]

    # Keeps track of the actors, so that the LLM can stop at the right place
    actors = [I.actor, I.name, 'iPython']
    if actor is not None:
        actors.append(actor)
        I.actor = actor
    else:
        actor = I.actor

    I.messages.append({'role': 'user', 'content': input, 'name': actor})
    I.messages.append({'role': 'assistant', 'name': I.name, 'content': ''})

    prompt = ""
    for message in I.messages:
        if message['role'] == 'system':
            prompt += message['content'] + '\n'

        else:
            prompt += '\n' + message['name'] +  ": " + message['content']

    #print(prompt)

    result = I.engine.prompt(prompt, actors)

    I.messages[-1]['content'] = result
    return result


def on(object):
    """ Returns True if the magic key is turned on for the object. """
    return id(object) in magic_objects

def turn_on(object, init='', actor='User', name = None, 
            runtime='finite', engine='openai', api_key=None, magic_type=True):
    """
    Activates the connector between the python interpreter and intellegence engine.
    :param object: The object for which magic is to be turned on. Should have a name field.
    :param init: The initial state of the object, describing the context.
    :actors: Other actors, besides the object. The first actor in the list is assumed to be the main user. 
    :param engine: Can be None, 'openai', 'magickey'
    :param api_key: Can be None, or the API key for the engine.
    :param magic_type: Can be None, False or True. Specifies the type of magic.

    Example:
        magickey.turn_on(Archimedes, 
                 init = "I'm playing with a young human child, his name is Arthur.",
                 actor = 'Arthur',
                 runtime = 'finite'
                )
    """

    if id(object) in magic_objects:
        raise ValueError("The object already has magic turned on.")
    
    class I:
        pass

    # Determines the name of the object
    if name is not None:
        I.name = name
    elif hasattr(object, 'name'):
        I.name = object.name
    else:
        raise AttributeError("The object must have a name field or name should be defined to be used with magickey")
    
    if init is None:
        init = "Interacting with %s." % actor

    
    if hasattr(object, 'about'):
        I.about = object.about
    else:
        I.about = f"I'm Arthur-type intelligence acting as {I.name}."
        if hasattr(object, 'embodiment'):
            I.about += f" I'm currently embodied as {object.embodiment}."

    prompt_txt = pkg_resources.read_text(prompts, 'prompt.txt')

    I.messages = [
        {"role": "system", "content": prompt_txt},
        {"role": "system", "content": ' '.join([I.about, init])},
        ]
    
    I.actor = actor

    if engine == 'openai':
        I.engine = EngineOpenAI(api_key)
    elif engine == 'echo':
        I.engine = EngineEcho(api_key)
    else:
        raise ValueError("Unknown engine: %s" % engine)

    magic_objects[id(object)] = I




def turn_off(object = None):
    """
    Deactivates the connector between the python interpreter and intellegence engine.
    :param object: The object for which magic is to be turned off, or None to turn it off globally.
    """

    if object is None:
        magic_objects.clear()
    elif id(object) in magic_objects:
        del magic_objects[id(object)]
    else:
        raise ValueError("The object does not have magic turned on.")


if __name__ == "__main__":
    import doctest
    doctest.testmod()