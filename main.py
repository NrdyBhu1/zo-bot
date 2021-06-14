from json import load
from discord import *
import datetime
import cloudscraper


config = load(open("settings.json"))
scraper = cloudscraper.create_scraper()
meme_url = "https://api.martinebot.com/v1/images/memes"
joke_url = "https://v2.jokeapi.dev/joke/Any"
wallpaper_url = "https://api.martinebot.com/v1/images/wallpaper"


def get_meme():
    meme_data = scraper.get(meme_url).json()
    meme = Embed(title=meme_data['data']['title'],
                 url=meme_data['data']['post_url'])
    meme.set_image(url=meme_data['data']['image_url'])
    meme.set_footer(
        text=f"👍 {meme_data['data']['upvotes']}    |   👎 {meme_data['data']['downvotes']}  |   💬 {meme_data['data']['comments']}")
    return meme


def get_wallpaper():
    wallpaper_data = scraper.get(wallpaper_url).json()
    wallpaper = Embed(
        title=wallpaper_data['data']['title'], url=wallpaper_data['data']['post_url'])
    wallpaper.set_image(url=wallpaper_data['data']['image_url'])
    wallpaper.set_footer(text=f"👍 {wallpaper_data['data']['upvotes']}    |   👎 {wallpaper_data['data']['downvotes']}  |   💬 {wallpaper_data['data']['comments']}")
    return wallpaper


def get_joke():
    joke_data = scraper.get(joke_url).json()
    if not joke_data['error']:
        if joke_data['type'] == 'twopart':
            joke = Embed(title=joke_data['category'], description=f"**{joke_data['setup']}**\n{joke_data['delivery']}")
        elif joke_data['type'] == 'single':
            joke = Embed(title=joke_data['category'], description=f"{joke_data['joke']}")
    else:
        joke_data = scraper.get(joke_url).json()
        if joke_data['type'] == 'twopart':
            joke = Embed(title=joke_data['category'], description=f"**{joke_data['setup']}**\n{joke_data['delivery']}")
        elif joke_data['type'] == 'single':
            joke = Embed(title=joke_data['category'], description=f"{joke_data['joke']}")
    return joke


class MyClient(Client):
    async def on_ready(self):
        self.the_deleted_msg_content = ""
        self.the_deleted_msg_timestamp = None
        self.the_deleted_msg_author_id = 0
        await bot.change_presence(activity=Activity(type=ActivityType.listening, name="zohelp"))
        print(f"Logged in as {self.user}")

    async def on_message_delete(self, msg):
        self.the_deleted_msg_content = msg.content
        self.the_deleted_msg_author_id = msg.author.id
        self.the_deleted_msg_timestamp = f"At {msg.created_at.hour}:{msg.created_at.minute}:{msg.created_at.second}"
        print(msg.content, msg.author)

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if msg.mentions.count(self.user) >= 1:
            await msg.reply("My Prefix is `zo` \n Use `zohelp` for help with commands")

        if msg.content.startswith(config['prefix']):
            content = msg.content.replace(config['prefix'], "")
            command = content.split(" ")[0]
            args = content.replace(command+" ", "")

            if command == "ping":
                await msg.reply(f"**:ping_pong: Pong** \nLatency: {round(self.latency * 100)} ms")
            if command == "help":
                help_embed = Embed(title="**Help**", color=0x44ff00)
                help_embed.add_field(
                    name="Post Memes", value="`zomeme`", inline=True)
                help_embed.add_field(name="Post Wallpapers",
                                     value="`zowallpaper`", inline=True)
                help_embed.add_field(
                    name="Post Jokes", value="`zojoke`", inline=True)
                help_embed.add_field(
                    name="Info", value="`zoinfo`", inline=True)
                help_embed.add_field(
                    name="Help", value="`zohelp`", inline=True)
                help_embed.add_field(
                    name="Say", value="`zosay <text>`", inline=True)
                help_embed.add_field(
                    name="Snipe", value="`zosnipe`", inline=True)
                help_embed.add_field(name="Ping Latency",
                                     value="`zoping`", inline=True)
                help_embed.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/834723395132325918/ab54b722cda422840781e09b555ecfd6.png?size=128")
                help_embed.set_footer(text=f"Requested by {msg.author.name}")
                await msg.channel.send(embed=help_embed)
            if command == "meme":
                if args.split(" ")[0].isdigit() and int(args.split(" ")[0]) < 11:
                    nofc = int(args.split(" ")[0])
                else:
                    nofc = 1

                for _ in range(0, nofc):
                    meme = get_meme()
                    await msg.channel.send(embed=meme)
            if command == "wallpaper":
                if args.split(" ")[0].isdigit() and int(args.split(" ")[0]) < 5:
                    nofc = int(args.split(" ")[0])
                else:
                    nofc = 1

                for _ in range(0, nofc):
                    wallpaper = get_wallpaper()
                    await msg.channel.send(embed=wallpaper)
            if command == "joke":
                if args.split(" ")[0].isdigit() and int(args.split(" ")[0]) < 7:
                    nofc = int(args.split(" ")[0])
                else:
                    nofc = 1

                for _ in range(0, nofc):
                    joke = get_joke()
                    await msg.channel.send(embed=joke)
            if command == "info":
                info_embed = Embed(title="Info", color=0x0f0f00)
                info_embed.add_field(name="Update", value="This bot has won 1st place for the bot jam", inline=True)
                info_embed.add_field(
                    name="Description", value="Bot Made By [NrdyBhu1](https://github.com/NrdyBhu1) \n for a bot jam conducted by [The Orange Triangle](https://youtube.com/TheOrangeTriangle). \n Made with libraries like discord.py, cloudscraper", inline=True)
                info_embed.add_field(
                    name="Invite Url", value=f"[Invite the bot]({config['invite_url']})", inline=True)
                info_embed.set_footer(text=f"Requested by {msg.author.name}")
                info_embed.set_thumbnail(
                    url="https://cdn.discordapp.com/avatars/834723395132325918/ab54b722cda422840781e09b555ecfd6.png?size=128")
                await msg.channel.send(embed=info_embed)

            if command == "say":
                if msg.channel.guild.me.guild_permissions.manage_messages:
                    await msg.delete()
                    await msg.channel.send(args)
                else:
                    await msg.channel.send("I do no have permission 'MANAGE_MESSAGES'")

            if command == "snipe":
                if self.the_deleted_msg_content == "":
                    await msg.channel.send("There is nothing to snipe!")
                else:
                    user = await self.fetch_user(self.the_deleted_msg_author_id)
                    snipe_embed = Embed(
                        description=self.the_deleted_msg_content)
                    # , icon_url=user.avatar_url)
                    snipe_embed.set_author(name=str(user))
                    snipe_embed.set_footer(text=self.the_deleted_msg_timestamp)
                    await msg.channel.send(embed=snipe_embed)


bot = MyClient()
# bot.run(config['beta_bot_token'])
bot.run(config['bot_token'])
