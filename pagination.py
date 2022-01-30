import nextcord
from nextcord.ui import View
from embed import create_embed

class PaginationView(View):
  
  def __init__(self, ctx, title, pages):
    super().__init__(timeout=120)
    self.ctx = ctx
    self.title = title
    self.pages = pages
    self.c_page = 0

  @nextcord.ui.button(emoji="⬅", custom_id="prev", disabled=True)
  async def prev_button_callback(self, button, interaction):
    self.c_page -= 1
    pages_button = [x for x in self.children if x.custom_id == "pages"][0]
    pages_button.label = "Page: {}/{}".format(self.c_page+1, len(self.pages))
    if self.c_page == 0:
      button.disabled = True
    next_button = [x for x in self.children if x.custom_id == "next"][0]
    if self.c_page+1 != len(self.pages):
      next_button.disabled = False
    await interaction.response.edit_message(embed=create_embed(self.title, self.pages[self.c_page]), view=self)

  @nextcord.ui.button(label="Page: 1", disabled=True, custom_id="pages")
  async def page_button_callback(self, button, interaction):
    pass

  @nextcord.ui.button(emoji="➡", custom_id="next")
  async def next_button_callback(self, button, interaction):
    self.c_page += 1
    pages_button = [x for x in self.children if x.custom_id == "pages"][0]
    pages_button.label = "Page: {}/{}".format(self.c_page+1, len(self.pages))
    if self.c_page+1 == len(self.pages):
      button.disabled = True
    prev_button = [x for x in self.children if x.custom_id == "prev"][0]
    if self.c_page != 0:
      prev_button.disabled = False
    await interaction.response.edit_message(embed=create_embed(self.title, self.pages[self.c_page]), view=self)
  
  async def interaction_check(self, interaction) -> bool:
    if interaction.user != self.ctx.author:
      await interaction.response.send_message("You cannot paginate for someone else.", ephemeral=True)
      return False
    else:
      return True