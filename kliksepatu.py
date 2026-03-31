import streamlit as st

st.set_page_config(page_title="KlikSepatu", page_icon="🖤", layout="wide")

# ── Session State Defaults ──────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "home",
        "logged_in": False,
        "user": None,
        "cart": [],
        "selected_product": None,
        "orders": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Design System (shared CSS) ──────────────────────────────────────────────
GLOBAL_CSS = """
<style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

* { box-sizing: border-box; margin: 0; padding: 0; }
body, .stApp { background: #fff; font-family: 'Old Standard TT', serif; }
a.st-emotion-cache-1f3w014, h1 a, h2 a, h3 a, h4 a { display: none !important; }
header { visibility: hidden; }
.block-container {
    padding: 0 0 80px 0 !important;
    max-width: 100% !important;
}

/* ── Global font override for ALL Streamlit native elements ── */
.stTextInput input, .stTextInput textarea,
.stSelectbox select, .stSelectbox div[data-baseweb="select"],
.stSelectbox [data-baseweb="select"] *,
.stNumberInput input,
.stTextArea textarea,
.stRadio label, .stRadio span,
.stCheckbox label, .stCheckbox span,
.stButton button,
.stForm label, .stForm p,
.stMarkdown p,
div[data-testid="stWidgetLabel"] p,
div[data-testid="stWidgetLabel"],
[data-testid="stText"],
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] *,
[data-baseweb="menu"] *,
[data-baseweb="list-item"] *,
.stSelectbox [role="listbox"] *,
.stSelectbox [role="option"] *,
.element-container p,
.element-container span:not(.material-symbols-outlined):not(.bebas-force) {
    font-family: 'Old Standard TT', serif !important;
}

/* ── Streamlit button font override ── */
div[data-testid="stButton"] > button,
.stButton > button {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
}
/* Also force Bebas Neue on the inner <p> that Streamlit wraps button text in */
div[data-testid="stButton"] > button p,
div[data-testid="stButton"] > button span:not(.material-symbols-outlined),
.stButton > button p,
.stButton > button span:not(.material-symbols-outlined) {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
}

/* ── Input field base styles ── */
.stTextInput div[data-baseweb="input"], .stTextArea div[data-baseweb="textarea"], .stNumberInput div[data-baseweb="input"] {
    border: 1.5px solid #ddd !important;
    border-radius: 8px !important;
    background-color: transparent !important;
    transition: border-color .2s !important;
}
.stTextInput input, .stTextArea textarea, .stNumberInput input {
    font-size: 15px !important;
    font-family: 'Old Standard TT', serif !important;
    border: none !important; 
    box-shadow: none !important;
}
.stTextInput div[data-baseweb="input"]:focus-within, .stTextArea div[data-baseweb="textarea"]:focus-within, .stNumberInput div[data-baseweb="input"]:focus-within {
    border-color: #030303 !important;
    box-shadow: none !important;
}

/* ── Selectbox styling ── */
[data-baseweb="select"] > div {
    border: 1.5px solid #ddd !important;
    border-radius: 8px !important;
    font-family: 'Old Standard TT', serif !important;
    font-size: 15px !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #030303 !important;
    box-shadow: none !important;
}
[data-baseweb="menu"] {
    font-family: 'Old Standard TT', serif !important;
    font-size: 14px !important;
}

/* ── Navbar ── */
.navbar {
    position: fixed; top: 0; left: 0; width: 100%; z-index: 9999;
    background: #fff; display: flex; align-items: center;
    padding: 12px 40px; border-bottom: 1px solid #eee;
    font-family: 'Bebas Neue', sans-serif;
}
.nav-logo { font-size: 42px; letter-spacing: 1px; color: #030303; flex: 1; }
.nav-menu { flex: 1; display: flex; justify-content: center; gap: 30px; font-size: 22px; }
.nav-menu span {
    cursor: pointer; padding: 0 16px; position: relative;
    color: #030303; transition: color .3s;
}
.nav-menu span::after {
    content: ""; position: absolute; bottom: -2px; left: 0;
    width: 0; height: 2px; background: #030303; transition: width .3s;
}
.nav-menu span:hover::after { width: 100%; }
.nav-actions { flex: 1; display: flex; justify-content: flex-end; align-items: center; gap: 12px; }
.nav-btn {
    display: flex; align-items: center; gap: 8px;
    padding: 4px 20px; font-size: 20px; font-family: 'Bebas Neue', sans-serif;
    background: transparent; border: 1.5px solid #030303;
    border-radius: 30px; cursor: pointer; color: #030303; transition: all .3s;
}
.nav-btn:hover { background: #030303; color: #fff; }
.nav-btn-red {
    display: flex; align-items: center; gap: 8px;
    padding: 4px 20px; font-size: 20px; font-family: 'Bebas Neue', sans-serif;
    background: transparent; border: 1.5px solid #da2a2b;
    border-radius: 30px; cursor: pointer; color: #da2a2b; transition: all .3s;
}
.nav-btn-red:hover { background: #da2a2b; color: #fff; }
.page-pad { padding-top: 80px; }

/* ── Buttons ── */
.btn-primary {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 12px 32px; font-size: 20px; font-family: 'Bebas Neue', sans-serif;
    background: #030303; color: #fff; border: none;
    border-radius: 30px; cursor: pointer; transition: all .3s; letter-spacing: 1px;
}
.btn-primary:hover { background: #da2a2b; }
.btn-outline {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 10px 28px; font-size: 20px; font-family: 'Bebas Neue', sans-serif;
    background: transparent; color: #030303; border: 1.5px solid #030303;
    border-radius: 30px; cursor: pointer; transition: all .3s;
}
.btn-outline:hover { background: #030303; color: #fff; }
.btn-red {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 12px 32px; font-size: 20px; font-family: 'Bebas Neue', sans-serif;
    background: #da2a2b; color: #fff; border: none;
    border-radius: 30px; cursor: pointer; transition: all .3s;
}
.btn-red:hover { background: #b01f20; }

/* ── Cards ── */
.product-card {
    background: #f6f6f6; border-radius: 14px; overflow: hidden;
    cursor: pointer; transition: transform .35s, box-shadow .35s;
    transform: scale(0.97);
}
.product-card:hover { transform: scale(1); box-shadow: 0 16px 40px rgba(0,0,0,.13); }
.product-card img { width: 100%; height: 280px; object-fit: cover; }
.card-body { padding: 18px; }
.card-name { font-family: 'Bebas Neue', sans-serif; font-size: 28px; letter-spacing: 1px; margin-bottom: 2px; }
.card-brand { font-size: 11px; color: #999; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 2px; }
.card-price { font-family: 'Bebas Neue', sans-serif; font-size: 22px; color: #da2a2b; }
.card-rating { display:flex; align-items:center; gap:4px; font-size: 12px; color: #888; margin-top: 4px; }
.star-icon { font-size:14px !important; color:#f0a500; }

/* ── Section title ── */
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 90px; line-height: .95; color: #030303;
}
.section-title em {
    font-family: 'Old Standard TT', serif;
    font-style: italic; font-weight: 200; font-size: 55px;
}

/* ── Section label ── */
.section-label {
    display: flex; align-items: center; gap: 8px;
    font-size: 11px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: #999; margin-bottom: 12px;
    font-family: 'Bebas Neue', sans-serif;
}
.section-label span { font-size: 16px !important; color: #da2a2b; }

/* ── Status badges ── */
.badge { display:inline-block; padding: 4px 14px; border-radius: 20px; font-size: 13px; font-family: 'Old Standard TT', serif; }
.badge-pending { background: #fff3cd; color: #856404; }
.badge-packed  { background: #cff4fc; color: #055160; }
.badge-shipped { background: #d1e7dd; color: #0a3622; }
.badge-delivered { background: #030303; color: #fff; }

/* ── Form native inputs ── */
input[type=text], input[type=email], input[type=tel], select, textarea {
    width: 100%; padding: 12px 16px; border: 1.5px solid #ddd;
    border-radius: 10px; font-family: 'Old Standard TT', serif;
    font-size: 15px; outline: none; transition: border .2s;
}
input:focus, select:focus, textarea:focus { border-color: #030303; }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid #eee; margin: 24px 0; }

/* ── Track step ── */
.track-step { display: flex; align-items: flex-start; gap: 24px; margin-bottom: 8px; }
.track-icon { width: 48px; height: 48px; border-radius: 50%; display:flex; align-items:center; justify-content:center; flex-shrink: 0; }
.track-icon.done   { background: #030303; }
.track-icon.active { background: #da2a2b; }
.track-icon.idle   { background: #e8e8e8; }
.track-icon span { font-size: 24px !important; color: #fff; }
.track-icon.idle span { color: #bbb; }
.track-line { width: 2px; height: 48px; margin-left: 23px; }
.track-line.done { background: #030303; }
.track-line.idle { background: #e8e8e8; }
.track-label { font-weight: 700; font-size: 20px; font-family: 'Old Standard TT', serif; }
.track-sub   { font-size: 14px; color: #999; font-family: 'Old Standard TT', serif; }

/* ── Empty state ── */
.empty-state { text-align:center; padding: 80px 20px; }
.empty-state .empty-icon { font-size: 72px !important; color: #ddd; margin-bottom: 20px; }
.empty-state h3 { font-family:'Bebas Neue',sans-serif; font-size:32px; color:#bbb; letter-spacing:2px; margin-bottom:8px; }
.empty-state p { font-size:14px; color:#aaa; font-family:'Old Standard TT',serif; }

/* ── Login page ── */
.login-wrap {
    min-height: calc(100vh - 0px);
    display: flex; align-items: center; justify-content: center;
    background: #fafafa;
}
.login-panel {
    display: flex; width: 820px; max-width: 98vw;
    box-shadow: 0 24px 64px rgba(0,0,0,.10);
    border: 1px solid #e8e8e8;
    background: #fff;
    min-height: 520px;
}
.login-left {
    flex: 1; background: #030303;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 48px 36px; text-align: center;
}
.login-left-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 52px; letter-spacing: 4px; color: #fff;
    margin-bottom: 10px;
}
.login-left-tag {
    font-family: 'Old Standard TT', serif;
    font-style: italic; font-size: 15px; color: rgba(255,255,255,.5);
    line-height: 1.6;
}
.login-left-accent {
    width: 40px; height: 2px; background: #da2a2b;
    margin: 20px auto 0;
}
.login-right {
    flex: 1; padding: 52px 44px;
    display: flex; flex-direction: column; justify-content: center;
}
.login-right-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 36px; letter-spacing: 3px; color: #030303;
    margin-bottom: 4px;
}
.login-right-sub {
    font-family: 'Old Standard TT', serif;
    font-style: italic; font-size: 13px; color: #aaa;
    margin-bottom: 32px;
}
.login-hint {
    text-align: center;
    font-family: 'Old Standard TT', serif;
    font-style: italic; font-size: 12px; color: #bbb;
    margin-top: 14px;
    padding: 10px; background: #f9f9f9; border-radius: 6px;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Data ────────────────────────────────────────────────────────────────────
PRODUCTS = [
    {"id":1,"name":"Air Max 97","brand":"Nike","price":2850000,"rating":4.8,"stock":50,"colors":["Black","White","Red"],"sizes":[38,39,40,41,42,43],"desc":"Iconic full-length Air cushioning with a sleek silhouette. Breathable mesh upper keeps your feet cool all day.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_4.jpg","category":"Sneakers"},
    {"id":2,"name":"Ultra Boost 22","brand":"Adidas","price":3200000,"rating":4.9,"stock":50,"colors":["White","Blue","Grey"],"sizes":[38,39,40,41,42],"desc":"Responsive Boost midsole returns energy with every stride. Primeknit upper adapts to the shape of your foot.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_5.jpeg","category":"Running"},
    {"id":3,"name":"Classic Loafer","brand":"Gucci","price":7500000,"rating":4.7,"stock":50,"colors":["Brown","Black","Tan"],"sizes":[39,40,41,42,43],"desc":"Handcrafted Italian leather loafer with signature horsebit hardware. Timeless elegance for every occasion.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_6.jpg","category":"Formal"},
    {"id":4,"name":"Sky High Pump","brand":"Jimmy Choo","price":9800000,"rating":4.6,"stock":50,"colors":["Nude","Black","Red"],"sizes":[36,37,38,39,40],"desc":"A soaring stiletto heel with a luxurious patent leather upper. The ultimate statement shoe.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_7.jpg","category":"Heels"},
    {"id":5,"name":"So Kate 120","brand":"Louboutin","price":12500000,"rating":4.9,"stock":50,"colors":["Black","Nude","Red"],"sizes":[36,37,38,39,40,41],"desc":"The iconic pointed-toe stiletto with signature red sole. Crafted in buttery soft leather for effortless glamour.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_8.jpeg","category":"Heels"},
    {"id":6,"name":"Andy Loafer","brand":"Berluti","price":18000000,"rating":4.8,"stock":50,"colors":["Ebony","Cognac","Navy"],"sizes":[40,41,42,43,44],"desc":"Hand-stitched Venezia leather with Berluti's iconic patina. An art piece you can wear.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_9.jpg","category":"Formal"},
    {"id":7,"name":"Air Max 97","brand":"Nike","price":2850000,"rating":4.8,"stock":50,"colors":["Black","White","Red"],"sizes":[38,39,40,41,42,43],"desc":"Iconic full-length Air cushioning with a sleek silhouette. Breathable mesh upper keeps your feet cool all day.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_4.jpg","category":"Sneakers"},
    {"id":8,"name":"Ultra Boost 22","brand":"Adidas","price":3200000,"rating":4.9,"stock":50,"colors":["White","Blue","Grey"],"sizes":[38,39,40,41,42],"desc":"Responsive Boost midsole returns energy with every stride. Primeknit upper adapts to the shape of your foot.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_5.jpeg","category":"Running"},
    {"id":9,"name":"Classic Loafer","brand":"Gucci","price":7500000,"rating":4.7,"stock":50,"colors":["Brown","Black","Tan"],"sizes":[39,40,41,42,43],"desc":"Handcrafted Italian leather loafer with signature horsebit hardware. Timeless elegance for every occasion.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_6.jpg","category":"Formal"},
    {"id":10,"name":"Sky High Pump","brand":"Jimmy Choo","price":9800000,"rating":4.6,"stock":50,"colors":["Nude","Black","Red"],"sizes":[36,37,38,39,40],"desc":"A soaring stiletto heel with a luxurious patent leather upper. The ultimate statement shoe.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_7.jpg","category":"Heels"},
    {"id":11,"name":"So Kate 120","brand":"Louboutin","price":12500000,"rating":4.9,"stock":50,"colors":["Black","Nude","Red"],"sizes":[36,37,38,39,40,41],"desc":"The iconic pointed-toe stiletto with signature red sole. Crafted in buttery soft leather for effortless glamour.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_8.jpeg","category":"Heels"},
    {"id":12,"name":"Andy Loafer","brand":"Berluti","price":18000000,"rating":4.8,"stock":50,"colors":["Ebony","Cognac","Navy"],"sizes":[40,41,42,43,44],"desc":"Hand-stitched Venezia leather with Berluti's iconic patina. An art piece you can wear.","img":"https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_9.jpg","category":"Formal"},
]

USERS = {
    "customer@ks.com": {"password":"123","name":"Alex","role":"customer"},
    "admin@ks.com": {"password":"123","name":"Admin","role":"admin"}
}

if "products" not in st.session_state:
    st.session_state.products = PRODUCTS.copy()

def fmt(price): return f"Rp {price:,.0f}".replace(",",".")

def nav(brands=True):
    cart_count = len(st.session_state.cart)
    cart_label = f"CART ({cart_count})" if cart_count else "CART"
    li = st.session_state.logged_in
    user_btn = f'<button class="nav-btn-red" onclick="" style="margin-right:8px">👤 {st.session_state.user["name"].upper()}</button>' if li else '<button class="nav-btn">LOGIN</button>'
    st.markdown(f"""
    <div class="navbar">
        <div class="nav-logo">KlikSepatu</div>
        <div class="nav-menu">
            <span>SHOP</span>
            <span>BRANDS</span>
            <span>EDITORIAL</span>
        </div>
        <div class="nav-actions">
            <button class="nav-btn">
                <span class="material-symbols-outlined" style="font-size:20px">search</span>
            </button>
            {user_btn}
            <button class="nav-btn">
                <span class="material-symbols-outlined" style="font-size:20px">shopping_cart</span>
                {cart_label}
            </button>
        </div>
    </div>
    <div class="page-pad"></div>
    """, unsafe_allow_html=True)

# ── NAV BUTTONS (Streamlit clickable) ───────────────────────────────────────
def nav_buttons():
    st.markdown("""
    <style>
    /* ── Sticky Navbar wrapper ── */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) {
        position: sticky; top: 0; z-index: 9999;
        background: #fff !important;
        border-bottom: 1px solid #ebebeb !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
        height: 70px !important;
        align-items: center !important;
    }

    /* ── All nav buttons: reset ── */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) button {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 2.5px !important;
        transition: all .2s !important;
        padding: 0 8px !important;
        height: 70px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #444 !important;
        font-size: 15px !important;
        width: 100% !important;
    }

    /* ── Logo button (col 0) ── */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(1) button {
        letter-spacing: 4px !important;
        color: #030303 !important;
        font-weight: 900 !important;
        padding: 0 !important;
        text-align: left !important;
        justify-content: flex-start !important;
        margin-left: -110px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(1) button p {
        font-size: 36px !important;
        -webkit-text-stroke: 1.5px #030303 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(1) button:hover {
        color: #da2a2b !important;
        background: transparent !important;
    }

    /* ── CENTER nav link buttons (HOME, SHOP, BRANDS) ── */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(3) button,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(4) button,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(5) button {
        letter-spacing: 2px !important;
        color: #555 !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(3) button p,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(4) button p,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(5) button p {
        font-size: 22px !important;
        font-family: 'Bebas Neue', sans-serif !important;
    }
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(3) button:hover,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(4) button:hover,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(5) button:hover {
        color: #030303 !important;
        border-bottom: 2px solid #030303 !important;
        background: transparent !important;
    }

    /* ── CART, ORDERS / LOGIN / LOGOUT pill buttons ── */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(7) button,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(8) button,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(9) button {
        background: transparent !important;
        border: 1.5px solid #030303 !important;
        border-radius: 30px !important;
        color: #030303 !important;
        letter-spacing: 2px !important;
        padding: 0 16px !important;
        height: 44px !important;
        min-height: unset !important;
        max-height: 44px !important;
        box-sizing: border-box !important;
        vertical-align: middle !important;
    }
    /* force the inner p tag to not add height */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(7) button p,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(8) button p,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(9) button p {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 19px !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        white-space: nowrap !important;
    }
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(7) button:hover,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(8) button:hover,
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(9) button:hover {
        background: #030303 !important;
        color: #fff !important;
    }
    /* make each pill column flex-center vertically */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(7),
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(8),
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(9) {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* CART Button Icon Injection */
    div[data-testid="stHorizontalBlock"]:has(#nav-marker) > div:nth-child(7) button p::before {
        font-family: 'Material Symbols Outlined';
        content: 'shopping_cart';
        font-size: 22px;
        vertical-align: -3px;
        margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Layout dynamically adjusting for login state to keep HOME/SHOP/BRANDS perfectly centered
    if st.session_state.logged_in:
        cols = st.columns([2.8, 0.8, 0.8, 0.8, 0.8, 0.3, 1.1, 1.1, 1.1])
    else:
        cols = st.columns([2.8, 0.8, 0.8, 0.8, 0.8, 1.4, 1.1, 1.1])
        
    with cols[0]:
        st.markdown('<div id="nav-marker" style="display:none"></div>', unsafe_allow_html=True)
        if st.button("KLIKSEPATU", key="nb_logo", use_container_width=True):
            st.session_state.page = "home"; st.rerun()
    with cols[2]:
        if st.button("HOME", key="nb_home", use_container_width=True):
            st.session_state.page = "home"; st.rerun()
    with cols[3]:
        if st.button("SHOP", key="nb_shop", use_container_width=True):
            st.session_state.page = "catalog"; st.rerun()
    with cols[4]:
        if st.button("BRANDS", key="nb_brands", use_container_width=True):
            st.session_state.page = "catalog"; st.rerun()
    with cols[6]:
        cart_n = len(st.session_state.cart)
        cart_count_txt = f" {cart_n}" if cart_n else ""
        lbl = f"CART{cart_count_txt}"
        if st.button(lbl, key="nb_cart", use_container_width=True):
            st.session_state.page = "cart"; st.rerun()
    with cols[7]:
        if st.session_state.logged_in:
            if st.button("ORDERS", key="nb_orders", use_container_width=True):
                st.session_state.page = "track"; st.rerun()
        else:
            if st.button("LOGIN", key="nb_login", use_container_width=True):
                st.session_state.page = "login"; st.rerun()
                
    if st.session_state.logged_in:
        with cols[8]:
            if st.button("LOGOUT", key="nb_logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.page = "home"; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════
def page_home():
    nav_buttons()
    st.markdown("""
    <style>
    .hero-title {
        font-family:'Bebas Neue',sans-serif;
        text-align:center; font-size:128px; line-height:.88;
        letter-spacing:3px; margin: 36px 0 0;
    }
    .hero-title em {
        font-family:'Old Standard TT',serif;
        font-style:italic; font-weight:400; font-size:68px;
        color:#555; letter-spacing:0;
    }
    .img-full img {
        width:100%; height:88vh; object-fit:cover;
        object-position:center; display:block;
    }
    .section-header {
        display:flex; justify-content:space-between; align-items:flex-end;
        padding: 80px 56px 32px;
    }
    .marquee-wrap { overflow:hidden; padding-bottom:72px; }
    .marquee-track {
        display:flex; gap:16px; width:max-content;
        animation:scroll-left 40s linear infinite;
    }
    .marquee-track:hover { animation-play-state:paused; }
    @keyframes scroll-left {
        0%{transform:translateX(0)} 100%{transform:translateX(calc(-50% - 8px))}
    }
    .home-card {
        flex:0 0 320px; height:540px;
        background:#fff; border:1px solid #e8e8e8;
        overflow:hidden; cursor:pointer;
        transform:translateY(0);
        transition:transform .4s, box-shadow .4s;
        position:relative;
    }
    .home-card:hover {
        transform:translateY(-6px);
        box-shadow:0 16px 40px rgba(0,0,0,.12);
    }
    .home-card .top {
        width:100%; height:72%;
        background-size:cover; background-position:center;
    }
    .home-card .info { padding:16px; background:#fff; }
    .home-card .cn {
        font-family:'Bebas Neue',sans-serif;
        font-size:26px; letter-spacing:2px; color:#111;
    }
    .home-card .cb {
        font-family:'Old Standard TT',serif;
        font-style:italic; font-size:11px; color:#aaa; margin-bottom:2px;
    }
    .home-card .cp {
        font-family:'Bebas Neue',sans-serif;
        font-size:18px; color:#da2a2b; letter-spacing:1px;
    }
    .big-btn {
        display:inline-flex; align-items:center; gap:10px;
        padding:10px 28px; font-size:22px;
        font-family:'Bebas Neue',sans-serif; letter-spacing:2px;
        background:transparent; border:1.5px solid #030303;
        border-radius:3px; cursor:pointer; color:#030303; transition:all .25s;
    }
    .big-btn:hover { background:#030303; color:#fff; }
    .big-btn-red {
        display:inline-flex; align-items:center; gap:10px;
        padding:10px 28px; font-size:22px;
        font-family:'Bebas Neue',sans-serif; letter-spacing:2px;
        background:transparent; border:1.5px solid #da2a2b;
        border-radius:3px; cursor:pointer; color:#da2a2b; transition:all .25s;
    }
    .big-btn-red:hover { background:#da2a2b; color:#fff; }

    /* ── Section promo header (matching app.py) ── */
    .tagline {
        margin-top: 100px !important;
        margin-left: 50px !important;
        margin-bottom: 20px !important;
    }
    .tagline h2 {
        font-family: 'Bebas Neue', sans-serif !important;
        text-align: start;
        font-size: 150px;
        font-weight: 700;
        line-height: 100px;
        margin: 0;
    }
    /* Force Bebas Neue — overrides the global element-container span rule */
    .element-container span.bebas-force,
    .stMarkdown span.bebas-force,
    span.bebas-force {
        font-family: 'Bebas Neue', sans-serif !important;
    }
    .button-b {
        display: flex;
        gap: 15px;
        padding: 10px 30px;
        margin-right: 50px;
        margin-bottom: 35px;
        font-weight: 400;
        font-size: 35px;
        color: #da2a2b;
        align-items: center;
        font-family: 'Bebas Neue', sans-serif;
        background-color: transparent;
        border-radius: 50px;
        border: 1px solid black;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .button-b:hover { background-color: #da2a2b; color: white; }
    .button-b-dark {
        display: flex;
        gap: 15px;
        padding: 10px 30px;
        margin-right: 50px;
        margin-bottom: 35px;
        font-weight: 400;
        font-size: 35px;
        color: #030303;
        align-items: center;
        font-family: 'Bebas Neue', sans-serif;
        background-color: transparent;
        border-radius: 50px;
        border: 1px solid #030303;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .button-b-dark:hover { background-color: #030303; color: white; }
    .cat-card {
        position:relative; overflow:hidden; cursor:pointer;
        border-radius:3px; margin: 0 6px;
    }
    .cat-card img {
        width:100%; height:400px; object-fit:cover; display:block;
        filter:brightness(.65); transition:filter .4s, transform .4s;
    }
    .cat-card:hover img { filter:brightness(.5); transform:scale(1.03); }
    .cat-label {
        position:absolute; bottom:0; left:0; right:0;
        padding:24px 20px;
        background: linear-gradient(transparent, rgba(0,0,0,.6));
    }
    .cat-label-main {
        font-family:'Bebas Neue',sans-serif;
        font-size:36px; letter-spacing:3px; color:#fff;
    }
    .cat-label-sub {
        font-family:'Old Standard TT',serif;
        font-style:italic; font-size:13px; color:rgba(255,255,255,.7);
    }
    
    /* Native Promo Buttons Custom Styling */
    div[data-testid="stHorizontalBlock"]:has(.promo-light),
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) {
        align-items: flex-end !important;
        padding-top: 20px !important; padding-bottom: 20px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-light) > div:first-child,
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) > div:first-child {
        padding-left: 50px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-light) > div:last-child,
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) > div:last-child {
        padding-right: 50px !important; display: flex; justify-content: flex-end;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-light) button,
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) button {
        display: inline-flex !important; padding: 10px 30px !important;
        font-family: 'Bebas Neue', sans-serif !important; font-weight: 400 !important;
        background-color: transparent !important; border-radius: 50px !important;
        cursor: pointer !important; transition: all 0.3s ease !important;
        width: auto !important; height: auto !important; align-items: center !important;
        justify-content: center !important; margin: 0 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-light) button {
        color: #da2a2b !important; border: 1px solid black !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-light) button:hover {
        background-color: #da2a2b !important; color: white !important; border-color: #da2a2b !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) button {
        color: #030303 !important; border: 1px solid #030303 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) button:hover {
        background-color: #030303 !important; color: white !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-light) button p,
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) button p {
        font-size: 35px !important; margin: 0 !important; display: flex !important;
        align-items: center !important; gap: 15px !important;
    }
    div[data-testid="stHorizontalBlock"]:has(.promo-light) button p::after,
    div[data-testid="stHorizontalBlock"]:has(.promo-dark) button p::after {
        content: 'arrow_circle_right'; font-family: 'Material Symbols Outlined'; font-size: 35px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-title">
        <em>the</em> Perfect Pair<br>Click. Choose. Use.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="img-full">
        <img src="https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_1.png">
    </div>
    """, unsafe_allow_html=True)
    col_t1, col_b1 = st.columns([7.5, 2.5])
    with col_t1:
        st.markdown("""
        <div class="promo-light" style="display:none"></div>
        <div class="tagline">
            <h2> <span style="font-family: 'Old Standard TT', serif; font-style: italic; font-weight: 200; font-size: 80px;"> our </span>
                <span class="bebas-force" style="font-family: 'Bebas Neue', sans-serif !important;">best</span>
                <span style="font-family: 'Old Standard TT', serif; font-style: italic; font-weight: 200; font-size: 80px;"> products </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
    with col_b1:
        if st.button("View All", key="va_best", use_container_width=False):
            st.session_state.cat_filter = "All Categories"
            st.session_state.page = "catalog"; st.rerun()

    def hcard(p):
        return f"""<div class="home-card">
            <div class="top" style="background-image:url('{p['img']}')"></div>
            <div class="info">
                <div class="cb">{p['brand']}</div>
                <div class="cn">{p['name']}</div>
                <div class="cp">{fmt(p['price'])}</div>
            </div>
        </div>"""

    cards_html = "".join(hcard(p) for p in PRODUCTS)
    st.markdown(f"""
    <div class="marquee-wrap">
        <div class="marquee-track">{cards_html}{cards_html}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="img-full">
        <img src="https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_2-fotor.png">
    </div>
    """, unsafe_allow_html=True)
    col_t2, col_b2 = st.columns([7.5, 2.5])
    with col_t2:
        st.markdown("""
        <div class="promo-dark" style="display:none"></div>
        <div class="tagline">
            <h2> <span class="bebas-force" style="font-family: 'Bebas Neue', sans-serif !important;">shoes</span>
                <span style="font-family: 'Old Standard TT', serif; font-style: italic; font-weight: 200; font-size: 80px;"> types </span>
            </h2>
        </div>
        """, unsafe_allow_html=True)
    with col_b2:
        if st.button("View All", key="va_types", use_container_width=False):
            st.session_state.cat_filter = "All Categories"
            st.session_state.page = "catalog"; st.rerun()

    cat_data = [
        ("Sneakers", "Street & Sport", "https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_4.jpg"),
        ("Heels",    "Elevated Glamour", "https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_8.jpeg"),
        ("Formal",   "Timeless Craft", "https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_9.jpg"),
    ]
    col1, col2, col3 = st.columns(3)
    for col, (cat, sub, img) in zip([col1, col2, col3], cat_data):
        with col:
            st.markdown(f"""
            <div class="cat-card">
                <img src="{img}">
                <div class="cat-label">
                    <div class="cat-label-sub">{sub}</div>
                    <div class="cat-label-main">{cat}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"SHOP {cat.upper()}", key=f"cat_{cat}", use_container_width=True):
                st.session_state.cat_filter = cat
                st.session_state.page = "catalog"; st.rerun()

    st.markdown("""
    <div style="text-align:center;padding:64px 0 40px;
        font-family:'Bebas Neue',sans-serif;font-size:13px;
        color:#ccc;letter-spacing:4px;border-top:1px solid #ebebeb;margin-top:56px">
        &copy; 2025 &nbsp; KLIKSEPATU &nbsp; &mdash; &nbsp; ALL RIGHTS RESERVED
    </div>""", unsafe_allow_html=True)

    _, c2, _ = st.columns([3,1,3])
    with c2:
        if st.button("SHOP NOW", key="home_shop", use_container_width=True):
            st.session_state.page = "catalog"; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ═══════════════════════════════════════════════════════════════════════════
def page_login():
    st.markdown("""
    <style>
    /* Page background */
    .stApp { background: #f5f5f5 !important; }
    /* Kill ALL top spacing — every Streamlit wrapper */
    header[data-testid="stHeader"] { display: none !important; height: 0 !important; }
    #stDecoration { display: none !important; }
    .stApp > header { display: none !important; }
    [data-testid="stAppViewContainer"] { padding-top: 0 !important; margin-top: 0 !important; }
    [data-testid="stMain"] { padding-top: 0 !important; margin-top: 0 !important; overflow: hidden; }
    [data-testid="stMainBlockContainer"] { padding-top: 0 !important; margin-top: 0 !important; }
    .block-container { padding-top: 0 !important; margin-top: 0 !important; }
    section.main { padding-top: 0 !important; margin-top: 0 !important; }
    section.main > div { padding-top: 0 !important; margin-top: 0 !important; }
    /* Remove column gaps so the two halves butt up cleanly */
    section.main > div > div[data-testid="stHorizontalBlock"] {
        gap: 0 !important;
        align-items: stretch !important;
    }
    /* Left column — black branding panel */
    section.main > div > div[data-testid="stHorizontalBlock"] > div:first-child {
        background: #030303 !important;
        padding: 0 !important;
    }
    section.main > div > div[data-testid="stHorizontalBlock"] > div:first-child > div {
        padding: 0 !important;
    }
    /* Right column — white form panel */
    section.main > div > div[data-testid="stHorizontalBlock"] > div:last-child {
        background: #fff !important;
        border-left: 1px solid #e8e8e8 !important;
        padding: 0 !important;
    }
    section.main > div > div[data-testid="stHorizontalBlock"] > div:last-child > div {
        padding: 56px 52px !important;
    }
    /* SIGN IN button */
    div[data-testid="stForm"] button {
        background: #030303 !important; color: #fff !important;
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 18px !important; letter-spacing: 3px !important;
        border-radius: 4px !important; border: none !important;
        padding: 14px !important; transition: background .25s !important;
    }
    div[data-testid="stForm"] button:hover { background: #da2a2b !important; }
    /* Field labels (EMAIL ADDRESS / PASSWORD) */
    div[data-testid="stForm"] div[data-testid="stWidgetLabel"] p {
        font-family: 'Bebas Neue', sans-serif !important;
        font-size: 11px !important; letter-spacing: 2.5px !important; color: #999 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])

    with c1:
        st.markdown("""
        <div style="
            min-height: 100vh;
            background: linear-gradient(rgba(3,3,3,0.3), rgba(3,3,3,0.85)), url('https://raw.githubusercontent.com/ChelseaNatasjaJesslyneSembiring/KlikSepatu/main/static/home/foto_8.jpeg') center/cover no-repeat;
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            text-align: center; padding: 48px 36px;
        ">
            <div style="
                font-family: 'Bebas Neue', sans-serif;
                font-size: 80px; letter-spacing: 6px;
                color: #fff; line-height: 0.85;
                margin-bottom: 24px;
            ">KLIK<br>SEPATU</div>
            <div style="width:40px;height:2px;background:#da2a2b;margin-bottom:24px;"></div>
            <div style="
                font-family: 'Old Standard TT', serif;
                font-style: italic; font-size: 15px;
                color: rgba(255,255,255,0.4); line-height: 1.8;
            ">Discover the world's<br>finest footwear.</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="margin-bottom: 28px; padding-top: 8px;">
            <div style="
                font-family: 'Bebas Neue', sans-serif;
                font-size: 46px; letter-spacing: 3px; color: #030303;
                margin-bottom: 6px;
            ">Sign In</div>
            <div style="
                font-family: 'Old Standard TT', serif;
                font-style: italic; font-size: 14px; color: #aaa;
            ">Welcome back &#8212; enter your details below</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("EMAIL ADDRESS", placeholder="customer@ks.com")
            password = st.text_input("PASSWORD", type="password", placeholder="Enter your password")
            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("SIGN IN", use_container_width=True)

        if submitted:
            if email in USERS and USERS[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = USERS[email]
                if USERS[email]["role"] == "admin":
                    st.session_state.page = "admin_dashboard"
                else:
                    st.session_state.page = "catalog"
                st.rerun()
            else:
                st.error("Incorrect email or password.")

        st.markdown("""
        <div style="
            text-align:center; margin-top:16px; margin-bottom:12px;
            font-family:'Old Standard TT',serif; font-style:italic;
            font-size:12px; color:#bbb;
            background:#f9f9f9; border-radius:6px; padding:10px 14px;
        ">Demo: &nbsp;<b style='color:#555'>customer@ks.com</b>&nbsp;/&nbsp;<b style='color:#555'>123</b> &nbsp;&nbsp;|&nbsp;&nbsp; Admin: &nbsp;<b style='color:#555'>admin@ks.com</b>&nbsp;/&nbsp;<b style='color:#555'>123</b></div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.button("← Back to Home", key="login_back", use_container_width=True):
            st.session_state.page = "home"; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CATALOG
# ═══════════════════════════════════════════════════════════════════════════
def page_catalog():
    nav_buttons()

    st.markdown("""
    <div style="padding:48px 56px 20px; border-bottom:1px solid #ebebeb; margin-bottom:28px;">
        <div style="font-family:'Old Standard TT',serif;font-style:italic;font-size:13px;color:#aaa;letter-spacing:2px;margin-bottom:8px">Collection</div>
        <div class="section-title"><em>our</em> catalog</div>
        <div style="font-family:'Old Standard TT',serif;font-style:italic;font-size:15px;color:#aaa;margin-top:10px">Discover the finest footwear from the world&rsquo;s top brands</div>
    </div>
    """, unsafe_allow_html=True)

    # Filters
    pad_l, head_col, pad_r = st.columns([0.25, 5, 0.25])
    with head_col:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding-bottom:12px">
            <span class="material-symbols-outlined" style="color:#da2a2b;font-size:20px">tune</span>
            <span style="font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#999">Filter &amp; Sort</span>
        </div>
        """, unsafe_allow_html=True)
    # Pick up category pre-filter from home page category cards
    if "cat_filter" not in st.session_state:
        st.session_state.cat_filter = "All Categories"

    with st.container():
        pad_l, fc1, fc2, fc3, fc4, pad_r = st.columns([0.25, 2, 1, 1, 1, 0.25])
        with fc1:
            search = st.text_input("Search", key="cat_search", label_visibility="collapsed", placeholder="Search products or brands...")
        with fc2:
            brands = ["All Brands"] + sorted(set(p["brand"] for p in PRODUCTS))
            brand_f = st.selectbox("Brand", brands, label_visibility="collapsed", key="cat_brand")
        with fc3:
            cats = ["All Categories","Sneakers","Running","Formal","Heels"]
            default_cat_idx = cats.index(st.session_state.cat_filter) if st.session_state.cat_filter in cats else 0
            cat_f = st.selectbox("Category", cats, index=default_cat_idx, label_visibility="collapsed", key="cat_cat")
            st.session_state.cat_filter = "All Categories"  # reset after use
        with fc4:
            sort_f = st.selectbox("Sort by", ["Default","Price: Low to High","Price: High to Low","Top Rated"], label_visibility="collapsed", key="cat_sort")

    filtered = PRODUCTS.copy()
    if search:
        filtered = [p for p in filtered if search.lower() in p["name"].lower() or search.lower() in p["brand"].lower()]
    if brand_f != "All Brands":
        filtered = [p for p in filtered if p["brand"] == brand_f]
    if cat_f != "All Categories":
        filtered = [p for p in filtered if p["category"] == cat_f]
    if sort_f == "Price: Low to High": filtered.sort(key=lambda x: x["price"])
    elif sort_f == "Price: High to Low": filtered.sort(key=lambda x: x["price"], reverse=True)
    elif sort_f == "Top Rated": filtered.sort(key=lambda x: x["rating"], reverse=True)

    pad_l, txt_col, pad_r = st.columns([0.25, 5, 0.25])
    with txt_col:
        st.markdown(f'<div style="color:#888;font-size:14px;margin-bottom:12px">{len(filtered)} products found</div>', unsafe_allow_html=True)

    # ── Pagination ──────────────────────────────────────────────────────────
    ITEMS_PER_PAGE = 6
    total_pages = max(1, -(-len(filtered) // ITEMS_PER_PAGE))  # ceiling division

    if "catalog_page" not in st.session_state:
        st.session_state.catalog_page = 1
    # Reset to page 1 when filters change
    filter_sig = (search, brand_f, cat_f, sort_f)
    if "_last_filter_sig" not in st.session_state:
        st.session_state._last_filter_sig = filter_sig
    if st.session_state._last_filter_sig != filter_sig:
        st.session_state.catalog_page = 1
        st.session_state._last_filter_sig = filter_sig
    # Clamp current page
    st.session_state.catalog_page = max(1, min(st.session_state.catalog_page, total_pages))
    cur_page = st.session_state.catalog_page

    start = (cur_page - 1) * ITEMS_PER_PAGE
    page_products = filtered[start : start + ITEMS_PER_PAGE]

    for row_idx in range(0, len(page_products), 3):
        row_items = page_products[row_idx : row_idx+3]
        pad_l, c1, c2, c3, pad_r = st.columns([0.15, 1, 1, 1, 0.15])
        row_cols = [c1, c2, c3]
        for i, p in enumerate(row_items):
            with row_cols[i]:
                full_stars = int(p["rating"])
                star_icons = '<span class="material-symbols-outlined star-icon">star</span>' * full_stars
                st.markdown(f"""
                <div class="product-card" style="margin:8px 4px 16px">
                    <img src="{p['img']}" style="width:100%;height:260px;object-fit:cover">
                    <div class="card-body">
                        <div class="card-brand">{p['brand']} · {p['category']}</div>
                        <div class="card-name">{p['name']}</div>
                        <div class="card-price">{fmt(p['price'])}</div>
                        <div class="card-rating">{star_icons} <span style="font-size:12px;color:#aaa">{p['rating']}</span></div>
                    </div>
                </div>""", unsafe_allow_html=True)
                if st.button("View Details", key=f"view_{p['id']}", use_container_width=True):
                    st.session_state.selected_product = p
                    st.session_state.page = "detail"; st.rerun()

    # ── Pagination Controls ────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .pg-btn {
        min-width: 44px; height: 44px;
        display: inline-flex; align-items: center; justify-content: center;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 16px; letter-spacing: 1px;
        background: transparent; border: 1.5px solid #ddd;
        border-radius: 4px; cursor: pointer;
        color: #555; transition: all .22s;
        padding: 0 14px;
    }
    .pg-btn:hover { background: #030303; color: #fff; border-color: #030303; }
    .pg-btn.active { background: #030303; color: #fff; border-color: #030303; }
    .pg-btn.disabled { opacity: .3; pointer-events: none; }
    </style>
    """, unsafe_allow_html=True)

    if total_pages > 1:
        st.markdown('<div style="border-top:1px solid #ebebeb;margin-top:80px;padding-top:8px"></div>',
                    unsafe_allow_html=True)

        def visible_pages(cur, total):
            if total <= 7:
                return list(range(1, total + 1))
            if cur <= 4:
                return list(range(1, 6)) + ["...", total]
            if cur >= total - 3:
                return [1, "..."] + list(range(total - 4, total + 1))
            return [1, "...", cur - 1, cur, cur + 1, "...", total]

        pages_to_show = visible_pages(cur_page, total_pages)
        n_inner = len(pages_to_show) + 2  # prev + pages + next
        spacer_w = max(0.5, (8 - n_inner) / 2)
        col_widths = [spacer_w, 0.85] + [0.5] * len(pages_to_show) + [0.85, spacer_w]
        pg_cols = st.columns(col_widths)

        with pg_cols[1]:
            if st.button("← PREV", key="pg_prev", use_container_width=True,
                         disabled=(cur_page == 1)):
                st.session_state.catalog_page -= 1; st.rerun()

        for idx, pg in enumerate(pages_to_show):
            with pg_cols[idx + 2]:
                if pg == "...":
                    st.markdown('<div style="text-align:center;padding:10px 0;'
                                'color:#bbb;font-size:18px;line-height:44px">···</div>',
                                unsafe_allow_html=True)
                else:
                    if st.button(str(pg), key=f"pg_{pg}", use_container_width=True):
                        st.session_state.catalog_page = int(pg); st.rerun()

        with pg_cols[len(pages_to_show) + 2]:
            if st.button("NEXT →", key="pg_next", use_container_width=True,
                         disabled=(cur_page == total_pages)):
                st.session_state.catalog_page += 1; st.rerun()

        st.markdown(
            f'<div style="text-align:center;font-family:\'Old Standard TT\',serif;'
            f'font-style:italic;font-size:13px;color:#bbb;padding:12px 0 48px">'
            f'Page {cur_page} of {total_pages} &nbsp;·&nbsp; {len(filtered)} products</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown('<div style="padding-bottom:48px"></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCT DETAIL
# ═══════════════════════════════════════════════════════════════════════════
def page_detail():
    nav_buttons()
    p = st.session_state.selected_product
    if not p:
        st.session_state.page = "catalog"; st.rerun(); return

    st.markdown("<div style='padding: 12px 50px 0'>", unsafe_allow_html=True)
    if st.button("← Back to Catalog", key="det_back"):
        st.session_state.page = "catalog"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='padding:0 50px'>", unsafe_allow_html=True)
    col_img, col_info = st.columns([1.1, 1])

    with col_img:
        st.markdown(f"""
        <div style="border-radius:16px;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,.1)">
            <img src="{p['img']}" style="width:100%;height:580px;object-fit:cover;display:block">
        </div>""", unsafe_allow_html=True)

    with col_info:
        st.markdown(f"""
        <div style="padding:20px 0">
            <div style="font-size:13px;color:#888;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px">{p['brand']} — {p['category']}</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:64px;line-height:.9;margin-bottom:16px">{p['name']}</div>
            <div style="font-family:'Bebas Neue',sans-serif;font-size:40px;color:#da2a2b;margin-bottom:12px">{fmt(p['price'])}</div>
            <div style="font-size:14px;color:#555;line-height:1.7;margin-bottom:24px">{p['desc']}</div>
        </div>""", unsafe_allow_html=True)

        sz_key = f"size_{p['id']}"
        cl_key = f"color_{p['id']}"
        qty_key = f"qty_{p['id']}"

        chosen_size = st.selectbox("Select Size", p["sizes"], key=sz_key)
        chosen_color = st.selectbox("Select Color", p["colors"], key=cl_key)
        qty = st.number_input("Quantity", min_value=1, max_value=10, value=1, key=qty_key)

        st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1:
            if st.button("ADD TO CART", key=f"atc_{p['id']}", use_container_width=True):
                if not st.session_state.logged_in:
                    st.warning("Please login to add items to cart.")
                else:
                    st.session_state.cart.append({
                        "product": p, "size": chosen_size,
                        "color": chosen_color, "qty": qty,
                        "id": f"{p['id']}-{chosen_size}-{chosen_color}"
                    })
                    st.success(f"Added {p['name']} — Size {chosen_size} to your cart.")
        with a2:
            if st.button("BUY NOW", key=f"bn_{p['id']}", use_container_width=True):
                if not st.session_state.logged_in:
                    st.warning("Please login first.")
                else:
                    st.session_state.cart = [{"product": p, "size": chosen_size, "color": chosen_color, "qty": qty, "id": f"{p['id']}-{chosen_size}-{chosen_color}"}]
                    st.session_state.page = "cart"; st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Related products
    st.markdown("""<div style="padding:60px 50px 0">
        <div style="font-family:'Bebas Neue',sans-serif;font-size:42px;margin-bottom:20px">YOU MAY ALSO LIKE</div>
    </div>""", unsafe_allow_html=True)
    related = [x for x in PRODUCTS if x["id"] != p["id"]][:3]
    rcols = st.columns(3)
    for i, rp in enumerate(related):
        with rcols[i]:
            st.markdown(f"""
            <div class="product-card" style="margin:4px">
                <img src="{rp['img']}" style="width:100%;height:200px;object-fit:cover">
                <div class="card-body">
                    <div class="card-brand">{rp['brand']}</div>
                    <div class="card-name">{rp['name']}</div>
                    <div class="card-price">{fmt(rp['price'])}</div>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button("View", key=f"rel_{rp['id']}", use_container_width=True):
                st.session_state.selected_product = rp
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CART
# ═══════════════════════════════════════════════════════════════════════════
def page_cart():
    st.markdown("""
    <style>
    .block-container { padding-left: 4rem !important; padding-right: 4rem !important; }
    
    /* Cart numeric stepper aesthetics and alignment fix */
    .stNumberInput div[data-baseweb="input"] { 
        border: 1.5px solid #ddd !important; 
        border-radius: 8px !important; 
        background-color: transparent !important; 
    }
    .stNumberInput input {
        background-color: transparent !important;
        text-align: center !important;
    }
    .stNumberInput [data-testid^="stNumberInputStep"] {
        background-color: transparent !important; 
        color: #030303 !important;
        margin-left: 6px !important; /* Restore the physical spacing the global reset destroyed */
    }
    
    /* VERY Specific CSS to force outline border on streamit buttons inside Cart */
    div[data-testid="stButton"] button, 
    div[data-testid="stButton"] button[kind="secondary"],
    .stButton > button {
        border: 2px solid #030303 !important;
        border-radius: 30px !important;
        background-color: transparent !important;
        color: #030303 !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: none !important;
    }
    div[data-testid="stButton"] button:hover,
    .stButton > button:hover {
        background-color: #030303 !important;
        color: #ffffff !important;
        border-color: #030303 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    nav_buttons()
    st.markdown('<div style="margin-top:20px"></div>', unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.markdown('<div class="section-title" style="margin-bottom: 20px;"><em>your</em> cart</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="empty-state">
            <span class="material-symbols-outlined empty-icon">shopping_cart</span>
            <h3>YOUR CART IS EMPTY</h3>
            <p>Explore our catalog and find your perfect pair.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("← Continue Shopping", key="cart_empty_back"):
            st.session_state.page = "catalog"; st.rerun()
        return

    c_left, c_right = st.columns([1.8, 1])
    to_remove = None
    qty_changes = {}

    with c_left:
        # Move title INSIDE column so it naturally aligns beautifully with the left margin
        st.markdown('<div class="section-title" style="margin-bottom: 30px; line-height: 0.9;"><em>your</em> cart</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-label">
            <span class="material-symbols-outlined">inventory_2</span> Your Items
        </div>""", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        for idx, item in enumerate(st.session_state.cart):
            p = item["product"]
            ic1, ic2, ic3 = st.columns([0.8, 2, 0.7], gap="medium")
            with ic1:
                st.image(p["img"], width=130)
            with ic2:
                st.markdown(f"""
                <div style="padding:12px 0; border-bottom: 1px solid transparent;">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:32px;line-height:1">{p['name']}</div>
                    <div style="font-size:12px;color:#888;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px">{p['brand']}</div>
                    <div style="font-size:14px;color:#555;font-family:'Old Standard TT',serif;font-style:italic">Size: {item['size']} &nbsp;|&nbsp; Color: {item['color']}</div>
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:24px;color:#da2a2b;margin-top:14px">{fmt(p['price'])}</div>
                </div>""", unsafe_allow_html=True)
            with ic3:
                st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
                new_qty = st.number_input("Qty", min_value=1, max_value=10, value=item["qty"], key=f"cq_{idx}", label_visibility="collapsed")
                if new_qty != item["qty"]:
                    qty_changes[idx] = new_qty
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                if st.button("✕ Remove", key=f"rm_{idx}"):
                    to_remove = idx
            st.markdown("<div style='border-bottom:1px solid #f0f0f0; margin:16px 0 32px'></div>", unsafe_allow_html=True)

    for idx, nq in qty_changes.items():
        st.session_state.cart[idx]["qty"] = nq
    if to_remove is not None:
        st.session_state.cart.pop(to_remove); st.rerun()

    with c_right:
        subtotal = sum(item["product"]["price"] * item["qty"] for item in st.session_state.cart)
        shipping = 25000 if subtotal < 1000000 else 0
        total = subtotal + shipping

        free_ship_html = (
            '<div style="display:flex;align-items:center;gap:6px;font-size:12px;color:#27ae60;margin-top:8px">'
            '<span class="material-symbols-outlined" style="font-size:15px">check_circle</span> Free shipping applied!</div>'
            if shipping == 0 else
            '<div style="display:flex;align-items:center;gap:6px;font-size:12px;color:#aaa;margin-top:8px">'
            '<span class="material-symbols-outlined" style="font-size:15px">local_shipping</span> Free shipping on orders above Rp 1.000.000</div>'
        )
        st.markdown(f"""
        <div style="background:#f6f6f6;border-radius:16px;padding:28px">
            <div style="display:flex;align-items:center;gap:8px;font-family:'Bebas Neue',sans-serif;font-size:24px;margin-bottom:20px;letter-spacing:1px">
                <span class="material-symbols-outlined" style="font-size:22px;color:#da2a2b">receipt_long</span> ORDER SUMMARY
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;font-size:14px">
                <span style="color:#777">Subtotal</span><span><b>{fmt(subtotal)}</b></span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;font-size:14px">
                <span style="color:#777">Shipping</span><span>{'FREE' if shipping == 0 else fmt(shipping)}</span>
            </div>
            <hr style="border:none;border-top:1px solid #e0e0e0;margin:16px 0">
            <div style="display:flex;justify-content:space-between;font-family:'Bebas Neue',sans-serif;font-size:30px;color:#da2a2b">
                <span>TOTAL</span><span>{fmt(total)}</span>
            </div>
            {free_ship_html}
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("PROCEED TO CHECKOUT", key="go_checkout", use_container_width=True):
            if not st.session_state.logged_in:
                st.warning("Please login to checkout.")
                st.session_state.page = "login"; st.rerun()
            else:
                st.session_state.page = "checkout"; st.rerun()
        if st.button("← Continue Shopping", key="cart_back", use_container_width=True):
            st.session_state.page = "catalog"; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: CHECKOUT
# ═══════════════════════════════════════════════════════════════════════════
def page_checkout():
    st.markdown("""
    <style>
    .block-container { padding-left: 4rem !important; padding-right: 4rem !important; }
    /* Force form columns in checkout to align perfectly to the left and right */
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:first-child {
        padding-left: 0 !important;
    }
    div[data-testid="stForm"] div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:last-child {
        padding-right: 0 !important;
    }

    /* Override primary button color just for checkout form */
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
        background-color: #030303 !important;
        border-color: #030303 !important;
        color: #fff !important;
    }
    div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
        background-color: #333 !important;
        border-color: #333 !important;
        color: #fff !important;
    }
    div[data-testid="stForm"] button[kind="primaryFormSubmit"]:active {
        background-color: #000 !important;
        border-color: #000 !important;
        color: #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    nav_buttons()
    st.markdown('<div style="margin-top:20px"></div>', unsafe_allow_html=True)

    ch_left, ch_right = st.columns([1.4, 1])

    with ch_left:
        st.markdown('<div class="section-title" style="margin-bottom: 30px; line-height: 0.9;">CHECKOUT</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="section-label">
            <span class="material-symbols-outlined">local_shipping</span> Shipping Details
        </div>""", unsafe_allow_html=True)
        with st.container(border=True):
            with st.form("checkout_form", border=False):
                fn = st.text_input("Full Name", placeholder="John Doe")
                c_p, c_e = st.columns(2)
                with c_p: ph = st.text_input("Phone Number", placeholder="+62 812 3456 7890")
                with c_e: em = st.text_input("Email", value=st.session_state.user["name"]+"@ks.com" if st.session_state.logged_in else "")
                
                addr = st.text_area("Delivery Address", placeholder="Jl. Contoh No. 123, Jakarta", height=90)
                c1, c2 = st.columns(2)
                with c1: city = st.text_input("City", placeholder="Jakarta")
                with c2: postal = st.text_input("Postal Code", placeholder="10110")

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.markdown("""
                <div style="font-family:'Bebas Neue',sans-serif;font-size:18px;letter-spacing:1px;margin-bottom:8px;border-bottom:1px solid #f0f0f0;padding-bottom:8px">
                    <span class="material-symbols-outlined" style="font-size:16px">payment</span> Payment Method
                </div>""", unsafe_allow_html=True)
                payment = st.radio("", ["Bank Transfer", "GoPay / OVO", "Dana"], key="pay_method", label_visibility="collapsed", horizontal=True)

                if payment == "Bank Transfer":
                    st.info("Transfer to BCA 1234567890 a/n KlikSepatu — Upload proof after order.")
                elif payment == "GoPay / OVO":
                    st.info("Pay via GoPay/OVO to +62 811 0000 0001 — KlikSepatu")
                else:
                    st.info("Pay via Dana to +62 811 0000 0002 — KlikSepatu")

                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                st.markdown("""
                <div style="font-family:'Bebas Neue',sans-serif;font-size:18px;letter-spacing:1px;margin-bottom:8px;border-bottom:1px solid #f0f0f0;padding-bottom:8px">
                    <span class="material-symbols-outlined" style="font-size:16px">edit_note</span> Order Notes
                </div>""", unsafe_allow_html=True)
                notes = st.text_area("Additional notes (optional)", height=80, label_visibility="collapsed", placeholder="Special instructions, e.g. leave at door")

                st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
                submitted = st.form_submit_button("CONFIRM SECURE ORDER", use_container_width=True, type="primary")

        if submitted:
            if not fn or not addr or not city:
                st.error("Please fill in all required fields.")
            else:
                subtotal = sum(item["product"]["price"] * item["qty"] for item in st.session_state.cart)
                import random, string, datetime
                oid = "KS" + "".join(random.choices(string.digits, k=6))
                order = {
                    "id": oid, "items": list(st.session_state.cart),
                    "total": subtotal, "status": "Pending",
                    "name": fn, "address": f"{addr}, {city} {postal}",
                    "payment": payment, "notes": notes,
                    "date": datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
                }
                st.session_state.orders.append(order)
                st.session_state.cart = []
                st.session_state.page = "confirm"
                st.session_state.last_order = order
                st.rerun()

    with ch_right:
        subtotal = sum(item["product"]["price"] * item["qty"] for item in st.session_state.cart)
        shipping = 25000 if subtotal < 1000000 else 0
        total = subtotal + shipping

        st.markdown("""
        <div class="section-label">
            <span class="material-symbols-outlined">receipt_long</span> Order Summary
        </div>""", unsafe_allow_html=True)
        for item in st.session_state.cart:
            p = item["product"]
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:center;margin-bottom:12px;padding:12px;background:#f6f6f6;border-radius:10px">
                <img src="{p['img']}" style="width:64px;height:64px;object-fit:cover;border-radius:8px">
                <div style="flex:1">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:18px">{p['name']}</div>
                    <div style="font-size:12px;color:#888">Size {item['size']} · {item['color']} · Qty {item['qty']}</div>
                    <div style="font-family:'Bebas Neue',sans-serif;color:#da2a2b">{fmt(p['price'] * item['qty'])}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#fff;border:1px solid #eaeaea;border-radius:14px;padding:24px;margin-top:16px;box-shadow:0 4px 16px rgba(0,0,0,0.02)">
            <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:15px;color:#030303">
                <span style="color:#666">Subtotal</span><span style="font-weight:bold">{fmt(subtotal)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:12px;font-size:15px;color:#030303">
                <span style="color:#666">Shipping</span><span style="font-weight:bold">{'FREE' if shipping == 0 else fmt(shipping)}</span>
            </div>
            <hr style="border:none;border-top:1px solid #f0f0f0;margin:16px 0">
            <div style="display:flex;justify-content:space-between;align-items:center;font-family:'Bebas Neue',sans-serif;font-size:32px;color:#da2a2b;line-height:1;margin-top:8px">
                <span>TOTAL</span><span>{fmt(total)}</span>
            </div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: ORDER CONFIRMATION
# ═══════════════════════════════════════════════════════════════════════════
def page_confirm():
    nav_buttons()
    order = st.session_state.get("last_order", {})
    st.markdown(f"""
    <div style="max-width:580px;margin:60px auto;text-align:center;padding:0 20px">
        <div style="width:80px;height:80px;border-radius:50%;background:#030303;display:flex;align-items:center;justify-content:center;margin:0 auto 24px">
            <span class="material-symbols-outlined" style="font-size:40px;color:#fff">check</span>
        </div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:56px;line-height:1;margin-bottom:8px;letter-spacing:2px">ORDER PLACED!</div>
        <div style="color:#aaa;font-size:14px;margin-bottom:6px">Thank you for your order. Your order ID is:</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:32px;color:#da2a2b;margin-bottom:28px">{order.get('id','—')}</div>
        <div style="background:#f6f6f6;border-radius:14px;padding:24px;text-align:left;font-size:14px;line-height:2.2">
            <div style="display:flex;gap:8px"><span class="material-symbols-outlined" style="font-size:16px;color:#999;margin-top:4px">person</span><span><b>Name:</b> {order.get('name','—')}</span></div>
            <div style="display:flex;gap:8px"><span class="material-symbols-outlined" style="font-size:16px;color:#999;margin-top:4px">location_on</span><span><b>Address:</b> {order.get('address','—')}</span></div>
            <div style="display:flex;gap:8px"><span class="material-symbols-outlined" style="font-size:16px;color:#999;margin-top:4px">payment</span><span><b>Payment:</b> {order.get('payment','—')}</span></div>
            <div style="display:flex;gap:8px"><span class="material-symbols-outlined" style="font-size:16px;color:#999;margin-top:4px">schedule</span><span><b>Date:</b> {order.get('date','—')}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    _, c2, c3, _ = st.columns([2,1,1,2])
    with c2:
        if st.button("TRACK ORDER", key="conf_track", use_container_width=True):
            st.session_state.page = "track"; st.rerun()
    with c3:
        if st.button("KEEP SHOPPING", key="conf_shop", use_container_width=True):
            st.session_state.page = "catalog"; st.rerun()

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: ORDER TRACKING
# ═══════════════════════════════════════════════════════════════════════════
def page_track():
    st.markdown("<style>.block-container { padding-left: 4rem !important; padding-right: 4rem !important; }</style>", unsafe_allow_html=True)
    nav_buttons()
    st.markdown('<div style="margin-top:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title"><em>track</em> orders</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.warning("Please login to view your orders.")
        if st.button("Login", key="track_login"):
            st.session_state.page = "login"; st.rerun()
        return

    if not st.session_state.orders:
        st.markdown("""
        <div class="empty-state">
            <span class="material-symbols-outlined empty-icon">inventory_2</span>
            <h3>NO ORDERS YET</h3>
            <p>Place your first order and track it right here.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Start Shopping", key="track_empty"):
            st.session_state.page = "catalog"; st.rerun()
        return

    STEPS = ["Pending", "Packed", "Shipped", "Delivered"]
    STATUS_BADGE = {"Pending":"badge-pending","Packed":"badge-packed","Shipped":"badge-shipped","Delivered":"badge-delivered"}

    for order in reversed(st.session_state.orders):
        cur_idx = STEPS.index(order["status"]) if order["status"] in STEPS else 0
        badge_cls = STATUS_BADGE.get(order["status"], "badge-pending")

        with st.container(border=True):
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:12px;border-bottom:1px solid #f0f0f0;margin-bottom:20px;padding-top:8px">
                <div>
                    <span style="font-family:'Bebas Neue',sans-serif;font-size:28px;letter-spacing:1px;color:#030303">ORDER #{order['id']}</span>
                    <span style="font-size:14px;color:#888;margin-left:14px;font-style:italic;font-family:'Old Standard TT',serif">{order['date']}</span>
                </div>
                <div style="display:flex;align-items:center;gap:16px">
                    <span class="badge {badge_cls}">{order['status'].upper()}</span>
                    <span style="font-family:'Bebas Neue',sans-serif;color:#da2a2b;font-size:26px">{fmt(order['total'])}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            tl_col, info_col = st.columns([1, 1.5])
            STEP_ICONS = {"Pending": "schedule", "Packed": "inventory_2", "Shipped": "local_shipping", "Delivered": "check_circle"}
            with tl_col:
                tl_html = """<div style="padding-left: 48px; padding-top: 12px;">"""
                tl_html += """
                <div class="section-label">
                    <span class="material-symbols-outlined">route</span> Tracking Timeline
                </div>"""
                for si, step in enumerate(STEPS):
                    if si < cur_idx: icon_cls = "done"; line_cls = "done"; label_color = "#030303"; sub_text = "Completed"
                    elif si == cur_idx: icon_cls = "active"; line_cls = "idle"; label_color = "#da2a2b"; sub_text = "Current Status"
                    else: icon_cls = "idle"; line_cls = "idle"; label_color = "#bbb"; sub_text = "Upcoming"

                    tl_html += f"""
<div class="track-step">
  <div>
    <div class="track-icon {icon_cls}">
      <span class="material-symbols-outlined">{STEP_ICONS[step]}</span>
    </div>
    {'<div class="track-line ' + line_cls + '"></div>' if si < len(STEPS)-1 else ''}
  </div>
  <div style="padding-top:4px">
    <div class="track-label" style="color:{label_color}">{step}</div>
    <div class="track-sub">{sub_text}</div>
  </div>
</div>
"""
                tl_html += "</div>"
                st.markdown(tl_html, unsafe_allow_html=True)

            with info_col:
                st.markdown("""
                <div style="font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:1px;margin-bottom:12px;color:#030303">
                    ITEMS ORDERED
                </div>""", unsafe_allow_html=True)
                for item in order["items"]:
                    p = item["product"]
                    st.markdown(f"""
                    <div style="display:flex;gap:16px;align-items:center;margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #f6f6f6">
                        <img src="{p['img']}" style="width:60px;height:60px;border-radius:6px;object-fit:cover;border:1px solid #eee">
                        <div>
                            <div style="font-family:'Bebas Neue',sans-serif;font-size:18px;letter-spacing:0.5px">{p['name']}</div>
                            <div style="font-size:13px;color:#666;font-family:'Old Standard TT',serif;font-style:italic">Size {item['size']}  |  {item['color']}  |  Qty {item['qty']}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                st.markdown(f"""
                <div style="border:1px solid #eaeaea;background:#fafafa;border-radius:12px;padding:24px;font-size:14px;color:#333;margin-top:24px;margin-bottom:24px">
                    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
                        <div><div style="font-family:'Bebas Neue';color:#888;letter-spacing:1px;font-size:16px">Order Number</div><div style="font-family:'Bebas Neue';font-size:20px">{order['id']}</div></div>
                        <div><div style="font-family:'Bebas Neue';color:#888;letter-spacing:1px;font-size:16px">Status</div><div><span class="badge {badge_cls}">{order['status']}</span></div></div>
                        <div style="grid-column:1 / span 2;border-top:1px solid #ebebeb;padding-top:12px;margin-top:8px">
                            <div style="font-family:'Bebas Neue';color:#888;letter-spacing:1px;font-size:16px">Shipping Address</div>
                            <div style="line-height:1.5">{order['address']}</div>
                        </div>
                        <div style="grid-column:1 / span 2;border-top:1px solid #ebebeb;padding-top:12px;margin-top:4px">
                            <div style="font-family:'Bebas Neue';color:#888;letter-spacing:1px;font-size:16px">Payment Structure</div>
                            <div>{order['payment']} — {sum(i['qty'] for i in order['items'])} Item(s)</div>
                        </div>
                        <div style="grid-column:1 / span 2;border-top:1px solid #ebebeb;padding-top:16px;margin-top:8px;display:flex;justify-content:space-between;align-items:center">
                            <div style="font-family:'Bebas Neue';font-size:24px;letter-spacing:1px">TOTAL AMOUNT</div>
                            <div style="font-family:'Bebas Neue';font-size:28px;color:#da2a2b">{fmt(order['total'])}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# PAGE: ADMIN DASHBOARD / SETTINGS
# ═══════════════════════════════════════════════════════════════════════════
def admin_sidebar():
    st.markdown("""
    <style>
    header { visibility: visible !important; background: transparent !important; }
    /* Hide the native Streamlit page navigation */
    [data-testid="stSidebarNav"] { display: none !important; }
    
    /* Let Streamlit handle width so collapse works, but apply our styling */
    [data-testid="stSidebar"] {
        background-color: #030303 !important;
        border-right: 1px solid #111 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: transparent !important;
    }

    /* Style the Sidebar Buttons */
    [data-testid="stSidebar"] .stButton button {
        width: 100% !important; border: none !important;
        background: transparent !important; color: #fff !important;
        text-align: left !important; justify-content: flex-start !important;
        padding: 12px 24px !important; margin: 0 0 4px 0 !important;
        transition: all .2s ease !important; border-radius: 8px !important;
    }
    
    /* Force specific font on the text inside the button */
    [data-testid="stSidebar"] .stButton button p {
        font-family: 'Bebas Neue', sans-serif !important; 
        font-size: 22px !important; letter-spacing: 2px !important;
        color: #ddd !important; margin: 0 !important;
        display: flex !important; align-items: center !important;
    }

    /* Hover effect */
    [data-testid="stSidebar"] .stButton button:hover {
        background: #111 !important;
    }
    
    /* Active color on text (optional) */
    [data-testid="stSidebar"] .stButton button:hover p {
        color: #fff !important;
    }

    /* Assign Material Icons to Buttons logically by index */
    /* 1: DASHBOARD */
    [data-testid="stSidebar"] .stButton:nth-of-type(1) button p::before { content: "space_dashboard"; font-family: 'Material Symbols Outlined'; font-size: 22px; margin-right: 14px; color: #da2a2b; transition: all .2s; }
    /* 2: PRODUCTS */
    [data-testid="stSidebar"] .stButton:nth-of-type(2) button p::before { content: "style"; font-family: 'Material Symbols Outlined'; font-size: 22px; margin-right: 14px; color: #da2a2b; transition: all .2s; }
    /* 3: INVENTORY */
    [data-testid="stSidebar"] .stButton:nth-of-type(3) button p::before { content: "inventory_2"; font-family: 'Material Symbols Outlined'; font-size: 22px; margin-right: 14px; color: #da2a2b; transition: all .2s; }
    /* 4: ORDERS */
    [data-testid="stSidebar"] .stButton:nth-of-type(4) button p::before { content: "receipt_long"; font-family: 'Material Symbols Outlined'; font-size: 22px; margin-right: 14px; color: #da2a2b; transition: all .2s; }
    /* 5: REPORTS */
    [data-testid="stSidebar"] .stButton:nth-of-type(5) button p::before { content: "monitoring"; font-family: 'Material Symbols Outlined'; font-size: 22px; margin-right: 14px; color: #da2a2b; transition: all .2s; }
    /* 6: LOGOUT */
    [data-testid="stSidebar"] .stButton:nth-of-type(6) button p::before { content: "logout"; font-family: 'Material Symbols Outlined'; font-size: 22px; margin-right: 14px; color: #da2a2b; transition: all .2s; }

    /* Logo */
    .admin-logo {
        color: #fff; font-family: 'Bebas Neue', sans-serif; font-size: 42px;
        letter-spacing: 4px; padding: 10px 10px 24px; margin: 10px 14px 20px;
        border-bottom: 1px solid #1a1a1a; line-height: 1;
    }
    .admin-logo span { color: #da2a2b; font-size: 16px; letter-spacing: 2px; }

    /* Push admin content up and to the right */
    .block-container {
        margin-top: -15px !important;
        padding-left: 55px !important;
        padding-right: 35px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown('<div class="admin-logo">KLIK<br>SEPATU<br><span>ADMIN</span></div>', unsafe_allow_html=True)
        if st.button("DASHBOARD"): st.session_state.page = "admin_dashboard"; st.rerun()
        if st.button("PRODUCTS"): st.session_state.page = "admin_products"; st.rerun()
        if st.button("INVENTORY"): st.session_state.page = "admin_inventory"; st.rerun()
        if st.button("ORDERS"): st.session_state.page = "admin_orders"; st.rerun()
        if st.button("REPORTS"): st.session_state.page = "admin_reports"; st.rerun()
        
        st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)
        if st.button("LOGOUT"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.page = "home"
            st.rerun()

def get_total_sales():
    return sum(o["total"] for o in st.session_state.orders if o["status"] != "Pending")

def page_admin_dashboard():
    admin_sidebar()
    st.markdown("<div class='section-title'>Overview <em>Dashboard</em></div>", unsafe_allow_html=True)
    st.markdown("<div class=\"divider\"></div>", unsafe_allow_html=True)
    
    total_orders = len(st.session_state.orders)
    total_revenue = get_total_sales()
    total_items = sum(p["stock"] for p in st.session_state.products)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"""
    <div style="background:#fff;padding:30px;border-radius:16px;border:1px solid #eaeaea;box-shadow:0 4px 16px rgba(0,0,0,0.04);position:relative;overflow:hidden">
        <div style="position:absolute;top:-10px;right:-10px;opacity:0.03;font-size:120px"><span class="material-symbols-outlined">payments</span></div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
            <div style="width:40px;height:40px;background:#fef2f2;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#da2a2b">
                <span class="material-symbols-outlined" style="font-size:24px">account_balance_wallet</span>
            </div>
            <div style="font-size:14px;color:#666;font-family:'Bebas Neue',sans-serif;letter-spacing:2px">TOTAL REVENUE (CONFIRMED)</div>
        </div>
        <div style="font-size:48px;color:#030303;font-family:'Bebas Neue',sans-serif;line-height:1">{fmt(total_revenue)}</div>
    </div>
    """, unsafe_allow_html=True)
    c2.markdown(f"""
    <div style="background:#fff;padding:30px;border-radius:16px;border:1px solid #eaeaea;box-shadow:0 4px 16px rgba(0,0,0,0.04);position:relative;overflow:hidden">
        <div style="position:absolute;top:-10px;right:-10px;opacity:0.03;font-size:120px"><span class="material-symbols-outlined">shopping_bag</span></div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
            <div style="width:40px;height:40px;background:#f5f5f5;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#111">
                <span class="material-symbols-outlined" style="font-size:24px">local_shipping</span>
            </div>
            <div style="font-size:14px;color:#666;font-family:'Bebas Neue',sans-serif;letter-spacing:2px">TOTAL ORDERS</div>
        </div>
        <div style="font-size:48px;color:#030303;font-family:'Bebas Neue',sans-serif;line-height:1">{total_orders}</div>
    </div>
    """, unsafe_allow_html=True)
    c3.markdown(f"""
    <div style="background:#fff;padding:30px;border-radius:16px;border:1px solid #eaeaea;box-shadow:0 4px 16px rgba(0,0,0,0.04);position:relative;overflow:hidden">
        <div style="position:absolute;top:-10px;right:-10px;opacity:0.03;font-size:120px"><span class="material-symbols-outlined">inventory_2</span></div>
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px">
            <div style="width:40px;height:40px;background:#f5f5f5;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#111">
                <span class="material-symbols-outlined" style="font-size:24px">category</span>
            </div>
            <div style="font-size:14px;color:#666;font-family:'Bebas Neue',sans-serif;letter-spacing:2px">TOTAL STOCK (UNITS)</div>
        </div>
        <div style="font-size:48px;color:#030303;font-family:'Bebas Neue',sans-serif;line-height:1">{total_items}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-label'>Recent Orders</div>", unsafe_allow_html=True)
    
    if not st.session_state.orders:
        st.markdown("<div style='color:#888;font-style:italic'>No orders have been placed yet.</div>", unsafe_allow_html=True)
    else:
        for idx, o in enumerate(reversed(st.session_state.orders[-3:])):
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;background:#fff;padding:20px 24px;border:1px solid #eaeaea;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,0.02)">
                <div style="display:flex;align-items:center;gap:20px">
                    <div style="width:48px;height:48px;background:#f9f9f9;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#da2a2b">
                        <span class="material-symbols-outlined">receipt</span>
                    </div>
                    <div>
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:24px;letter-spacing:1px;color:#030303">ORDER #{o['id']}</div>
                        <div style="font-size:13px;color:#888">{o['name']} • {len(o['items'])} items • {o['date']}</div>
                    </div>
                </div>
                <div style="text-align:right">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:24px;color:#da2a2b">{fmt(o['total'])}</div>
                    <div style="font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px;display:inline-block;margin-top:4px;
                        background:{'#f0f0f0' if o['status']=='Pending' else '#e3f2fd' if o['status']=='Packed' else '#fff3e0' if o['status']=='Shipped' else '#e8f5e9'};
                        color:{'#555' if o['status']=='Pending' else '#1565c0' if o['status']=='Packed' else '#e65100' if o['status']=='Shipped' else '#2e7d32'};">
                        {o['status']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

def page_admin_products():
    admin_sidebar()
    st.markdown("<div class='section-title'>Product <em>Management</em></div>", unsafe_allow_html=True)
    st.markdown("<div class=\"divider\"></div>", unsafe_allow_html=True)
    
    with st.expander("➕ ADD NEW PRODUCT", expanded=False):
        with st.form("add_product_form"):
            r1, r2 = st.columns(2)
            n_name = r1.text_input("Product Name", "New Shoe")
            n_brand = r2.text_input("Brand", "Nike")
            n_price = r1.number_input("Price (Rp)", value=1500000, step=10000)
            n_cat = r2.selectbox("Category", ["Sneakers", "Running", "Formal", "Heels"])
            n_stock = r1.number_input("Initial Stock", value=50, step=1)
            n_img = r2.text_input("Image URL", "https://via.placeholder.com/400")
            n_desc = st.text_area("Description")
            submit_prod = st.form_submit_button("SAVE PRODUCT", use_container_width=True)
            if submit_prod:
                new_id = len(st.session_state.products) + 1
                st.session_state.products.append({
                    "id": new_id, "name": n_name, "brand": n_brand, "price": n_price,
                    "rating": 5.0, "stock": n_stock, "colors": ["Black"], "sizes": [40, 41, 42],
                    "desc": n_desc, "img": n_img, "category": n_cat
                })
                st.success("Product added successfully!")
                st.rerun()

    st.markdown("<br><div class='section-label'>Current Products</div>", unsafe_allow_html=True)

    if "edit_product_idx" not in st.session_state:
        st.session_state.edit_product_idx = None

    for idx, p in enumerate(st.session_state.products):
        with st.container(border=True):
            pc1, pc2, pc3 = st.columns([5, 2, 2.5])
            with pc1:
                st.markdown(f"""
                <div style="display:flex;gap:16px;align-items:center;padding:4px 0">
                    <img src="{p['img']}" style="width:70px;height:70px;object-fit:cover;border-radius:8px;border:1px solid #eee">
                    <div style="flex:1">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:26px;letter-spacing:1px;color:#030303;line-height:1">{p['name']}</div>
                        <div style="font-size:12px;color:#666;margin-top:6px;display:flex;align-items:center;gap:8px">
                            <span style="font-weight:600;color:#111;text-transform:uppercase;letter-spacing:1px">{p['brand']}</span>
                            <span style="background:#f5f5f5;padding:3px 10px;border-radius:20px;font-size:11px;color:#555">{p['category']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with pc2:
                st.markdown(f"<div style=\"font-family:'Bebas Neue',sans-serif;font-size:24px;color:#da2a2b;padding-top:16px\">{fmt(p['price'])}</div>", unsafe_allow_html=True)
            with pc3:
                st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("✎ EDIT", key=f"edit_{p['id']}", use_container_width=True):
                        st.session_state.edit_product_idx = idx
                with bc2:
                    if st.button("✕ DEL", key=f"del_{p['id']}", use_container_width=True):
                        st.session_state.products.pop(idx)
                        st.session_state.edit_product_idx = None
                        st.rerun()

        if st.session_state.edit_product_idx == idx:
            with st.container(border=True):
                st.markdown(f"<div style='font-family:Bebas Neue,sans-serif;font-size:20px;letter-spacing:1px;margin-bottom:8px'>EDITING: {p['name']}</div>", unsafe_allow_html=True)
                with st.form(f"edit_form_{p['id']}"):
                    er1, er2 = st.columns(2)
                    e_name  = er1.text_input("Product Name", value=p["name"])
                    e_brand = er2.text_input("Brand", value=p["brand"])
                    e_price = er1.number_input("Price (Rp)", value=p["price"], step=10000)
                    e_cat   = er2.selectbox("Category", ["Sneakers","Running","Formal","Heels"],
                                            index=["Sneakers","Running","Formal","Heels"].index(p["category"]) if p["category"] in ["Sneakers","Running","Formal","Heels"] else 0)
                    e_stock = er1.number_input("Stock (units)", value=p["stock"], step=1)
                    e_img   = er2.text_input("Image URL", value=p["img"])
                    e_desc  = st.text_area("Description", value=p["desc"])
                    save_col, cancel_col = st.columns(2)
                    saved = save_col.form_submit_button("SAVE CHANGES", use_container_width=True)
                    cancelled = cancel_col.form_submit_button("CANCEL", use_container_width=True)
                    if saved:
                        st.session_state.products[idx].update({
                            "name": e_name, "brand": e_brand, "price": e_price,
                            "category": e_cat, "stock": e_stock, "img": e_img, "desc": e_desc
                        })
                        st.session_state.edit_product_idx = None
                        st.success("Product updated!")
                        st.rerun()
                    if cancelled:
                        st.session_state.edit_product_idx = None
                        st.rerun()

        st.markdown("<div style='margin-bottom:12px'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def page_admin_inventory():
    admin_sidebar()
    st.markdown("<div class='section-title'>Inventory <em>Stock</em></div>", unsafe_allow_html=True)
    st.markdown("<div class=\"divider\"></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .inv-wrapper { border: 1px solid #eaeaea; border-radius: 12px; overflow: hidden; background: #fff; box-shadow: 0 2px 12px rgba(0,0,0,0.02); margin-bottom: 24px; }
    .inv-table { width: 100%; border-collapse: collapse; font-family: 'Old Standard TT', serif; }
    .inv-table th { text-align: left; padding: 16px 20px; background: #f9f9f9; font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; font-size:16px; color:#555; border-bottom: 1px solid #eaeaea; }
    .inv-table td { padding: 16px 20px; border-bottom: 1px solid #f2f2f2; font-size:15px; color:#111; vertical-align: middle; }
    .inv-table tr:hover td { background-color: #fafafa; }
    .inv-table tr:last-child td { border-bottom: none; }
    </style>
    """, unsafe_allow_html=True)
    
    html = "<div class='inv-wrapper'><table class='inv-table'><tr><th>ID</th><th>PRODUCT</th><th>BRAND</th><th>PRICE</th><th>STOCK</th><th>STATUS</th></tr>"
    for p in st.session_state.products:
        status_badge = "<span style='background:#e8f5e9;color:#2e7d32;padding:4px 10px;border-radius:20px;font-size:11px;font-family:sans-serif;font-weight:600;letter-spacing:0.5px;'>IN STOCK</span>" if p["stock"] > 10 else ("<span style='background:#fff3e0;color:#e65100;padding:4px 10px;border-radius:20px;font-size:11px;font-family:sans-serif;font-weight:600;letter-spacing:0.5px;'>LOW STOCK</span>" if p["stock"] > 0 else "<span style='background:#ffebee;color:#c62828;padding:4px 10px;border-radius:20px;font-size:11px;font-family:sans-serif;font-weight:600;letter-spacing:0.5px;'>OUT OF STOCK</span>")
        html += f"<tr><td style='color:#888'>#{p['id']}</td><td><div style='font-family:\"Bebas Neue\",sans-serif;font-size:22px;letter-spacing:1px;line-height:1'>{p['name']}</div></td><td>{p['brand']}</td><td><span style='color:#da2a2b;font-family:\"Bebas Neue\",sans-serif;font-size:20px'>{fmt(p['price'])}</span></td><td style='font-size:22px;font-family:\"Bebas Neue\",sans-serif;font-weight:bold'>{p['stock']}</td><td>{status_badge}</td></tr>"
    html += "</table></div>"
    st.markdown(html, unsafe_allow_html=True)

    st.markdown("<br><div class='section-label'>Quick Update Stock</div>", unsafe_allow_html=True)
    # Group inputs in columns of 2 to save space
    pairs = [st.session_state.products[i:i+2] for i in range(0, len(st.session_state.products), 2)]
    for pair in pairs:
        c1, c2 = st.columns(2, gap="large")
        for i, p in enumerate(pair):
            col = c1 if i == 0 else c2
            with col:
                with st.container(border=True):
                    sc1, sc2, sc3 = st.columns([12, 5, 4])
                    with sc1:
                        st.markdown(f"<div style='font-family:Bebas Neue,sans-serif;font-size:20px;letter-spacing:1px;padding-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis' title='{p['name']}'>{p['name']} <span style='color:#aaa;font-size:12px;font-family:Old Standard TT,serif'>({p['brand']})</span></div>", unsafe_allow_html=True)
                    with sc2:
                        new_stock = st.number_input("Stock", min_value=0, max_value=9999, value=p["stock"], key=f"inv_{p['id']}", label_visibility="collapsed")
                    with sc3:
                        if st.button("SET", key=f"upd_{p['id']}", use_container_width=True):
                            pidx = next(index for (index, d) in enumerate(st.session_state.products) if d["id"] == p["id"])
                            st.session_state.products[pidx]["stock"] = new_stock
                            st.success(f"Stock updated to {new_stock}!")
                            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

def page_admin_orders():
    admin_sidebar()
    st.markdown("<div class='section-title'>Order <em>Processing</em></div>", unsafe_allow_html=True)
    st.markdown("<div class=\"divider\"></div>", unsafe_allow_html=True)
    
    if not st.session_state.orders:
        st.markdown("<div class='empty-state'><span class='material-symbols-outlined empty-icon'>inventory_2</span><h3>NO ORDERS YET</h3><p>Waiting for customers to checkout.</p></div>", unsafe_allow_html=True)
    else:
        for idx, o in enumerate(reversed(st.session_state.orders)):
            real_idx = len(st.session_state.orders) - 1 - idx
            
            # Badge logic for expander header
            b_bg = "#f0f0f0" if o['status']=="Pending" else "#e3f2fd" if o['status']=="Packed" else "#fff3e0" if o['status']=="Shipped" else "#e8f5e9"
            b_co = "#555" if o['status']=="Pending" else "#1565c0" if o['status']=="Packed" else "#e65100" if o['status']=="Shipped" else "#2e7d32"
            
            # We can't inject HTML directly into expander titles in Streamlit easily, so we just use plain text for the title, 
            # but we can make the inside beautiful.
            o_title = f"{o['status'].upper()}  —  ORDER #{o['id']}  —  {fmt(o['total'])}"
            
            with st.expander(o_title, expanded=(idx==0)):
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #eee">
                    <div style="font-family:'Bebas Neue',sans-serif;font-size:28px;color:#030303">ORDER #{o['id']}</div>
                    <div style="background:{b_bg};color:{b_co};padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;letter-spacing:1px">{o['status'].upper()}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1.2], gap="large")
                with col1:
                    st.markdown(f"""
                    <div style="background:#fafafa;padding:16px;border-radius:8px;border:1px solid #eaeaea;margin-bottom:16px">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:20px;margin-bottom:8px">CUSTOMER DETAILS</div>
                        <div style="font-size:14px;color:#444;line-height:1.6">
                            <b>Name:</b> {o['name']}<br>
                            <b>Date:</b> {o['date']}<br>
                            <b>Address:</b> {o['address']}<br>
                            <b>Payment:</b> {o['payment']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<div style='font-family:\"Bebas Neue\",sans-serif;font-size:20px;margin-bottom:8px'>PURCHASED ITEMS</div>", unsafe_allow_html=True)
                    for item in o["items"]:
                        p = item["product"]
                        st.markdown(f"""
                        <div style="display:flex;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid #f0f0f0">
                            <img src="{p['img']}" style="width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid #eee">
                            <div style="flex:1">
                                <div style="font-family:'Bebas Neue',sans-serif;font-size:18px;line-height:1.2">{p['name']}</div>
                                <div style="font-size:12px;color:#888">Size {item['size']} | {item['color']}</div>
                            </div>
                            <div style="font-family:'Bebas Neue',sans-serif;font-size:18px;color:#da2a2b">x {item['qty']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div style="background:#fef2f2;padding:16px;border-radius:8px;border:1px solid #fcdada;margin-bottom:16px">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:20px;color:#da2a2b;margin-bottom:8px">UPDATE STATUS</div>
                    """, unsafe_allow_html=True)
                    status_opts = ["Pending", "Packed", "Shipped", "Delivered"]
                    cur_idx = status_opts.index(o["status"]) if o["status"] in status_opts else 0
                    with st.form(f"status_form_{o['id']}"):
                        new_status = st.selectbox("Select Status:", status_opts, index=cur_idx, label_visibility="collapsed")
                        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                        if st.form_submit_button("APPLY UPDATE", use_container_width=True):
                            st.session_state.orders[real_idx]["status"] = new_status
                            st.success(f"Order #{o['id']} updated to {new_status}!")
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def page_admin_reports():
    admin_sidebar()
    st.markdown("<div class='section-title'>Sales <em>Reports</em></div>", unsafe_allow_html=True)
    st.markdown("<div class=\"divider\"></div>", unsafe_allow_html=True)
    
    import pandas as pd
    import numpy as np

    # Generate dummy data for charts
    dates = pd.date_range(end=pd.Timestamp.today(), periods=7)
    revenue = np.array([2500000, 5000000, 1800000, 7500000, 4200000, 9800000, 12500000])
    df = pd.DataFrame({"Revenue (IDR)": revenue}, index=dates.strftime('%b %d'))
    
    cat_df = pd.DataFrame({
        "Sales": [45, 30, 15, 10]
    }, index=["Sneakers", "Running", "Formal", "Heels"])

    st.markdown(f"""
    <div style="background:#fff;padding:24px 30px;border-radius:12px;border:1px solid #eaeaea;box-shadow:0 4px 12px rgba(0,0,0,0.02);margin-bottom:32px">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
            <div style="width:44px;height:44px;background:#fef2f2;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#da2a2b">
                <span class="material-symbols-outlined">auto_graph</span>
            </div>
            <div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:24px;letter-spacing:1px;color:#030303;line-height:1">RECENT WEEKLY REVENUE</div>
                <div style="font-size:13px;color:#888;font-family:'Old Standard TT',serif;font-style:italic">Simulated 7-day trailing revenue data</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.bar_chart(df, height=320, color="#030303")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background:#fff;padding:24px 30px;border-radius:12px;border:1px solid #eaeaea;box-shadow:0 4px 12px rgba(0,0,0,0.02);margin-bottom:32px">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
            <div style="width:44px;height:44px;background:#fafafa;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#111">
                <span class="material-symbols-outlined">pie_chart</span>
            </div>
            <div>
                <div style="font-family:'Bebas Neue',sans-serif;font-size:24px;letter-spacing:1px;color:#030303;line-height:1">TOP SELLING CATEGORIES</div>
                <div style="font-size:13px;color:#888;font-family:'Old Standard TT',serif;font-style:italic">Distribution of units sold by product category</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.bar_chart(cat_df, height=280, color="#da2a2b")
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════
PAGE_MAP = {
    "home":     page_home,
    "login":    page_login,
    "catalog":  page_catalog,
    "detail":   page_detail,
    "cart":     page_cart,
    "checkout": page_checkout,
    "confirm":  page_confirm,
    "track":    page_track,
    "admin_dashboard": page_admin_dashboard,
    "admin_products":  page_admin_products,
    "admin_inventory": page_admin_inventory,
    "admin_orders":    page_admin_orders,
    "admin_reports":   page_admin_reports,
}

renderer = PAGE_MAP.get(st.session_state.page, page_home)
renderer()
