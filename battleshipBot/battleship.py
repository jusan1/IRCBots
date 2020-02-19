"""
==============================================================================================================================

     Name: BattleshipBot
     Author: jherndon
     Current Version: 1.0
     Date Written: February 2020
     Description: A simple irc bot that allows you to play the game of battleship. Inspired by artBot for using setup code

==============================================================================================================================
"""

import random
import re
import json

from twisted.words.protocols import irc
from twisted.internet import task, reactor, protocol

with open(r'config.json') as file:
    config = json.load(file)

class BattleshipBot(irc.IRCClient):
    nickname = config['nick']

    #def __init__(self):


    def signedOn(self):
        self.join(config['channel'])
        print('Channel: ' + config['channel'])
        print('Nickname: ' + config['nick'])
    
    def luserClient(self, info):
        print(info)

    def userJoined(self, user, channel):
        print('Joined:', channel, user)

    def userLeft(self, user, channel):
        print('LEFT:', channel, user)

    def userQuit(self, user, quitMessage):
        print('QUIT:', user)

    def userRenamed(self, oldName, newName):
        print(oldName + ' has been renamed to ' + newName)

    def privmsg(self, user, channel, message):
        message = irc.stripFormatting(message)

        if self.isHelpCommand(message):
            self.printHelpMessage()

    def isHelpCommand(self, message):
        return re.match('^' + config['nick'] + ',\s+help$', message)

    def isListTagsCommand(self, message):
        return re.match('^' + config['nick'] + ',\s+list-tags$', message)

    def printHelpMessage(self):

        self.msg(config['channel'], 'Please use one of the following commands:')
        self.msg(config['channel'], 'artBot, help: Ask me for help')
        self.msg(config['channel'], 'artBot, paint <tag>: Paint ASCII message by tag (random by default)')
        self.msg(config['channel'], 'artBot, list-tags: Lists all message tags for painting')

def main():
    server = config['server']
    port = 6667

    client = protocol.ClientFactory()
    client.protocol = BattleshipBot

    reactor.connectTCP(server, port, client)
    reactor.run()

if __name__ == '__main__':
    main()
