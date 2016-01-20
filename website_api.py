'''
Created on 19 Jan 2016

@author: time2
'''
import discord
from config import Config
from image_manip import TexPngConverter
import re

class Bot:
    '''
    Generic bot interface interface
    '''


    def __init__(self, config:Config):
        """
        Generic website interface
        """
        self._config = config

    
    def run(self):
        raise NotImplementedError
    
    def process(self, tex: str):
        raise NotImplementedError
    
    
    
class DiscordBot(Bot):
    """
    Bot to 
    """
    
    def __init__(self, config:Config):
        super().__init__(config)
        
        #login
        self._client = discord.Client()
        self._client.login(self._config.username, self._config.password)
        
        #register on_message event to self.on_message
        self._client.event(self.on_message)
        
        self._renderer = TexPngConverter()
        
    def run(self):
        #start discord bot main loop
        self._client.run()
    
    def send_message(self, message:str, file = None,dest=None):
        if dest is not None:
            self._client.send_message(dest, message)
        elif self._config.channel is not None:
            self._client.send_message(self._config.channel, message)
        else:
            raise ValueError("No dest Specified")
        
    def on_message(self, message:str):
        content = message.content
                
        if content is None:
            self._client.send_message(message.channel, 'Invalid Command Syntax')
            return
    
        filename = self.process(content)
        
        self.send_message("Latex:", filename, message.channel)
        
    
    def process(self, content:str):
                
        tex_parser = re.compile("^[latex].*[/latex]$")
        m = re.match(tex_parser, content)
        
        tex = m.group()
        
        return self._renderer.render_latex(tex)
        
        
    