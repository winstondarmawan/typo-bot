import os
import time
import nextcord
from nextcord.ext import commands
from replit import db
from embed import helpF, create_embed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from farmables import badges, classes, easy, medium, hard, points
from admins import admins
from pagination import PaginationView

from webserver import keep_alive

intents = nextcord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='*', intents=intents)
client.remove_command("help")
  
@client.event
async def on_ready():
  # await client.user.edit(username="Typo Bot")
  print('We have logged in as ' + str(client.user))

@client.command()
async def help(ctx):
  await ctx.send(embed=helpF)

@client.command()
async def register(ctx, *args):
  user = str(ctx.message.author.id)
  # Argument check.
  if len(args) == 0:
    await ctx.send(embed=create_embed("Error!", "Please add your IGN as an argument.\n```$f register [ign]```"))
    return
  ign = ' '.join(args)
  url = "https://account.aq.com/CharPage?id=" + ign
  # Check if Discord user has registered.
  if user in db.keys():
    await ctx.send(embed=create_embed("Error!", "You have already registered."))
    return
  # Check if AQW IGN has been registered by another Discord user.
  for check in db.keys():
    if db[check]["ign"].lower() == ign.lower():
      await ctx.send(embed=create_embed("Error!", "This IGN has already been registered."))
      return
  # Run webdriver to check for valid IGN.
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  checkIGN = driver.find_elements_by_class_name("mt-2")
  # await ctx.send("Finding your character...", delete_after=1)
  for i in checkIGN:
    if "Not Found!" in i.get_attribute('outerHTML'):
      driver.quit()
      await ctx.send(embed=create_embed("Error!", "That character does not exist!"))
      return
  
  # Initialise user and add them to the DB.
  db[user] = {
    "ign": ign,
    "badges": [],
    "items": [],
    "points": 0
  }
  
  driver.quit()
  await ctx.send(embed=create_embed("Success!", "{} has been registered. Do ```*update``` to assign your farmables.".format(ign)))

  return

@client.command()
async def update(ctx):
  user = str(ctx.message.author.id)
  # Check if user is registered.
  if user not in db.keys():
    await ctx.send(embed=create_embed("Error!", "You are not registered! Please register with:\n ``` *register [ign]```"))
    return

  await ctx.send("Scanning your page...", delete_after=3)

  # Run webdriver to scan for badges and items.
  ign = db[user]["ign"]
  url = "https://account.aq.com/CharPage?id=" + ign
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  
  buttons = driver.find_elements_by_class_name("btn-xs")

  found = []
  add_points = 0

  # Expand badge section
  buttons[0].click()
  time.sleep(1)
  search = driver.find_element_by_id("badgesRendered").get_attribute('outerHTML')
  for badge in badges.keys():
    if badge in search:
      if badge not in db[user]["badges"]:
        found.append(badge)
        db[user]["badges"].append(badge)
        # db[username]["points"] += points[badge]
        add_points += badges[badge]

  # Expand inventory section
  buttons[1].click()
  time.sleep(2)
  search = driver.find_element_by_id("inventoryRendered").get_attribute('outerHTML')
  for item in classes.keys():
    if ">{} (Rank".format(item) in search and item not in db[user]["items"]:
      if item not in db[user]["items"]:
        found.append(item)
        db[user]["items"].append(item)
        add_points += classes[item]
  for item in easy.keys():
    if ">{}<".format(item) in search and item not in db[user]["items"]:
      if item not in db[user]["items"]:
        found.append(item)
        db[user]["items"].append(item)
        add_points += easy[item]
  for item in medium.keys():
    if ">{}<".format(item) in search and item not in db[user]["items"]:
      if item not in db[user]["items"]:
        found.append(item)
        db[user]["items"].append(item)
        add_points += medium[item]
  for item in hard.keys():
    if ">{}<".format(item) in search and item not in db[user]["items"]:
      if item not in db[user]["items"]:
        found.append(item)
        db[user]["items"].append(item)
        add_points += hard[item]

  db[user]["points"] += add_points

  if len(found) != 0:
    title = "Farmables found! You are truly a profarmer."
    desc = "The following farmables have been added:\n"
    for farmable in found:
      desc += "\n∘ {}".format(farmable)
    desc += "\n\n{} points have been added to your account.".format(add_points)
  else:
    title = "Your account is up to date."
    desc = "Go farm some items!"
  
  driver.quit()
  await ctx.send(embed=create_embed(title, desc))
  return

@client.command()
async def list(ctx, *args):
  user = str(ctx.message.author.id)
  # Check if user is registered.
  if user not in db.keys():
    await ctx.send(embed=create_embed("Error!", "You are not registered! Please register with:\n ```*register [ign]```"))
    return

  await ctx.send("Fetching list...", delete_after=1)   
  c_user = user
  if len(args) > 0:
    ign = ' '.join(args)
    for check in db.keys():
      if db[check]["ign"].lower() == ign.lower():
        c_user = check
        break
    if c_user not in check:
      await ctx.send(embed=create_embed("Error!", "User not found."))
      return

  if len(db[c_user]["badges"]) == 0 and len(db[c_user]["items"]) == 0:
    await ctx.send(embed=create_embed("Error!", "There is nothing to be found!"))
    return

  desc = [""]
  desc[0] = "**Total Points:** {}".format(db[c_user]["points"])
  desc[0] += "\n\n**Badges**" 
  for badge in badges.keys():
    if badge in db[c_user]["badges"]:
      desc[0] += ("\n✅ {} *[{}pt]*".format(badge, badges[badge]))
    else:
      desc[0] += ("\n❌ {} *[{}pt]*".format(badge, badges[badge]))

  desc.append("")
  desc[1] += "**Classes**"
  for item in classes.keys():
    if item in db[c_user]["items"]:
      desc[1] += ("\n✅ {} *[{}pt]*".format(item, classes[item]))
    else:
      desc[1] += ("\n❌ {} *[{}pt]*".format(item, classes[item]))
  
  desc.append("")
  desc[2] += "**Easy**"
  for item in easy.keys():
    if item in db[c_user]["items"]:
      desc[2] += ("\n✅ {} *[{}pt]*".format(item, easy[item]))
    else:
      desc[2] += ("\n❌ {} *[{}pt]*".format(item, easy[item]))

  desc.append("")
  desc[3] += "**Medium**"
  for item in medium.keys():
    if item in db[c_user]["items"]:
      desc[3] += ("\n✅ {} *[{}pt]*".format(item, medium[item]))
    else:
      desc[3] += ("\n❌ {} *[{}pt]*".format(item, medium[item]))

  desc.append("")
  desc[4] += "**Hard**"
  for item in hard.keys():
    if item in db[c_user]["items"]:
      desc[4] += ("\n✅ {} *[{}pt]*".format(item, hard[item]))
    else:
      desc[4] += ("\n❌ {} *[{}pt]*".format(item, hard[item]))

  desc[4] += "\n\n**Total Points:** {}".format(db[c_user]["points"])

  view = PaginationView(ctx, "{}'s Farmables".format(db[c_user]["ign"]), desc)

  await ctx.send(embed=create_embed("{}'s Farmables".format(db[c_user]["ign"]), desc[0]), view=view)
  return

@client.command()
async def leaderboard(ctx):
  await ctx.send("Fetching leaderboard...", delete_after=2)
  pt_db = {}
  for user in db.keys():
    pt_db[user] = db[user]["points"]
  s_pt = sorted(pt_db, key=pt_db.get, reverse=True)

  i = 1
  desc_index = 0
  desc = [""]
  for user in s_pt:
    if i % 20 == 1 and i != 1:
      desc_index += 1
      desc.append("")
    desc[desc_index] += "\n**{}.** {} **|** {} *[{} pt]*".format(i, client.get_user(int(user)), db[user]["ign"], db[user]["points"])
    i += 1
    
  view = PaginationView(ctx, "Leaderboard", desc)

  await ctx.send(embed=create_embed("Leaderboard", desc[0]), view=view)

@client.command()
async def delete(ctx):
  user = str(ctx.message.author.id)
  if user in db.keys():
    await ctx.send(embed=create_embed("Success!", "You have been deleted from the database."))
    del db[user]
  else:
    await ctx.send(embed=create_embed("Error!", "You are not currently registered."))

@client.command()
async def admin_update(ctx):
  user = str(ctx.message.author.id)
  if user not in admins: 
    await ctx.send("You cannot use that command.")
  else:
    for user in db.keys():
      db[user]["points"] = 0
      for badge in db[user]["badges"]:
        db[user]["points"] += points[badge]
      for item in db[user]["items"]:
        db[user]["points"] += points[item]
    await ctx.send("Points updated.")
  return

@client.command()
async def admin_delete(ctx, *args):
  ign = ' '.join(args)
  user = str(ctx.message.author.id)
  if user not in admins:
    await ctx.send("You cannot use that command.")
  else:
    for check in db.keys():
        if db[check]["ign"].lower() == ign.lower():
          del db[check]
          await ctx.send("Target neutralised.")
  return

keep_alive()
client.run(os.environ['auth_key'])

