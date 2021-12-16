@bot.command()
async def birthday(ctx, Day, Month):
  await ctx.message.delete()
  with open("birthday.json", "r") as f:
    data=json.load(f)
  if ist_bereits_eingetragen(ctx.author.id) != -1:
    embed=discord.Embed(title="Oh, du hast bereits deinen Geburtstag eingetragen.",color=0x18cdca)
    await ctx.send(embed=embed, hidden=True)
    return
  if int(Day)>=31:
    embed=discord.Embed(title="Diesen Tag gibt es leider nicht",color=0x18cdca)
    await ctx.send(embed=embed, hidden=True)
    return
  if int(Month)>=12:
    embed=discord.Embed(title="Diesen Monat gibt es leider nicht",color=0x18cdca)
    await ctx.send(embed=embed, hidden=True)
  with open('birthday.json') as f:
    data = json.load(f)
  if int(Month)==1:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Januar"].append(user)
  elif int(Month)==2:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Februar"].append(user)
  elif int(Month)==3:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Maerz"].append(user)
  elif int(Month)==4:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["April"].append(user)
  elif int(Month)==5:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Mai"].append(user)
  elif int(Month)==6:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Juni"].append(user)
  elif int(Month)==7:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Juli"].append(user)
  elif int(Month)==8:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["August"].append(user)
  elif int(Month)==9:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["September"].append(user)
  elif int(Month)==10:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Oktober"].append(user)
  elif int(Month)==11:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["November"].append(user)
  elif int(Month)==12:
    user = {
        "geburtstagskind": ctx.author.id,
        "monat": f"{Day}.{Month}"}
    data["Dezember"].append(user)
  with open('birthday.json', 'w') as f:
      json.dump(data, f, indent=4)
  with open('birthday.json', encoding='utf-8') as fp:
    data = json.load(fp)
  Januar=[]
  Februar=[]
  März=[]
  April=[]
  Mai=[]
  Juni=[]
  Juli=[]
  August=[]
  September=[]
  Oktober=[]
  November=[]
  Dezember=[]
  for x in data["Januar"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    Januar.append(f"<@{geburtstagskind.id}>: {monat}")
    test1=f" \n".join(Januar)
  if data["Januar"]==[]:
    test1="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["Februar"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    Februar.append(f"<@{geburtstagskind.id}>: {monat}")
    test2=f" \n".join(Februar)
  if data["Februar"]==[]:
    test2="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["Maerz"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    März.append(f"<@{geburtstagskind.id}>: {monat}")
    test3=f" \n".join(März)
  if data["Maerz"]==[]:
    test3="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["April"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    April.append(f"<@{geburtstagskind.id}>: {monat}")
    test4=f" \n".join(April)
  if data["April"]==[]:
    test4="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["Mai"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    Mai.append(f"<@{geburtstagskind.id}>: {monat}")
    test5=f" \n".join(Mai)
  if data["Mai"]==[]:
    test5="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["Juni"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    Juni.append(f"<@{geburtstagskind.id}>: {monat}")
    test6=f" \n".join(Juni)
  if data["Juni"]==[]:
    test6="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["Juli"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    Juli.append(f"<@{geburtstagskind.id}>: {monat}")
    test7=f" \n".join(Juli)
  if data["Juli"]==[]:
    test7="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["August"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    August.append(f"<@{geburtstagskind.id}>: {monat}")
    test8=f" \n".join(August)
  if data["August"]==[]:
    test8="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["September"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    September.append(f"<@{geburtstagskind.id}>: {monat}")
    test9=f" \n".join(September)
  if data["September"]==[]:
    test9="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["Oktober"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    Oktober.append(f"<@{geburtstagskind.id}>: {monat}")
    test10=f" \n".join(Oktober)
  if data["Oktober"]==[]:
    test10="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["November"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    November.append(f"<@{geburtstagskind.id}>: {monat}")
    test11=f" \n".join(November)
  if data["November"]==[]:
    test11="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  for x in data["Dezember"]:
    geburtstagskind = bot.get_user(int(x["geburtstagskind"]))
    monat = x["monat"]
    Dezember.append(f"<@{geburtstagskind.id}>: {monat}")
    test12=f" \n".join(Dezember)
  if data["Dezember"]==[]:
    test12="Für diesen Monat ist leider noch kein Geburtstag eingetragen"
  channel = bot.get_channel(901106297313820692)
  message = await channel.fetch_message(920756572634898442)
  embed=discord.Embed(title="Geburtstage", description="Hier siehst du die Geburtstage unserer Mitglieder - du kannst deinen Geburtstag mit ``/birthday`` hinzufügen.", color=0x00ff04)
  embed.add_field(name="Januar", value=f"{test1}")
  embed.add_field(name="Februar", value=f"{test2}")
  embed.add_field(name="März", value=f"{test3}")
  embed.add_field(name="April", value=f"{test4}")
  embed.add_field(name="Mai", value=f"{test5}")
  embed.add_field(name="Juni", value=f"{test6}")
  embed.add_field(name="Juli", value=f"{test7}")
  embed.add_field(name="August", value=f"{test8}")
  embed.add_field(name="September", value=f"{test9}")
  embed.add_field(name="Oktober", value=f"{test10}")
  embed.add_field(name="November", value=f"{test11}")
  embed.add_field(name="Dezember", value=f"{test12}")
  embed.add_field(name="-----------------------------------------------------------------------------------------------", value="--------------------------------------------------------------------------------------------", inline=False)
  embed.add_field(name="Was passiert an deinem Geburtstag?", value="An deinem Geburtstag bekommst du **1 Monat Discord Nitro** ~geschenkt~. Wir nehmen uns vor deinen Geburtstag anhand eines __Ausweis-Dokuments__ zu kontrollieren, um fake zu vermeiden", inline=False)
  embed.set_footer(text="Die Chance auf Nitro beträgt: 1/4")
  await message.edit(embed=embed)

def ist_bereits_eingetragen(userid):
  user = -1
  i = 0
  with open('birthday.json', encoding='utf-8') as fp:
      data = json.load(fp)
  for x in data["Januar"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["Februar"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["Maerz"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["April"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["Mai"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["Juni"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["Juli"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["August"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["September"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["Oktober"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["November"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  for x in data["Dezember"]:
      if int(x["geburtstagskind"]) == int(userid):
          user = i
      i += 1
  return user
