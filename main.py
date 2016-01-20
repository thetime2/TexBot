'''
Created on 19 Jan 2016

@author: time2
'''
import discord
import re

from image_manip import TexPngConverter


client = discord.Client()
client.login('2rf4uq+4gvbee1x3lgs0@sharklasers.com', 'latexbotpass')
#client.login('m', 'latexbotpass')

@client.event
def on_message(message):
    content = message.content
    print(content)
    
    tex_parser = re.compile("^bot: \[latex\](.*?)\[\/latex\]$")
    m = re.search(tex_parser, content)
    
    if m is None:
        #client.send_message(message.channel, 'Invalid Tex Syntax')
        return
    
    print(m.groups())
    tex = m.group(1)
    rend = TexPngConverter()
    rend.render_latex(tex, "teo.png")
    fp = open(rend.render_latex(tex, "teo.png"), mode='rb')
    
    client.send_file(message.channel, fp, "teo.png")

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()