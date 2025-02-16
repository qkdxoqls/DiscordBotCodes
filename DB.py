import discord
from discord.ext import commands
import datetime
import random

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True  # 멤버 관련 이벤트 활성화

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """봇이 온라인이 될 때 실행"""
    print(f'로그인 성공: {bot.user}이 정상적으로 작동중입니다.')
    activity = discord.Game("냥이봇은 일🛠️")  # 상태 설정
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def 삭제(ctx, member: discord.Member, amount: int = 1):
    """특정 유저의 최근 메시지를 삭제"""
    def is_user_message(msg):
        return msg.author == member
    deleted = await ctx.channel.purge(limit=amount+1, check=is_user_message)
    await ctx.send(f'🧹 {member.name}의 메시지 {len(deleted)-1}개 삭제 완료!', delete_after=5)

@bot.event
async def on_message(message):
    """특정 키워드에 반응"""
    if message.author == bot.user:
        return

    if "안녕 냥이봇" in message.content:
        now = datetime.datetime.now()
        hour = now.hour

        # 시간대에 따른 인사말 선택
        if 5 <= hour < 12:
            greetings = ["좋은 아침이에요! ☀️", "안녕하세요! 상쾌한 아침입니다.", "좋은 하루의 시작입니다!"]
        elif 12 <= hour < 18:
            greetings = ["안녕하세요! 좋은 오후네요. 🌞", "점심 잘 드셨나요?", "오후도 힘내세요!"]
        elif 18 <= hour < 22:
            greetings = ["안녕하세요! 좋은 저녁입니다. 🌙", "저녁 맛있게 드셨나요?", "편안한 저녁 보내세요!"]
        else:
            greetings = ["안녕하세요! 늦은 밤이네요. 🌌", "새벽에도 깨어 계시네요!", "푹 쉬세요! 😴"]

        greeting_message = random.choice(greetings)
        await message.channel.send(f'{greeting_message} {message.author.mention}님')

    await bot.process_commands(message)

@bot.command()
async def 청소(ctx, amount: int = 10):
    """원하는 개수만큼 메시지 삭제 (봇 메시지도 포함)"""
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f'🧹 {len(deleted)}개의 메시지를 삭제했습니다.', delete_after=5)

@bot.command()
async def 킥(ctx, member: discord.Member, *, reason=None):
    """유저 강퇴"""
    await member.kick(reason=reason)
    await ctx.send(f'🚨 {member.mention}을(를) 강퇴했습니다.')

@bot.command()
async def 도움말(ctx):
    """임베드 형식으로 명령어 정리"""
    embed = discord.Embed(title="📜 도움말", description="냥이봇의 명령어 목록", color=0x00ff00)
    embed.add_field(name="🖐️ 안녕 냥이봇", value="냥이봇이 인사를 합니다.", inline=False)
    embed.add_field(name="🧹 !청소 [개수]", value="채팅을 원하는 개수만큼 삭제합니다.", inline=False)
    embed.add_field(name="❌ !삭제 @유저 [개수]", value="특정 유저의 메시지를 삭제합니다.", inline=False)
    embed.add_field(name="🚪 !킥 @유저", value="특정 유저를 강퇴합니다.", inline=False)
    embed.add_field(name="📢 !투표 질문", value="투표를 시작합니다.", inline=False)
    embed.add_field(name="🔇 !뮤트 @유저", value="특정 유저를 뮤트합니다.", inline=False)
    embed.add_field(name="ℹ️ !정보", value="봇의 정보(개발자, 개발 날짜 등)를 확인합니다.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def 투표(ctx, *, question):
    """투표 생성"""
    msg = await ctx.send(f'📢 **투표:** {question}')
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command()
async def 뮤트(ctx, member: discord.Member):
    """특정 유저 뮤트"""
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)
    await member.add_roles(muted_role)
    await ctx.send(f'🔇 {member.mention}을(를) 뮤트했습니다.')

@bot.command()
async def 정보(ctx):
    """봇의 정보 표시"""
    embed = discord.Embed(title="ℹ️ 냥이봇 정보", color=0x3498db)
    embed.add_field(name="📌 개발자", value="지슬(lyin231127)", inline=False)
    embed.add_field(name="🤖 봇 이름", value="냥이봇-A01#0576", inline=False)
    embed.add_field(name="🛠️ 개발 날짜", value="2025년 2월 15일", inline=False)
    embed.add_field(name="🚀 버전", value="v1.2.3", inline=False)
    embed.set_footer(text="냥이봇을 사용해주셔서 감사합니다! 🐱")
    await ctx.send(embed=embed)

TOKEN = "MTM0MDUzNDQ0NTc3MzU1Nzc4MQ.GPTwjz.-rUW43APioTzeClAX9FlkuUOMTQYREnEhbWaCU"
bot.run(TOKEN)
