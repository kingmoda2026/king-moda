import streamlit as st
from supabase import create_client

# إعداد الاتصال
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("🛍 نظام كينج موضة الاحترافي")

# إدارة الجلسة
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.is_admin = False

# واجهة الدخول
if not st.session_state.user:
    tab1, tab2 = st.tabs(["دخول المسوقين", "إنشاء حساب جديد"])
    
    with tab1:
        email = st.text_input("البريد الإلكتروني للدخول")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            # البحث عن المستخدم في جدول profiles مباشرة
            user = supabase.table("profiles").select("*").eq("email", email).eq("password", password).execute()
            if user.data:
                st.session_state.user = email
                if email == "admin@kingmoda.com": # إيميلك كأدمن
                    st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة!")

    with tab2:
        new_email = st.text_input("البريد الإلكتروني الجديد")
        new_pass = st.text_input("كلمة مرور جديدة", type="password")
        if st.button("إنشاء حساب"):
            # إضافة المسوق للجدول مباشرة
            supabase.table("profiles").insert({
                "email": new_email,
                "password": new_pass,
                "role": "marketer"
            }).execute()
            st.success("تم إنشاء حسابك! يمكنك تسجيل الدخول الآن.")

# لوحة التحكم بعد الدخول
else:
    st.write(f"مرحباً بك: {st.session_state.user}")
    if st.button("خروج"):
        st.session_state.user = None
        st.rerun()
    
    # واجهة تسجيل الأوردرات
    st.subheader("🛍 تسجيل أوردر جديد")
    # (هنا تكمل كود تسجيل الأوردرات كما في السابق)
