import streamlit as st
from supabase import create_client
import os

# إعداد Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# نظام إدارة الجلسة (Session)
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    st.title("🚀 نظام كينج موضة الاحترافي")
    
    # واجهة تسجيل الدخول
    if not st.session_state.user:
        tab1, tab2 = st.tabs(["تسجيل دخول", "إنشاء حساب"])
        with tab1:
            email = st.text_input("البريد الإلكتروني")
            password = st.text_input("كلمة المرور", type="password")
            if st.button("دخول"):
                # هنا نضيف منطق التحقق من Supabase Auth
                st.success("تم الدخول بنجاح!")
                st.session_state.user = email
                st.rerun()
        return

    # واجهة التطبيق بعد الدخول
    st.sidebar.write(f"مرحباً: {st.session_state.user}")
    if st.sidebar.button("خروج"):
        st.session_state.user = None
        st.rerun()

    # لوحة تحكم الأدمن (تظهر فقط إذا كان الإيميل هو إيميلك)
    if st.session_state.user == "admin@kingmoda.com":
        st.subheader("🛠 لوحة تحكم الأدمن")
        # هنا ستظهر جداول الأوردرات وطلبات السحب
    else:
        st.subheader("🛍 تسجيل أوردر جديد")
        # هنا ستظهر خانات إدخال الأوردر (اسم العميل، العنوان، الخ...)
        
main()
