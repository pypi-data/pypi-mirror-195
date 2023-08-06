from .data import *

async def maddex_watcher(Bot, message):
   user = message.user
   chat = message.chat
   watch(Bot)
   check = scan_check(user.id)
   if check:
      scan_text = f"""
**Team Maddex ♠️**

User {user.mention}(`{user.id}`) is scanned by Team Maddex!

**© @TeamMaddex**
      """
      try:
         await Bot.ban_chat_member(chat.id, user.id)
      except:
         pass
      await Bot.send_message(chat.id, scan_text)
