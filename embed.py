import nextcord

helpF=nextcord.Embed(title="Leaderboard Bot Commands", description="All the commands for the TypoBot.", color=0x0059ff)
helpF.set_author(name="Typo Bot",icon_url="https://media.discordapp.net/attachments/744547152272818178/935801553896501248/typologonobg-min.png?width=611&height=563")
helpF.add_field(name="```*register [ign]```", value="Registers your IGN to the bot.", inline=False)
helpF.add_field(name="```*update```", value="Checks your character page and updates the farmables. \nMake sure to unbank the farmables first.",inline=False)
helpF.add_field(name="```*list [ign]```", value="Shows a registered players farmables.\nArgument is optional, if none will display your own.", inline=False)
helpF.add_field(name="```*leaderboard```", value="View the leaderboard.", inline=False)
helpF.add_field(name="```*delete```", value="Deletes your data from the bot.", inline=False)

def create_embed(title, desc):
  embed=nextcord.Embed(title=title, description=desc, color=0x0059ff)
  embed.set_author(name="Typo Bot",icon_url="https://media.discordapp.net/attachments/744547152272818178/935801553896501248/typologonobg-min.png?width=611&height=563")
  return embed