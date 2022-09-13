import json
import discord
from discord.ui import Button, View, Modal
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from random import randint

import smtplib
import stripe

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='.', help_command=None, intents=intents,case_insensitive=True)

#insert stripe api key
stripe.api_key = "sk_test_51J5GF6BiE0bgLr5dcwsJugN775YibhacvanSHTbSxEh0bLvDdwieZHT0luvsXUt6sUVoir10rZ3lThddvBYUldm900uWKWlNke"
#insert stripe api key

cod={263623:-7623767}
emaillist={263623:"abcdef@hmail.xom"}


@tasks.loop(minutes=120)
async def checksubscription():
  with open("subscription/data/data.json", "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
  for k in data:
    onsubscription=False
    with open("subscription/data/whitelist.json", "r") as jsonFile:
          whitelist = json.load(jsonFile)
          jsonFile.close()
    if str(emaillist[user.id]).lower() in whitelist:
          onsubscription=True

    
    info=stripe.Customer.list(email=k,expand=['data.subscriptions'])
    if len(info)<1:
      dict=data[k]
      dict["sub"]="false"
      data[k]=dict
      with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()
      with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()


      
    else:
      stripedata=info["data"]
      if len(stripedata)<1:
        dict=data[k]
        dict["sub"]="false"
        data[k]=dict
        with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()
        with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()
        
      elif len(stripedata)==1:
        id=stripedata[0]["id"]
        sub=stripedata[0]["subscriptions"]
        if len(sub)<1:
          dict=data[k]
          dict["sub"]="false"
          data[k]=dict
          with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()
          with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()

          
        elif len(sub)==1:
          if str(sub[0]["cancel_at_period_end"]).lower()=="false":
            dict=data[k]
            dict["sub"]="false"
            data[k]=dict
            with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()
            with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()
          
          else:
                onsubscription=True
        else:
          for s in sub:
            if str(s["cancel_at_period_end"]).lower()=="true":
              onsubscription=True
              break
          if onsubscription==False:
            dict=data[k]
            dict["sub"]="false"
            data[k]=dict
            with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()
            with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()
      else:
        for k in stripedata:
          id=k["id"]
          sub=k["subscriptions"]
          if len(sub)==1:
            if str(sub[0]["cancel_at_period_end"]).lower()=="true":
              onsubscription=True
          else:
            for s in sub:
              if str(s["cancel_at_period_end"]).lower()=="true":
                onsubscription=True
                break
    if onsubscription==False:
      try:
        guild = client.get_guild(00000000) #insert server id in the brackets
        acces = guild.get_role(0000000) #insert role id in the brackets
        user= await guild.fetch_member(data[k]["id"])
        await user.remove_roles(acces)
      except:
        pass
      dict=data[k]
      dict["sub"]="false"
      data[k]=dict
      with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()
      with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()
            
            #log pt remove subscription











@client.event
async def on_ready():
  await client.change_presence(
	    activity=discord.Activity(type=discord.ActivityType.watching, name="THE CRYPTO INSIDERZ"))
  checksubscription.start()
  print("gata")


class verif(Modal, title="Verificare e-mail"):
  def __init__(self):
    super().__init__()
    self.add_item(discord.ui.TextInput(label="Introdu codul primit pe mail", style=discord.TextStyle.short,placeholder="000000",required=True))
    self.custom_id="cod"
    




class mail(Modal, title="Verificare achizitie"):
  def __init__(self):
    super().__init__()
    self.add_item(discord.ui.TextInput(label="Care este numele tau?", style=discord.TextStyle.short,placeholder="Nume",required=True))
    self.add_item(discord.ui.TextInput(label="Cu ce e-mail ai cumparat abonamentul?", style=discord.TextStyle.short,placeholder="mail@email.xyz",required=True))
    self.custom_id="mail"
  
  
@client.event
async def on_interaction(interaction):
  print("ok")
  buttondata = interaction.data
  user=interaction.user
  print(buttondata['custom_id'])
  
  if str(interaction.type)=="InteractionType.modal_submit":
    if buttondata['custom_id']=="mail":
      nume=buttondata['components'][0]['components'][0]['value']
      email=buttondata['components'][1]['components'][0]['value']
      global emaillist
      emaillist[user.id]=str(email)
      global cod
      cod[user.id]=randint(10000,99999)
      print(nume)
      print(email)
      #await interaction.message.edit(verif())
      view=View()
      buton1=Button(style=discord.ButtonStyle.primary,emoji="⏪", disabled=False,custom_id="codeverify")
      view.add_item(buton1)



      with open("subscription/data/data.json", "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
      if email in data:
        if data[email]["id"]!=interaction.user.id:
          await interaction.response.send_message(f"Email-ul este deja folosit de alt cont de discord. Daca ti-ai schimbat contul de discord, discuta cu un administrator pentru a primi acces. \n\nAtentie: nu poti avea acces la server pe multiple conturi avand acelasi email.",view=view,ephemeral=True)
          return
      
      await interaction.response.send_message(f"{user.mention}, ti-am trimis un cod pe mail. Cand il primesti, apasa pe butonul de mai jos!",view=view,ephemeral=True)
      server = smtplib.SMTP('mail.server.eu', port=587) #insert mail server
      server.ehlo()
      server.starttls()
      server.ehlo()
      server.login('mail', 'pass') #insert email and password
      print("mail conectat")
      server.sendmail("mail", str(email), f"Subject: Cod verificare\n\nCodul de confirmare pentru serverul de discord X este {cod[user.id]}")
      server.close()
      print("mail trimis")
      return

    if buttondata['custom_id']=="cod":
      if user.id not in cod or str(cod[user.id])=="-1":
        await interaction.response.send_message(f"Nu ti-a fost trimis un cod pe mail. Completeaza din nou formularul de mai sus",ephemeral=True)
      if str(buttondata['components'][0]['components'][0]['value'])==str(cod[user.id]):
        print("ok")
        cod[user.id]=-1
        with open("subscription/data/whitelist.json", "r") as jsonFile:
          whitelist = json.load(jsonFile)
          jsonFile.close()
        if str(emaillist[user.id]).lower() in whitelist:
          acces = interaction.message.guild.get_role(00000000) #insert role id in the brackets
          await user.add_roles(acces)
          dict={}
          dict["id"]=user.id
          dict["sub"]="true"
          with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()
          data[str(emaillist[user.id])]=dict
          with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()          
          await interaction.response.send_message(f"Bun",ephemeral=True)
          return
        #stripe
        info=stripe.Customer.list(email=emaillist[user.id],expand=['data.subscriptions'])
        if len(info)<1:
          await interaction.response.send_message(f"Nu ti-am gasit un abonament activ. Daca totusi ai cumparat un plan, contacteaza un administrator",ephemeral=True)
        else:
          stripedata=info["data"]
          onsubscription=False
          if len(stripedata)<1:
            await interaction.response.send_message(f"Nu ti-am gasit un abonament activ. Daca totusi ai cumparat un plan, contacteaza un administrator",ephemeral=True)
          elif len(stripedata)==1:
            id=stripedata[0]["id"]
            sub=stripedata[0]["subscriptions"]
            if len(sub)<1:
              await interaction.response.send_message(f"Nu ti-am gasit un abonament activ. Daca totusi ai cumparat un abonament, contacteaza un administrator",ephemeral=True)
            elif len(sub)==1:
              if str(sub[0]["cancel_at_period_end"]).lower()=="false":
                await interaction.response.send_message(f"Ti-a expirat abonamentul. Reinnoieste-l pentru a continua sa ai acces pe acest server!",ephemeral=True)
              else:
                onsubscription=True
            else:
              for s in sub:
                if str(s["cancel_at_period_end"]).lower()=="true":
                  onsubscription=True
                  break
              if onsubscription==False:
                await interaction.response.send_message(f"Ti-a expirat abonamentul. Reinnoieste-l pentru a continua sa ai acces pe acest server!",ephemeral=True)
          else:
            for k in stripedata:
              id=k["id"]
              sub=k["subscriptions"]
              if len(sub)==1:
                if str(sub[0]["cancel_at_period_end"]).lower()=="true":
                  onsubscription=True
              else:
                for s in sub:
                  if str(s["cancel_at_period_end"]).lower()=="true":
                    onsubscription=True
                    break
          if onsubscription==False:
            await interaction.response.send_message(f"Nu ti-am gasit un abonament activ. Daca totusi ai cumparat un abonament, contacteaza un administrator",ephemeral=True)
          else:
            acces = interaction.message.guild.get_role(00000000) #insert role id in the brackets
            await user.add_roles(acces)
            dict={}
            dict["id"]=user.id
            dict["sub"]="true"
            with open("subscription/data/data.json", "r") as jsonFile:
              data = json.load(jsonFile)
              jsonFile.close()
            data[str(emaillist[user.id])]=dict
            with open("subscription/data/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                jsonFile.close()
              
        await interaction.response.send_message(f"Bun",ephemeral=True)
      else:
        await interaction.response.send_message(f"Cod incorect, incearca din nou",ephemeral=True)
        
  if str(interaction.type)=="InteractionType.component":
    type = buttondata['component_type']
    custom_id = buttondata['custom_id']
    print("ok")
    if custom_id=="mailverify":
      print("ok")
      await interaction.response.send_modal(mail())
    if custom_id=="codeverify":
      if user.id not in cod or str(cod[user.id])=="-1":
        await interaction.response.send_message(f"Nu ti-a fost trimis un cod pe mail. Completeaza formularul de mai sus",ephemeral=True)
      print("ok")
      await interaction.response.send_modal(verif())


@client.command()
@commands.has_permissions(administrator=True)
async def addwhitelist(ctx, mail):
  with open("subscription/data/whitelist.json", "r") as jsonFile:
    whitelist = json.load(jsonFile)
    jsonFile.close()
  if str(mail).lower() not in whitelist:
    whitelist[str(mail).lower()] = ""

  with open("subscription/data/whitelist.json", "w") as jsonFile:
    json.dump(whitelist, jsonFile)
    jsonFile.close()


@client.command()
@commands.has_permissions(administrator=True)
async def click(ctx):
  view=View()
  buton1=Button(style=discord.ButtonStyle.primary,emoji="⏪", disabled=False,custom_id="mailverify")
  view.add_item(buton1)
  await ctx.send(content="Click jos pentru a-ti verifica mail-ul", view=view)

@client.command()
@commands.has_permissions(administrator=True)
async def rol(ctx,member:discord.Member=None):
  member=member or ctx.author
  acces = ctx.guild.get_role(0000000000) #insert role id in the brackets
  await member.add_roles(acces)
  print("yeah")



client.run('TOKEN') #insert token