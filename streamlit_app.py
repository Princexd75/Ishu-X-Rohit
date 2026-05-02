import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import hashlib
import os
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import database as db

st.set_page_config(
    page_title="E2E BY ROW3DY",
    page_icon="🥵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SINGLE/FILE CONTAINER CSS ====================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background: linear-gradient(160deg, #0B0F1C 0%, #0F172A 50%, #1E1B2E 100%);
        background-attachment: fixed;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    .stAlert {display: none !important;}
    
    /* Main wrapper - Centered */
    .main-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 2rem;
    }
    
    /* ========== SINGLE/FILE CONTAINER ========== */
    .single-file-container {
        max-width: 550px;
        width: 100%;
        background: linear-gradient(145deg, #0E1322 0%, #090C17 100%);
        border-radius: 32px;
        padding: 2rem 1.8rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(78, 205, 196, 0.15);
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.3s ease;
    }
    
    /* Header with icon */
    .file-header {
        text-align: center;
        margin-bottom: 1.8rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    .file-header h1 {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4ecdc4, #a855f7);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        letter-spacing: 1px;
    }
    
    .file-header p {
        font-size: 0.7rem;
        color: #64748B;
        margin-top: 0.5rem;
    }
    
    /* List item style */
    .list-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.2s ease;
    }
    
    .list-item:hover {
        background: rgba(78, 205, 196, 0.08);
        border-color: rgba(78, 205, 196, 0.2);
    }
    
    .item-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .item-value {
        font-size: 0.9rem;
        font-weight: 500;
        color: #E2E8F0;
    }
    
    /* Divider line */
    .divider-light {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.3), transparent);
        margin: 1rem 0;
    }
    
    /* Start button - single */
    .start-btn {
        background: linear-gradient(135deg, #11998e, #0f8a6e);
        border: none;
        width: 100%;
        padding: 1rem;
        border-radius: 40px;
        font-weight: 700;
        font-size: 1rem;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    .start-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(17, 153, 142, 0.4);
    }
    
    /* Input fields inside container */
    .custom-input {
        width: 100%;
        background: #0A0E18;
        border: 1.5px solid #1E293B;
        border-radius: 16px;
        padding: 0.9rem 1.2rem;
        color: #E2E8F0;
        font-size: 0.85rem;
        transition: all 0.3s;
    }
    
    .custom-input:focus {
        outline: none;
        border-color: #4ecdc4;
        box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1);
    }
    
    .custom-textarea {
        width: 100%;
        background: #0A0E18;
        border: 1.5px solid #1E293B;
        border-radius: 16px;
        padding: 0.9rem 1.2rem;
        color: #E2E8F0;
        font-size: 0.85rem;
        resize: vertical;
        min-height: 80px;
    }
    
    .custom-textarea:focus {
        outline: none;
        border-color: #4ecdc4;
    }
    
    /* Status pill */
    .status-pill {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 40px;
        font-size: 0.7rem;
        font-weight: 600;
        text-align: center;
        width: 100%;
        margin-top: 1rem;
    }
    
    .status-running {
        background: rgba(56, 239, 125, 0.15);
        border: 1px solid #38ef7d;
        color: #38ef7d;
    }
    
    .status-stopped {
        background: rgba(245, 87, 108, 0.15);
        border: 1px solid #f5576c;
        color: #f5576c;
    }
    
    /* Hide Streamlit default widgets */
    .stTextInput, .stTextArea, .stNumberInput {
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar style */
    [data-testid="stSidebar"] {
        background: rgba(8, 12, 20, 0.95);
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(78, 205, 196, 0.15);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 4px;
    }
    ::-webkit-scrollbar-track {
        background: #0A0E18;
    }
    ::-webkit-scrollbar-thumb {
        background: #4ecdc4;
        border-radius: 10px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ==================== BACKEND FUNCTIONS (same as before) ====================
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

# Session state
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

# Selenium functions (keep same)
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
    
    chromium_paths = ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome', '/usr/bin/chrome']
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            break
    
    chromedriver_paths = ['/usr/bin/chromedriver', '/usr/local/bin/chromedriver']
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
                            driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com', 'path': '/'})
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
                """, message_input, message_to_send)
                time.sleep(1)
                
                driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i], [data-testid="send-button"]');
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            break;
                        }
                    }
                """)
                
                messages_sent += 1
                automation_state.message_count = messages_sent
                if messages_sent % 5 == 0:
                    st.session_state.status_message = f"✅ Sent {messages_sent} messages!"
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

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    if automation_state.running:
        return
    automation_state.running = True
    automation_state.message_count = 0
    db.set_automation_running(user_id, True)
    username = db.get_username(user_id)
    thread = threading.Thread(target=send_messages, args=(user_config, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

# ==================== SINGLE/FILE STYLE LOGIN PAGE ====================
def login_page():
    st.markdown("""
    <div class="main-wrapper">
        <div class="single-file-container">
            <div class="file-header">
                <h1>🥵 E2E BY ROW3DY</h1>
                <p>SINGLE • FILE • SECURE</p>
            </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 SIGN UP"])
    
    with tab1:
        st.markdown('<div class="list-item"><span class="item-label">USERNAME</span></div>', unsafe_allow_html=True)
        username = st.text_input("", placeholder="Enter your username", key="login_user", label_visibility="collapsed")
        
        st.markdown('<div class="list-item"><span class="item-label">PASSWORD</span></div>', unsafe_allow_html=True)
        password = st.text_input("", placeholder="Enter your password", type="password", key="login_pass", label_visibility="collapsed")
        
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        
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
                    else:
                        st.session_state.key_approved = False
                        st.session_state.approval_status = 'not_requested'
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials!")
            else:
                st.warning("⚠️ Fill all fields!")
    
    with tab2:
        st.markdown('<div class="list-item"><span class="item-label">USERNAME</span></div>', unsafe_allow_html=True)
        new_username = st.text_input("", placeholder="Choose username", key="signup_user", label_visibility="collapsed")
        
        st.markdown('<div class="list-item"><span class="item-label">PASSWORD</span></div>', unsafe_allow_html=True)
        new_password = st.text_input("", placeholder="Create password", type="password", key="signup_pass", label_visibility="collapsed")
        
        st.markdown('<div class="list-item"><span class="item-label">CONFIRM</span></div>', unsafe_allow_html=True)
        confirm_password = st.text_input("", placeholder="Confirm password", type="password", key="signup_confirm", label_visibility="collapsed")
        
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        
        if st.button("✨ CREATE ACCOUNT", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords don't match!")
            else:
                st.warning("⚠️ Fill all fields!")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==================== SINGLE/FILE STYLE APPROVAL PAGE ====================
def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-wrapper">
        <div class="single-file-container">
            <div class="file-header">
                <h1>🔐 ACCESS REQUEST</h1>
                <p>APPROVAL • PENDING</p>
            </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.approval_status == 'not_requested':
        st.markdown(f'<div class="list-item"><span class="item-label">YOUR KEY</span><span class="item-value">{user_key}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="list-item"><span class="item-label">NAME</span><span class="item-value">{username}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📨 REQUEST", use_container_width=True):
                pending = load_pending_approvals()
                pending[user_key] = {"name": username, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
                save_pending_approvals(pending)
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
        with col2:
            if st.button("👑 ADMIN", use_container_width=True):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
    
    elif st.session_state.approval_status == 'pending':
        st.markdown('<div class="status-pill status-running" style="background:rgba(245,158,11,0.15);border-color:#f59e0b;color:#f59e0b;">⏳ PENDING APPROVAL</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="list-item"><span class="item-label">YOUR KEY</span><span class="item-value">{user_key}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        
        whatsapp_url = send_whatsapp_message(username, user_key)
        if not st.session_state.whatsapp_opened:
            components.html(f"<script>setTimeout(()=>{{window.open('{whatsapp_url}','_blank');}},300);</script>", height=0)
            st.session_state.whatsapp_opened = True
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 CHECK", use_container_width=True):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.rerun()
                else:
                    st.error("❌ Not approved yet!")
        with col2:
            if st.button("◀️ BACK", use_container_width=True):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_login':
        st.markdown('<div class="list-item"><span class="item-label">ADMIN PASSWORD</span></div>', unsafe_allow_html=True)
        admin_pass = st.text_input("", type="password", key="admin_pass", label_visibility="collapsed", placeholder="Enter admin password")
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 LOGIN", use_container_width=True):
                if admin_pass == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else:
                    st.error("❌ Wrong password!")
        with col2:
            if st.button("◀️ BACK", use_container_width=True):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_panel':
        pending = load_pending_approvals()
        approved_keys = load_approved_keys()
        
        st.markdown(f'<div class="list-item"><span class="item-label">APPROVED</span><span class="item-value">{len(approved_keys)}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="list-item"><span class="item-label">PENDING</span><span class="item-value">{len(pending)}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        
        if pending:
            for key, info in pending.items():
                st.markdown(f'<div class="list-item"><span class="item-label">👤 {info["name"]}</span><span class="item-value">{key}</span></div>', unsafe_allow_html=True)
                if st.button(f"✅ Approve {key[:10]}...", key=f"approve_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.rerun()
        else:
            st.caption("✨ No pending approvals")
        
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.approval_status = 'not_requested'
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==================== SINGLE/FILE STYLE MAIN APP ====================
def main_app():
    st.markdown("""
    <div class="main-wrapper">
        <div class="single-file-container">
            <div class="file-header">
                <h1>🥵 E2E BY ROW3DY</h1>
                <p>SINGLE • FILE • AUTOMATION</p>
            </div>
    """, unsafe_allow_html=True)
    
    # Sidebar content (hidden but needed for functionality)
    st.sidebar.markdown(f"### 👤 {st.session_state.username}")
    st.sidebar.markdown(f"**🆔 ID:** `{st.session_state.user_id}`")
    st.sidebar.markdown(f"**🔑 KEY:** `{st.session_state.user_key}`")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
        st.session_state.logged_in = False
        st.session_state.key_approved = False
        st.session_state.approval_status = 'not_requested'
        st.rerun()
    
    user_config = db.get_user_config(st.session_state.user_id)
    
    if user_config:
        # 1. ENTER SINGLE TOKEN / CHAT ID
        st.markdown('<div class="list-item"><span class="item-label">1. CONVERSATION ID</span></div>', unsafe_allow_html=True)
        chat_id = st.text_input("", value=user_config['chat_id'], placeholder="Enter Chat ID / Token", key="chat_id", label_visibility="collapsed")
        
        # 2. ENTER HATER NAME / NAME PREFIX
        st.markdown('<div class="list-item"><span class="item-label">2. HATER NAME</span></div>', unsafe_allow_html=True)
        name_prefix = st.text_input("", value=user_config['name_prefix'], placeholder="Enter name prefix", key="prefix", label_visibility="collapsed")
        
        # 3. SPEED (IN SECONDS)
        st.markdown('<div class="list-item"><span class="item-label">3. SPEED (SECONDS)</span></div>', unsafe_allow_html=True)
        delay = st.number_input("", min_value=1, max_value=300, value=user_config['delay'], key="delay", label_visibility="collapsed")
        
        # 4. UPLOAD FILES / MESSAGES
        st.markdown('<div class="list-item"><span class="item-label">4. MESSAGES</span></div>', unsafe_allow_html=True)
        messages = st.text_area("", value=user_config['messages'], placeholder="One message per line\nHello!\nHow are you?", key="messages", label_visibility="collapsed", height=100)
        
        # 5. COOKIES (optional)
        st.markdown('<div class="list-item"><span class="item-label">5. COOKIES (OPTIONAL)</span></div>', unsafe_allow_html=True)
        cookies = st.text_area("", value="", placeholder="Paste cookies here if needed", key="cookies", label_visibility="collapsed", height=60)
        
        st.markdown('<div class="divider-light"></div>', unsafe_allow_html=True)
        
        # Status message
        if st.session_state.status_message:
            st.caption(f"💬 {st.session_state.status_message}")
        
        # START SERVER BUTTON
        if st.session_state.automation_state.running:
            st.markdown('<div class="status-pill status-running">🟢 RUNNING - SENDING MESSAGES</div>', unsafe_allow_html=True)
            if st.button("⏹️ STOP SERVER", use_container_width=True):
                stop_automation(st.session_state.user_id)
                st.session_state.status_message = "Server stopped!"
                st.rerun()
        else:
            if st.button("🚀 START SERVER", use_container_width=True):
                if chat_id:
                    final_cookies = cookies if cookies.strip() else user_config['cookies']
                    db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, final_cookies, messages)
                    updated_config = db.get_user_config(st.session_state.user_id)
                    if updated_config and updated_config['chat_id']:
                        start_automation(updated_config, st.session_state.user_id)
                        st.session_state.status_message = "✅ SERVER STARTED!"
                        st.rerun()
                    else:
                        st.session_state.status_message = "❌ Invalid Chat ID!"
                        st.rerun()
                else:
                    st.session_state.status_message = "❌ Enter Conversation ID first!"
                    st.rerun()
            
            st.markdown('<div class="status-pill status-stopped">🔴 STOPPED - CLICK START</div>', unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# ==================== ROUTER ====================
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()
