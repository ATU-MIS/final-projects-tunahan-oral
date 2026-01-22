import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- DATABASE LAYER ---
# Veritabanı işlemlerini her seferinde tekrar yazmamak için bir fonksiyon haline getirdim.
# SQLite kullandım çünkü ekstra kurulum gerektirmiyor, projenin taşınabilir olmasını sağlıyor.
def init_db():
    conn = sqlite3.connect('proje_final.db')
    cursor = conn.cursor()
    # Eğer tablolar daha önce oluşturulmamışsa hata vermesin diye 'IF NOT EXISTS' kontrolü ekledim.
    cursor.execute('CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, name TEXT, target REAL, current REAL, deadline TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, amount REAL, category TEXT, date TEXT)')
    conn.commit()
    conn.close()

# --- VIRTUAL ADVISOR LOGIC ---
# Projenin UML şemasına uygun olması için 'Advisor' mantığını bir sınıf (Class) içinde topladım.
# Bu sayede OOP standartlarına uymuş oldum.
class Advisor:
    @staticmethod
    def calculate(target, current, deadline):
        try:
            # Hedef tarihe kaç gün kaldığını hesaplıyoruz.
            days = (datetime.strptime(deadline, "%Y-%m-%d").date() - datetime.now().date()).days
            # Sıfıra bölünme hatası almamak için minimum 1 ay olarak kabul ettim.
            months = max(1, days // 30)
            
            # Aylık ne kadar kenara atılması gerektiğini buluyoruz.
            needed = (target - current) / months
            return round(needed, 2), months
        except:
            # Herhangi bir tarih hatası olursa program çökmesin, varsayılan değer dönsün.
            return 0, 1

# --- UI APP ---
# Sayfa yapısını 'wide' seçtim çünkü grafikler geniş ekranda daha okunaklı duruyor.
st.set_page_config(page_title="FinTrack Pro Final", layout="wide")

# Veritabanını başlatıyoruz (Uygulama her açıldığında kontrol etsin).
init_db()

# Custom CSS
# Streamlit'in standart görünümü çok sadeydi. Metrik kutularını biraz daha şık göstermek için
# kendi yazdığım CSS kodunu buraya enjekte ettim. (Koyu tema uyumu için)
st.markdown("""<style> .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border-left: 5px solid #00d4ff; } </style>""", unsafe_allow_html=True)

# Navigation
# Kullanıcının sayfalar arasında kolay gezmesi için sol tarafa bir sidebar menüsü koydum.
menu = st.sidebar.radio("MENÜ", ["📊 Dashboard", "🎯 Hedef Planlayıcı", "💸 Harcamalar", "📋 Raporlar"])

# Ana veritabanı bağlantısını burada açıyorum.
conn = sqlite3.connect('proje_final.db')

if menu == "📊 Dashboard":
    st.title("📊 Finansal Özet")
    
    # Hedefleri veritabanından çekip genel durumu özetliyorum.
    df = pd.read_sql_query("SELECT * FROM goals", conn)
    
    if not df.empty:
        c1, c2 = st.columns(2)
        # Toplam tutarları anlık olarak gösteriyoruz.
        c1.metric("Toplam Hedef Tutar", f"{df['target'].sum():,.0f} ₺")
        c2.metric("Toplam Birikim", f"{df['current'].sum():,.0f} ₺")
        
        # Grafik kütüphanesi olarak Plotly'i tercih ettim çünkü interaktif (üzerine gelince detay gösteriyor).
        fig = px.bar(df, x='name', y=['target', 'current'], barmode='group', title="Hedef vs Birikim Durumu", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Henüz veri yok. Hedef Planlayıcı'dan başlayın.")

elif menu == "🎯 Hedef Planlayıcı":
    st.title("🎯 Yeni Finansal Hedef")
    
    # Veri girişlerini düzenli tutmak için form yapısı kullandım.
    with st.form("goal_form"):
        name = st.text_input("Hedef Adı (Örn: Yeni Araba)")
        target = st.number_input("Hedef Tutar (₺)", min_value=1.0)
        current = st.number_input("Mevcut Birikim (₺)", min_value=0.0)
        date = st.date_input("Hedef Tarihi")
        
        if st.form_submit_button("Analiz Et ve Kaydet"):
            # Advisor sınıfındaki statik metodu çağırarak hesaplama yapıyoruz (Code Reusability).
            needed, months = Advisor.calculate(target, current, str(date))
            
            # Sonuçları veritabanına işliyoruz.
            conn.execute("INSERT INTO goals (name, target, current, deadline) VALUES (?,?,?,?)", (name, target, current, str(date)))
            conn.commit()
            
            # Kullanıcıya anlık geri bildirim veriyoruz.
            st.success(f"Analiz Tamamlandı: Bu hedefe ulaşmak için ayda {needed} ₺ biriktirmelisiniz ({months} ay boyunca).")
            st.balloons() # Başarı hissi vermek için balon efekti :)

elif menu == "💸 Harcamalar":
    st.title("💸 Harcama Kaydı")
    
    with st.form("trans_form"):
        amt = st.number_input("Tutar (₺)")
        cat = st.selectbox("Kategori", ["Mutfak", "Kira", "Eğlence", "Ulaşım", "Diğer"])
        
        if st.form_submit_button("Kaydet"):
            # Tarihi otomatik olarak bugünün tarihi alıyoruz.
            conn.execute("INSERT INTO transactions (amount, category, date) VALUES (?,?,?)", (amt, cat, str(datetime.now().date())))
            conn.commit()
            st.success("Harcama kaydedildi.")
    
    # Son yapılan harcamaları tablo olarak gösteriyorum.
    df_t = pd.read_sql_query("SELECT * FROM transactions", conn)
    if not df_t.empty:
        st.table(df_t.tail(5))

elif menu == "📋 Raporlar":
    st.title("📋 Finansal Analiz Raporu")
    
    # Raporlar için tüm veriyi çekiyoruz.
    df_g = pd.read_sql_query("SELECT * FROM goals", conn)
    df_t = pd.read_sql_query("SELECT * FROM transactions", conn)
    
    col1, col2 = st.columns(2)
    with col1:
        if not df_g.empty:
            # Pasta grafiği (Pie Chart) dağılımı görmek için en iyi seçenekti.
            st.plotly_chart(px.pie(df_g, values='target', names='name', title="Hedef Dağılımı", hole=0.3))
    with col2:
        if not df_t.empty:
            st.plotly_chart(px.pie(df_t, values='amount', names='category', title="Harcama Dağılımı", hole=0.3))
    
    if not df_g.empty:
        st.subheader("Stratejik Durum Tablosu")
        # Pandas ile basit bir veri manipülasyonu yaparak tamamlanma yüzdesini hesapladım.
        df_g['Tamamlanma %'] = (df_g['current'] / df_g['target'] * 100).round(1)
        st.dataframe(df_g, use_container_width=True)
    
    # Financial Health Score Algoritması
    # Basit bir algoritma ile kullanıcının birikim/harcama dengesine göre 100 üzerinden puan veriyoruz.
    savings = df_g['current'].sum() if not df_g.empty else 0
    expenses = df_t['amount'].sum() if not df_t.empty else 1 # Sıfıra bölünme hatasını önlemek için 1 yaptım.
    score = min(100, int((savings / expenses) * 10))
    st.metric("Finansal Sağlık Skoru", f"{score}/100")