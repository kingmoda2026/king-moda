import streamlit as st
from supabase import create_client

# إعداد الاتصال بقاعدة البيانات
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.set_page_config(page_title="نظام كينج موضة", layout="centered")
st.title("🛍 نظام كينج موضة الاحترافي")

# إدارة الجلسة (Login Session)
if 'logged_in' not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    # واجهة دخول المسوق
    email = st.text_input("البريد الإلكتروني")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        # التحقق من بيانات المسوق
        user = supabase.table("marketers").select("*").eq("email", email).eq("password", password).execute()
        if user.data:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.rerun()
        else: st.error("بيانات غير صحيحة!")
else:
    # بعد الدخول: واجهة تسجيل الأوردرات وحساب العمولات
    st.success(f"مرحباً بك يا {st.session_state.user_email}")
    
    with st.form("order_form", clear_on_submit=True):
        # جلب الموديلات من جدول products
        products = supabase.table("products").select("name, commission").execute()
        prod_names = [p['name'] for p in products.data]
        selected_prod = st.selectbox("اختر الموديل", prod_names)
        
        name = st.text_input("اسم العميل")
        phone = st.text_input("رقم الهاتف")
        gov = st.text_input("المحافظة")
        
        if st.form_submit_button("إرسال الأوردر"):
            # سحب العمولة بناءً على الموديل
            prod_info = next(p for p in products.data if p['name'] == selected_prod)
            
            # تسجيل الأوردر
            supabase.table("orders").insert({
                "customer_name": name, 
                "phone": phone, 
                "gov": gov,
                "commission": prod_info.get('commission', 0)
            }).execute()
            st.success(f"تم تسجيل الأوردر! العمولة المحتسبة: {prod_info.get('commission', 0)}")

    if st.button("خروج"):
        st.session_state.logged_in = False
        st.rerun()
