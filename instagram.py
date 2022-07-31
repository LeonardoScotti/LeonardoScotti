
import re
import time
from json import loads

from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#import mysql.connector


#'https://instagram.com/graphql/query/?query_id=17888483320059182&variables={"id":"' + id + '","first":' + post + ',"after":null}'

#img_class = "_6q-tv"
#bio_class = "-vDIg"
#name_class = "rhpdm"
#stats_class =  "_3dEHb"

#"edge_liked_by":{"count":(\d+)}
#{"src":"([^\s,}]+)","config_width":320,"config_height":320}

TOKEN = '1885449858:AAFLOKKRk3bNqAT6Dt9v229mJuEwHceb3fw'
users = {}

def start():
    
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    global driver
    driver = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe",options=options)
    driver.implicitly_wait(10) 
    
    print("Program Succesfully Started...")
    login(driver, "Auto")
    
    ''' 
    config = {
      'user': '3533837_freeregrambot',
      'password': 'Leonardo25#',
      'host': 'fdb30.awardspace.net',
      'database': '3533837_freeregrambot',
      'raise_on_warnings': True
    }
    
    cnx = mysql.connector.connect(**config)
    '''

def login(browser, x=""):

    credenziali = {"username": "sidncjedj", "password": "ciaociaolala"}
    
    print(f'{x}Login({credenziali})\n')
    if browser.current_url != 'https://www.instagram.com/accounts/login/':
        browser.get('https://www.instagram.com/accounts/login/')

    driver.find_element(by=By.NAME, value="username").send_keys(credenziali['username'])
    driver.find_element(by=By.NAME, value="password").send_keys(credenziali['password'])
    driver.find_element(by=By.NAME, value="password").send_keys(Keys.RETURN)
    time.sleep(5)
    if browser.page_source == "https://www.instagram.com/accounts/onetap/?next=%2F":
        browser.find_element_by_name("""//button[@type='button' and text()='Salva le informazioni']""").send_keys(Keys.RETURN) 
        
    if browser.current_url != 'https://www.instagram.com/accounts/login/':
        return True
    else:
        return False
    
def get_instagram_info(username):
    global driver
    
    url = "https://www.instagram.com/" + username + "/?__a=1"
    driver.get(url)
    if driver.current_url == "https://www.instagram.com/accounts/login/":
        login()
        driver.get(url)
    data = driver.page_source        
    
    img_link = "".join(re.findall('"profile_pic_url_hd":"([^"]*)"', str(data))[0].split("amp;"))
    bio = re.findall('"biography":"([^"]*)"', str(data))[0]
    name = re.findall('"full_name":"([^"]*)"', str(data))[0]
    
    try:
        category = re.findall('"category_name":"([^",]*)"', str(data))[0]    
    except:
        category = "null"
    
    try:
        external_links = re.findall('"external_url":"([^"]*)"', str(data))[0]
    except:
        external_links = "null"   
    
    is_private = re.findall('"is_private":([a-z]+),', str(data))[0]

    is_verified = re.findall('"is_verified":([a-z]+),', str(data))[0]    
    
    is_lc_blocked = re.findall('"hide_like_and_view_counts":([a-z]+),', str(data))[0]
    
    fb_id = re.findall('"fbid":"(\d+)"', str(data))[0]
    id = re.findall('"id":"(\d+)"', str(data))[0]
    
    follower = re.findall('"edge_followed_by":{"count":(\d*)}', str(data))[0]
    seguiti = re.findall('"edge_follow":{"count":(\d*)}', str(data))[0]
    post = re.findall('edge_owner_to_timeline_media":{"count":(\d*),', str(data))[0]
    
    liked_posts = sorted(re.findall('"edge_liked_by":{"count":(\d+)}', str(data)), reverse=True)
    post_url = re.findall('{"src":"([^\s,}]+)","config_width":320,"config_height":320}', str(data))
    
    stats = "follower: {0} seguiti: {1} post: {2}".format(follower, seguiti, post)

    bio = re.subn("\*", "\*", bio)[0]
    bio = re.sub(r"((?:^|\s)(?:[^@\s]*?))(_)((?:[^@\s]*?))(?=@|\s|$)", "\\1\\\\_\\3", bio)
    tag = re.findall('(@[^\s@]+)', bio)
    for elem in tag:
        bio = re.sub(elem, '[{0}](https://www.instagram.com/{1})'.format(elem, elem.strip('@')), bio)
    
    txt = []
    txt.append("*" + loads('"' + name + '"') + "*")
    if category != "null":
        txt.append(category)    
    try:
        txt.append(loads('"' + bio + '"'))
    except:
        txt.append(bio)       
    txt.append(stats)
    if external_links != "null":
        txt.append(external_links)
    
    return img_link, "\n\n".join(txt), id, post, is_private, fb_id, is_lc_blocked
    
def get_most_liked_post(id, post):
    
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    temp = webdriver.Chrome("C:/Program Files/ChromeDriver/chromedriver.exe",options=options)
    temp.implicitly_wait(10)     
    
    url = 'https://instagram.com/graphql/query/?query_id=17888483320059182&variables={"id":"' + id + '","first":' + post + ',"after":null}'
    temp.get(url)
    if temp.current_url.startswith('https://www.instagram.com/accounts/login/'):
        login(temp, "Emergence")
        temp.get(url)
    data = temp.page_source  
    temp.quit()
    
    #r = re.compile('"edge_liked_by":{"count":(?P<like>\d+)}[^\s]+"src":"(?P<url>[^\s,}{}]+)","config_width":320,"config_height":320}')
    #post_sorted_per_like = [m.groupdict() for m in r.finditer(str(data))]  
    #likelist = re.findall('"edge_liked_by":{"count":(\d+)}', str(data))
    #postlist = re.findall('"src":"([^\s,}{}]+)","config_width":320,"config_height":320}', str(data))
    
    try:
        top_like = sorted(re.findall('"edge_media_preview_like":{"count":(\d+)}', str(data)))[0]
        post_url = re.subn('\\\\u0026', '&', re.findall('"edge_media_preview_like":{"count":' + top_like + '},"owner":{"id":"' + id + '"},"thumbnail_src":"([^"]+)"', str(data))[0])[0]
        
        return post_url, top_like
    
    except:  
        return False, False
    
def OnChatMessage(msg):
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    print(f'NewRequest({{{chat_id}: {msg["text"]}}})\n')
    
    if content_type == 'text':
        if msg['text'].startswith("/"):
            if msg['text'] == "/start":
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                [InlineKeyboardButton(text='Info', callback_data="/info")],
                                                                [InlineKeyboardButton(text='Help', callback_data="/help")],
                                                                ])
                bot.sendMessage(chat_id, "*Free Regrambot*\n benvenuto nel bot,\nper sapere di piu su di noi digita /info\nper imparare a usare il bot usa /help", parse_mode="Markdown", reply_markup=keyboard)
                
            elif msg['text'] == "/info":
                bot.sendMessage(chat_id, "*BENVENUTO*\n\nho sempre trovato le funzionalita' di @Regrambot molto utili, interessanti, comode e funzionali, e da quando queste sono diventate prerogative dei premium user ho deciso di creare questo bot che ha piu' o meno le solite funzioni ma completamente gratuite.", parse_mode='Markdown')      
                
            elif msg['text'] == "/help":
                bot.sendMessage(chat_id, "*ISTRUZIONI*\nper utilizzare il bot ti bastera' inviare come messaggio l'username del profilo instagram che vuoi cercare e riceverai statistiche, bio e foto profilo, inoltre, se il profilo NON e' privato potrai anche ottenere il post con piu' like cliccando il pulsante \"Most Liked Post\"", parse_mode="Markdown")            
        else:
            a = bot.sendMessage(chat_id, u" \u26D4 Attendere Prego...")
            try:
                username = msg['text'].strip()
                img_link, text, id, post, is_private, fb_id, is_lc_blocked = get_instagram_info(username)
                try:
                    bot.deleteMessage(telepot.message_identifier(a))
                except:
                    pass
                bot.sendPhoto(chat_id, img_link)
                
                print(f"{'-'*73}\n{text}\nfb_id: {fb_id}\nid: {id}\nis_private: {is_private}\n{'-'*73}\n")
                
                if is_private == "false" :
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                    [InlineKeyboardButton(text='Most Liked Post', callback_data=f"most liked post {id} {post}")],
                                                                    [InlineKeyboardButton(text='View on Instagram', url=f"https://www.instagram.com/{username}")],
                                                                    ])
                elif is_private == "true":
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                                                    [InlineKeyboardButton(text='Most Liked Post  \U0001f512', callback_data=f"most liked post blocked")],
                                                                    [InlineKeyboardButton(text='View on Instagram', url=f"https://www.instagram.com/{username}")],
                                                                    ])    
                #elif is_lc_blocked == "true":
                 #   keyboard = InlineKeyboardMarkup(inline_keyboard=[
                  #                                                  [InlineKeyboardButton(text='Most Liked Post  \u26D4', callback_data=f"most liked post {id} {post}")],
                   #                                                 [InlineKeyboardButton(text='View on Instagram', url=f"https://www.instagram.com/{username}")],
                    #                                                ])                      
                try:
                    bot.sendMessage(chat_id, text, parse_mode='Markdown', reply_markup=keyboard) 
                except telepot.exception.TelegramError:
                    bot.sendMessage(chat_id, text, reply_markup=keyboard)                     
            except IndexError:
                try:
                    bot.deleteMessage(telepot.message_identifier(a))
                except:
                    pass                    
                bot.sendMessage(chat_id, "\u26a0*Errore\n\nusername insistente*", parse_mode='Markdown')
                print("BadRequest({'Issue': 'No account founded'})\n")
                """if str(chat_id) == "823449661":
                    import traceback
                    x = traceback.format_exc()   
                    bot.sendMessage(chat_id, 'ERRORE\n\n' + x)"""                  
            except:
                if str(chat_id) == "823449661":
                    import traceback
                    x = traceback.format_exc()
                    try:
                        bot.deleteMessage(telepot.message_identifier(a))
                    except:
                        pass
                    bot.sendMessage(chat_id, 'ERRORE\n\n' + x) 
                    print("Alert({'issue': 'Exception occurred'})\n")


def OnCallbackQuery(msg):
    
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    bot.answerCallbackQuery(query_id)

    print(f'New Query({{{chat_id}: {query_data}}})\n')
    
    if query_data.startswith("/"):
        if query_data == "/info":
            bot.sendMessage(chat_id, "*BENVENUTO*\n\nho sempre trovato le funzionalita' di @Regrambot molto utili, interessanti, comode e funzionali, e da quando queste sono diventate prerogative dei premium user ho deciso di creare questo bot che ha piu' o meno le solite funzioni ma completamente gratuite.", parse_mode='Markdown')      
            
        elif query_data == "/help":
            bot.sendMessage(chat_id, "*ISTRUZIONI*\nper utilizzare il bot ti bastera' inviare come messaggio l'username del profilo instagram che vuoi cercare e riceverai statistiche, bio e foto profilo, inoltre, se il profilo NON e' privato potrai anche ottenere il post con piu' like cliccando il pulsante \"Most Liked Post\"", parse_mode="Markdown")
    elif query_data.startswith("most liked post "):
        
        if query_data == "most liked post blocked":
            bot.sendMessage(chat_id, u"\U0001f512*BLOCCATO*\npurtroppo il post che hai richiesto appartiene a un profilo privato e non e' visibile", parse_mode="Markdown")
        #elif query_data == "most liked post hidden":
         #   bot.sendMessage(chat_id, u"\u26D4*BLOCCATO*\npurtroppo il post che hai richiesto appartiene a un profilo che ha nascosto il conteggio dei like ai suoi post", parse_mode="Markdown")            
        else:
            b = bot.sendMessage(chat_id, u" \u26D4 Attendere Prego...")
            try:
                id, post = query_data.strip("most liked post").split()
                post_url, like = get_most_liked_post(id, post)
                if post_url not in [False, None, ""]:
                    try:
                        bot.deleteMessage(telepot.message_identifier(b))
                    except:
                        pass                    
                    print(post_url)
                    bot.sendPhoto(chat_id, post_url)
                    bot.sendMessage(chat_id, f'like: {like}')
                else:
                    bot.sendMessage(chat_id, 'Oops, qualcosa è andato sorto.')
                print(f'Error({{chat_id: {chat_id}, type: most liked post, object_id: {query_data.strip("most liked post").split()[0]}}})')
            except:
                try:
                    bot.deleteMessage(telepot.message_identifier(b))
                except:
                    pass                
                if str(chat_id) == "823449661":
                    import traceback
                    x = traceback.format_exc()
                    try:
                        bot.deleteMessage(telepot.message_identifier(b))
                    except:
                        pass
                    bot.sendMessage(chat_id, 'ERRORE\n\n' + x) 
                else:
                    bot.sendMessage(chat_id, 'Oops, qualcosa é andato sorto.')
                print(f'Error({{chat_id: {chat_id}, type: most liked post, object_id: {query_data.strip("most liked post").split()[0]}}})')
            
        
    
    
start()
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': OnChatMessage,
                  'callback_query': OnCallbackQuery}).run_as_thread()
    
while True:
    time.sleep(10)
