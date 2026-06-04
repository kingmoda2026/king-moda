import streamlit as st
from supabase import create_client

# إعداد Supabase
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# إدارة الجلسة
if 'user' not in st.session_state:
    st.session_state.user = None
    st.session_state.is_admin = False

def main():
    st.title("🛍 نظام كينج موضة الاحترافي")

    # واجهة تسجيل الدخول
    if not st.session_state.user:
        choice = st.selectbox("اختر الإجراء", ["تسجيل دخول", "إنشاء حساب"])
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        
        if st.button("تنفيذ"):
            if choice == "تسجيل دخول":
                # تسجيل الدخول
                auth_res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = email
                # التحقق إذا كان أدمن (استبدل بالإيميل الخاص بك)
                if email == "admin@kingmoda.com": 
                    st.session_state.is_admin = True
                st.rerun()
            else:
                # إنشاء حساب
                supabase.auth.sign_up({"email": email, "password": password})
                st.success("تم إنشاء الحساب! سجل دخول الآن.")

    # بعد تسجيل الدخول
    else:
        st.sidebar.write(f"مرحباً: {st.session_state.user}")
        if st.sidebar.button("خروج"):
            st.session_state.user = None
            st.rerun()

        # لوحة تحكم الأدمن
        if st.session_state.is_admin:
            st.subheader("🛠 لوحة تحكم الأدمن")
            orders = supabase.table("orders").select("*").execute()
            st.table(orders.data)
        
        # واجهة المسوق
        else:
            st.subheader("🛍 تسجيل أوردر جديد")
            with st.form("order_form"):
                cust_name = st.text_input("اسم العميل")
                phone = st.text_input("رقم التليفون")
                addr = st.text_input("العنوان")
                model = st.text_input("اسم الموديل")
                if st.form_submit_button("تسجيل الأوردر"):
                    supabase.table("orders").insert({
                        "customer_name": cust_name,
                        "customer_phone": phone,
                        "customer_address": addr,
                        "model_name": model
                    }).execute()
                    st.success("تم تسجيل الأوردر بنجاح!")

if __name__ == "__main__":
    main()
