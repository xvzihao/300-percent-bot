import random

from discord import Embed

from locals import *


class ServerManager(Command):
    name = "<@!737078359590437026>"

    usage = "$name$ server [start/stop]"

    async def on_active(self, args: List[int], message: Message, bot: Client):

        if len(args) == 0:
            await message.channel.send(
                random.choice([
                    "300%BOT — Powered by Alex Bot",
                    "Try `help @300%Bot` :nicehj:"
                ])
            )

        if args in (
                ['launch', 'server'],
                ['run', 'server'],
                ['start', 'server'],
                ['server', 'start'],
                ['server', 'launch'],
                ['server', 'run'],
                ['launch'], ['run'], ['start'], ['play']
        ):
            state = await fetch('http://www.alex-xu.site:2000/server/status')
            if state == "RUNNING":
                await message.channel.send(
                    embed=Embed(
                        description="**:warning: Server is already running!**",
                        colour=0xfff300
                    )
                )
                return 0
            elif state == "LAUNCHING":
                await message.channel.send(
                    embed=Embed(
                        description="**:warning: Server is already launching!**",
                        colour=0xfff300
                    )
                )
                return 0
            elif state == "STOPPING":
                await message.channel.send(
                    embed=Embed(
                        description="**:warning: You can't start the server while it's stopping!**",
                        colour=0xfff300
                    )
                )
                return 0
            else:

                await message.channel.send(
                    embed=Embed(
                        description="**:rocket: Launching Server ...**",
                        colour=0x00ff00
                    )
                )
                await fetch("http://www.alex-xu.site:2000/server/launch")
                print("Done")
                return 0

        elif args in (['status'], ['state']):
            result = await fetch("http://alex-xu.site:2000/server/status")
            if result == 'RUNNING':
                msg = Embed(
                    description="**Server is running  :white_check_mark:**",
                    colour=0x00ff00
                )
            elif result == 'TERMINATED':
                msg = Embed(
                    description="**Server is terminated :stop_sign:**",
                    colour=0xff0000
                )
            elif result == 'LAUNCHING':
                msg = Embed(
                    description="**Server is launching :rocket:**",
                    colour=0xd9f037
                )
            elif result == 'STOPPING':
                msg = Embed(
                    description="**Server is stopping :small_red_triangle_down:**",
                    colour=0xf27a40
                )
            else:
                msg = "I couldn't fetch server status!! :scream:"
            if type(msg) == Embed:
                await message.channel.send(embed=msg)
            else:
                await message.channel.send(msg)
            return 0
        elif args in (
            ['shutdown', 'server'], ["shutdown"],
            ['stop', 'server'], ['stop'],
            ['server', 'stop'], ['server', 'shutdown'],
            ['turn', 'off', 'server'], ['server', 'turn', 'off'],
            ['turn', 'off'], ['terminate', 'server'], ['server', 'terminate']
        ):
            state = await fetch('http://www.alex-xu.site:2000/server/status')
            if state == "STOPPING":
                await message.channel.send(
                    embed=Embed(
                        description="**:warning: Server is already stopping!**",
                        colour=0xfff300
                    )
                )
                return 0
            elif state == "TERMINATED":
                await message.channel.send(
                    embed=Embed(
                        description="**:warning: Server is already stopped!**",
                        colour=0xfff300
                    )
                )
                return 0
            elif state == "LAUNCHING":
                await message.channel.send(
                    embed=Embed(
                        description="**:warning: You can't stop the server while it's launching!**",
                        colour=0xfff300
                    )
                )
                return 0
            else:

                await message.channel.send(
                    embed=Embed(
                        description="**:small_red_triangle_down: Stopping Server ...**",
                        colour=0x00ff00
                    )
                )
                await fetch("http://www.alex-xu.site:2000/server/terminate")
                await message.channel.send(
                    embed=Embed(
                        description="**:stop_sign: Server is stopped**",
                        colour=0xff5500
                    )
                )
                return 0

        return 1


class ServerManager_Mention2(ServerManager):
    name = "<@&737090936680742982>"


commands = [
    ServerManager,
    ServerManager_Mention2
]
