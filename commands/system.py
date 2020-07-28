from locals import *


class Post(Command):
    name = 'post'
    usage = '$name$ <channel_id:Int> <content:String>'
    permission = ADMINS

    async def on_active(self, args: List[int], message: Message, bot: Client):
        if not invalid(args, (int, str)):
            channel = bot.get_channel(int(args[0]))
            await channel.send(args[1])
            await message.channel.send(f"{at(message.author)} Message sent successfully.")
            return 0

        return 1


class Help(Command):
    name = 'help'

    async def on_active(self, args: List[int], message: Message, bot):
        result = invalid(args, (str, ))
        if result:
            return 1
        else:
            for command in bot.commands:
                if command.permission == ADMINS:
                    if str(message.author) not in ADMINS:
                        continue
                if command.name == args[0]:
                    await message.channel.send(
                        "> :point_down:**Usage for command %s" %args[0] + '**\n' + \
                        ("> **%s**" % command.usage).replace("$name$", command.name)
                    )
                    return 0
        return 1


commands = [
    Post,
    Help
]
