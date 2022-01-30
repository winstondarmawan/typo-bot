import discord
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

noArgs=discord.Embed(title="Error!", description="Please add your IGN as an argument.\n```$f hunt [ign]```", color=0x0059ff)
noArgs.set_author(name="Typo Bot",icon_url="https://media.discordapp.net/attachments/744547152272818178/882878296696692736/Typo_Logo_Circle.png")

noIGN=discord.Embed(title="Error!", description="That character does not exist!", color=0x0059ff)
noIGN.set_author(name="Typo Bot",icon_url="https://media.discordapp.net/attachments/744547152272818178/882878296696692736/Typo_Logo_Circle.png")

failed=discord.Embed(title="Drip check FAILED!", description="You don't have everything! Go back and farm!")
failed.set_author(name="Typo Bot",icon_url="https://media.discordapp.net/attachments/744547152272818178/882878296696692736/Typo_Logo_Circle.png")

success=discord.Embed(title="Drip Check Passed! B)", description="Congratulations! You have gathered enough drip to please the Drip King.", color=0x0059ff)
success.set_author(name="Typo Bot",icon_url="https://media.discordapp.net/attachments/744547152272818178/882878296696692736/Typo_Logo_Circle.png")

items = [
  # "Archfiend's Amber",
  # "Tendou's Moonstone",
  # "Asuka's Ruby",
  "King Klunk's Crown",
  # "Pirate Mage SpellBook",
  "Black Pirate Costume",
  "RockRune Cape",
  "Treasure Pile"
  #"Jewel of the Sea"
]

def hunt(user, args):
  if len(args) == 0:
      return noArgs
  else:
    ign = ' '.join(args)
    url = "https://account.aq.com/CharPage?id=" + ign

    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    init = driver.find_elements_by_class_name("mt-2")
    for i in init:
      if "Not Found!" in i.get_attribute('outerHTML'):
        driver.quit()
        return noIGN

    buttons = driver.find_elements_by_class_name("btn-xs")

    buttons[1].click()
    time.sleep(1)
    search = driver.find_element_by_id("inventoryRendered").get_attribute('outerHTML')
    for item in items:
      if item not in search:
        driver.quit()
        return failed

  driver.quit()

  return success
