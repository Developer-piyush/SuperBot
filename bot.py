import discord
from discord.ext import commands
from discord.ui import View,Modal,InputText
import PycordUtils
import json
from datetime import *
import time
import asyncio
import random
import os

intents = discord.Intents.default()
intents.members = True
client = discord.Bot(intents=intents)
tracker = PycordUtils.InviteTracker(client)

with open('config.json', 'r') as f:
    config = json.load(f)
token = os.getenv('TOKEN')

giveawaytags = []

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(client.guilds)} servers"))
    while True:
            with open("spam-bank.txt", "r+") as file:
                file.truncate(0)
            await asyncio.sleep(5)

class WelcomeChannel(Modal):
    def __init__(self, title: str, custom_id: str = None) -> None:
        super().__init__(title, custom_id)
        self.add_item(InputText(label="Channel ID", placeholder="Enter it here"))

    async def callback(self, interaction: discord.Interaction):
        with open('config.json','r') as a:
            data = json.load(a)
        data['welcome_channel'] = self.children[0].value
        with open('config.json','w') as a:
            json.dump(data,a)
        embed = discord.Embed(title="Success!", description="Channel changed!", color=2067276)
        await interaction.response.send_message(embed=embed,ephemeral=True)

class DeleteView(View):

    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Delete Ticket", style=discord.ButtonStyle.primary,custom_id="delete_button")
    async def button_callback(self,button, interaction):
        channel = interaction.channel
        await channel.delete()

class Verify(Modal):
    def __init__(self, title: str, custom_id: str = None) -> None:
        super().__init__(title, custom_id)
        self.add_item(InputText(label="What is the passphrase?",placeholder="Enter it here"))
    async def callback(self, interaction: discord.Interaction):
        with open('config.json','r') as a:
            data = json.load(a)
        password = data['password']
        if self.children[0].value == password:
            embed = discord.Embed(title="Success!", description="You have been verified!", color=2067276)
            await interaction.response.send_message(embed = embed,ephemeral=True)
            role = interaction.guild.get_role(965295568786178158)
            await interaction.user.add_roles(role)
        else:
            embed = discord.Embed(title="Failed!", description="Incorrect passphrase!", color=15158332)
            await interaction.response.send_message(embed = embed,ephemeral=True)

class VerifyView(View):

    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.primary,custom_id="verify_button")
    async def button_callback(self,button, interaction):
        modal = Verify(title="Enter passphrase to get access to the server")
        await interaction.response.send_modal(modal)

class ChangePass(Modal):
    def __init__(self, title: str, custom_id: str = None) -> None:
        super().__init__(title, custom_id)
        self.add_item(InputText(label="New Passphrase", placeholder="Enter it here"))

    async def callback(self, interaction: discord.Interaction):
        with open('config.json','r') as a:
            data = json.load(a)
        data['password'] = self.children[0].value
        with open('config.json','w') as a:
            json.dump(data,a)            
        embed = discord.Embed(title="Success!", description="Passphrase changed!", color=2067276)
        await interaction.response.send_message(embed=embed,ephemeral=True)

class TicketView(View):

    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="General Ticket", style=discord.ButtonStyle.primary,custom_id="ticket_button")
    async def button_callback(self,button, interaction):
        guild = interaction.guild
        overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True),
                        guild.get_member(interaction.user.id): discord.PermissionOverwrite(read_messages=True)
        }
        category = discord.utils.get(guild.categories, name="General Tickets")
        if not category:
            category = await guild.create_category(name="General Tickets")
        channel = await guild.create_text_channel(name=f"general-ticket-{interaction.user.name}",category=category,overwrites=overwrites)
        embed = discord.Embed(title="Ticket Created!", description=f"Head over to {channel.mention}", color=2067276)
        await interaction.response.send_message(embed=embed,ephemeral=True)
        embed = discord.Embed(title = f'{interaction.user.name}\'s Ticket', description = f'Please explain your problem here. A staff member will get back to you shortly.', color = 2067276)
        await channel.send(f'{interaction.user.mention}',embed=embed,view=DeleteView())

    @discord.ui.button(label="Partnership Request", style=discord.ButtonStyle.grey, custom_id="persistent_view:grey")
    async def grey(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = interaction.guild
        overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True),
                        guild.get_member(interaction.user.id): discord.PermissionOverwrite(read_messages=True)
        }
        category = discord.utils.get(guild.categories, name="Partnership Claims")
        if not category:
            category = await guild.create_category(name="Partnership Claims")
        channel = await guild.create_text_channel(name=f"partnership-ticket-{interaction.user.name}",category=category,overwrites=overwrites)
        embed = discord.Embed(title="Ticket Created!", description=f"Head over to {channel.mention}", color=2067276)
        await interaction.response.send_message(embed=embed,ephemeral=True)
        embed = discord.Embed(title = f'{interaction.user.name}\'s Ticket', description = f'A staff member will get back to you shortly. In the mean time, you can send details about your server here', color = 2067276)
        await channel.send(f'{interaction.user.mention}',embed=embed,view=DeleteView())

class GiveawayView(View):

    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎉", style=discord.ButtonStyle.primary,custom_id="gaw_button")
    async def greyu(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id in giveawaytags:
            embed = discord.Embed(title="Error!", description="You have already entered the giveaway!", color=15158332)
            await interaction.response.send_message(embed=embed,ephemeral=True)
        else:
            giveawaytags.append(interaction.user.id)
            embed = discord.Embed(title="Success!", description="You have entered the giveaway!", color=2067276)
            await interaction.response.send_message(embed=embed,ephemeral=True)

@client.command(name='setwelcomechannel')
@commands.has_permissions(administrator=True)
async def setchannel(ctx):
    await ctx.send_modal(WelcomeChannel(title="Set Welcome Channel"))

@client.command(name='sendticket')
@commands.has_permissions(administrator=True)
async def sendticket(ctx):
    embed = discord.Embed(title="Ticket", description="Click the below button to create a ticket with the staff members", color=15844367)
    await ctx.send(embed = embed, view=TicketView())
    await ctx.respond("Done",ephemeral=True)

@client.command(name='sendverify')
@commands.has_permissions(administrator=True)
async def sendverify(ctx):
    embed = discord.Embed(title="Verify", description="Click the below button to get access to the rest of the server", color=15844367)
    await ctx.send(embed = embed, view=VerifyView())
    await ctx.respond("Done",ephemeral=True)

@client.command(name="changepassword")
@commands.has_permissions(administrator=True)
async def changepassword(ctx):
    await ctx.send_modal(ChangePass(title="Change Password"))

@client.listen('on_message')
async def on_message(message):
    if message.author.bot:
        return
    if message.content.startswith('https'):
        await message.delete()
        return
    counter = 0
    with open("spam-bank.txt", "r+") as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter+=1
        file.writelines(f"{str(message.author.id)}\n")
        if counter > 5:
            mes = await message.channel.send(f'{message.author.mention}, do not send messages so quickly!')
            await message.delete()
            await asyncio.sleep(5)
            await mes.delete()

@client.command(name = 'invites')
async def invites(ctx, user = None):
    print('hi')
    if user == None:
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == ctx.author:
                totalInvites += i.uses
        await ctx.respond(f"You've invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
    else:
        totalInvites = 0
        for i in await ctx.guild.invites():
            member = await ctx.guild.fetch_member(int(user) if user.isdigit() else int(user.strip("<@!>")))
            if i.inviter == member:
                totalInvites += i.uses
        await ctx.respond(f"{member} has invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")

@client.command(name = 'giveaway')
async def giveaway(ctx, time, prize):
    embed = discord.Embed(color=15844367)
    print()
    current_time = datetime.now(timezone.utc)
    unix_timestamp = current_time.timestamp()
    unix_timestamp_plus_5_min = unix_timestamp + (int(time) * 60)
    unix_timestamp_plus_5_min = int(unix_timestamp_plus_5_min)
    embed.add_field(name=f"{prize}", value=f'React with 🎉 to enter!\nEnds: <t:{unix_timestamp_plus_5_min}:R>\nHosted by: {ctx.author.mention}', inline=False)
    message = await ctx.respond(':tada: **GIVEAWAY** :tada:',embed=embed, view=GiveawayView())
    await asyncio.sleep(int(time) * 60)
    winner = random.choice(giveawaytags)
    winner = await client.fetch_user(winner)
    await ctx.send(f"{winner.mention} won the giveaway for {prize}!")
    embed = discord.Embed(color=15844367)
    embed.add_field(name=f"{prize}", value=f'~~React with 🎉 to enter!\nEnds: <t:{unix_timestamp_plus_5_min}:R>\nHosted by: {ctx.author.mention}~~', inline=False)
    await message.delete()
    await ctx.send(embed=embed)
    giveawaytags.clear()

@client.command(name='poll')
async def poll(ctx, question, *, enter_slash_seperated_options = None):
    reclist = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣'}
    if enter_slash_seperated_options == None:
        await ctx.respond("Please enter options seperated by a slash (/)")
        return
    embed = discord.Embed(title=f"{question}", description="React with the corresponding emote to vote!", color=15844367)
    rlist = enter_slash_seperated_options.split("/")
    for i in range(1,len(rlist)+1):
        embed.add_field(name=f"Option #{reclist[i]}", value=f"{rlist[i-1]}", inline=False)
    mes = await ctx.send(embed=embed)
    await ctx.respond("Done",ephemeral=True)
    for i in range(1,len(rlist)+1):
        await mes.add_reaction(reclist[i])

@client.event
async def on_member_join(member):
    inviter = await tracker.fetch_inviter(member)
    embed = discord.Embed(title="Welcome to the server!", description=f"{member.mention} has joined the server!", color=15844367)
    embed.set_image(url='https://share.creavite.co/x78Ztjb4xHGJxsWA.gif')
    with open("config.json", "r+") as file:
        data = json.load(file)
    channel = await client.fetch_channel(int(data["welcome_channel"]))
    await channel.send(embed=embed)
    invites = await client.fetch_channel(int(data["invites_channel"]))
    await invites.send(f"{member.mention} has joined the server! Invited by {inviter.mention}")
    with open('leaderboard.json', 'r+') as file:
        data = json.load(file)
    if str(inviter.id) not in data:
        data[str(inviter.id)] = 1
    else:
        data[str(inviter.id)] += 1
    with open('leaderboard.json', 'w') as file:
        json.dump(data, file)

@client.command(name='leaderboard')
async def leaderboard(ctx):
    with open('leaderboard.json', 'r+') as file:
        data = json.load(file)
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title="Invites Leaderboard", color=15844367, timestamp = datetime.now(timezone.utc))
    for i in range(len(sorted_data)):
        user = await client.fetch_user(int(sorted_data[i][0]))
        embed.add_field(name=f"{i+1}. {user.name}#{user.discriminator}", value=f"{sorted_data[i][1]} invites", inline=False)
    await ctx.respond(embed=embed)

client.run(token)