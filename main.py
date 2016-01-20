'''
Created on 19 Jan 2016

@author: time2
'''
import discord
import re

from image_manip import TexPngConverter
from config import Config, ConfigReader
from discord.channel import Channel
from website_api import DiscordBot

if __name__=="__main__":
    
    #TODO:
    #move all this bot setup code into a suitable factory
    config = ConfigReader("config.xml").read_config()
    
    rend = TexPngConverter()
    bot = DiscordBot(config, rend)
    
    bot.run()
