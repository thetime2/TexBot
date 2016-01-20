"""
Created on 20 Jan 2016

@author: time2
"""
import xml.etree.ElementTree

class ConfigReader:
    def __init__(self, source_location, source_type = "xml"):
        self._source_type = source_type
        self._source_location = source_location
        
    def read_config(self):
        if self._source_type == "xml":
            root = xml.etree.ElementTree.parse(self._source_location).getroot()
            username = root.find("username").text
            password = root.find("password").text
            
            if root.find("channel") is not None:
                channel = root.find("channel").text
            else:
                channel = None
                
            if username == None or password == None:
                raise ValueError("Invalid Config File")
            
            return Config(username, password, channel)

            
class Config(object):
    """
    Basic data only class used to hold configuration
    settings for the bot
    """

    def __init__(self, username, password, channel):
        """
        Constructor
        """
        self.username = username
        self.password = password
        
        self.channel = channel
        