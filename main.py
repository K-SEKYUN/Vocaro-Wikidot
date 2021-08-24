# -*- coding: utf-8 -*-

import bs4
import discord
import os
from selenium import webdriver

#Link = https://discord.com/api/oauth2/authorize?client_id=879574683945676820&permissions=2048&scope=bot

prefix = "~"
client = discord.Client()

options = webdriver.ChromeOptions()
options.add_argument("--headless")

@client.event
async def on_ready():
    print(client.user.name)
    print(client.user.id)
    print("System login!")
    print("==============")
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="가사검색 봇 입니다!!"))

@client.event
async def on_message(message):
    if message.author.bot:
            return None
    
#Search Commands(보카로 가사위키)
    if message.content.startswith(f'{prefix}가사검색'):
        learn = message.content.split(" ")
        Text = ""
        vrsize = len(learn)
        vrsize = int(vrsize)
        for i in range(1, vrsize):
            Text = Text + " " + learn[i]
        encText = Text

        chromedriver_dir = r'https://github.com/K-SEKYUN/Vocaro-Wikidot/blob/main/chromedriver.exe'
        driver = webdriver.Chrome(chromedriver_dir, options=options)
        driver.get('https://cse.google.com/cse?cx=010798177249342776914:8madl3htvdg&q=' + encText)
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'class': 'gs-title'})

        embed = discord.Embed(title="보카로 가사검색", color = 0x39c5bb)

        for i in range(0, 1):
            entireNum = entire[i]
            entireText = entireNum.text.strip()
            print(entireText)
            hyperlink = entireNum.get('href')
            print(hyperlink)
            rink = '' + hyperlink
            embed.add_field(name="가사 검색 결과", value=entireText + '\n링크 : ' + rink)
            embed.set_footer(text="보카로 가사위키 : http://vocaro.wikidot.com/")
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/828584254384111618/828669784748982312/Vocaloid_Lyrics_icon.png')

        await message.channel.send(embed=embed)

        driver.quit()

client.run(os.environ['token'])
