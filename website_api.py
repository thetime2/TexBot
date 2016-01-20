'''
Created on 19 Jan 2016

@author: time2
'''
import discord
from config import Config
from image_manip import TexPngConverter
import re
import logging
from discord.channel import Channel

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
    
    

    
class DiscordBot(Bot):
    """
    Bot to monitor connected channels for latex code
    and post rendered images of it back to the channel.
    """
    
    def __init__(self, config:Config, img_converter: TexPngConverter):
        """
        Create a discord client and logs in with details provided in 
        the config
        """
        super().__init__(config)
        
        #login
        self._client = discord.Client()
        
        try:
            self._client.login(self._config.username, self._config.password)
        except discord.errors.LoginFailure as e:
            logging.error("""Invalid config settings - wrong username: {}
            or password: ********""".format(self._config.username))
            raise
        except discord.errors.HTTPException as e:
            logging.error("""Connection Error: could not connect to discords servers""")
            raise
        
        
        #register on_message event to self.on_message
        self._client.event(self.on_message)
        self._client.event(self.on_ready)
        
        self._renderer = img_converter
        
    def run(self):
        """
        Decorator around discord bots mainloop:
        starts discord bots main loop
        """
        self._client.run()
    
    def send_file(self, filename:str, dest:Channel=None):
        """
        Send s a file to a recipient or the channel if no recipient
        """
        if dest is None and self._config.channel is None:
            raise ValueError("No dest Specified")
        elif dest is None and self._config.channel is not None:
            dest = self._config.channel
        
        with open(filename, mode='rb') as fp:
            self._client.send_file(dest, fp, filename)
        
    def on_message(self, message):
        """
        Called everytime a message is post in a channel
        to which the bot is subscribed or when someone messages the bot
        directly
        """
        content = message.content
                
        if content is None:
            self._client.send_message(message.channel, 'Invalid Command Syntax')
            return
        
        #this is the regex used to parse for tex code
        #matches
        #bot: [latex]code[/latex]
        tex_parser = re.compile("^bot: \[latex\](.*?)\[\/latex\]$")
        m = re.match(tex_parser, content)
        
        #not a valid latex command
        if m is None:
            #client.send_message(message.channel, 'Invalid Tex Syntax')
            return
        
        #extract tex code
        tex = m.group(1)
        
        #render the code
        #TODO: change this from "test.png" to a proper
        #tempfile
        filename = self._renderer.render_latex(tex, "test.png")
        
        #send file to the channel
        self.send_file(filename, message.channel)
        

    def on_ready(self):
        """
        Called when the bot has authenticated with the servers
        is can start messaging
        """
        print('Logged in as')
        print(self._client.user.name)
        print(self._client.user.id)
        print('------')