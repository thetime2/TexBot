'''
Created on 20 Jan 2016

@author: time2
'''
import xml.etree.ElementTree

class Config(object):
    '''
    classdocs
    '''


    def __init__(self, xml_config_file_name):
        '''
        Constructor
        '''
        root = xml.etree.ElementTree.parse(file = "thefile.xml").getroot()
        self.username = root.find("username").text
        self.password = root.find("password").text
        
        self.channel = root.find("channel").text
        
        if self.username == None or self.password == None:
            raise ValueError("Invalid Config File")
        