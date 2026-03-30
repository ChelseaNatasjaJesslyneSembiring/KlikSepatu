import streamlit as st

st.set_page_config(
    page_title="KlikSepatu | Home",
    page_icon="👟",
    layout="wide"
)

#D:\Tugas Kuliah\Semester 4\Workshop RPL\kliksepatu

st.markdown("""    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');        
        @import url('https://fonts.googleapis.com/css2?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&display=swap');
            
        a.st-emotion-cache-1f3w014, h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        padding: 15px 40px;
        width: 100%;
        background-color: #FFFFFF;
        color: #030303;
        padding: 10px;
        z-index: 9999;
        display: flex;
        align-items: center;
        font-family: 'Bebas Neue', sans-serif;
    }
            
    .header-logo {
        flex: 1;
        font-size: 45px;
        font-weight: bold;
        margin-left: 30px;
        letter-spacing: 1;
    }
            
    .header-menu {
        flex: 1;
        display: flex;
        justify-content: center;
        gap: 30px;
        font-weight: 400;
        font-size: 25px; 
    }
    
    .header-menu span {
        cursor: pointer;
        padding: 0px 20px;
        position: relative;
        transition: color 0.3s ease-in-out;
    }

    .header-menu span::after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 0%;
        height: 2px;
        background-color: #030303;
        transition: width 0.3s ease-in-out;
    }

    .header-menu span:hover::after {
        width: 100%;
    }
            
    .header-spacer {
        flex: 1;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
                
    .button {
        gap: 10px;
        display: flex;
        padding: 3px 20px;
        font-weight: 400;
        font-size: 25px;
        text-align: center;
        color: black;
        align-items: center;
        margin-right: 30px;
        background-color: transparent;
        border-radius: 30px;
        border-color: black;
        border-width: 1px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
            
    .button:hover {
        background-color: black;
        color: white;
    }
            
    .block-container {padding-top: 80px;}       
    header {visibility: hidden;}
    </style>

    <div class="sticky-header">
        <div class="header-logo"> KlikSepatu </div>
        <div class="header-menu">
            <span>SHOP</span>
            <span>BRANDS</span>
            <span>EDITORIAL</span>
        </div>
        <div class="header-spacer">
            <button class="button"> CART
                <span class="material-symbols-outlined"> shopping_cart </span>
            </button>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown ("""
    <style>
    .tagline h1 {
        margin-top: 30px;
        font-family: 'Bebas Neue', sans-serif;
        text-align: center;
        font-size: 150px;
        font-weight: 700;
        line-height: 100px;
    }
    </style>
    <div class="tagline">
        <h1> <span style="font-family: 'Old Standard TT', serif; font-style: italic; font-weight: 200; font-size: 80px;"> the </span> Perfect Pair <br> Click. Choose. Use. </h1>
    </div>
""", unsafe_allow_html=True)

st.markdown ("""
    <style>
    .block-container {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
        padding-top: 100px;
    }
             
    .img-container {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-top: 35px;
    }
             
    .img-container img {
        width: 100%;
        height: 900px;
        object-fit: cover;
        object-position: center;
    }
    </style>
    <div class="img-container"> <img src="app/static/home/foto_1.png"> </div>
""", unsafe_allow_html=True)

st.markdown ("""
    <style>
    .promo {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-top: 120px;
        margin-left: 50px;
    }
             
    .tagline h2 {
        font-family: 'Bebas Neue', sans-serif;
        text-align: start;
        font-size: 150px;
        font-weight: 700;
        line-height: 100px;
    }
    
    .button-b {
        display: flex;
        gap: 15px;
        padding: 10px 30px;
        margin-right: 50px;
        margin-bottom: 35px;
        font-weight: 400;
        font-size: 35px;
        text-align: center;
        color: #da2a2b;
        align-items: center;
        font-family: 'Bebas Neue', sans-serif;
        background-color: transparent;
        border-radius: 50px;
        border-color: black;
        border-width: 1px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .button-b:hover {
        background-color: #da2a2b;
        color: white;
    }
    </style>
    <div class="promo">
        <div class="tagline">
            <h2> <span style="font-family: 'Old Standard TT', serif; font-style: italic; font-weight: 200; font-size: 80px;"> our </span>
                best
                <span style="font-family: 'Old Standard TT', serif; font-style: italic; font-weight: 200; font-size: 80px;"> products </span>
            </h2>
        </div> 
        <div>
            <button class="button-b"> View All
                <span class="material-symbols-outlined" style="font-size: 35px;"> arrow_circle_right </span>
            </button>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown ("""
    <style>
    .bestpr {
        display: flex;
        justify-content: space-between;
        margin-bottom: 100px;
    }

    .card{
        flex: 0 0 350px;
        scroll-snap-align: start;
        width: 400px;
        height: 550px;
        background: #f6f6f6;
        margin: auto;
        position: relative;
        overflow: hidden;
        border-radius: 10px 10px 10px 10px;
        box-shadow: 0;
        cursor: pointer;
        transform: scale(0.95);
        transition: box-shadow 0.5s, transform 0.5s;
        &:hover{
            transform: scale(1);
            box-shadow: 5px 20px 30px rgba(0,0,0,0.2);
        }
  
        .container{
            width:100%;
            height:100%;
            line-height: 40px;
            .top{
                height: 80%;
                width:100%;
                background: no-repeat center center; 
                -webkit-background-size: 100%;
                -moz-background-size: 100%;
                -o-background-size: 100%;
                background-size: cover;
            }
            .brand-title {
                margin-top: 15px;
                margin-left: 15px;
                padding:0;
                font-size: 35px;
                font-family: 'Bebas Neue', sans-serif;
                letter-spacing: 2px;
            }
            .price-text {
                margin-left: 15px;
                padding:0;
                font-size: 26px;
                font-family: 'Bebas Neue', sans-serif;
            }
            .left{
                height:100%;
                width: 50%;
                background: #f6f6f6;
                position:relative;
                float:left;
            }
        }
  
        .inside{
            z-index:9;
            background: #92879B;
            width:140px;
            height:140px;
            position: absolute;
            top: -70px;
            right: -70px;
            border-radius: 0px 0px 200px 200px;
            transition: all 0.5s, border-radius 2s, top 1s;
            overflow: hidden;
        }
    }
             
    .marquee-wrapper {
        width: 100%;
        overflow: hidden;
        padding-bottom: 40px;
    }

    .marquee-track {
        display: flex;
        gap: 20px;
        width: max-content;
        animation: scroll-left 35s linear infinite;
    }

    .marquee-track:hover {
        animation-play-state: paused;
    }

    @keyframes scroll-left {
        0% { transform: translateX(0); }
        100% { transform: translateX(calc(-50% - 10px)); } 
    }   
    </style>
""", unsafe_allow_html=True)

def product_cards(name, price, url):
    return f"""<div class="card">
<div class="container">
    <div class="top" style="background-image: url('{url}');"></div>
        <div class="left">
            <div class="brand-title">{name}</div>
            <div class="price-text">{price}</div>
        </div>
    </div>
</div>"""

shoe_lists = [
    {"name": "Prada", "price": "$1250", "pict": "app/static/home/foto_4.jpg"},
    {"name": "Nodaleto", "price": "$895", "pict": "app/static/home/foto_5.jpeg"},
    {"name": "Gucci", "price": "$1285", "pict": "app/static/home/foto_6.jpg"},
    {"name": "Jimmy Choo", "price": "$1095", "pict": "app/static/home/foto_7.jpg"},
    {"name": "Louboutin", "price": "$1195", "pict": "app/static/home/foto_8.jpeg"},
    {"name": "Berluti", "price": "$3160", "pict": "app/static/home/foto_9.jpg"},
]

all_cards = ""
for shoe in shoe_lists:
    all_cards += product_cards(shoe["name"], shoe["price"], shoe["pict"])

infinite_cards = all_cards + all_cards

st.markdown(f"""<div class="bestpr">
    <div class="marquee-wrapper">
        <div class="marquee-track">
            {infinite_cards}
        </div>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown ("""
    <div class="img-container"> <img src="app/static/home/foto_2-fotor.png"> </div>
""", unsafe_allow_html=True)

st.markdown ("""
    <div class="promo">
        <div class="tagline">
            <h2> shoes
                <span style="font-family: 'Old Standard TT', serif; font-style: italic; font-weight: 200; font-size: 80px;"> types </span>
            </h2>
        </div> 
        <div>
            <button class="button-b"> View All
                <span class="material-symbols-outlined" style="font-size: 35px;"> arrow_circle_right </span>
            </button>
        </div>
    </div>
""", unsafe_allow_html=True)