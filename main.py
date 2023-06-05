import discord
import sqlite3
import json

from discord.ext import commands
from random import choice, randint
from time import sleep
from tabulate import tabulate

from commands import items, dicta, data

with open("token.txt") as f:
  token = f.read(70)
with open("prefix.txt") as f:
  prefix = f.read(1)

conn = sqlite3.connect("database")
cursor = conn.cursor()

try:
  cursor.execute(""" 
  CREATE TABLE "users"(
    "id" INT,
    "nickname" TEXT,
    "Acoin" INT
    )
  """)

  cursor.execute(
  """ 
  CREATE TABLE "shop"(
    "id" INT,
    "cost" INT
    )
  """)
except:
  pass

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = prefix, intents = intents)

@bot.event
async def on_ready():
  print("Бот запущен")
  for guild in bot.guilds:
    print(guild.id)
    server = guild
    for member in guild.members:
      cursor.execute(f"SELECT id FROM users where id = {member.id}")
      if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO users VALUES ({member.id}, '{member.name}',100000)")
      else:
        pass
      conn.commit()

@bot.command()
async def chlen(ctx):
        result = randint(0,20)
        if result > 15:
            await ctx.reply(f"Размер твоего члена: {result} cm, хуя ты гигант")
        else:
            await ctx.reply(f"Размер твоего члена: {result} cm, у моего бати больше")
  

@bot.command()
async def test(ctx, *args):
        mas_1 = [i for i in args]
        procent = 0
        message = await ctx.send("Сканируем...")
        while procent != 100:
                sleep(0.2)
                procent += 5
                await message.edit(content = f"Завершено: {procent}%")
        choising = choice(mas_1)
        await ctx.reply(f"Сканирование завершено, {ctx.author.name}: {choising}")

@bot.command()
async def case(ctx):
  uid = ctx.author.id
  for row in cursor.execute(f"SELECT Acoin FROM users where id = {uid}"):
      money = row[0]
    #for row in cursor.execute(f"SELECT cost FROM shop"):
      #cost = row[1]
      if money >= 250:
        money -= 250
        await ctx.send("Открываем кейс...")
        sleep(5)
        #{Алгоритм открытия кейса}
        #Планы: сделать прибавление шанса к супер призу!
        result = randint(0,100)
        if result == 1:
          result = items["5"]
          money += 0
        elif result >= 2 and result <= 10:
          result = items["4"]
          money += 500
        elif result > 10 and result <= 30:
          result = items["3"]
          money += 200
        elif result > 30 and result <= 50:
          result = items["2"]
          money += 10
        else:
          result = items["1"]
        await ctx.send(f"Тебе выпало: {result}")
        cursor.execute("UPDATE users SET Acoin = ? where id = ?",(money,uid))
      if money < 250:
        await ctx.send("Недостаточно денег!")
        pass
  conn.commit()

@bot.command()
async def commands(ctx):
  embedVar = discord.Embed(title = "Команды A.PY")
  for i in dicta:
    embedVar.add_field(name=i, value=dicta[i], inline=False)
  await ctx.send(embed = embedVar)

@bot.command()
async def bal(ctx):
  table = []
  n = 0
  embedVar = discord.Embed(title = "Аккаунт")
  for row in cursor.execute(f"SELECT nickname, Acoin FROM users where id = {ctx.author.id}"):
    for i in range(2):
        table.append(row[i])
    for i in table:
        embedVar.add_field(name = data[n], value = f"{i}")
        n += 1
    await ctx.send(embed = embedVar)

if __name__ == "__main__":
        bot.run(token)
