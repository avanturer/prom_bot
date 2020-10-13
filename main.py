from builtins import range
import discord
import json
import requests
import asyncio
import datetime
import psycopg2
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from config import settings

bad_words = ['6ля', '6лядь', '6лять', 'b3ъeб', 'cock', 'cunt', 'e6aль', 'ebal', 'eblan', 'eбaл', 'eбaть', 'eбyч',
             'eбать', 'eбёт', 'eблантий', 'fuck', 'fucker', 'fucking', 'xyёв', 'xyй', 'xyя', 'xуе,xуй', 'xую', 'zaeb',
             'zaebal', 'zaebali', 'zaebat', 'архипиздрит', 'ахуел', 'ахуеть', 'бздение', 'бздеть', 'бздех', 'бздецы',
             'бздит', 'бздицы', 'бздло', 'бзднуть', 'бздун', 'бздунья', 'бздюха', 'бздюшка', 'бздюшко', 'бля', 'блябу',
             'блябуду', 'бляд', 'бляди', 'блядина', 'блядище', 'блядки', 'блядовать', 'блядство', 'блядун', 'блядуны',
             'блядунья', 'блядь', 'блядюга', 'блять', 'вафел', 'вафлёр', 'взъебка', 'взьебка', 'взьебывать', 'въеб',
             'въебался', 'въебенн', 'въебусь', 'въебывать', 'выблядок', 'выблядыш', 'выеб', 'выебать', 'выебен',
             'выебнулся', 'выебон', 'выебываться', 'выпердеть', 'высраться', 'выссаться', 'вьебен', 'гавно', 'гавнюк',
             'гавнючка', 'гамно', 'гандон', 'гнид', 'гнида', 'гниды', 'говенка', 'говенный', 'говешка', 'говназия',
             'говнецо', 'говнище', 'говно', 'говноед', 'говнолинк', 'говночист', 'говнюк', 'говнюха', 'говнядина',
             'говняк', 'говняный', 'говнять', 'гондон', 'доебываться', 'долбоеб', 'долбоёб', 'долбоящер', 'дрисня',
             'дрист', 'дристануть', 'дристать', 'дристун', 'дристуха', 'дрочелло', 'дрочена', 'дрочила', 'дрочилка',
             'дрочистый', 'дрочить', 'дрочка', 'дрочун', 'е6ал', 'е6ут', 'е', 'тво', 'мать', 'ё', 'тво', 'мать', 'ёбaн',
             'ебaть', 'ебyч', 'ебал', 'ебало', 'ебальник', 'ебан', 'ебанамать', 'ебанат', 'ебаная', 'ёбаная',
             'ебанический', 'ебанный', 'ебанныйврот', 'ебаное', 'ебануть', 'ебануться', 'ёбаную', 'ебаный', 'ебанько',
             'ебарь', 'ебат', 'ёбат', 'ебатория', 'ебать', 'ебать-копать', 'ебаться', 'ебашить', 'ебёна', 'ебет',
             'ебёт', 'ебец', 'ебик', 'ебин', 'ебись', 'ебическая', 'ебки', 'ебла', 'еблан', 'ебливый', 'еблище', 'ебло',
             'еблыст', 'ебля', 'ёбн', 'ебнуть', 'ебнуться', 'ебня', 'ебошить', 'ебская', 'ебский', 'ебтвоюмать', 'ебун',
             'ебут', 'ебуч', 'ебуче', 'ебучее', 'ебучий', 'ебучим', 'ебущ', 'ебырь', 'елда', 'елдак', 'елдачить',
             'жопа', 'жопу', 'заговнять', 'задрачивать', 'задристать', 'задрота', 'зае6', 'заё6', 'заеб', 'заёб',
             'заеба', 'заебал', 'заебанец', 'заебастая', 'заебастый', 'заебать', 'заебаться', 'заебашить', 'заебистое',
             'заёбистое', 'заебистые', 'заёбистые', 'заебистый', 'заёбистый', 'заебись', 'заебошить', 'заебываться',
             'залуп', 'залупа', 'залупаться', 'залупить', 'залупиться', 'замудохаться', 'запиздячить', 'засерать',
             'засерун', 'засеря', 'засирать', 'засрун', 'захуячить', 'заябестая', 'злоеб', 'злоебучая', 'злоебучее',
             'злоебучий', 'ибанамат', 'ибонех', 'изговнять', 'изговняться', 'изъебнуться', 'ипать', 'ипаться', 'ипаццо',
             'Какдвапальцаобоссать', 'конча', 'курва', 'курвятник', 'лох', 'лошарa', 'лошара', 'лошары', 'лошок',
             'лярва', 'малафья', 'манда', 'мандавошек', 'мандавошка', 'мандавошки', 'мандей', 'мандень', 'мандеть',
             'мандища', 'мандой', 'манду', 'мандюк', 'минет', 'минетчик', 'минетчица', 'млять', 'мокрощелка',
             'мокрощёлка', 'мразь', 'мудak', 'мудaк', 'мудаг', 'мудак', 'муде', 'мудель', 'мудеть', 'муди', 'мудил',
             'мудила', 'мудистый', 'мудня', 'мудоеб', 'мудозвон', 'мудоклюй', 'н', 'хер', 'н', 'хуй', 'набздел',
             'набздеть', 'наговнять', 'надристать', 'надрочить', 'наебать', 'наебет', 'наебнуть', 'наебнуться',
             'наебывать', 'напиздел', 'напиздели', 'напиздело', 'напиздили', 'насрать', 'настопиздить', 'нахер',
             'нахрен', 'нахуй', 'нахуйник', 'н', 'ебет', 'н', 'ебёт', 'невротебучий', 'невъебенно', 'нехира', 'нехрен',
             'Нехуй', 'нехуйственно', 'ниибацо', 'ниипацца', 'ниипаццо', 'ниипет', 'никуя', 'нихера', 'нихуя',
             'обдристаться', 'обосранец', 'обосрать', 'обосцать', 'обосцаться', 'обсирать', 'объебос', 'обьебат',
             'обьебос', 'однохуйственно', 'опездал', 'опизде', 'опизденивающе', 'остоебенить', 'остопиздеть',
             'отмудохать', 'отпиздить', 'отпиздячить', 'отпороть', 'отъебись', 'охуевательский', 'охуевать',
             'охуевающий', 'охуел', 'охуенно', 'охуеньчик', 'охуеть', 'охуительно', 'охуительный', 'охуяньчик',
             'охуячивать', 'охуячить', 'очкун', 'падла', 'падонки', 'падонок', 'паскуда', 'педерас', 'педик', 'педрик',
             'педрила', 'педрилло', 'педрило', 'педрилы', 'пездень', 'пездит', 'пездишь', 'пездо', 'пездят',
             'пердануть', 'пердеж', 'пердение', 'пердеть', 'пердильник', 'перднуть', 'пёрднуть', 'пердун', 'пердунец',
             'пердунина', 'пердунья', 'пердуха', 'пердь', 'переёбок', 'пернуть', 'пёрнуть', 'пи3д', 'пи3де', 'пи3ду',
             'пиzдец', 'пидар', 'пидарaс', 'пидарас', 'пидарасы', 'пидары', 'пидор', 'пидорасы', 'пидорка', 'пидорок',
             'пидоры', 'пидрас', 'пизда', 'пиздануть', 'пиздануться', 'пиздарваньчик', 'пиздато', 'пиздатое',
             'пиздатый', 'пизденка', 'пизденыш', 'пиздёныш', 'пиздеть', 'пиздец', 'пиздит', 'пиздить', 'пиздиться',
             'пиздишь', 'пиздища', 'пиздище', 'пиздобол', 'пиздоболы', 'пиздобратия', 'пиздоватая', 'пиздоватый',
             'пиздолиз', 'пиздонутые', 'пиздорванец', 'пиздорванка', 'пиздострадатель', 'пизду', 'пиздуй', 'пиздун',
             'пиздунья', 'пизды', 'пиздюга', 'пиздюк', 'пиздюлина', 'пиздюля', 'пиздят', 'пиздячить', 'писбшки',
             'писька', 'писькострадатель', 'писюн', 'писюшка', 'п', 'хуй', 'п', 'хую', 'подговнять', 'подонки',
             'подонок', 'подъебнуть', 'подъебнуться', 'поебать', 'поебень', 'поёбываает', 'поскуда', 'посрать',
             'потаскуха', 'потаскушка', 'похер', 'похерил', 'похерила', 'похерили', 'похеру', 'похрен', 'похрену',
             'похуй', 'похуист', 'похуистка', 'похую', 'придурок', 'приебаться', 'припиздень', 'припизднутый',
             'припиздюлина', 'пробзделся', 'проблядь', 'проеб', 'проебанка', 'проебать', 'промандеть', 'промудеть',
             'пропизделся', 'пропиздеть', 'пропиздячить', 'раздолбай', 'разхуячить', 'разъеб', 'разъеба', 'разъебай',
             'разъебать', 'распиздай', 'распиздеться', 'распиздяй', 'распиздяйство', 'распроеть', 'сволота', 'сволочь',
             'сговнять', 'секель', 'серун', 'серька', 'сестроеб', 'сикель', 'сила', 'сирать', 'сирывать', 'соси',
             'спиздел', 'спиздеть', 'спиздил', 'спиздила', 'спиздили', 'спиздит', 'спиздить', 'срака', 'сраку',
             'сраный', 'сранье', 'срать', 'срун', 'ссака', 'ссышь', 'стерва', 'страхопиздище', 'сука', 'суки',
             'суходрочка', 'сучара', 'сучий', 'сучка', 'сучко', 'сучонок', 'сучье', 'сцание', 'сцать', 'сцука', 'сцуки',
             'сцуконах', 'сцуль', 'сцыха', 'сцышь', 'съебаться', 'сыкун', 'трахае6', 'трахаеб', 'трахаёб', 'трахатель',
             'ублюдок', 'уебать', 'уёбища', 'уебище', 'уёбище', 'уебищное', 'уёбищное', 'уебк', 'уебки', 'уёбки',
             'уебок', 'уёбок', 'урюк', 'усраться', 'ушлепок', 'х_у_я_р_а', 'хyё', 'хyй', 'хyйня', 'хамло', 'хер',
             'херня', 'херовато', 'херовина', 'херовый', 'хитровыебанный', 'хитрожопый', 'хуeм', 'хуе', 'хуё',
             'хуевато', 'хуёвенький', 'хуевина', 'хуево', 'хуевый', 'хуёвый', 'хуек', 'хуёк', 'хуел', 'хуем', 'хуенч',
             'хуеныш', 'хуенький', 'хуеплет', 'хуеплёт', 'хуепромышленник', 'хуерик', 'хуерыло', 'хуесос', 'хуесоска',
             'хуета', 'хуетень', 'хуею', 'хуи', 'хуй', 'хуйком', 'хуйло', 'хуйня', 'хуйрик', 'хуище', 'хуля', 'хую',
             'хуюл', 'хуя', 'хуяк', 'хуякать', 'хуякнуть', 'хуяра', 'хуясе', 'хуячить', 'целка', 'чмо', 'чмошник',
             'чмырь', 'шалава', 'шалавой', 'шараёбиться', 'шлюха', 'шлюхой', 'шлюшка','cock','dick','penis','еба','ема','ебалай','пенис','ля','нах','бл','suck','f u']
botid = f"<@{settings['id']}>"
SPECIAL_PREFIX = ""


def context_prefix(client, message):
    special_command1 = client.get_command("-rep")
    special_command2 = client.get_command("+rep")
    if any(
            message.content.startswith(f"{SPECIAL_PREFIX}{command_string}")
            for command_string in
            [special_command1.name, *special_command1.aliases, special_command2.name, *special_command2.aliases]
    ):
        return SPECIAL_PREFIX
    return "!"


client = commands.Bot(command_prefix=context_prefix)
client.remove_command('help')

connection = psycopg2.connect(
    host='ec2-34-251-118-151.eu-west-1.compute.amazonaws.com',
    user='nmmdqfjrgykixx',
    password='ba0c960897eb65cddaeff739205f536657b77ee28afd3a10aaa90886c7891f33',
    dbname='ddru8hp0ktb4jb'
)
cursor = connection.cursor()


def gt(data: str = None, id: int = None):
    cursor.execute(f"SELECT {data} FROM users WHERE id = {id}")
    return str(cursor.fetchone()[0])


# Ready
@client.event
async def on_ready():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    id BIGINT,
    lvl INT,
    lvlup INT,
    cash FLOAT,
    cashm FLOAT,
    vtime FLOAT,
    rep INT,
    warns INT,
    bans INT,
    bans_time FLOAT,
    mute_time FLOAT
    )''')
    cursor.execute("""CREATE TABLE IF NOT EXISTS voice_data(
            c_name TEXT,
            c_id BIGINT,
            v_name TEXT,
            v_id BIGINT
        )""")
    cursor.execute(f"SELECT c_name FROM voice_data")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO voice_data VALUES ('0',0,'0',0)")
        connection.commit()
    for guild in client.guilds:
        for member in guild.members:
            cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO users VALUES ('{member}',{member.id},1,2000,0,10.0,0,0,0,0,0,0)")
            else:
                pass
    connection.commit()
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game('!help'))

    for guild in client.guilds:
        for member in guild.members:
            # REP 0 AND Create
            rep_0 = discord.utils.get(guild.roles, name='Реп: нейтральный')
            if rep_0 is None:
                await guild.create_role(name="Реп: нейтральный")
                rep_0 = discord.utils.get(guild.roles, name='Реп: нейтральный')

            rep: int = int(gt('rep', member.id))
            if rep == 0 and member.id != settings['id']:
                await member.add_roles(rep_0)

            rep_m1000 = discord.utils.get(guild.roles, name='Реп: 💩')
            if rep_m1000 is None:
                await guild.create_role(name="Реп: 💩", colour=discord.Colour(0x85502b))
                rep_m1000 = discord.utils.get(guild.roles, name='Реп: 💩')

            rep_m100_51 = discord.utils.get(guild.roles, name='Реп: 👺сын беса👹')
            if rep_m100_51 is None:
                await guild.create_role(name="Реп: 👺сын беса👹", colour=discord.Colour(0xaf0d1a))
                rep_m100_51 = discord.utils.get(guild.roles, name='Реп: 👺сын беса👹')

            rep_m50_26 = discord.utils.get(guild.roles, name='Реп: ☢️Toxic☢️')
            if rep_m50_26 is None:
                await guild.create_role(name="Реп: ☢️Toxic☢️", colour=discord.Colour(0x39ff14))
                rep_m50_26 = discord.utils.get(guild.roles, name='Реп: ☢️Toxic☢️')

            rep_m25_16 = discord.utils.get(guild.roles, name='Реп: 🐛вредитель')
            if rep_m25_16 is None:
                await guild.create_role(name="Реп: 🐛вредитель", colour=discord.Colour(0x64941f))
                rep_m25_16 = discord.utils.get(guild.roles, name='Реп: 🐛вредитель')

            rep_m15_6 = discord.utils.get(guild.roles, name='Реп: ребёнок с углем')
            if rep_m15_6 is None:
                await guild.create_role(name="Реп: ребёнок с углем", colour=discord.Colour(0x010d1a))
                rep_m15_6 = discord.utils.get(guild.roles, name='Реп: ребёнок с углем')

            rep_m5_1 = discord.utils.get(guild.roles, name='Реп: 🙊пакостник😝')
            if rep_m5_1 is None:
                await guild.create_role(name="Реп: 🙊пакостник😝", colour=discord.Colour(0xffc83d))
                rep_m5_1 = discord.utils.get(guild.roles, name='Реп: 🙊пакостник😝')

            rep_1_5 = discord.utils.get(guild.roles, name='Реп: наводчик😉')
            if rep_1_5 is None:
                await guild.create_role(name="Реп: наводчик😉", colour=discord.Colour(0xd48c00))
                rep_1_5 = discord.utils.get(guild.roles, name='Реп: наводчик😉')

            rep_6_15 = discord.utils.get(guild.roles, name='Реп: мамин советчик🕵')
            if rep_6_15 is None:
                await guild.create_role(name="Реп: мамин советчик🕵", colour=discord.Colour(0x6d6767))
                rep_6_15 = discord.utils.get(guild.roles, name='Реп: мамин советчик🕵')

            rep_16_25 = discord.utils.get(guild.roles, name='Реп: умник🤓')
            if rep_16_25 is None:
                await guild.create_role(name="Реп: умник🤓", colour=discord.Colour(0xf03a17))
                rep_16_25 = discord.utils.get(guild.roles, name='Реп: умник🤓')

            rep_26_50 = discord.utils.get(guild.roles, name='Реп: просвещённый🧐')
            if rep_26_50 is None:
                await guild.create_role(name="Реп: просвещённый🧐", colour=discord.Colour(0xb3dbf2))
                rep_26_50 = discord.utils.get(guild.roles, name='Реп: просвещённый🧐')

            rep_51_100 = discord.utils.get(guild.roles, name='Реп: хацкер👨‍💻')
            if rep_51_100 is None:
                await guild.create_role(name="Реп: хацкер👨‍💻", colour=discord.Colour(0x17891c))
                rep_51_100 = discord.utils.get(guild.roles, name='Реп: хацкер👨‍💻')

            rep_101_500 = discord.utils.get(guild.roles, name='Реп: ИИ🤖')
            if rep_101_500 is None:
                await guild.create_role(name="Реп: ИИ🤖", colour=discord.Colour(0x31d2f7))
                rep_101_500 = discord.utils.get(guild.roles, name='Реп: ИИ🤖')

            rep_501_999 = discord.utils.get(guild.roles, name='Реп: 😎GOD😎')
            if rep_501_999 is None:
                await guild.create_role(name="Реп: 😎GOD😎", colour=discord.Colour(0xffd700))
                rep_501_999 = discord.utils.get(guild.roles, name='Реп: 😎GOD😎')

            rep_1000 = discord.utils.get(guild.roles, name='Реп: 🧠')
            if rep_1000 is None:
                await guild.create_role(name="Реп: 🧠", colour=discord.Colour(0xe84757))
                rep_1000 = discord.utils.get(guild.roles, name='Реп: 🧠')

            # MUTE
            mute_role = discord.utils.get(guild.roles, name='muted')
            mute_time: float = float(gt('mute_time', member.id))
            if mute_time > 0:
                if mute_time > 0:
                    while mute_time != 0:
                        await asyncio.sleep(1)
                        cursor.execute("UPDATE users SET mute_time = mute_time - 1 WHERE id = {} ".format(member.id))
                        connection.commit()
                        mute_time: float = float(gt('mute_time', member.id))
                        if mute_time == 0:
                            await member.remove_roles(mute_role)
                            emb = None
                            return
            # BAN
            ban_role = discord.utils.get(guild.roles, name='ban')
            bans_time: float = float(gt('bans_time', member.id))
            bans: int = int(gt('bans', member.id))
            if bans > 0:
                if bans_time > 0:
                    while bans_time != 0:
                        await asyncio.sleep(1)
                        cursor.execute("UPDATE users SET bans_time = bans_time - 1 WHERE id = {} ".format(member.id))
                        connection.commit()
                        bans_time: float = float(gt('bans_time', member.id))
                        if bans_time == 0:
                            emb = discord.Embed(title=':white_check_mark: Разбан',
                                                description="Вы были разбанены.\n\n"
                                                            "**Модератор:** {}"
                                                .format(botid),
                                                colour=0x28CC28)

                            await member.send(embed=emb)
                            cursor.execute("UPDATE users SET warns = 0 WHERE id = {} ".format(member.id))
                            connection.commit()
                            await member.remove_roles(ban_role)


@client.event
async def on_member_join(member):
    cursor.execute(f"SELECT id FROM users WHERE id = {member.id}")
    if cursor.fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}','{member.id}', 1, 0, 0, 10.0, 0, 0, 0, 0, 0, 0)")
        connection.commit()
    else:
        pass


# VOICE TIME AND COINS
@client.event
async def on_voice_state_update(member, before, after):
    await private_room(member, before, after)
    if after.channel:
        cursor.execute(f"SELECT v_name FROM voice_data")
        voice_name = str(cursor.fetchone()[0])
        while after.channel:
            if before.channel is not None:
                if str(before.channel) != member.voice.channel:
                    break
            await asyncio.sleep(1)
            cursor.execute("UPDATE users SET cash = cash + (cashm/60) WHERE id = {} ".format(member.id))
            cursor.execute("UPDATE users SET vtime = vtime + 1 WHERE id = {} ".format(member.id))
            vtime = gt('vtime', member.id)
            connection.commit()
            vtime: float = float(vtime) / 3600
            if vtime >= 1 and vtime < 50:
                pasprot = discord.utils.get(member.guild.roles, name='Паспорт')
                await member.add_roles(pasprot)
            if vtime >= 50:
                postol = discord.utils.get(member.guild.roles, name='Постоялец')
                await member.remove_roles(pasprot)
                await member.add_roles(postol)


async def private_room(member, before, after):
    guild = member.guild
    cursor.execute(f"SELECT v_name FROM voice_data")
    voice_name = str(cursor.fetchone()[0])
    cursor.execute(f"SELECT c_id FROM voice_data")
    category_id = int(cursor.fetchone()[0])
    if str(after.channel) == voice_name:
        for guild in client.guilds:
            main_category = discord.utils.get(guild.categories, id=category_id)
            new_channel = await guild.create_voice_channel(name=member.name, category=main_category)
            await member.move_to(new_channel)
            await new_channel.set_permissions(member, connect=True, move_members=True,
                                              manage_channels=True)

            def check_for_zero(a, b, c):
                return len(new_channel.members) == 0

            await client.wait_for('voice_state_update', check=check_for_zero)
            await new_channel.delete()


@client.command(pass_context=True)
async def kick(ctx, member: discord.Member):
    channel = ctx.message.author.voice.channel
    if member.voice is None:
        await ctx.send(f"{ctx.author.mention}, пользователя нет в вашем войс канале.", delete_after=5)
        return
    if not channel.permissions_for(ctx.author).manage_channels:
        await ctx.send(f"{ctx.author.mention}, у вас нет прав, вы находитесь не в своем канале.", delete_after=5)
        return
    if ctx.author == member:
        await ctx.send(f"{ctx.author.mention}, вы не можете кикнуть себя.", delete_after=5)
        return
    await member.edit(voice_channel=None)
    await channel.set_permissions(member, connect=False)
    await ctx.send(f"{member.mention}, успешно кикнут.", delete_after=3)


@client.command()
@commands.has_permissions(administrator=True)
async def private(ctx, name_category: str = None, name_voice: str = None):
    guild = ctx.guild
    if name_category is None or name_voice is None:
        await ctx.send(f"{ctx.author.mention}, введите название категории и войс канала.", delete_after=5)
        return
    category_private = await guild.create_category_channel(name=f"{name_category}")
    voice_private = await guild.create_voice_channel(name=name_voice, category=category_private)
    await ctx.send(f"{ctx.author.mention}, фуннкция приватов успешно включена.", delete_after=5)
    cursor.execute("UPDATE voice_data SET c_name = '{}'".format(name_category))
    cursor.execute("UPDATE voice_data SET c_id = '{}'".format(category_private.id))
    cursor.execute("UPDATE voice_data SET v_name = '{}'".format(voice_private))
    cursor.execute("UPDATE voice_data SET v_id = '{}'".format(voice_private.id))
    connection.commit()


# REPUTATION pre-release


@client.command(aliases=['arep'])
@commands.has_permissions(administrator=True)
async def admin_reputation(ctx, member: discord.Member, rep=1, arg='Не указана'):
    reason = arg
    await rep_brain(ctx, member, rep, reason)
    await ctx.send(f"Пользователю {member}, было начислено ``{rep}`` очко(-в) репутации.", delete_after=5)


@client.command(aliases=['+rep'])
async def reputation_plus(ctx, member: discord.Member, *, arg='Не указана'):
    if ctx.author.id == member.id or member.id == settings['id']:
        return
    reason = arg
    await rep_brain(ctx, member, 1, reason)
    await ctx.send(f"Пользователю {member}, было начислено ``{1}`` очко репутации.", delete_after=5)


@client.command(aliases=['-rep'])
async def reputation_minus(ctx, member: discord.Member, *, arg='Не указана'):
    if ctx.author.id == member.id or member.id == settings['id']:
        return
    reason = arg
    await rep_brain(ctx, member, -1, reason)
    await ctx.send(f"Пользователю {member}, было начислено ``{-1}`` очко репутации.", delete_after=5)


async def rep_brain(ctx, member, crep: int = None, reason=None):
    rep_m1000 = discord.utils.get(ctx.message.guild.roles, name='Реп: 💩')
    rep_m100_51 = discord.utils.get(ctx.message.guild.roles, name='Реп: 👺сын беса👹')
    rep_m50_26 = discord.utils.get(ctx.message.guild.roles, name='Реп: ☢️Toxic☢️')
    rep_m25_16 = discord.utils.get(ctx.message.guild.roles, name='Реп: 🐛вредитель')
    rep_m15_6 = discord.utils.get(ctx.message.guild.roles, name='Реп: ребёнок с углем')
    rep_m5_1 = discord.utils.get(ctx.message.guild.roles, name='Реп: 🙊пакостник😝')
    rep_0 = discord.utils.get(ctx.message.guild.roles, name='Реп: нейтральный')
    rep_1_5 = discord.utils.get(ctx.message.guild.roles, name='Реп: наводчик😉')
    rep_6_15 = discord.utils.get(ctx.message.guild.roles, name='Реп: мамин советчик🕵')
    rep_16_25 = discord.utils.get(ctx.message.guild.roles, name='Реп: умник🤓')
    rep_26_50 = discord.utils.get(ctx.message.guild.roles, name='Реп: просвещённый🧐')
    rep_51_100 = discord.utils.get(ctx.message.guild.roles, name='Реп: хацкер👨‍💻')
    rep_101_500 = discord.utils.get(ctx.message.guild.roles, name='Реп: ИИ🤖')
    rep_501_999 = discord.utils.get(ctx.message.guild.roles, name='Реп: 😎GOD😎')
    rep_1000 = discord.utils.get(ctx.message.guild.roles, name='Реп: 🧠')

    last_rep: str = None
    rep: int = int(gt('rep', member.id))
    if rep <= -1000:
        last_rep = rep_m1000
    if -100 <= rep <= -51:
        last_rep = rep_m100_51
    if -50 <= rep <= -26:
        last_rep = rep_m50_26
    if -25 <= rep <= -16:
        last_rep = rep_m25_16
    if -15 <= rep <= -6:
        last_rep = rep_m15_6
    if -5 <= rep <= -1:
        last_rep = rep_m5_1
    if rep == 0:
        last_rep = rep_0
    if 1 <= rep <= 5:
        last_rep = rep_1_5
    if 6 <= rep <= 15:
        last_rep = rep_6_15
    if 16 <= rep <= 25:
        last_rep = rep_16_25
    if 26 <= rep <= 50:
        last_rep = rep_26_50
    if 51 <= rep <= 100:
        last_rep = rep_51_100
    if 101 <= rep <= 500:
        last_rep = rep_101_500
    if 501 <= rep <= 999:
        last_rep = rep_501_999
    if rep >= 1000:
        last_rep = rep_1000

    cursor.execute("UPDATE users SET rep = rep + {} WHERE id = {} ".format(crep, member.id))
    connection.commit()

    rep: int = int(gt('rep', member.id))

    rep_now: str = None
    if rep <= -1000:
        rep_now = rep_m1000
    if -100 <= rep <= -51:
        rep_now = rep_m100_51
    if -50 <= rep <= -26:
        rep_now = rep_m50_26
    if -25 <= rep <= -16:
        rep_now = rep_m25_16
    if -15 <= rep <= -6:
        rep_now = rep_m15_6
    if -5 <= rep <= -1:
        rep_now = rep_m5_1
    if rep == 0:
        rep_now = rep_0
    if 1 <= rep <= 5:
        rep_now = rep_1_5
    if 6 <= rep <= 15:
        rep_now = rep_6_15
    if 16 <= rep <= 25:
        rep_now = rep_16_25
    if 26 <= rep <= 50:
        rep_now = rep_26_50
    if 51 <= rep <= 100:
        rep_now = rep_51_100
    if 101 <= rep <= 500:
        rep_now = rep_101_500
    if 501 <= rep <= 999:
        rep_now = rep_501_999
    if rep >= 1000:
        rep_now = rep_1000

    await member.remove_roles(last_rep)
    await member.add_roles(rep_now)

    await member.send(
        f"Вам было добавлено ``{crep}`` очко репутации пользователем {ctx.author.mention}.\n"
        f"Причина: ``{reason}``.\n"
        f"Ваша текущая репутация: ``{rep}``, ``{rep_now}``.")


# Stats


@client.command()
async def stats(ctx):
    emb = discord.Embed(title='Статистика Вашего аккаунта', color=0xf1b958)
    emb.add_field(
        name="Уровень",
        value=f"{gt('lvl', ctx.author.id)}"
    )

    emb.add_field(
        name="Шестерёнки",
        value=f"{gt('round(cash::numeric, 1)', ctx.author.id)}"
    )
    emb.add_field(
        name="Шестерёнок в минуту",
        value=f"{gt('cashm', ctx.author.id)}"
    )
    vtime = f"{gt('vtime', ctx.author.id)}"
    vtime: float = float(vtime) / 3600
    emb.add_field(
        name="Время в войсе",
        value=f"{round(vtime)} часов"
    )
    emb.add_field(
        name="Репутация",
        value=f"{gt('rep', ctx.author.id)}"
    )
    emb.add_field(
        name="Количество варнов",
        value=f"{gt('warns', ctx.author.id)}/3"
    )
    emb.set_footer(text=f"Стоимость {gt('lvl+1', ctx.author.id)} уровня: {gt('lvlup', ctx.author.id)}")
    await ctx.author.send(embed=emb)


# UP LVL
@client.command()
async def up(ctx):
    cash: float = float(
        gt('cash', ctx.author.id))
    lvlup: int = int(
        gt('lvlup', ctx.author.id))
    lvl: int = int(
        gt('lvl', ctx.author.id))

    if cash >= lvlup:
        cursor.execute("UPDATE users SET lvl = lvl + 1 WHERE id = {} ".format(ctx.author.id))
        cursor.execute("UPDATE users SET cash = cash - lvlup WHERE id = {} ".format(ctx.author.id))
        cursor.execute("UPDATE users SET lvlup = lvlup + 2000 WHERE id = {} ".format(ctx.author.id))
        cursor.execute("UPDATE users SET cashm = cashm + 2 WHERE id = {} ".format(ctx.author.id))
        connection.commit()
        cash: float = float(
            gt('cash', ctx.author.id))
        await ctx.author.send(
            f'Вы успешно приобрели **{lvl + 1} уровень**, теперь шестерёнки будут фармиться ещё быстрее! \n'
            f"С Вас было списано **{lvlup} шестерёнок**  \n"
            f"Теперь ваш Баланс составляет **{round(cash, 1)} шестерёнок**")
    else:
        await ctx.send(f"{ctx.author.mention}, у вас недостаточно средств.", delete_after = 3)


# HELP
@client.command(pass_context=True)
async def help(ctx, dlc: str = None):
    raz = ['модерация', 'учитель', 'развлечения']
    if dlc is not None:
        dlc = dlc.lower()
        if dlc not in raz:
            ctx.send(f"{ctx.author.mention}, раздел введен не правильно.", delete_after=5)
            return
        else:
            if dlc == raz[0]:
                emb = discord.Embed(title='**Модерация**', description=
                "``!warn @user`` - добавляет участнику 1 варн, что бы снять варн есть команда ``!unwarn @user``, "
                "когда пользователь наберёт 3 варна, он автоматически уйдет в бан на 2 дня и счетчик кол-ва банов "
                "увеличится на 1, при достижении 4х банов, пользователь уходит в бан навсегда.\n\n"

                "``!ban @user days(0 если хотите забанить навсегда) reason(не обязательно)`` - банит участника на опеделённое кол-во дней, "
                "что бы разбанить человека есть команда ``!unban @user`` (она побочно уменьшает счётчик банов на 1).\n\n"

                "``!mute @user minutes(0 если хотите замутить навсегда) reason(не обязательно)`` - мутит участника на определённое кол-во минут, "
                "что бы размутить человека есть команда ``!unmute @user``.\n\n"

                "``!arep @user +-value`` - добавляет или убавляет репутацию участника на value.\n\n"

                "``!clear, !clear n, !clear all`` - !clear удаляет последнее сообщение, !clear n удаляет n сообщений, !clear all удаляет "
                "все сообщения в канале. ")
                await ctx.send(embed=emb, delete_after=120)
                return
            if dlc == raz[1]:
                emb = discord.Embed(title='**Учитель**',
                                    description="``!lesson url`` - команда отправляет сообщение от лица бота о начале урока (в канал, в котором вы прописали эту команду), "
                                                "пингуя ``@everyone``."
                                    )
                await ctx.send(embed=emb, delete_after=30)
                return
            if dlc == raz[2]:
                emb = discord.Embed(title='**Развлечения**',
                                    description="``На этом сервере присутствует система репутации, а также личной статистики пользователя.``\n\n"
                                                "Репутация - показывает вашу продуктивность на сервере в виде роли, как её можно получить смотрите в канале <#761963102886428672>\n"
                                                "Статистика пользователя - ваша личная карточка с разными показателями.\n\n\n"

                                                "``!stats`` - бот присылает вам в лс карточку с вашей статистикой.\n\n"

                                                "``!up`` - увеличивает количество шестеренок в минуту.\n\n"

                                                "``+-rep @user reason(не обязательно)`` - команда, с помощью которой, вы можете начислить(отнять) пользователю 1 очко репутации за какую то заслугу.\n\n"

                                                "``!kick @user`` - кикнуть пользователя с вашей приватной комнаты.\n\n"
                                                "``!fox,dog,cat`` - за 150 шестерёнок вы можете отправить картинку лисы, собаки, кота.")
                await ctx.send(embed=emb, delete_after=120)
                return

    emb = discord.Embed(title='Мои разделы')
    emb.add_field(name='**Модерация**', value='тут написаны команды для модерации сервера'
                  )
    emb.add_field(name='**Учитель**', value='тут написаны команды для учителя'
                  )
    emb.add_field(name='**Развлечения**', value='тут написаны команды для всех пользователей'
                  )
    emb.set_footer(text='что бы посмотреть раздел нужно написать "!help Раздел"')
    await ctx.send(embed=emb, delete_after=20)


# Clear 1  or n or all massage
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, arg=''):
    if arg == 'all':
        await ctx.channel.purge(limit=2147483647 ** 20000)
    if arg.isdigit():
        await ctx.channel.purge(limit=int(arg))
    if arg == '':
        await ctx.channel.purge(limit=1)


# Warn pre-release
@client.command()
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, arg='Не указана'):
    reason = arg

    bans: int = int(gt('bans', member.id))
    bans_time: float = float(
        gt('bans_time', member.id))
    if bans <= 3 and bans_time > 0:
        await ctx.send(f"{member.mention}, уже находится в бане.", delete_after=5)
        return
    if bans > 3:
        await ctx.send(f"{member.mention}, уже находится в бане.", delete_after=5)
        return

    cursor.execute("UPDATE users SET warns = warns + 1 WHERE id = {} ".format(member.id))
    connection.commit()

    warns: int = int(
        gt('warns', member.id))
    emb = discord.Embed(title=':name_badge: Варн ``{}/3``'.format(warns),
                        description="{} получил прежупреждение. \n\n"
                                    "**Модератор:** {}"
                                    "```Причина: {}```".format(member.mention, ctx.author.mention,
                                                               reason),

                        colour=0xff3232)
    await ctx.send(embed=emb, delete_after=20)
    await member.send(f"Вам было выдано предупреждение за нарушение правил сервера. Предупреждений: {warns}/3 \n"
                      f"Причина: {reason}")

    if warns >= 3:

        ban_role = discord.utils.get(ctx.message.guild.roles, name='ban')
        await member.add_roles(ban_role)
        cursor.execute("UPDATE users SET bans_time = 172800 WHERE id = {} ".format(member.id))
        cursor.execute("UPDATE users SET bans = bans + 1 WHERE id = {} ".format(member.id))
        connection.commit()

        bans_time: float = float(
            gt('bans_time', member.id))
        bans: int = int(
            gt('bans', member.id))

        if bans > 3:
            cursor.execute("UPDATE users SET bans_time = -1 WHERE id = {} ".format(member.id))
            connection.commit()
            cursor.execute("UPDATE users SET bans = -1 WHERE id = {} ".format(member.id))
            connection.commit()
            emb = discord.Embed(title=':no_entry: Бан',
                                description="{} был забанен на вечно. \n\n"
                                            "**Модератор:** {}"
                                            "```Причина: Превышен лимит предупреждений.```".format(member.mention,
                                                                                                   botid),

                                colour=0xff3232)
            await ctx.send(embed=emb, delete_after=20)
            await member.send(
                f"Вы были забанены на данном сервере пожизненно.\n"
                f"Причина: Превышен лимит банов.")
        else:
            emb = discord.Embed(title=':no_entry: Бан',
                                description="{} был забанен на {} дн.\n\n"
                                            "**Модератор:** {} "
                                            "```Причина: Превышен лимит предупреждений.```".format(member.mention,
                                                                                                   round(
                                                                                                       bans_time / 86400),
                                                                                                   botid),

                                colour=0xff3232)
            await ctx.send(embed=emb, delete_after=20)
            await member.send(
                f"Вы были забанены на данном сервере на {round(bans_time / 86400)} дн.\n"
                f"Причина: Превышен лимит предупреждений.")

            while bans_time != 0:
                await asyncio.sleep(1)
                cursor.execute("UPDATE users SET bans_time = bans_time - 1 WHERE id = {} ".format(member.id))
                connection.commit()
                bans_time: float = float(
                    gt('bans_time', member.id))
                if bans_time == 0:
                    cursor.execute("UPDATE users SET warns = 0 WHERE id = {} ".format(member.id))
                    connection.commit()
                    await member.remove_roles(ban_role)
            if bans_time == 0:
                cursor.execute("UPDATE users SET warns = 0 WHERE id = {} ".format(member.id))
                connection.commit()


# UNWARN
@client.command()
@commands.has_permissions(administrator=True)
async def unwarn(ctx, member: discord.Member):
    warns: int = int(
        gt('warns', member.id))
    if warns == 0:
        await ctx.send(f"У пользователя {member.mention} и так ``0`` варнов.", delete_after=5)
        return
    cursor.execute("UPDATE users SET warns = warns - 1 WHERE id = {} ".format(member.id))
    connection.commit()
    await ctx.send(f"C пользователя {member.mention} был снят варн.", delete_after=5)
    await member.send(f"C вас был снят варн.")


# Ban
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, ban_d: int = None, *, arg='Не указана'):
    bans_time: float = float(
        gt('bans_time', member.id))
    if bans_time > 0:
        await ctx.send(f"{member.mention}, и так находится в бане.", delete_after=3)
        return

    reason = arg
    if ban_d is None:
        await ctx.send(f"<@{ctx.author.id}>, укажите длительность бана.", delete_after=5)
        return

    if ban_d == 0:
        ban_d = 'вечно'
    if ban_d == 'вечно':
        emb = discord.Embed(title=':no_entry: Бан',
                            description="{} был забанен на {}. \n\n"
                                        "**Модератор:** {}"
                                        "```Причина: {}```".format(member.mention, ban_d, ctx.author.mention,
                                                                   reason),

                            colour=0xff3232)
    else:
        emb = discord.Embed(title=':no_entry: Бан',
                            description="{} был забанен на {} дн. \n\n"
                                        "**Модератор:** {}"
                                        "```Причина: {}```".format(member.mention, ban_d, ctx.author.mention,
                                                                   reason),

                            colour=0xff3232)

    await ctx.send(embed=emb, delete_after=20)

    if ban_d == 'вечно':
        emb = discord.Embed(title=':no_entry: Бан',
                            description="Вы были забанены на данном сервере на {}.\n\n"
                                        "**Модератор:** {}"
                                        "```Причина: {}```".format(ban_d, ctx.author.mention,
                                                                   reason),

                            colour=0xff3232)
        ban_d = 0
    else:
        emb = discord.Embed(title=':no_entry: Бан',
                            description="Вы были забанены на данном сервере на {} дн.\n\n"
                                        "**Модератор:** {}"
                                        "```Причина: {}```".format(ban_d, ctx.author.mention,
                                                                   reason),

                            colour=0xff3232)
    await member.send(embed=emb)

    ban_role = discord.utils.get(ctx.message.guild.roles, name='ban')
    await member.add_roles(ban_role)

    cursor.execute("UPDATE users SET bans_time = bans_time + {} WHERE id = {} ".format(ban_d * 86400, member.id))
    connection.commit()
    bans_time: float = float(
        gt('bans_time', member.id))
    cursor.execute("UPDATE users SET bans = bans + 1 WHERE id = {} ".format(member.id))
    connection.commit()
    if bans_time > 0:
        while bans_time != 0:
            await asyncio.sleep(1)
            cursor.execute("UPDATE users SET bans_time = bans_time - 1 WHERE id = {} ".format(member.id))
            connection.commit()
            bans_time: float = float(
                gt('bans_time', member.id))
            if bans_time == 0:
                emb = discord.Embed(title=':white_check_mark: Разбан',
                                    description="Вы были разбанены.\n\n"
                                                "**Модератор:** {}"
                                    .format(botid),
                                    colour=0x28CC28)

                await member.send(embed=emb)
                cursor.execute("UPDATE users SET warns = 0 WHERE id = {} ".format(member.id))
                connection.commit()
                await member.remove_roles(ban_role)


# Unban
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, member: discord.Member):
    emb = discord.Embed(title=':white_check_mark: Разбан',
                        description="{} был разбанен. \n\n"
                                    "**Модератор:** {}"
                        .format(member.mention, ctx.author.mention,
                                ),

                        colour=0x28CC28)
    await ctx.send(embed=emb, delete_after=20)

    emb = discord.Embed(title=':white_check_mark: Разбан',
                        description="Вы были разбанены.\n\n"
                                    "**Модератор:** {}"
                        .format(ctx.author.mention),
                        colour=0x28CC28)

    await member.send(embed=emb)

    ban_role = discord.utils.get(ctx.message.guild.roles, name='ban')
    await member.remove_roles(ban_role)
    cursor.execute("UPDATE users SET warns = 0 WHERE id = {} ".format(member.id))
    cursor.execute("UPDATE users SET bans_time = 1 WHERE id = {} ".format(member.id))
    cursor.execute("UPDATE users SET bans = bans - 1 WHERE id = {} ".format(member.id))
    connection.commit()


# Mute
@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, mute_minutes: int = None, *, arg='Не указана'):
    mute_time: float = float(
        gt('mute_time', member.id))
    if mute_time > 0:
        await ctx.send(f"{member.mention}, и так находится в муте.", delete_after=3)
        return
    reason = arg
    if mute_minutes is None:
        await ctx.send(f"<@{ctx.author.id}>, укажите длительность мута.", delete_after=5)
        return
    cursor.execute("UPDATE users SET mute_time = mute_time + {} WHERE id = {} ".format(mute_minutes * 60, member.id))
    connection.commit()
    if mute_minutes == 0:
        emb = discord.Embed(title=':mute: Мут',
                            description="{} был замучен на вечно. \n\n"
                                        "**Модератор:** {}"
                                        "```Причина: {}```".format(member.mention, ctx.author.mention,
                                                                   reason),

                            colour=0xffa500)
    else:
        emb = discord.Embed(title=':mute: Мут',
                            description="{} был замучен на {} мин. \n\n"
                                        "**Модератор:** {}"
                                        "```Причина: {}```".format(member.mention, mute_minutes, ctx.author.mention,
                                                                   reason),

                            colour=0xffa500)

    await ctx.send(embed=emb, delete_after=10)
    mute_role = discord.utils.get(ctx.message.guild.roles, name='muted')
    await member.add_roles(mute_role)

    mute_time: float = float(
        gt('mute_time', member.id))
    if mute_time > 0:
        while mute_time != 0:
            await asyncio.sleep(1)
            cursor.execute("UPDATE users SET mute_time = mute_time - 1 WHERE id = {} ".format(member.id))
            connection.commit()
            mute_time: float = float(
                gt('mute_time', member.id))
            if mute_time == 0:
                emb = discord.Embed(title=':loud_sound: Анмут',
                                    description="{} был размучен. \n\n"
                                                "**Модератор:** {}"
                                    .format(member.mention, botid,
                                            ),

                                    colour=0x1047A9, )

                await ctx.send(embed=emb, delete_after=7)
                await member.remove_roles(mute_role)


# Unmute
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    cursor.execute("UPDATE users SET mute_time = 1 WHERE id = {} ".format(member.id))
    connection.commit()
    emb = discord.Embed(title=':loud_sound: Анмут',
                        description="{} был размучен. \n\n"
                                    "**Модератор:** {}"
                        .format(member.mention, ctx.author.mention,
                                ),

                        colour=0x1047A9)

    await ctx.send(embed=emb, delete_after=7)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='muted')
    await member.remove_roles(mute_role)


# LESSON START
@client.command()
@commands.has_permissions(administrator=True)
async def lesson(ctx, *, url: str = 'None'):
    if 'https://events.webinar.ru' in url:
        emb = discord.Embed(title="**Начался урок**",
                            description=f"{url}", timestamp=datetime.utcnow());

        await ctx.send(embed=emb)
        await ctx.send("@everyone", delete_after=0)
    else:
        await ctx.send(f"{ctx.author.mention}, указана неверная ссылка на урок.", delete_after=5)


# # Voice join
# @client.command()
# @commands.has_permissions(administrator=True)
# async def join(ctx):
#     channel = ctx.message.author.voice.channel
#     voice = get(client.voice_clients, guild=ctx.guild)
#
#     if voice and voice.is_connected() and voice.channel != channel:
#         emb = discord.Embed(description=f'{botid} перепрыгнул на канал: \n``{channel}``')
#         await ctx.send(embed=emb, delete_after=10)
#         await voice.move_to(channel)
#     else:
#         emb = discord.Embed(description=f'{botid} прыгнул на канал: \n``{channel}``')
#         await ctx.send(embed=emb, delete_after=5)
#         voice = await channel.connect()
#
#
# # Voice leave
# @client.command()
# @commands.has_permissions(administrator=True)
# async def leave(ctx):
#     channel = ctx.message.author.voice.channel
#     voice = get(client.voice_clients, guild=ctx.guild)
#
#     if voice and voice.is_connected():
#         emb = discord.Embed(description=f'{botid} ушел из канала: \n``{channel}``')
#         await ctx.send(embed=emb, delete_after=5)
#         await voice.disconnect()


# Image
@client.command()
async def fox(ctx):
    money: float = float(
        gt('cash', ctx.author.id))
    if money < 200:
        await ctx.send(f"{ctx.author.mention}, у вас недостаточно средств.", delete_after=3)
        return
    else:
        cursor.execute("UPDATE users SET cash = cash - 200 WHERE id = {}".format(ctx.author.id))
        connection.commit()
        await ctx.author.send(f"С вас было списано 200 шестерёнок.\n"
                              f"Ваш текущий баланс: **{round(money - 200, 1)} шестерёнок**")

    response = requests.get('https://some-random-api.ml/img/fox')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON
    embed = discord.Embed(color=0xff9900)  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


@client.command()
async def dog(ctx):
    money: float = float(
        gt('cash', ctx.author.id))
    if money < 150:
        await ctx.send(f"{ctx.author.mention}, у вас недостаточно средств.", delete_after=3)
        return
    else:
        cursor.execute("UPDATE users SET cash = cash - 150 WHERE id = {}".format(ctx.author.id))
        connection.commit()
        await ctx.author.send(f"С вас было списано 150 шестерёнок.\n"
                              f"Ваш текущий баланс: **{round(money - 150, 1)} шестерёнок**")

    response = requests.get('https://some-random-api.ml/img/dog')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON
    embed = discord.Embed(color=0x2f3136)  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


@client.command()
async def cat(ctx):
    money: float = float(
        gt('cash', ctx.author.id))
    if money < 150:
        await ctx.send(f"{ctx.author.mention}, у вас недостаточно средств.", delete_after=3)
        return
    else:
        cursor.execute("UPDATE users SET cash = cash - 150 WHERE id = {}".format(ctx.author.id))
        connection.commit()
        await ctx.author.send(f"С вас было списано 150 шестерёнок.\n"
                              f"Ваш текущий баланс: **{round(money - 150, 1)} шестерёнок**")

    response = requests.get('https://some-random-api.ml/img/cat')  # Get-запрос
    json_data = json.loads(response.text)  # Извлекаем JSON
    embed = discord.Embed(color=0x2f3136)  # Создание Embed'a
    embed.set_image(url=json_data['link'])  # Устанавливаем картинку Embed'a
    await ctx.send(embed=embed)  # Отправляем Embed


# f u corgi and ! - delete and Chat Filter
@client.event
async def on_message(message):
    prefixs = ('!', '+r', '-r')
    if message.content.startswith(prefixs):
        await message.delete()

    await client.process_commands(message)

    msg = message.content.lower()
    if msg in bad_words:
        await message.delete()

    if message.author == client.user:
        return
    if msg.startswith('f u ахалаймахалай'):
        await message.channel.send(f'no f u, {message.author.mention}!')


client.run(settings['token'])
