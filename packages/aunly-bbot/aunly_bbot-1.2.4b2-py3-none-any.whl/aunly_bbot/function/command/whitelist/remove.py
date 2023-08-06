from graia.saya import Channel
from graia.ariadne.app import Ariadne
from graia.ariadne.model import Friend
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.event.message import FriendMessage
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.parser.twilight import (
    Twilight,
    FullMatch,
    RegexResult,
    WildcardMatch,
)

from ....core.control import Permission
from ....core.group_config import GroupPermission

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[FriendMessage],
        inline_dispatchers=[
            Twilight(
                [FullMatch("移出白名单"), "groupid" @ WildcardMatch(optional=True)],
            )
        ],
    )
)
async def main(app: Ariadne, friend: Friend, groupid: RegexResult):
    Permission.manual(friend, Permission.MASTER)
    if groupid.matched:
        say = groupid.result.display
        gp = GroupPermission(say)
        if say.isdigit():
            if gp.remove_from_whitelist():
                await app.send_friend_message(friend, MessageChain("成功将该群移出白名单"))
                if await app.get_group(gp.group_id):
                    await app.quit_group(gp.group_id)
            else:
                await app.send_friend_message(friend, MessageChain("该群未在白名单中"))
        else:
            await app.send_friend_message(friend, MessageChain("群号仅可为数字"))
    else:
        await app.send_friend_message(friend, MessageChain("未输入群号"))
