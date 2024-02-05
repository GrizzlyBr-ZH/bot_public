# 2024/02/03紀錄：在找到更好的方案前勿取消註解print(get_sheet("資料庫"))，以免造成機器人無法正常運作
import discord
import traceback
from discord.ext import commands
import re
import json
import moment
from datetime import datetime
from discord import app_commands
from googleSheet import get_sheet
from googleSheet import add_row_sheet
with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata=json.load(jfile)

#intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot=commands.Bot(command_prefix='!', intents=intents, help_command=None)
tree = app_commands.CommandTree(client)

# 下拉選單 - 歷屆試題
class zj_apcs_select(discord.ui.View):
    @discord.ui.select(
        placeholder = "選擇任一場考試",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
            label="2024年1月",
            description="1. 遊戲選角 2. 蜜蜂觀察 3. 邏輯電路 4. 合併成本"
            ),
            discord.SelectOption(
            label="2023年10月",
            description="1. 機械鼠 2. 卡牌遊戲 3. 搬家 4. 投資遊戲"
            ),
            discord.SelectOption(
            label="2023年6月",
            description="1. 路徑偵測 2. 特殊位置 3. 磁軌移動序列 4. 開啟寶盒"
            ),
            discord.SelectOption(
            label="2023年1月",
            description="1. 程式考試 2. 造字程式 3. 先加後乘與函數 4. 機器出租"
            ),
            discord.SelectOption(
            label="2022年10月",
            description="1. 巴士站牌 2. 運貨站 3. 石窟探險 4. 蓋步道"
            ),
            discord.SelectOption(
            label="2022年6月",
            description="1. 數字遊戲 2. 字串解碼 3. 雷射測試 4. 內積"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        # select.disabled = True
        if select.values[0] == "2024年1月": msg = "[1. 遊戲選角](https://zerojudge.tw/ShowProblem?problemid=m931)、[2. 蜜蜂觀察](https://zerojudge.tw/ShowProblem?problemid=m932)、[3. 邏輯電路](https://zerojudge.tw/ShowProblem?problemid=m933)、[4. 合併成本](https://zerojudge.tw/ShowProblem?problemid=m934"
        elif select.values[0] == "2023年10月": msg = "[1. 機械鼠](https://zerojudge.tw/ShowProblem?problemid=m370)、[2. 卡牌遊戲](https://zerojudge.tw/ShowProblem?problemid=m371)、[3. 搬家](https://zerojudge.tw/ShowProblem?problemid=m372)、[4. 投資遊戲](https://zerojudge.tw/ShowProblem?problemid=m373"
        elif select.values[0] == "2023年6月": msg = "[1. 路徑偵測](https://zerojudge.tw/ShowProblem?problemid=k731)、[2. 特殊位置](https://zerojudge.tw/ShowProblem?problemid=k732)、[3. 磁軌移動序列](https://zerojudge.tw/ShowProblem?problemid=k733)、[4. 開啟寶盒](https://zerojudge.tw/ShowProblem?problemid=k734)"
        elif select.values[0] == "2023年1月": msg = "[1. 程式考試](https://zerojudge.tw/ShowProblem?problemid=j605)、[2. 造字程式](https://zerojudge.tw/ShowProblem?problemid=j606)、[3. 先加後乘與函數](https://zerojudge.tw/ShowProblem?problemid=j607)、[4. 機器出租](https://zerojudge.tw/ShowProblem?problemid=j608)"
        elif select.values[0] == "2022年10月": msg = "[1. 巴士站牌](https://zerojudge.tw/ShowProblem?problemid=i428)、[2. 運貨站](https://zerojudge.tw/ShowProblem?problemid=j123)、[3. 石窟探險](https://zerojudge.tw/ShowProblem?problemid=j124)、[4. 蓋步道](https://zerojudge.tw/ShowProblem?problemid=j125)"
        elif select.values[0] == "2022年6月": msg = "[1. 數字遊戲](https://zerojudge.tw/ShowProblem?problemid=i399)、[2. 字串解碼](https://zerojudge.tw/ShowProblem?problemid=i400)、[3. 雷射測試](https://zerojudge.tw/ShowProblem?problemid=i401)、[4. 內積](https://zerojudge.tw/ShowProblem?problemid=i402)"
        await interaction.response.edit_message(content=msg)

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(">>> 機器人已登入")
    print(f"載入 {len(slash)} 個斜線指令")
    game = discord.Game('C++大戰Python')
    #discord.Status.<狀態>，可以是online,offline,idle,dnd,invisible
    await bot.change_presence(status=discord.Status.idle, activity=game)
    # print(get_sheet("資料庫"))

@bot.event
async def on_error(e, *arg, **kwarg):
    traceback_ = traceback.format_exc()
    print(traceback_)

# /我想刷題
@bot.tree.command(name = "我想刷題", description = "想練題嗎？這裡提供一些歷屆APCS試題來讓你練練手感")
async def zj_apcs(interaction: discord.Interaction):
    # embed = discord.Embed(title="APCS歷屆試題", description="以下連結使用的測驗平台：[ZeroJudge](https://zerojudge.tw/)\n若是解題過程中遇到阻礙，歡迎至<#1115986414136463501>尋求協助！",colour=0xccf500,timestamp=datetime.now())
    # embed.add_field(name="2024年1月",value="[1. 遊戲選角](https://zerojudge.tw/ShowProblem?problemid=m931)\n[2. 蜜蜂觀察](https://zerojudge.tw/ShowProblem?problemid=m932)\n[3. 邏輯電路](https://zerojudge.tw/ShowProblem?problemid=m933)\n[4. 合併成本](https://zerojudge.tw/ShowProblem?problemid=m934)",inline=True)
    # embed.add_field(name="2023年10月",value="[1. 機械鼠](https://zerojudge.tw/ShowProblem?problemid=m370)\n[2. 卡牌遊戲](https://zerojudge.tw/ShowProblem?problemid=m371)\n[3. 搬家](https://zerojudge.tw/ShowProblem?problemid=m372)\n[4. 投資遊戲](https://zerojudge.tw/ShowProblem?problemid=m373)",inline=True)
    # embed.add_field(name="2023年6月",value="[1. 路徑偵測](https://zerojudge.tw/ShowProblem?problemid=k731)\n[2. 特殊位置](https://zerojudge.tw/ShowProblem?problemid=k732)\n[3. 磁軌移動序列](https://zerojudge.tw/ShowProblem?problemid=k733)\n[4. 開啟寶盒](https://zerojudge.tw/ShowProblem?problemid=k734)",inline=True)
    # embed.add_field(name="2023年1月",value="[1. 程式考試](https://zerojudge.tw/ShowProblem?problemid=j605)\n[2. 造字程式](https://zerojudge.tw/ShowProblem?problemid=j606)\n[3. 先加後乘與函數](https://zerojudge.tw/ShowProblem?problemid=j607)\n[4. 機器出租](https://zerojudge.tw/ShowProblem?problemid=j608)",inline=True)
    # embed.add_field(name="2022年10月",value="[1. 巴士站牌](https://zerojudge.tw/ShowProblem?problemid=i428)\n[2. 運貨站](https://zerojudge.tw/ShowProblem?problemid=j123)\n[3. 石窟探險](https://zerojudge.tw/ShowProblem?problemid=j124)\n[4. 蓋步道](https://zerojudge.tw/ShowProblem?problemid=j125)",inline=True)
    # embed.add_field(name="2022年6月",value="[1. 數字遊戲](https://zerojudge.tw/ShowProblem?problemid=i399)\n[2. 字串解碼](https://zerojudge.tw/ShowProblem?problemid=i400)\n[3. 雷射測試](https://zerojudge.tw/ShowProblem?problemid=i401)\n[4. 內積](https://zerojudge.tw/ShowProblem?problemid=i402)",inline=True)
    # embed.set_footer(text="目前機器人仍處開發階段，如有問題請回報")
    # await interaction.response.send_message(embed=embed)
    await interaction.response.send_message("選擇任意一場考試以查看考題...", view=zj_apcs_select())

bot.run(jdata['TOKEN'])
