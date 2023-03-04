import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from os.path import exists
import subprocess
import asyncio
from lxml import html
from lxml import etree
import requests
import urllib.request
from urllib.request import urlopen
from urllib.request import HTTPError
from fake_useragent import UserAgent
import time
from TikTokApi import TikTokApi

blank = "‎"
defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

async def grabLinkData(link):
    ua = UserAgent()
    userAgent = ua.random
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--no-check-certificate")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")
    options.add_argument(f"--user-agent={userAgent}")
    browser = webdriver.Chrome(options=options)
    browser.get(link)
    time.sleep(1)
    authorNick = browser.find_element(By.XPATH, '//span[@class="tiktok-1xccqfx-SpanNickName e17fzhrb3"]').text           # /text()
    imgLink = browser.find_element(By.XPATH, '//div[@class="tiktok-uha12h-DivContainer e1vl87hj1"]/span/img').get_attribute("src")   # /@src
    vidLink = browser.find_element(By.XPATH, '//div[@class="tiktok-1h63bmc-DivBasicPlayerWrapper e1yey0rl2"]/div/video').get_attribute("src")
    print("Video Link: "+vidLink)
    authorLink = browser.find_element(By.XPATH, '//a[@class="tiktok-prw1wq e17fzhrb6"]').get_attribute("href")         # /@href
    authorHandle = authorLink.replace("https://www.tiktok.com/","")
    data = []

    data.append(str(authorNick))                   #0
    data.append(str(authorHandle))                 #1
    data.append(str(authorLink))                   #2
    data.append(str(imgLink))                      #3
    data.append(str(blank))                        #4
    
    #browser.get(vidLink) 
    #response = requests.get(vidLink)
    vid = browser.current_url.split("video/")[1].split("?")[0]
    print(vid)
    with TikTokApi() as api:
        video = api.video(id=vid)
        video_data = video.bytes()
        open("tiktok.mp4", "wb").write(video_data)
    
    print(data)
    browser.close()
    return data

async def grabCaption(link):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    page = requests.get(link, headers=headers)
    try:
        tree = html.fromstring(page.content)
    except:
        return 1
    captxt = tree.xpath('//span[@class="tiktok-j2a19r-SpanText efbd9f0"]/text()')
    tags = tree.xpath('//a[@class="tiktok-q3q1i1-StyledCommonLink ejg0rhn4"]/@href')
    caption = ""
    for words in captxt:
        caption+=words+' '
    for tag in tags:
        if "/@" in tag:
            replurl = "https://www.tiktok.com"+tag
            tag=tag.replace("/","")
            caption = caption[:12]+"[**"+tag+"**]"+"("+replurl+")"+caption[12:]
            continue
        alt = tag.replace("/tag/", "#")
        caption+=alt+' '
    return caption

pytesseract.pytesseract.tesseract_cmd=r'/usr/bin/tesseract'

class TikTokCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Print code here

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        raw = msg.content
        print(raw) 
    
        if "https://www.tiktok.com/" in raw:
            errorEmbed = discord.Embed(color=red)
            defaultEmbed = discord.Embed(color=defaultEmbedColor)
            startloc = raw.find("https://www.tiktok.com/")
            url = raw[startloc:]
            url = url.split()[0]
            sent = raw.split(url)
            caption = await grabCaption(url)
            if caption==1:
                errorEmbed.add_field(name=":x: Broken Link!", value="You sure that leads to a video?")
                await msg.channel.send(embed=errorEmbed)
                return
            try:
                tiktokEmbed = discord.Embed(color=0xFF0050, description=caption+" [#link]("+url+")")
                if(exists("./tiktok.mp4")):
                    os.remove("./tiktok.mp4")
                data = await grabLinkData(url)
                print(url)
    
                tiktokEmbed.set_author(name=str(data[0]+" ("+data[1]+")"),url=data[2],icon_url=data[3])
                tiktokEmbed.set_footer(text="TikTok "+data[4], icon_url="https://cdn4.iconfinder.com/data/icons/social-media-flat-7/64/Social-media_Tiktok-512.png")
                await msg.edit(suppress=True)
                await msg.channel.send(embed=tiktokEmbed)
                await msg.channel.send(file=discord.File(r'./tiktok.mp4'))
                os.remove("./tiktok.mp4")
            except ValueError:#IndexError:
                await msg.add_reaction('\U0001F5BC')


async def setup(bot):
	await bot.add_cog(TikTokCog(bot))
