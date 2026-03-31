import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="KlikSepatu",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    products = pd.read_csv("data/products_table.csv")
    users = pd.read_csv("data/users_table.csv")
    orders = pd.read_csv("data/orders_table.csv")
    order_items = pd.read_csv("data/order_items_table.csv")
    categories = pd.read_csv("data/categories_table.csv")
    return products, users, orders, order_items, categories

products_df, users_df, orders_df, order_items_df, categories_df = load_data()

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if 'admin_page' not in st.session_state:
    st.session_state.admin_page = 'dashboard'

# ============================================
# GLOBAL STYLES
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    
    .stApp {
        font-family: 'Montserrat', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Bebas Neue', sans-serif !important;
        letter-spacing: 2px;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Header */
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        padding: 15px 40px;
        background-color: #FFFFFF;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header-logo {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 32px;
        font-weight: bold;
        color: #030303;
        letter-spacing: 2px;
    }
    
    .header-menu {
        display: flex;
        gap: 30px;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 18px;
    }
    
    .header-menu span {
        cursor: pointer;
        padding: 5px 15px;
        transition: all 0.3s ease;
        border-radius: 20px;
    }
    
    .header-menu span:hover {
        background-color: #030303;
        color: white;
    }
    
    .header-actions {
        display: flex;
        gap: 15px;
        align-items: center;
    }
    
    .btn-primary {
        background-color: #030303;
        color: white;
        padding: 10px 25px;
        border-radius: 25px;
        border: none;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .btn-primary:hover {
        background-color: #da2a2b;
        transform: translateY(-2px);
    }
    
    .btn-outline {
        background-color: transparent;
        color: #030303;
        padding: 10px 25px;
        border-radius: 25px;
        border: 2px solid #030303;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 1px;
    }
    
    .btn-outline:hover {
        background-color: #030303;
        color: white;
    }
    
    .btn-danger {
        background-color: #da2a2b;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        border: none;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-danger:hover {
        background-color: #b81c1c;
    }
    
    /* Main Content Padding */
    .block-container {
        padding-top: 100px !important;
        max-width: 100% !important;
    }
    
    /* Product Card */
    .product-card {
        background: #f8f8f8;
        border-radius: 15px;
        overflow: hidden;
        transition: all 0.3s ease;
        cursor: pointer;
        height: 100%;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .product-image {
        width: 100%;
        height: 250px;
        object-fit: cover;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .product-info {
        padding: 20px;
    }
    
    .product-brand {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 24px;
        color: #030303;
        margin-bottom: 5px;
    }
    
    .product-name {
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
    }
    
    .product-price {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 20px;
        color: #da2a2b;
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #f5f5f5 0%, #e8e8e8 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    }
    
    .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 80px;
        line-height: 1;
        color: #030303;
        margin-bottom: 20px;
    }
    
    .hero-subtitle {
        font-family: 'Old Standard TT', serif;
        font-style: italic;
        font-size: 24px;
        color: #666;
    }
    
    /* Status Badges */
    .status-pending {
        background-color: #fef3cd;
        color: #856404;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-paid {
        background-color: #cce5ff;
        color: #004085;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-shipped {
        background-color: #d4edda;
        color: #155724;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-completed {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .status-cancelled {
        background-color: #f8d7da;
        color: #721c24;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .metric-value {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 36px;
        color: #030303;
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    
    /* Admin Sidebar */
    .admin-sidebar {
        background: #030303;
        padding: 30px 20px;
        border-radius: 15px;
        color: white;
        min-height: 80vh;
    }
    
    .admin-menu-item {
        padding: 15px 20px;
        margin: 5px 0;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 16px;
        letter-spacing: 1px;
    }
    
    .admin-menu-item:hover {
        background: rgba(255,255,255,0.1);
    }
    
    .admin-menu-item.active {
        background: #da2a2b;
    }
    
    /* Cart Item */
    .cart-item {
        display: flex;
        align-items: center;
        padding: 20px;
        background: #f8f8f8;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    
    .cart-item-image {
        width: 80px;
        height: 80px;
        border-radius: 10px;
        object-fit: cover;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin-right: 20px;
    }
    
    .cart-item-details {
        flex: 1;
    }
    
    /* Order Timeline */
    .timeline {
        position: relative;
        padding-left: 30px;
    }
    
    .timeline::before {
        content: '';
        position: absolute;
        left: 10px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: #e0e0e0;
    }
    
    .timeline-item {
        position: relative;
        padding-bottom: 30px;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -25px;
        top: 5px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #e0e0e0;
    }
    
    .timeline-item.active::before {
        background: #da2a2b;
    }
    
    .timeline-item.completed::before {
        background: #28a745;
    }
    
    /* Section Title */
    .section-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 48px;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .section-title-italic {
        font-family: 'Old Standard TT', serif;
        font-style: italic;
        font-weight: 400;
        font-size: 32px;
    }
    
    /* Login Card */
    .login-card {
        background: white;
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        max-width: 450px;
        margin: 0 auto;
    }
    
    .login-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 36px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Table Styles */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }
    
    .data-table th {
        background: #030303;
        color: white;
        padding: 15px;
        text-align: left;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 16px;
        letter-spacing: 1px;
    }
    
    .data-table td {
        padding: 15px;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .data-table tr:hover {
        background: #f8f8f8;
    }
    
    /* Filter Section */
    .filter-section {
        background: #f8f8f8;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    
    /* Low Stock Alert */
    .low-stock-alert {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px 20px;
        border-radius: 0 10px 10px 0;
        margin-bottom: 15px;
    }
    
    /* Checkout Form */
    .checkout-section {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    
    .checkout-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 24px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f0f0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HELPER FUNCTIONS
# ============================================
def format_currency(amount):
    return f"Rp {amount:,.0f}"

def get_status_badge(status):
    status_lower = status.lower()
    return f'<span class="status-{status_lower}">{status.upper()}</span>'

def get_product_image(product_id):
    images = [
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400",
        "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=400",
        "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400",
        "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400",
        "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400",
    ]
    return images[product_id % len(images)]

# ============================================
# LOGIN PAGE
# ============================================
def render_login_page():
    st.markdown("""
        <div style="text-align: center; padding: 40px 0;">
            <h1 style="font-family: 'Bebas Neue', sans-serif; font-size: 60px; margin-bottom: 10px;">KlikSepatu</h1>
            <p style="font-family: 'Old Standard TT', serif; font-style: italic; font-size: 20px; color: #666;">the Perfect Pair</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-title">LOGIN</h2>', unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        role = st.radio("Login as:", ["Customer", "Admin"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("LOGIN", use_container_width=True, type="primary"):
            # Simple authentication (in production, use proper authentication)
            user = users_df[users_df['username'] == username]
            
            if not user.empty:
                user_data = user.iloc[0]
                expected_role = 'admin' if role == 'Admin' else 'customer'
                
                if user_data['role'] == expected_role:
                    st.session_state.logged_in = True
                    st.session_state.user_role = expected_role
                    st.session_state.user_id = user_data['id']
                    st.session_state.username = username
                    st.session_state.current_page = 'home' if expected_role == 'customer' else 'admin_dashboard'
                    st.rerun()
                else:
                    st.error(f"This account is not registered as {role}")
            else:
                # Demo login - create session anyway for demo purposes
                st.session_state.logged_in = True
                st.session_state.user_role = 'admin' if role == 'Admin' else 'customer'
                st.session_state.user_id = 1
                st.session_state.username = username if username else 'demo_user'
                st.session_state.current_page = 'home' if role == 'Customer' else 'admin_dashboard'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div style="text-align: center; margin-top: 20px; color: #666;">
                <p>Demo credentials:</p>
                <p><strong>Customer:</strong> ddunn0 | <strong>Admin:</strong> lduigenan1</p>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# CUSTOMER HEADER
# ============================================
def render_customer_header():
    cart_count = len(st.session_state.cart)
    
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 1, 1, 2])
    
    with col1:
        st.markdown(f"<h2 style='font-family: Bebas Neue; margin: 0;'>KlikSepatu</h2>", unsafe_allow_html=True)
    
    with col2:
        if st.button("HOME", use_container_width=True):
            st.session_state.current_page = 'home'
            st.rerun()
    
    with col3:
        if st.button("SHOP", use_container_width=True):
            st.session_state.current_page = 'catalog'
            st.rerun()
    
    with col4:
        if st.button(f"CART ({cart_count})", use_container_width=True):
            st.session_state.current_page = 'cart'
            st.rerun()
    
    with col5:
        if st.button("ORDERS", use_container_width=True):
            st.session_state.current_page = 'orders'
            st.rerun()
    
    with col6:
        st.markdown(f"<p style='margin: 10px 0; text-align: center;'>Hi, {st.session_state.username}</p>", unsafe_allow_html=True)
    
    with col7:
        if st.button("LOGOUT", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.session_state.cart = []
            st.rerun()
    
    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

# ============================================
# CUSTOMER HOME PAGE
# ============================================
def render_customer_home():
    render_customer_header()
    
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <p class="hero-subtitle">the</p>
            <h1 class="hero-title">Perfect Pair</h1>
            <p class="hero-subtitle">Click. Choose. Use.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Featured Products
    st.markdown("""
        <div class="section-title">
            <span class="section-title-italic">our</span> BEST PRODUCTS
        </div>
    """, unsafe_allow_html=True)
    
    featured_products = products_df.head(8)
    
    cols = st.columns(4)
    for idx, (_, product) in enumerate(featured_products.iterrows()):
        with cols[idx % 4]:
            with st.container():
                st.image(get_product_image(product['id']), use_container_width=True)
                st.markdown(f"**{product['brand']}**")
                st.markdown(f"{product['product_name']}")
                st.markdown(f"<span style='color: #da2a2b; font-weight: bold;'>{format_currency(product['price'])}</span>", unsafe_allow_html=True)
                if st.button("View Details", key=f"view_{product['id']}", use_container_width=True):
                    st.session_state.selected_product = product['id']
                    st.session_state.current_page = 'product_detail'
                    st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Shop by Category
    st.markdown("""
        <div class="section-title">
            SHOP BY <span class="section-title-italic">category</span>
        </div>
    """, unsafe_allow_html=True)
    
    categories = categories_df['category_name'].unique()
    cat_cols = st.columns(len(categories))
    for idx, cat in enumerate(categories):
        with cat_cols[idx]:
            st.markdown(f"""
                <div style="background: #f8f8f8; padding: 30px; border-radius: 15px; text-align: center; cursor: pointer;">
                    <h3 style="font-family: 'Bebas Neue'; font-size: 24px;">{cat}</h3>
                </div>
            """, unsafe_allow_html=True)

# ============================================
# PRODUCT CATALOG PAGE
# ============================================
def render_catalog_page():
    render_customer_header()
    
    st.markdown("""
        <div class="section-title">
            PRODUCT <span class="section-title-italic">catalog</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Filters
    with st.container():
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            search = st.text_input("Search", placeholder="Search products...")
        
        with col2:
            brands = ['All'] + sorted(products_df['brand'].unique().tolist())
            selected_brand = st.selectbox("Brand", brands)
        
        with col3:
            sizes = ['All'] + sorted(products_df['size'].unique().tolist())
            selected_size = st.selectbox("Size", sizes)
        
        with col4:
            colors = ['All'] + sorted(products_df['color'].unique().tolist())
            selected_color = st.selectbox("Color", colors)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter products
    filtered_products = products_df.copy()
    
    if search:
        filtered_products = filtered_products[
            filtered_products['product_name'].str.contains(search, case=False, na=False) |
            filtered_products['brand'].str.contains(search, case=False, na=False)
        ]
    
    if selected_brand != 'All':
        filtered_products = filtered_products[filtered_products['brand'] == selected_brand]
    
    if selected_size != 'All':
        filtered_products = filtered_products[filtered_products['size'] == selected_size]
    
    if selected_color != 'All':
        filtered_products = filtered_products[filtered_products['color'] == selected_color]
    
    st.markdown(f"**Showing {len(filtered_products)} products**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Product Grid
    cols = st.columns(4)
    for idx, (_, product) in enumerate(filtered_products.iterrows()):
        with cols[idx % 4]:
            with st.container():
                st.image(get_product_image(product['id']), use_container_width=True)
                st.markdown(f"**{product['brand']}**")
                st.markdown(f"{product['product_name']} - Size {product['size']}")
                st.markdown(f"Color: {product['color']}")
                st.markdown(f"<span style='color: #da2a2b; font-weight: bold;'>{format_currency(product['price'])}</span>", unsafe_allow_html=True)
                
                if product['stock'] > 0:
                    st.markdown(f"<span style='color: green;'>In Stock ({product['stock']})</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='color: red;'>Out of Stock</span>", unsafe_allow_html=True)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("View", key=f"view_cat_{product['id']}", use_container_width=True):
                        st.session_state.selected_product = product['id']
                        st.session_state.current_page = 'product_detail'
                        st.rerun()
                with col_b:
                    if product['stock'] > 0:
                        if st.button("Add", key=f"add_cat_{product['id']}", use_container_width=True, type="primary"):
                            st.session_state.cart.append({
                                'product_id': product['id'],
                                'product_name': product['product_name'],
                                'brand': product['brand'],
                                'price': product['price'],
                                'size': product['size'],
                                'color': product['color'],
                                'quantity': 1
                            })
                            st.success("Added to cart!")
                            st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# PRODUCT DETAIL PAGE
# ============================================
def render_product_detail():
    render_customer_header()
    
    if st.session_state.selected_product is None:
        st.warning("No product selected")
        return
    
    product = products_df[products_df['id'] == st.session_state.selected_product].iloc[0]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.image(get_product_image(product['id']), use_container_width=True)
    
    with col2:
        st.markdown(f"<h1 style='font-family: Bebas Neue; font-size: 48px; margin-bottom: 5px;'>{product['brand']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='font-size: 24px; color: #666; margin-top: 0;'>{product['product_name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='color: #da2a2b; font-family: Bebas Neue; font-size: 36px;'>{format_currency(product['price'])}</h2>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"**Size:** {product['size']}")
        st.markdown(f"**Color:** {product['color']}")
        st.markdown(f"**Stock:** {product['stock']} available")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("**Description:**")
        st.markdown(product['description'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        quantity = st.number_input("Quantity", min_value=1, max_value=product['stock'], value=1)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("ADD TO CART", use_container_width=True, type="primary"):
                st.session_state.cart.append({
                    'product_id': product['id'],
                    'product_name': product['product_name'],
                    'brand': product['brand'],
                    'price': product['price'],
                    'size': product['size'],
                    'color': product['color'],
                    'quantity': quantity
                })
                st.success("Added to cart!")
        
        with col_b:
            if st.button("BACK TO CATALOG", use_container_width=True):
                st.session_state.current_page = 'catalog'
                st.rerun()

# ============================================
# SHOPPING CART PAGE
# ============================================
def render_cart_page():
    render_customer_header()
    
    st.markdown("""
        <div class="section-title">
            SHOPPING <span class="section-title-italic">cart</span>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Start shopping!")
        if st.button("Browse Products"):
            st.session_state.current_page = 'catalog'
            st.rerun()
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        total = 0
        items_to_remove = []
        
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([1, 2, 1, 1, 1])
                
                with c1:
                    st.image(get_product_image(item['product_id']), width=80)
                
                with c2:
                    st.markdown(f"**{item['brand']}**")
                    st.markdown(f"{item['product_name']}")
                    st.markdown(f"Size: {item['size']} | Color: {item['color']}")
                
                with c3:
                    new_qty = st.number_input("Qty", min_value=1, value=item['quantity'], key=f"qty_{idx}")
                    st.session_state.cart[idx]['quantity'] = new_qty
                
                with c4:
                    subtotal = item['price'] * item['quantity']
                    total += subtotal
                    st.markdown(f"**{format_currency(subtotal)}**")
                
                with c5:
                    if st.button("Remove", key=f"remove_{idx}"):
                        items_to_remove.append(idx)
                
                st.markdown("<hr>", unsafe_allow_html=True)
        
        # Remove items
        for idx in reversed(items_to_remove):
            st.session_state.cart.pop(idx)
            st.rerun()
    
    with col2:
        st.markdown("""
            <div class="checkout-section">
                <h3 class="checkout-title">ORDER SUMMARY</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**Subtotal:** {format_currency(total)}")
        st.markdown(f"**Shipping:** {format_currency(50000)}")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"### Total: {format_currency(total + 50000)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("PROCEED TO CHECKOUT", use_container_width=True, type="primary"):
            st.session_state.current_page = 'checkout'
            st.rerun()

# ============================================
# CHECKOUT PAGE
# ============================================
def render_checkout_page():
    render_customer_header()
    
    st.markdown("""
        <div class="section-title">
            <span class="section-title-italic">secure</span> CHECKOUT
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Shipping Details
        st.markdown("""
            <div class="checkout-section">
                <h3 class="checkout-title">SHIPPING DETAILS</h3>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            first_name = st.text_input("First Name")
        with c2:
            last_name = st.text_input("Last Name")
        
        address = st.text_input("Street Address")
        
        c3, c4, c5 = st.columns(3)
        with c3:
            city = st.text_input("City")
        with c4:
            province = st.text_input("Province")
        with c5:
            postal = st.text_input("Postal Code")
        
        phone = st.text_input("Phone Number")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Payment Method
        st.markdown("""
            <div class="checkout-section">
                <h3 class="checkout-title">PAYMENT METHOD</h3>
            </div>
        """, unsafe_allow_html=True)
        
        payment_method = st.radio(
            "Select payment method:",
            ["Bank Transfer (BCA/Mandiri/BNI)", "E-Wallet (GoPay/OVO/Dana)", "Credit Card"],
            horizontal=True
        )
        
        if payment_method == "Bank Transfer (BCA/Mandiri/BNI)":
            st.info("You will receive bank transfer details after confirming your order.")
        elif payment_method == "E-Wallet (GoPay/OVO/Dana)":
            st.info("You will be redirected to your e-wallet app after confirming your order.")
        else:
            st.text_input("Card Number", placeholder="1234 5678 9012 3456")
            c6, c7 = st.columns(2)
            with c6:
                st.text_input("Expiry Date", placeholder="MM/YY")
            with c7:
                st.text_input("CVV", placeholder="123")
    
    with col2:
        st.markdown("""
            <div class="checkout-section">
                <h3 class="checkout-title">ORDER SUMMARY</h3>
            </div>
        """, unsafe_allow_html=True)
        
        total = 0
        for item in st.session_state.cart:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            st.markdown(f"{item['brand']} {item['product_name']} x{item['quantity']}")
            st.markdown(f"**{format_currency(subtotal)}**")
            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        
        st.markdown(f"**Subtotal:** {format_currency(total)}")
        st.markdown(f"**Shipping:** {format_currency(50000)}")
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"### Total: {format_currency(total + 50000)}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("CONFIRM ORDER", use_container_width=True, type="primary"):
            st.session_state.cart = []
            st.success("Order placed successfully! Redirecting to order tracking...")
            st.session_state.current_page = 'orders'
            st.rerun()

# ============================================
# ORDER TRACKING PAGE (Customer)
# ============================================
def render_order_tracking():
    render_customer_header()
    
    st.markdown("""
        <div class="section-title">
            MY <span class="section-title-italic">orders</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Get user orders (demo - show some orders)
    user_orders = orders_df.head(10)
    
    for _, order in user_orders.iterrows():
        with st.expander(f"Order #{order['id']} - {order['created_at']} - {format_currency(order['total_price'])}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Order Items
                order_items = order_items_df[order_items_df['order_id'] == order['id']].head(3)
                
                st.markdown("**Order Items:**")
                for _, item in order_items.iterrows():
                    product = products_df[products_df['id'] == item['product_id']]
                    if not product.empty:
                        product = product.iloc[0]
                        st.markdown(f"- {product['brand']} {product['product_name']} x{item['quantity']} - {format_currency(item['subtotal'])}")
            
            with col2:
                st.markdown("**Order Status:**")
                st.markdown(get_status_badge(order['status']), unsafe_allow_html=True)
                
                # Order Timeline
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("**Tracking:**")
                
                statuses = ['pending', 'paid', 'shipped', 'completed']
                current_status = order['status'].lower()
                current_idx = statuses.index(current_status) if current_status in statuses else 0
                
                for idx, status in enumerate(statuses):
                    if idx < current_idx:
                        st.markdown(f"✅ {status.upper()}")
                    elif idx == current_idx:
                        st.markdown(f"🔵 {status.upper()} (Current)")
                    else:
                        st.markdown(f"⚪ {status.upper()}")

# ============================================
# ADMIN SIDEBAR
# ============================================
def render_admin_sidebar():
    with st.sidebar:
        st.markdown(f"<h2 style='font-family: Bebas Neue; color: white;'>KlikSepatu</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #888;'>Admin Dashboard</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #666;'>Welcome, {st.session_state.username}</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
        
        if st.button("Dashboard", use_container_width=True):
            st.session_state.admin_page = 'dashboard'
            st.rerun()
        
        if st.button("Products", use_container_width=True):
            st.session_state.admin_page = 'products'
            st.rerun()
        
        if st.button("Inventory", use_container_width=True):
            st.session_state.admin_page = 'inventory'
            st.rerun()
        
        if st.button("Orders", use_container_width=True):
            st.session_state.admin_page = 'orders'
            st.rerun()
        
        if st.button("Sales Reports", use_container_width=True):
            st.session_state.admin_page = 'reports'
            st.rerun()
        
        st.markdown("<hr style='border-color: #333;'>", unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True, type="secondary"):
            st.session_state.logged_in = False
            st.session_state.user_role = None
            st.rerun()

# ============================================
# ADMIN DASHBOARD
# ============================================
def render_admin_dashboard():
    st.markdown("""
        <div class="section-title">
            ADMIN <span class="section-title-italic">dashboard</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = orders_df['total_price'].sum()
    total_orders = len(orders_df)
    total_products = len(products_df)
    pending_orders = len(orders_df[orders_df['status'] == 'pending'])
    
    with col1:
        st.metric("Total Revenue", format_currency(total_revenue))
    
    with col2:
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col3:
        st.metric("Total Products", f"{total_products:,}")
    
    with col4:
        st.metric("Pending Orders", f"{pending_orders:,}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Revenue Trend")
        # Create sample daily revenue data
        dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
        revenue_data = pd.DataFrame({
            'date': dates,
            'revenue': [random.randint(10000000, 50000000) for _ in range(30)]
        })
        
        fig = px.line(revenue_data, x='date', y='revenue', title='Daily Revenue')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Orders by Status")
        status_counts = orders_df['status'].value_counts().reset_index()
        status_counts.columns = ['status', 'count']
        
        fig = px.pie(status_counts, values='count', names='status', title='Order Status Distribution')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Orders
    st.markdown("### Recent Orders")
    recent_orders = orders_df.head(10)
    
    for _, order in recent_orders.iterrows():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
        with col1:
            st.markdown(f"**#{order['id']}**")
        with col2:
            user = users_df[users_df['id'] == order['user_id']]
            username = user.iloc[0]['username'] if not user.empty else 'Unknown'
            st.markdown(username)
        with col3:
            st.markdown(format_currency(order['total_price']))
        with col4:
            st.markdown(get_status_badge(order['status']), unsafe_allow_html=True)
        with col5:
            st.markdown(order['created_at'])
        
        st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)

# ============================================
# ADMIN PRODUCTS PAGE
# ============================================
def render_admin_products():
    st.markdown("""
        <div class="section-title">
            PRODUCT <span class="section-title-italic">management</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Add Product Form
    with st.expander("Add New Product"):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Product Name")
            new_brand = st.selectbox("Brand", products_df['brand'].unique())
            new_price = st.number_input("Price", min_value=0)
        with col2:
            new_size = st.selectbox("Size", sorted(products_df['size'].unique()))
            new_color = st.selectbox("Color", products_df['color'].unique())
            new_stock = st.number_input("Stock", min_value=0)
        
        new_description = st.text_area("Description")
        
        if st.button("Add Product", type="primary"):
            st.success("Product added successfully!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Search and Filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("Search products", placeholder="Search by name or brand...")
    with col2:
        filter_brand = st.selectbox("Filter by Brand", ['All'] + list(products_df['brand'].unique()))
    
    # Products Table
    filtered_products = products_df.copy()
    
    if search:
        filtered_products = filtered_products[
            filtered_products['product_name'].str.contains(search, case=False, na=False) |
            filtered_products['brand'].str.contains(search, case=False, na=False)
        ]
    
    if filter_brand != 'All':
        filtered_products = filtered_products[filtered_products['brand'] == filter_brand]
    
    st.markdown(f"**Showing {len(filtered_products)} products**")
    
    # Display products in table format
    for _, product in filtered_products.head(20).iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 2, 1, 1, 2])
        
        with col1:
            st.markdown(f"**#{product['id']}**")
        with col2:
            st.markdown(f"**{product['brand']}**")
            st.markdown(f"{product['product_name']}")
        with col3:
            st.markdown(f"Size: {product['size']} | Color: {product['color']}")
        with col4:
            st.markdown(format_currency(product['price']))
        with col5:
            if product['stock'] < 20:
                st.markdown(f"<span style='color: red;'>{product['stock']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"{product['stock']}")
        with col6:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Edit", key=f"edit_{product['id']}"):
                    st.info(f"Editing product #{product['id']}")
            with c2:
                if st.button("Delete", key=f"delete_{product['id']}"):
                    st.warning(f"Delete product #{product['id']}?")
        
        st.markdown("<hr style='margin: 5px 0;'>", unsafe_allow_html=True)

# ============================================
# ADMIN INVENTORY PAGE
# ============================================
def render_admin_inventory():
    st.markdown("""
        <div class="section-title">
            INVENTORY <span class="section-title-italic">management</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Inventory Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_stock = products_df['stock'].sum()
    low_stock_count = len(products_df[products_df['stock'] < 20])
    out_of_stock = len(products_df[products_df['stock'] == 0])
    avg_stock = products_df['stock'].mean()
    
    with col1:
        st.metric("Total Stock", f"{total_stock:,}")
    with col2:
        st.metric("Low Stock Items", f"{low_stock_count:,}", delta="-5", delta_color="inverse")
    with col3:
        st.metric("Out of Stock", f"{out_of_stock:,}")
    with col4:
        st.metric("Avg Stock/Product", f"{avg_stock:.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Low Stock Alerts
    st.markdown("### Low Stock Alerts")
    low_stock_products = products_df[products_df['stock'] < 20].sort_values('stock')
    
    for _, product in low_stock_products.head(10).iterrows():
        st.markdown(f"""
            <div class="low-stock-alert">
                <strong>{product['brand']} {product['product_name']}</strong> - 
                Only <span style="color: red; font-weight: bold;">{product['stock']}</span> items left!
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Stock by Brand
    st.markdown("### Stock by Brand")
    stock_by_brand = products_df.groupby('brand')['stock'].sum().reset_index()
    stock_by_brand = stock_by_brand.sort_values('stock', ascending=True)
    
    fig = px.bar(stock_by_brand, x='stock', y='brand', orientation='h', title='Total Stock by Brand')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Update Stock
    st.markdown("### Update Stock")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_product = st.selectbox("Select Product", products_df['id'].tolist())
    with col2:
        stock_change = st.number_input("Stock Change (+/-)", value=0)
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Update Stock", type="primary"):
            st.success(f"Stock updated for product #{selected_product}")

# ============================================
# ADMIN ORDERS PAGE
# ============================================
def render_admin_orders():
    st.markdown("""
        <div class="section-title">
            ORDER <span class="section-title-italic">management</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox("Filter by Status", ['All', 'pending', 'paid', 'shipped', 'completed', 'cancelled'])
    with col2:
        date_from = st.date_input("From Date")
    with col3:
        date_to = st.date_input("To Date")
    
    # Filtered Orders
    filtered_orders = orders_df.copy()
    if status_filter != 'All':
        filtered_orders = filtered_orders[filtered_orders['status'] == status_filter]
    
    st.markdown(f"**Showing {len(filtered_orders)} orders**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Orders List
    for _, order in filtered_orders.head(20).iterrows():
        with st.expander(f"Order #{order['id']} - {order['created_at']} - {format_currency(order['total_price'])} - {order['status'].upper()}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Customer Info
                user = users_df[users_df['id'] == order['user_id']]
                if not user.empty:
                    st.markdown(f"**Customer:** {user.iloc[0]['username']}")
                    st.markdown(f"**Email:** {user.iloc[0]['email']}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Order Items
                st.markdown("**Order Items:**")
                order_items = order_items_df[order_items_df['order_id'] == order['id']]
                
                for _, item in order_items.head(5).iterrows():
                    product = products_df[products_df['id'] == item['product_id']]
                    if not product.empty:
                        product = product.iloc[0]
                        st.markdown(f"- {product['brand']} {product['product_name']} x{item['quantity']} - {format_currency(item['subtotal'])}")
            
            with col2:
                st.markdown("**Update Status:**")
                
                status_options = ['pending', 'paid', 'shipped', 'completed', 'cancelled']
                current_idx = status_options.index(order['status']) if order['status'] in status_options else 0
                
                new_status = st.selectbox(
                    "New Status",
                    status_options,
                    index=current_idx,
                    key=f"status_{order['id']}"
                )
                
                if st.button("Update Status", key=f"update_{order['id']}", type="primary"):
                    st.success(f"Order #{order['id']} status updated to {new_status}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"**Total:** {format_currency(order['total_price'])}")

# ============================================
# ADMIN SALES REPORTS
# ============================================
def render_admin_reports():
    st.markdown("""
        <div class="section-title">
            SALES <span class="section-title-italic">reports</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Report Period Selection
    col1, col2 = st.columns([1, 3])
    with col1:
        report_period = st.selectbox("Report Period", ["Daily", "Weekly", "Monthly"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Summary Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = orders_df['total_price'].sum()
    completed_orders = len(orders_df[orders_df['status'] == 'completed'])
    avg_order_value = total_revenue / len(orders_df) if len(orders_df) > 0 else 0
    
    with col1:
        st.metric("Total Revenue", format_currency(total_revenue))
    with col2:
        st.metric("Completed Orders", f"{completed_orders:,}")
    with col3:
        st.metric("Avg Order Value", format_currency(avg_order_value))
    with col4:
        st.metric("Conversion Rate", "3.2%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Revenue Chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Revenue Over Time")
        
        # Create sample data based on period
        if report_period == "Daily":
            dates = pd.date_range(start='2025-03-01', periods=30, freq='D')
        elif report_period == "Weekly":
            dates = pd.date_range(start='2025-01-01', periods=12, freq='W')
        else:
            dates = pd.date_range(start='2025-01-01', periods=12, freq='ME')
        
        revenue_data = pd.DataFrame({
            'date': dates,
            'revenue': [random.randint(50000000, 200000000) for _ in range(len(dates))]
        })
        
        fig = px.area(revenue_data, x='date', y='revenue', title=f'{report_period} Revenue')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        fig.update_traces(fill='tozeroy', line_color='#da2a2b')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Top Selling Brands")
        
        # Calculate sales by brand
        brand_sales = products_df.groupby('brand')['stock'].count().reset_index()
        brand_sales.columns = ['brand', 'products_sold']
        brand_sales = brand_sales.sort_values('products_sold', ascending=False).head(10)
        
        fig = px.bar(brand_sales, x='brand', y='products_sold', title='Sales by Brand')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        fig.update_traces(marker_color='#030303')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sales by Category
    st.markdown("### Sales by Category")
    
    # Merge with categories
    products_with_category = products_df.merge(categories_df, left_on='category_id', right_on='id', suffixes=('', '_cat'))
    category_sales = products_with_category.groupby('category_name').agg({
        'stock': 'sum',
        'price': 'mean'
    }).reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(category_sales, values='stock', names='category_name', title='Stock Distribution by Category')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(category_sales, x='category_name', y='price', title='Average Price by Category')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        fig.update_traces(marker_color='#da2a2b')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download Report
    st.markdown("### Export Report")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Download Sales Report (CSV)", use_container_width=True):
            st.info("Generating CSV report...")
    
    with col2:
        if st.button("Download Order Details (CSV)", use_container_width=True):
            st.info("Generating order details...")
    
    with col3:
        if st.button("Download Inventory Report (CSV)", use_container_width=True):
            st.info("Generating inventory report...")

# ============================================
# MAIN APP ROUTING
# ============================================
def main():
    if not st.session_state.logged_in:
        render_login_page()
    elif st.session_state.user_role == 'customer':
        # Customer Pages
        if st.session_state.current_page == 'home':
            render_customer_home()
        elif st.session_state.current_page == 'catalog':
            render_catalog_page()
        elif st.session_state.current_page == 'product_detail':
            render_product_detail()
        elif st.session_state.current_page == 'cart':
            render_cart_page()
        elif st.session_state.current_page == 'checkout':
            render_checkout_page()
        elif st.session_state.current_page == 'orders':
            render_order_tracking()
        else:
            render_customer_home()
    else:
        # Admin Pages
        render_admin_sidebar()
        
        if st.session_state.admin_page == 'dashboard':
            render_admin_dashboard()
        elif st.session_state.admin_page == 'products':
            render_admin_products()
        elif st.session_state.admin_page == 'inventory':
            render_admin_inventory()
        elif st.session_state.admin_page == 'orders':
            render_admin_orders()
        elif st.session_state.admin_page == 'reports':
            render_admin_reports()
        else:
            render_admin_dashboard()

if __name__ == "__main__":
    main()
