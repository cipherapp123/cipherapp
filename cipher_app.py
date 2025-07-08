
import streamlit as st

# ====== إعداد كلمة المرور ======
PASSWORD = "1234"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "logout" not in st.session_state:
    st.session_state.logout = False

# ====== CSS لتنسيق الواجهة ======
st.markdown("""
    <style>
    body {background-color: #f0f2f5;}
    .main-container {
        background-color: #ffffff;
        padding: 2rem 3rem;
        border-radius: 20px;
        box-shadow: 0 0 25px rgba(0,0,0,0.05);
        max-width: 800px;
        margin: auto;
    }
    h1, h2, h3 {
        color: #1f77b4;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        font-size: 18px;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        padding: 10px 25px;
        font-size: 18px;
        border-radius: 10px;
        border: none;
        margin-top: 15px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #105a8b;
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

# ====== شاشة تسجيل الدخول ======
if not st.session_state.authenticated or st.session_state.logout:
    st.set_page_config(page_title="🔐 Login", layout="centered")
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    st.markdown("<h2>🔐 تسجيل الدخول</h2>", unsafe_allow_html=True)
    password = st.text_input("أدخل كلمة المرور", type="password")
    if st.button("دخول"):
        if password == PASSWORD:
            st.session_state.authenticated = True
            st.session_state.logout = False
            st.experimental_rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ====== اللغة ======
with st.sidebar:
    lang = st.selectbox("🌐 اختر اللغة / Select Language", ["العربية", "English"])

translations = {
    "العربية": {
        "title": "🔐 مشروع التشفير وفك التشفير",
        "operation": "اختر العملية:",
        "encrypt": "تشفير",
        "decrypt": "فك التشفير",
        "enter_text": "✍️ أدخل النص:",
        "offset": "🔑 أدخل مقدار الإزاحة:",
        "run": "🚀 تنفيذ",
        "result_enc": "✅ النص المشفر:",
        "result_dec": "🔓 النص المفكوك:",
        "copy": "📋 نسخ الناتج إلى الحافظة",
        "save": "💾 حفظ الناتج إلى ملف .txt",
        "empty_warning": "الرجاء إدخال نص أولاً.",
        "logout": "🚪 تسجيل الخروج",
    },
    "English": {
        "title": "🔐 Encryption & Decryption Project",
        "operation": "Select Operation:",
        "encrypt": "Encrypt",
        "decrypt": "Decrypt",
        "enter_text": "✍️ Enter your text:",
        "offset": "🔑 Enter shift amount:",
        "run": "🚀 Run",
        "result_enc": "✅ Encrypted text:",
        "result_dec": "🔓 Decrypted text:",
        "copy": "📋 Copy result to clipboard",
        "save": "💾 Save result as .txt file",
        "empty_warning": "Please enter some text first.",
        "logout": "🚪 Logout",
    }
}

with st.sidebar:
    if st.button(translations[lang]["logout"]):
        st.session_state.logout = True
        st.session_state.authenticated = False
        st.experimental_rerun()

# ====== الأبجديات ======
arabic_alphabet = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
english_alphabet = "abcdefghijklmnopqrstuvwxyz"

def get_alphabet(letter):
    if letter.lower() in arabic_alphabet:
        return arabic_alphabet
    elif letter.lower() in english_alphabet:
        return english_alphabet
    else:
        return None

def get_order(letter, offset):
    alphabet = get_alphabet(letter)
    if alphabet is None:
        return 0
    letter = letter.lower()
    index = alphabet.index(letter)
    adjusted = (index + offset) % len(alphabet)
    return adjusted + 1

def get_letter(order, offset, alphabet):
    adjusted = (order - 1 - offset) % len(alphabet)
    return alphabet[adjusted]

def encode_sentence(sentence, offset):
    words = sentence.strip().split()
    encoded_words = []
    for word in words:
        if not word:
            continue
        word = word.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        first = word[0]
        remaining = word[1:]
        remaining_length = len(remaining)
        order_list = [str(get_order(ch, offset)) for ch in remaining]
        encoded_word = [first, str(remaining_length)] + order_list
        encoded_words.append(" ".join(encoded_word))
    return " ".join(encoded_words)

def decode_sentence(code, offset):
    parts = code.strip().split()
    decoded_words = []
    i = 0
    while i < len(parts):
        try:
            first = parts[i]
            length = int(parts[i+1])
            numbers = parts[i+2:i+2+length]
            alphabet = get_alphabet(first)
            if alphabet is None:
                alphabet = arabic_alphabet
            chars = [get_letter(int(n), offset, alphabet) for n in numbers]
            word = first + ''.join(chars)
            decoded_words.append(word)
            i += 2 + length
        except:
            decoded_words.append("[خطأ]" if lang == "العربية" else "[Error]")
            break
    return ' '.join(decoded_words)

# ====== واجهة التطبيق ======
st.set_page_config(page_title=translations[lang]["title"], layout="centered")
st.markdown("<div class='main-container'>", unsafe_allow_html=True)
st.markdown(f"<h2>{translations[lang]['title']}</h2>", unsafe_allow_html=True)

operation = st.radio(translations[lang]["operation"], [translations[lang]["encrypt"], translations[lang]["decrypt"]])
text_input = st.text_area(translations[lang]["enter_text"], height=150)
offset = st.number_input(translations[lang]["offset"], min_value=0, max_value=100, value=1)

if st.button(translations[lang]["run"]):
    if not text_input.strip():
        st.warning(translations[lang]["empty_warning"])
    else:
        if operation == translations[lang]["encrypt"]:
            st.session_state.result = encode_sentence(text_input, offset)
            st.success(translations[lang]["result_enc"])
        else:
            st.session_state.result = decode_sentence(text_input, offset)
            st.success(translations[lang]["result_dec"])

if "result" in st.session_state and st.session_state.result.strip():
    st.text_area("📄 Output:", value=st.session_state.result, height=150, key="output_area")

    st.markdown(f"""
        <button onclick="navigator.clipboard.writeText(document.getElementById('output_area').value)"
        style="background-color:#4CAF50;border:none;color:white;padding:8px 16px;
        text-align:center;text-decoration:none;display:inline-block;font-size:14px;
        border-radius:6px;margin-top:10px;cursor:pointer;">
        {translations[lang]["copy"]}
        </button>
    """, unsafe_allow_html=True)

    st.download_button(
        label=translations[lang]["save"],
        data=st.session_state.result.encode("utf-8"),
        file_name="encrypted.txt" if operation == translations[lang]["encrypt"] else "decrypted.txt",
        mime="text/plain"
    )

st.markdown("</div>", unsafe_allow_html=True)
