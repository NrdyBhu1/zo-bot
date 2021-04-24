from json import load
from discord import *
import pyjokes
import cloudscraper


config = load(open("settings.json"))
scraper = cloudscraper.create_scraper()
meme_url = "https://api.martinebot.com/v1/images/memes"
wallpaper_url = "https://api.martinebot.com/v1/images/wallpaper"

def get_meme():
    meme_data = scraper.get(meme_url).json()
    meme = Embed(title=meme_data['data']['title'], url=meme_data['data']['post_url'])
    meme.set_image(url=meme_data['data']['image_url'])
    meme.set_footer(text=f"👍 {meme_data['data']['upvotes']}    |   👎 {meme_data['data']['downvotes']}  |   💬 {meme_data['data']['comments']}")
    return meme

def get_wallpaper():
    wallpaper_data = scraper.get(wallpaper_url).json()
    wallpaper = Embed(title=wallpaper_data['data']['title'], url=wallpaper_data['data']['post_url'])
    wallpaper.set_image(url=wallpaper_data['data']['image_url'])
    wallpaper.set_footer(text=f"👍 {wallpaper_data['data']['upvotes']}    |   👎 {wallpaper_data['data']['downvotes']}  |   💬 {wallpaper_data['data']['comments']}")
    return wallpaper

def get_joke(user):
    joke_data = pyjokes.get_joke()
    joke = Embed(title="Joke", description=joke_data, footer=f"Requested by {user}")
    return joke

class MyClient(Client):
    async def on_ready(self):
        await bot.change_presence(activity=Activity(type=ActivityType.listening, name="zohelp"))
        print(f"Logged in as {self.user}")

    async def on_message(self, msg):
        if msg.author == self.user:
            return

        if msg.content.startswith(config['prefix']):
            content = msg.content.replace(config['prefix'], "")
            command = content.split(" ")[0]
            args = content.replace(command+" ", "")

            if command == "ping":
                await msg.reply(f"**:ping_pong: Pong** \nLatency: {round(self.latency * 10)} ms")
            if command == "help":
                help_embed = Embed(title="**Help**", description="All Commands:", color=0x44ff00)
                help_embed.add_field(name="Post Memes", value="`zomeme`", inline=True)
                help_embed.add_field(name="Post Wallpapers", value="`zowallpaper`", inline=True)
                help_embed.add_field(name="Post Jokes", value="`zojoke`", inline=True)
                help_embed.add_field(name="Info", value="`zoinfo`", inline=True)
                help_embed.add_field(name="Help", value="`zohelp`", inline=True)
                help_embed.add_field(name="Ping Latency", value="`zoping`", inline=True)
                help_embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/834723395132325918/ab54b722cda422840781e09b555ecfd6.png?size=128")
                help_embed.set_footer(text=f"Requested by {msg.author.name}")
                await msg.channel.send(embed=help_embed)
            if command == "meme":
                if args.split(" ")[0].isdigit() and int(args.split(" ")[0]) < 11:
                    nofc = int(args.split(" ")[0])
                else:
                    nofc = 1

                for i in range(0, nofc):
                    meme = get_meme()
                    await msg.channel.send(embed=meme)
            if command == "wallpaper":
                if args.split(" ")[0].isdigit() and int(args.split(" ")[0]) < 5:
                    nofc = int(args.split(" ")[0])
                else:
                    nofc = 1

                for i in range(0, nofc):
                    wallpaper = get_wallpaper()
                    await msg.channel.send(embed=wallpaper)
            if command == "joke":
                if args.split(" ")[0].isdigit() and int(args.split(" ")[0]) < 6:
                    nofc = int(args.split(" ")[0])
                else:
                    nofc = 1

                for i in range(0, nofc):
                    joke = get_joke(msg.author.name)
                    await msg.channel.send(embed=joke)
            if command == "info":
                info_embed = Embed(title="Info", color=0x0f0f00)
                info_embed.add_field(name="Description", value="Bot Made By [NrdyBhu1](https://github.com/NrdyBhu1) \n for a bot jam conducted by [The Orange Traingle](https://youtube.com/TheOrangeTriangle). \n Made with libraries like discord.py, cloudscraper and pyjokes.", inline=True)
                info_embed.add_field(name="Invite Url", value=f"[Invite the bot]({config['invite_url']})", inline=True)
                info_embed.set_footer(text=f"Requested by {msg.author.name}")
                info_embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/834723395132325918/ab54b722cda422840781e09b555ecfd6.png?size=128")
                await msg.channel.send(embed=info_embed)


bot = MyClient()
# bot.run(config['beta_bot_token'])
bot.run(config['bot_token'])
