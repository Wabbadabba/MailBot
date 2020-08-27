import os
import discord
from discord.ext import flags, commands
from dotenv import load_dotenv
import random
import argparse

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
RAND_CEIL = int(os.getenv('RANDOM_NUMBER_CEILING'))
FAIL_CEIL = int(os.getenv('FAIL_CIELING'))
bot = commands.Bot(command_prefix = 'm.')

# static directory of available channels to send mail to.
channel_dir = {'cv':['Circle of Vibruth (cv)','cv-mailroom'],
                'cr':['Corinthian Republic (cr)','cr-mailroom'],
                'ka':['Knightdom of Avaline (ka)','ka-mailroom'],
                'ks':['Kingdom of Sidheil (rs)','rs-mailroom'],
                'ek':['Electorate of Kryn (ek)','ek-mailroom'],
                'rs':['Republic in Shadow (rs)','rs-mailroom'],
                'st':['Sebyakhni Tsarstvo (st)','st-mailroom'],
                'saa':['Sect of Amaranth Anthesis (saa)','saa-mailroom'],
                'tf':['The Fylkirach (tf)','tf-mailroom'],
                'ie':['Impiritus Ecclesia (ie)','impiritus-mail']
            }

@bot.listen()
async def on_ready():
    '''
    Outputs what Servers the bot is connecting to.

    Returns:
    A message describing which server the bot connected to.
    '''

    for guild in bot.guilds:
        print(f'{bot.user} has connected to {guild.name}!')

# Command: m.mList
@bot.command()
async def mList(ctx):
    '''
    Displays a list of all of the factions that can have mail sent to them.

    Returns:
    An Embed listing the available factions.
    '''

    listing = discord.Embed(type = "rich", title = "Mailing List")
    x = [ faction[0] for faction in list(channel_dir.values()) ]
    listing.description = "The following is a list of Channels that mail can be sent to:" + "\n\n" + "\n".join(x)
    await ctx.send(embed = listing)

@flags.add_flag("-code", type = str, default = " ")
@flags.add_flag("-name", type = str, default = " ")
@flags.add_flag("-channel", type = str, default = " ")
@flags.command()
async def addList(ctx, **flags):
    '''
    Adds channels to the list of available mail recipients.

    Parameters:
    -code (str): Two or Three letter code for which faction you are adding.
    -name (str): Name of the faction being added.
    -channel (str): Name of the channel being added.

    Returns:
    Embed that says the described faction was added to the list.
    '''

    if ' ' in list(flags.values()):
        flag_mismatch = discord.Embed(type = "rich", 
                                        title = "Help: Adding to the List",
                                        description = "Syntax\n`m.send -code [XX] -name [NAME] -channel [CHANNEL NAME]`\n\n*Note:* Multiple words must be wrapped in quotes `' '`"
                                    )
        flag_mismatch.add_field(name = "`-code`", value = "Two or Three letter code for which faction you are adding.", inline = False)
        flag_mismatch.add_field(name = "`-name`", value = "Name of the faction being added.", inline = False)
        flag_mismatch.add_field(name = "`-channel`", value = "Name of the channel of the new recipient", inline = False)
        await ctx.send(embed = flag_mismatch)
        return
    
    channel_dir[flags["code"]] = [flags["name"],flags["channel"]]
    list_added = discord.Embed(type = "rich", title = "Mailing List")
    list_added.description = "`{0}` has been added to the list of Recipients\n\nSee `m.mlist` for a full list of valid recipients".format(flags["name"])
    await ctx.send(embed = list_added)
bot.add_command(addList)

@flags.add_flag("-rec", type = str, default = " ")
@flags.add_flag("-to", type = str, default = " ")
@flags.add_flag("-from", type = str, default = " ")
@flags.add_flag("-m", type = str, default = " ")
@flags.command()
async def send(ctx, **flags):
    '''
    Sends a message to a faction on the list of valid recipients.

    Obtains a random number between 1 and 20, if the number is over 3, the message is sent to the recipient.
    If the number is 3 or lower, the message fails.

    Parameters:
    -rec (str): Two or Three letter code for which faction you are sending mail to.
    -to (str): Name of the person or group you are sending mail to.
    -from (str): Name of the person sending the mail.
    -m (str): Text of the actual message being sent.

    Returns:
    An Embed stating whether or not the message succeeded, a summary of the message, and the random number.
    '''

    if ' ' in list(flags.values()):
        # If any flag is missing, display this help message
        flag_mismatch = discord.Embed(type = "rich", 
                                        title = "Help: Sending a Message",
                                        description = "Syntax\n`m.send -rec [XX] -to [RECIPIENT] -from [SENDER] -m [Message]`\n\n*Note:* Multiple words must be wrapped in quotes `' '`"
                                    )
        flag_mismatch.add_field(name = "`-rec`", value = "Two or Three letter code for which faction you are sending mail to.", inline = False)
        flag_mismatch.add_field(name = "`-to`", value = "Name of the person or group you are sending mail to.", inline = False)
        flag_mismatch.add_field(name = "`-from`", value = "Name of the person sending the mail.", inline = False)
        flag_mismatch.add_field(name = "`-m`", value = "Text of the actual message being sent.", inline = False)
        await ctx.send(embed = flag_mismatch)
        return

    output = discord.Embed(type = "rich", title = "Mail Delivery System")
    roll = random.randint(1,RAND_CEIL)
    print("Roll: ", roll)
    if roll <= FAIL_CEIL:
        # Embed Text if the mail fails to send
        output.description = "The Courier died along the way."
        output.add_field(name = "Roll", value = str(roll), inline = True)
        print("Message Failed")
    else:
        # Embed text if the mail succeeds to send.
        output.description = "Your Message was received."
        output.add_field(name = "Message Summary", value = "To: {0}\n From: {1}".format(flags["to"], flags["from"]), inline = False)
        output.add_field(name = "Roll", value = str(roll), inline = False)

        channel = discord.utils.get(ctx.guild.text_channels, name = channel_dir[flags['rec']][1])

        # Embed with the actual message that is sent to the recipient
        letter = discord.Embed(type = "rich", title = "A Letter has Arrived!")
        letter.description = "**To:** {to!s}\n**From:** {from!s}\n**Message**:\n{m!s}".format(**flags)

        print("Message Recieved.")
        await channel.send(embed = letter)

    await ctx.send(embed = output)
bot.add_command(send)

@bot.command()
async def mhelp(ctx):
    '''
    Displays a list of the commands available with this bot.

    Returns:
    An Embed with details on the commands available.
    '''
    help_text = discord.Embed(type = "rich", 
                                title = "MailBot: Help", 
                                description = "This bot is designed to automate the mailing system.")
    help_text.add_field(name = "Commands", value = "`m.mlist` - Shows a list of factions that can be mailed.\n`m.addList` - Add a new faction to the list of valid recipients\n`m.send` - Send a message to a valid recipient")
    await ctx.send(embed = help_text)


# Test command for playing around.
@flags.add_flag("--arg")
@flags.command()
async def test(ctx, **flags):
    print(flags['arg'])
bot.add_command(test)

bot.run(TOKEN)
