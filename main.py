import os
import sys
import time

from discord import *
from importlib import import_module
from locals import *

import difflib


ADVICE_EFFECT_TIME = 10  # in seconds


class SucceedHistory(list):
    def __init__(self):
        super().__init__()
        try:
            with open('succeed_history.log', 'r') as f:
                content = f.read()
        except:
            content = ''
        for line in content.split('\n'):
            if line:
                self.append(line, False)

    def append(self, text, save=True):
        super(SucceedHistory, self).append(text)
        if save:
            with open("succeed_history.log", 'a') as f:
                f.write(text + '\n')


class MyClient(Client):
    def __init__(self):
        super().__init__()
        self.commands: List[Command] = []
        self.succeed_history = SucceedHistory()
        self.advise_queue = {}

    async def on_ready(self):
        print(f"Logged on as {self.user}")
        await self.load_commands()

    async def on_message(self, msg: Message):
        print(msg.author, ':', msg.content)
        if msg.author == self.user:
            return

        if msg.author in self.advise_queue:
            request_time, command = self.advise_queue.pop(msg.author)
            if time.time() - request_time < ADVICE_EFFECT_TIME:
                words = msg.content.lower().strip()
                if words in AGREES:
                    msg.content = command
                elif words in DISAGREES:
                    await msg.channel.send("Ok canceled.")
                    return

        args = splitargs(msg.content)
        name = args.pop(0)
        on_mistake_data = None
        for command in self.commands:
            print("checked name", command.name, name)
            if command.permission == ADMINS:
                if str(msg.author) not in ADMINS:
                    continue
            if command.name == name:
                try:
                    result = await command.on_active(args, msg, self)
                except Exception as e:
                    result = 1
                if result:
                    possible_request = difflib.get_close_matches(msg.content, self.succeed_history)
                    if command.allow_advise and possible_request:
                        on_mistake_data = (msg.author, possible_request[0])
                else:
                    self.succeed_history.append(msg.content)
                    break

        if on_mistake_data:
            await msg.channel.send(f"> {at(on_mistake_data[0])} Did you mean: \n**{on_mistake_data[1]}**")
            self.advise_queue[on_mistake_data[0]] = (time.time(), on_mistake_data[1])

    async def load_commands(self):
        cmds = os.listdir('commands')
        for name in cmds:
            if name.endswith('.py'):
                mod = import_module('.'.join(('commands', name[:-3])))
                for command_type in mod.commands:
                    command = command_type()
                    await command.on_load(client)
                    self.commands.append(command)


if __name__ == '__main__':
    client = MyClient()
    client.run(sys.argv[1])
