import os
import re
import json
import asyncio
from typing import Union, Optional, List, Dict, Tuple

import discord
import datetime

from discord.ext import commands

intents = discord.Intents.default()
intents.members = True # YYou need to enable them in the developer-portal
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=)

TOKEN = ''  # The Bot-Token

bd_channel_id: Optional[int] = 853000092156035083  # the channel the message with birthdays should send to
b_message_id: Optional[int] = None  # the message to use for the birthday panel. Must be a message of the bot in the channel wich id is specified above.

_EmbedEmpty = discord.embeds.EmptyEmbed

bd_message_title = 'Birthdays for {guild}'  # the title of the birthdays panel
bd_no_birthdays_message = 'There are no birthdays registered for this month.'  # the message that should be displayed if no birthday in this month.
bd_embed_description = 'Here you could see the birthdays of {guild}\'s members.' \
                       'Add your birthday with `{prefix}birthday set <date>`(without the `<>`).' \
                       'The `date` should be in the format `dd.mm.yyyy`'  # the description the birthday embed should have
bd_embed_footer = ('Last updated at', 'https://discord.com/assets/b052a4bef57c1aa73cd7cff5bc4fb61d.svg', 'datetime.datetime.utcnow()')  # footer (text, icon_url, timestamp) for the birthday embed. Be careful what you enter here. The values will be passed to eval().
bd_embed_image_url = _EmbedEmpty  # the url of the image that should be set as the image of the birthday panel
bd_embed_thumbnail_url = _EmbedEmpty  # the url of the image that should be set as the thumbnail of the birthday panel
bd_embed_color = discord.Color.blue()  # The color of the birthday panel

bd_set_already_exists = 'You already set your birthday. Use `{prefix}birthday edit <date>`(without the `<>`) to update it.'  # message that should be shown if the birthday is already set

months = {
    '1': 'January',
    '2': 'February',
    '3': 'March',
    '4': 'April',
    '5': 'May',
    '6': 'June',
    '7': 'July',
    '8': 'August',
    '9': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}  # the name of the months that should used


@bot.event
async def on_ready():
    with open('./birthdays.json') as fp:
        data = json.load(fp)

    for guild in bot.guilds:
        if str(guild.id) not in data:
            data[str(guild.id)] = {'guild_id': guild.id, 'birthdays': {}}

    with open('./birthdays.json', 'w') as fp:
        json.dump(data, fp, indent=4)

    bot.loop.create_task(update_birthday_panel_loop())
    print('Bot is ready')

@bot.event
async def on_raw_message_delete(payload: discord.RawMessageDeleteEvent):
    if payload.guild_id:
        with open('./birthdays.json') as fp:
            data = json.load(fp)
        bd_message_id = data[str(payload.guild_id)].get('bd_message_id', None)
        if payload.message_id == bd_message_id:
            await update_birthday_panel(guild_id=payload.guild_id)

@bot.event
async def on_member_remove(member: discord.Member):
    with open('./birthdays.json') as fp:
        data = json.load(fp)

    try:
        data[str(member.guild.id)]['birthdays'].pop(str(member.id))
    except IndexError:
        pass
    else:
        with open('./birthdays.json', 'w') as fp:
            json.dump(data, fp, indent=4)

@bot.event
async def on_guild_add(guild: discord.Guild):
    with open('./birthdays.json') as fp:
        data = json.load(fp)

    try:
        data[str(guild.id)]
    except KeyError:
        data[str(guild.id)] = {'guild_id': guild.id, 'birthdays': {}}
        with open('./birthdays.json', 'w') as fp:
            json.dump(data, fp, indent=4)


@bot.event
async def on_guild_remove(guild: discord.Guild):
    with open('./birthdays.json') as fp:
        data = json.load(fp)

    try:
        await bot.wait_for('guild_add', check=lambda g: g.id == guild.id, timeout=600)
    except asyncio.TimeoutError:
        data.pop(str(guild.id))
        with open('./birthdays.json', 'w') as fp:
            json.dump(data, fp, indent=4)

async def update_birthday_panel_loop():
    await asyncio.sleep(10)
    while True:
        await update_birthday_panel()
        await asyncio.sleep(120)

def build_bd_embed(data: dict) -> Tuple[discord.TextChannel, discord.Embed]:
    bd_channel_id = data.get('bd_channel_id', None)
    if bd_channel_id:
        channel = bot.get_guild(data['guild_id']).get_channel(bd_channel_id)
        birthdays: Dict[str, List] = {str(i): [] for i in range(1, 13)}

        bd_embed = discord.Embed(
            title=bd_message_title.format(guild=channel.guild.name),
            description=bd_embed_description.format(prefix=bot.command_prefix(bot, None)[-1], guild=channel.guild.name),
            timestamp=eval(bd_embed_footer[2]),
            color=bd_embed_color
        )
        now = datetime.datetime.utcnow()
        for member_id, date in data['birthdays'].items():
            wich = now.year - date['year']
            next_year = False
            if (now.month == date['month'] and now.day > date['day']) or now.month > date['month']:
                wich += 1
                next_year = True
            day = str(date['day'])
            if day[-1] == '1':
                ending = 'st'
            elif day[-1] == '2':
                ending = 'nd'
            else:
                ending = 'th'
            birthdays[str(date['month'])].append(
                f'<@{member_id}>\'s **{wich}.** {"today 🎉🥳" if (date["month"], day) == (now.month, now.day) else f"on {day}{ending}" + (" next year" if next_year else "")}'
            )

        for month, m_birthdays in birthdays.items():
            if not len(m_birthdays):
                bd_embed.add_field(name=months.get(month), value=bd_no_birthdays_message)
            else:
                m_birthdays.sort(
                    key=lambda msg: int(re.search(r'(?P<day>3[0-1]|[1-2][0-9]|0?[0-9])(st|nd|th)', msg).group('day')))
                bd_embed.add_field(name=months.get(month), value='\n'.join(m_birthdays))
        icon_url = eval(f"f'{bd_embed_footer[1]}'")
        if icon_url is not _EmbedEmpty:
            bd_embed.set_footer(text=eval(f"f'{bd_embed_footer[0]}'"), icon_url=icon_url)
        else:
            bd_embed.set_footer(text=eval(f"f'{bd_embed_footer[0]}'"))
        if bd_embed_thumbnail_url is not _EmbedEmpty:
            bd_embed.set_thumbnail(url=bd_embed_thumbnail_url)
        if bd_embed_image_url is not _EmbedEmpty:
            bd_embed.set_image(url=bd_embed_image_url)

        return channel, bd_embed
    return None, None

async def update_birthday_panel(guild_id: Optional[int] = None):
    with open('./birthdays.json') as fp:
        data = json.load(fp)
    if guild_id:
        channel, bd_embed = build_bd_embed(data[str(guild_id)])
        if channel and bd_embed:
            bd_message_id = data[str(guild_id)].get('bd_message_id', None)

            if bd_message_id:
                try:
                    message = await discord.PartialMessage(channel=channel, id=bd_message_id).edit(embed=bd_embed)
                except discord.NotFound:
                    message = await channel.send(embed=bd_embed)
            else:
                message = await channel.send(embed=bd_embed)

            data[str(guild_id)]['bd_message_id'] = message.id
    else:
        for guild_id, guild_data in data.items():
            channel, bd_embed = build_bd_embed(data[str(guild_id)])
            if channel and bd_embed:
                bd_message_id = data[str(guild_id)].get('bd_message_id', None)

                if bd_message_id:
                    try:
                        message = await discord.PartialMessage(channel=channel, id=bd_message_id).edit(embed=bd_embed)
                    except discord.NotFound:
                        message = await channel.send(embed=bd_embed)
                else:
                    message = await channel.send(embed=bd_embed)

                data[str(guild_id)]['bd_message_id'] = message.id

    with open('./birthdays.json', 'w') as fp:
        json.dump(data, fp, indent=4)


class DatetimeConversionFailure(commands.BadArgument):
    """Exception raised when the conversion to a :class:`datetime.datetime` object failed

    This inherits from :exc:`BadArgument`

    Attributes
    -----------
    argument: :class: :class:`str`
        The date/time supplied by the caller that could not converted.
    original_exception: Optional[Any]
        The original exception that was raised when trying to create the datetime.datetime object.
    """
    def __init__(self, argument, original_exception=None):
        self.argument = argument
        self.original_exception = original_exception
        super().__init__(
            '"{}" could not be converted to a datetime.datetime object. '
            'The time should be in a format like H(H):M(M):S(S) '
            'and date in a format like d(d).m(m).yyyy'.format(argument)
        )


class datetimeConverter(commands.Converter):
    """Converts to a :class:`datetime.datetime`. Made by mccuber04#2960

    Valid formats for the time(``H`` = hour | ``M`` = minute | ``S`` = second):
        ``HH:MM:SS``,
        ``HH:MM``

        Each value can also be specified as a single digit.

        All ``:`` could be ``-`` too.

    Valid formats for the date(``d`` = day | ``m`` = month | ``y`` = year):
        ``dd.mm.yyyy``,
        ``dd.mm``,
        ``dd``,
        ``yyyy``
        ``mm.yyyy``

        Each value for day and month can also be specified as a single digit.

        All ``.`` could be ``,``, ``-`` and ``/`` too.

    .. note::
        Values that are not specified are filled with those of the current time.

        If you want to pass a time in 12h-format that is in the afternoon,
        the ``pm`` must be after the time like ``08:42 pm 04.10.2022``.
    """
    time_regex = re.compile(
        r'(?P<hour>'  # group for hour value
        r'0?[0-9]'  # 0 to 9
        r'|'  # or
        r'1[0-9]'  # 10 to 19
        r'|'  # or
        r'2[0-3]'  # 20 to 23
        r')'
        r'[:\-]'  # brake could be : or -
        r'(?P<minute>'  # group for minute value
        r'[1-5][0-9]'  # 10 to 59
        r'|'  # or
        r'0?[0-9]'  # 0 to 9
        r')'
        r'('  # group for brake and second
        r'[:\-]'  # brake could be : or -
        r'(?P<second>'  # group for second value
        r'[1-5][0-9]'  # 10 to 59
        r'|'  # or
        r'[0-9]'  # 0 to 9
        r')'
        r')?'  # mark the brake and second group as optional
        r' ?' # a optional whitespace
        r'(?P<am_or_pm>'  # group for am or pm value if it is in 12h-format
        r'am' # am for ante mediteran (Morning), would be ignored
        r'|'  # or
        r'pm'  # pm for post mediteran (afternoon)
        r')'
    )
    date_regex = re.compile(
        r'(?P<day>'  # group for day value
        r'3[0-1]'  # 31. or 30.
        r'|'  # or
        r'[1-2][0-9]'  # 10. to 29.
        r'|'  # or
        r'0?[1-9]'  # 1. to 9.
        r')?'  # mark the day as optional
        r'('  # group for brake and month
        r'[.,\-/]'  # brake could be . or , or - or /
        r'(?P<month>'  # group for month value
        r'1[0-2]'  # october to december
        r'|'  # or
        r'0?[1-9]'  # january to september
        r')'
        r')?'  # mark the brake and month group as optional 
        r'('  # group for brake and year
        r'[.,\-/]'  # brake could be . or , or - or /
        r'(?P<year>'  # group for year value
        r'[1-9][0-9]{3}'  # any year from 1000 to 9999 in format yyyy
        r'|'  # or
        r'[0-9]{2}'   # any year from 2000 to 2099 in format YY (20YY)
        r')'
        r'(\s|$)' # to be shure that "1996telefon" is not valid there should be a whitespace or the end of the string after the year
        r')?'  # mark the brake and year group as optional
    )

    async def convert(self, ctx, argument) -> datetime.datetime:
        argument = argument.lower().rstrip()

        now = datetime.datetime.utcnow()  # to set defaults for non provided parts
        invalid = False

        date = self.date_regex.search(argument)

        if date and any(date.groups()):
            day = int(date.group('day') or now.day)
            month = int(date.group('month') or now.month)
            year = date.group('year')

            if year and len(year) == 2: # it is in YY (20YY) format, convert it to a full year (yyyy)
                year = '20' + year

            year = int(year or now.year)
            # to make something like ``10.2022`` also valid
            if date.group('day') and not date.group('month'):
                month = day
                day = now.day
        else:
            invalid = True
            day, month, year = now.day, now.month, now.year

        time = self.time_regex.search(argument)

        if time and any(time.groups()):
            invalid = False
            pm = bool(time.group('am_or_pm') == 'pm')
            hour = int(time.group('hour') or now.hour)
            # if it is in 12-hour format and pm, just increase it by 12 so that it is in 24-hour format
            if pm and hour <= 12:
                hour += 12
            minute = int(time.group('minute') or now.minute)
            second = int(time.group('second') or now.second)

        else:
            # set the time to the current if no time provided
            hour, minute, second = now.hour, now.minute, now.second

        if invalid:
            raise DatetimeConversionFailure(argument)

        try:
            result = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
        except Exception as exc:
            raise DatetimeConversionFailure(argument, original_exception=exc)
        else:
            return result


@bot.group()
async def birthday(ctx):
    pass


@birthday.command()
async def set(ctx, *, date: datetimeConverter):
    await ctx.message.delete()

    with open("birthdays.json", "r") as f:
        data = json.load(f)

    if str(ctx.author.id) in data[str(ctx.guild.id)]['birthdays']:
        embed = discord.Embed(
            description=bd_set_already_exists.format(prefix=bot.command_prefix(bot, ctx.message)[-1]),
            color=discord.Color.orange())
        return await ctx.send(embed=embed, delete_after=10)

    data[str(ctx.guild.id)]['birthdays'][str(ctx.author.id)] = {'day': date.day, 'month': date.month, 'year': date.year}

    await ctx.send(
        embed=discord.Embed(
            description=f'Successful set your birthday to <t:{int(date.timestamp())}:D>',
            color=discord.Color.green()),
        delete_after=5
    )

    with open('birthdays.json', 'w') as fp:
        json.dump(data, fp, indent=4)

    await update_birthday_panel(guild_id=ctx.guild.id)

@birthday.command()
@commands.cooldown(2, 600, commands.BucketType.member)
async def edit(ctx, *, date: datetimeConverter):
    await ctx.message.delete()

    with open("birthdays.json", "r") as f:
        data = json.load(f)

    data[str(ctx.guild.id)]['birthdays'][str(ctx.author.id)] = {'day': date.day, 'month': date.month, 'year': date.year}

    with open('birthdays.json', 'w') as fp:
        json.dump(data, fp, indent=4)

    await ctx.send(
        embed=discord.Embed(
            description=f'Successful updated your birthday to <t:{int(date.timestamp())}:D>',
            color=discord.Color.green()),
        delete_after=5
    )

    await update_birthday_panel(guild_id=ctx.guild.id)

@edit.error
async def edit_error(ctx, exc):
    if isinstance(exc, commands.CommandOnCooldown):
        await ctx.send(
            embed=discord.Embed(
                title='You\'r on cooldown 🧊',
                description=f'You could use this command again in {exc.retry_after:.f0} Seconds. {ctx.author.mention}',
                color=discord.Color.red()
            ),
            delete_after=5
        )
    else:
        await ctx.send(
            embed=discord.Embed(
                title='❗There was an Error while executing this command❗',
                description=f'```py\n{exc}\n```',
                color=discord.Color.red()
            ),
            delete_after=10
        )

@birthday.command()
@commands.cooldown(1, 600, commands.BucketType.member)
async def remove(ctx):
    await ctx.message.delete()

    with open("birthdays.json", "r") as f:
        data = json.load(f)

    if str(ctx.author.id) not in data[str(ctx.guild.id)]['birthdays']:
        return await ctx.send(
            embed=discord.Embed(
                title='No birthday set',
                description='You haven\'t set a birthday yet.'
                            'To set it use `{prefix}birthday set <date>`(without the `<>`).'.format(prefix=bot.command_prefix(bot, None)[-1]),
                color=discord.Color.orange()
            ),
            delete_after=10
        )
    else:
        data[str(ctx.guild.id)]['birthdays'].pop(str(ctx.author.id))
        await ctx.send(
            embed=discord.Embed(
                title='Successful removed',
                description='Successful removed your birthday from the list.',
                color=discord.Color.green()
            ),
            delete_after=10
        )

    with open('birthdays.json', 'w') as fp:
        json.dump(data, fp, indent=4)

    await update_birthday_panel(guild_id=ctx.guild.id)

@remove.error
async def remove_error(ctx, exc):
    await ctx.message.delete()
    if isinstance(exc, commands.CommandOnCooldown):
        await ctx.send(
            embed=discord.Embed(
                title='You\'r on cooldown 🧊',
                description=f'You could use this command again in {int(exc.retry_after)} Seconds',
                color=discord.Color.red()
            )
        )
    else:
        await ctx.send(
            embed=discord.Embed(
                title='❗There was an Error while executing this command❗',
                description=f'```py\n{exc}\n```',
                color=discord.Color.red()
            )
        )

@birthday.command()
@commands.cooldown(2, 300, commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def channel(ctx, channel: discord.TextChannel):
    await ctx.message.delete()

    with open("birthdays.json", "r") as f:
        data = json.load(f)

    data[str(ctx.guild.id)]['bd_channel_id'] = channel.id
    data[str(ctx.guild.id)]['bd_message_id'] = channel.id

    await ctx.send(
        embed=discord.Embed(
            title='Channel successful set',
            description=f'Successful set {channel.mention} as the birthday channel.',
            color=discord.Color.green()
        ),
        delete_after=10
    )

    with open('birthdays.json', 'w') as fp:
        json.dump(data, fp, indent=4)

    await update_birthday_panel(guild_id=ctx.guild.id)

@channel.error
async def channel_error(ctx, exc):
    await ctx.message.delete()
    if isinstance(exc, commands.CommandOnCooldown):
        await ctx.send(
            embed=discord.Embed(
                title='You\'r on cooldown 🧊',
                description=f'You could use this command again in {exc.retry_after:.f0} Seconds',
                color=discord.Color.red()
            )
        )
    elif isinstance(exc, commands.MissingPermissions):
        await ctx.send(
            embed=discord.Embed(
                title='❗Missing Permissions❗',
                description=f'Only a member with administrator permissions could set the channel.',
                color=discord.Color.red()
            )
        )
    else:
        await ctx.send(
            embed=discord.Embed(
                title='❗There was an Error while executing this command❗',
                description=f'```py\n{exc}\n```',
                color=discord.Color.red()
            )
        )

bot.run(TOKEN)
