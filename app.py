import streamlit as st
from supabase import create_client

# إعداد الاتصال (تأكد من وجودهم في Secrets)
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.title("🛍 كينج موضة - تسجيل أوردر سريع")

# نموذج إدخال بيانات الأوردر (متطابق مع جدولك)
with st.form("order_form", clear_on_submit=True):
    customer_name = st.text_input("اسم العميل")
    phone = st.text_input("رقم الهاتف")
    gov = st.text_input("المحافظة")
    submit = st.form_submit_button("إرسال الأوردر")

    if submit:
        # الإضافة المباشرة للجدول بدون تعقيدات
        try:
            data = {
                "customer_name": customer_name,
                "phone": phone,
                "gov": gov
            }
            # هذا هو السطر "الذهبي" الذي سينجز المهمة
            supabase.table("orders").insert(data).execute()
            st.success("تم تسجيل الأوردر بنجاح! 🚀")
        except Exception as e:
            st.error(f"حدث خطأ أثناء الحفظ: {e}")
