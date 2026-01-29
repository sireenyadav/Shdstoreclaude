import streamlit as st
import time

# ============================================================================
# 1. CONFIG & STATE MANAGEMENT
# ============================================================================
st.set_page_config(
    page_title="ShadeStore",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State
if 'bags' not in st.session_state:
    st.session_state.bags = 1
if 'show_booking' not in st.session_state:
    st.session_state.show_booking = False
if 'show_success' not in st.session_state:
    st.session_state.show_success = False

PRICE_PER_BAG = 99

# ============================================================================
# 2. BRUTAL CSS INJECTION (The "No Compromise" Visuals)
# ============================================================================
st.markdown("""
<style>
    /* GLOBAL DARK THEME & RESET */
    .stApp {
        background-color: #050505;
        color: white;
    }
    
    /* ANIMATIONS */
    @keyframes rotate {
        0% { transform: rotateX(0deg) rotateY(0deg); }
        100% { transform: rotateX(10deg) rotateY(360deg); }
    }
    
    @keyframes gradient-text {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.1); }
    }

    /* 3D SHIELD CONTAINER */
    .shield-container {
        perspective: 1000px;
        width: 200px;
        height: 200px;
        margin: 0 auto;
    }
    .shield-inner {
        width: 100%;
        height: 100%;
        position: relative;
        transform-style: preserve-3d;
        animation: rotate 8s infinite linear;
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.2), rgba(217, 70, 239, 0.2));
        border: 1px solid rgba(249, 115, 22, 0.3);
        border-radius: 20px;
        box-shadow: 0 0 60px rgba(251, 146, 60, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* TYPOGRAPHY */
    .hero-text {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        line-height: 1.2;
        margin-bottom: 20px;
    }
    .gradient-span {
        background: linear-gradient(to right, #fb923c, #e879f9, #fb923c);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        background-size: 200% auto;
        animation: gradient-text 3s linear infinite;
    }
    
    /* GLASS CARDS */
    .glass-card {
        background: rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(249, 115, 22, 0.2);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .glass-card:hover {
        border-color: rgba(249, 115, 22, 0.5);
        transform: translateY(-5px);
    }

    /* CUSTOM BUTTONS */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #f97316, #d946ef);
        border: none;
        color: white;
        font-weight: bold;
        padding: 0.75rem 1.5rem;
        border-radius: 9999px;
        box-shadow: 0 0 30px rgba(251, 146, 60, 0.4);
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        box-shadow: 0 0 50px rgba(251, 146, 60, 0.6);
        transform: scale(1.02);
        color: white;
    }
    
    /* MAP STYLING */
    .map-grid {
        position: relative;
        height: 300px;
        background: rgba(0,0,0,0.4);
        border: 1px solid rgba(249, 115, 22, 0.2);
        border-radius: 24px;
        overflow: hidden;
    }
    .map-line {
        position: absolute;
        background: rgba(249, 115, 22, 0.1);
    }
    .map-pin {
        position: absolute;
        color: #fb923c;
        animation: pulse-glow 2s infinite;
    }
    
    /* HIDE STREAMLIT UI BLOAT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 3. HELPER FUNCTIONS
# ============================================================================
def book_now_callback():
    st.session_state.show_booking = True

def close_booking_callback():
    st.session_state.show_booking = False

def confirm_booking_callback():
    st.session_state.show_booking = False
    st.session_state.show_success = True
    
def reset_app_callback():
    st.session_state.bags = 1
    st.session_state.show_success = False

# ============================================================================
# 4. MAIN UI LAYOUT
# ============================================================================

# --- HERO SECTION ---
if not st.session_state.show_success:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # 3D Shield Simulation using pure HTML/CSS
        st.markdown("""
            <div class="shield-container">
                <div class="shield-inner">
                    <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#fb923c" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                    </svg>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="hero-text">
                <span class="gradient-span">Store Bags.</span><br>
                <span style="color: white;">Own the City.</span>
            </div>
            <p style="text-align: center; color: #9ca3af; font-size: 1.1rem; margin-bottom: 2rem;">
                Premium luggage storage network across Gurugram. Drop your bags. Live your life.
            </p>
        """, unsafe_allow_html=True)

        if not st.session_state.show_booking:
            st.button("✨ Book Now", on_click=book_now_callback)

    st.markdown("---")

    # --- BOOKING DRAWER SIMULATION ---
    if st.session_state.show_booking:
        with st.container():
            st.markdown("""
                <div style="background: linear-gradient(to bottom, #18181b, #000); border-top: 1px solid rgba(249, 115, 22, 0.3); border-radius: 20px 20px 0 0; padding: 20px; margin-top: 20px;">
                    <h3 style="text-align: center; font-size: 1.5rem; margin-bottom: 1rem;">Book Storage</h3>
                </div>
            """, unsafe_allow_html=True)
            
            b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
            with b_col2:
                # Bag Counter
                c1, c2, c3 = st.columns([1, 1, 1])
                with c1:
                    if st.button("➖", key="minus"):
                        if st.session_state.bags > 1:
                            st.session_state.bags -= 1
                with c2:
                    st.markdown(f"<h1 style='text-align: center; margin: 0;'>{st.session_state.bags}</h1>", unsafe_allow_html=True)
                    st.caption("Bags")
                with c3:
                    if st.button("➕", key="plus"):
                        st.session_state.bags += 1
                
                total = st.session_state.bags * PRICE_PER_BAG
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 20px 0; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                        <span style="color: #9ca3af;">Total</span>
                        <span style="font-size: 1.5rem; font-weight: bold; background: linear-gradient(to right, #fb923c, #d946ef); -webkit-background-clip: text; color: transparent;">₹{total}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                conf_col1, conf_col2 = st.columns(2)
                with conf_col1:
                    st.button("Cancel", on_click=close_booking_callback) # Styling overridden by CSS, effectively acts as secondary
                with conf_col2:
                    st.button("Confirm Booking", on_click=confirm_booking_callback)

    # --- MAP SECTION ---
    st.markdown("<h2 style='text-align: center; margin-top: 40px;'>Secured <span class='gradient-span'>Safe Zones</span></h2>", unsafe_allow_html=True)
    
    # HTML Grid Map simulation
    st.markdown("""
        <div class="map-grid">
            <div style="width: 100%; height: 1px; background: rgba(249, 115, 22, 0.1); top: 20%; position: absolute;"></div>
            <div style="width: 100%; height: 1px; background: rgba(249, 115, 22, 0.1); top: 40%; position: absolute;"></div>
            <div style="width: 100%; height: 1px; background: rgba(249, 115, 22, 0.1); top: 60%; position: absolute;"></div>
            <div style="width: 100%; height: 1px; background: rgba(249, 115, 22, 0.1); top: 80%; position: absolute;"></div>
            
            <div style="height: 100%; width: 1px; background: rgba(249, 115, 22, 0.1); left: 20%; position: absolute;"></div>
            <div style="height: 100%; width: 1px; background: rgba(249, 115, 22, 0.1); left: 40%; position: absolute;"></div>
            <div style="height: 100%; width: 1px; background: rgba(249, 115, 22, 0.1); left: 60%; position: absolute;"></div>
            <div style="height: 100%; width: 1px; background: rgba(249, 115, 22, 0.1); left: 80%; position: absolute;"></div>

            <div class="map-pin" style="top: 30%; left: 25%;">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                <div style="font-size: 10px; color: #fdba74; text-align: center; margin-top: 5px;">Cyber Hub</div>
            </div>
            
            <div class="map-pin" style="top: 45%; left: 60%; animation-delay: 0.5s;">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                <div style="font-size: 10px; color: #fdba74; text-align: center; margin-top: 5px;">Golf Course</div>
            </div>

            <div class="map-pin" style="top: 65%; left: 40%; animation-delay: 1s;">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                <div style="font-size: 10px; color: #fdba74; text-align: center; margin-top: 5px;">Sohna Road</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # --- FEATURES GRID ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)

    with f_col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #fb923c;">🛡️ Insured</h3>
            <p style="font-weight: bold;">₹10,000 protection</p>
            <span style="font-size: 0.8rem; color: #9ca3af;">Full coverage per bag</span>
        </div>
        """, unsafe_allow_html=True)

    with f_col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #fb923c;">⚡ Instant</h3>
            <p style="font-weight: bold;">QR Check-in</p>
            <span style="font-size: 0.8rem; color: #9ca3af;">No waiting in lines</span>
        </div>
        """, unsafe_allow_html=True)

    with f_col3:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: #fb923c;">📍 24/7</h3>
            <p style="font-weight: bold;">Premium Locales</p>
            <span style="font-size: 0.8rem; color: #9ca3af;">Always accessible</span>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# 5. SUCCESS SCREEN (The "Modal")
# ============================================================================
else:
    st.balloons() # Native Streamlit confetti
    
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
            <div class="glass-card" style="max-width: 400px; border: 1px solid #22c55e;">
                <div style="font-size: 4rem; color: #22c55e; margin-bottom: 1rem;">✓</div>
                <h2 style="margin-bottom: 0.5rem;">Booking Confirmed!</h2>
                <p style="color: #9ca3af; margin-bottom: 2rem;">Your storage is secured</p>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 2rem; display: inline-block;">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=ShadeStoreBooking123" width="150" />
                </div>
                
                <p style="font-size: 0.8rem; color: #9ca3af; margin-bottom: 20px;">Show this QR code at the location</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("Done", on_click=reset_app_callback)

