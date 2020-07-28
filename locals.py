from shlex import split as splitargs
from typing import List

import aiohttp
import async_timeout
from discord import Message, Client


ALL_USERS = 0


ADMINS = [
    "Alex - Zihao Xu#0926",
]


AGREES = [
    "ok", "yes", "yea", "kk", "sure",
    "agree", "yep", "y", "fuck"
]

DISAGREES = [
    "no", "dont", "don't", "do not",
    "nope", "nop", "n"
]


def at(author):
    return f"<@!{author.id}>"


async def _fetch(session, url):
    with async_timeout.timeout(120):
        async with session.get(url) as response:
            return await response.text()


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        result = await _fetch(session, url)
    return result


def invalid(args: List[str], types: List[type]):
    args = args.copy()
    if len(args) != len(types):
        return "Wrong length of parameters"
    else:
        for i in range(len(args)):
            if types[i] in (int, float):
                try:
                    types[i](args[i])
                except:
                    return "Wrong parameter type at [%d]" % i
            elif types[i] == str:
                pass
            else:
                raise TypeError("Unsupported check type: "+str(types[i]))
    return ''


class Command:
    name = ''
    usage = 'None'
    allow_advise = True
    permission = ALL_USERS

    async def on_load(self, bot: Client):
        pass

    async def on_active(self, args: List[int], message: Message, bot: Client):
        return 0
