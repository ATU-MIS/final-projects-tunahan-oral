import sys
import os
import subprocess
import time
import threading
from streamlit.web import cli as stcli

# PyInstaller ile EXE yapıldığında dosya yolları karışabiliyor.
# Bu fonksiyon, dosyaların geçici (Temp) klasörde mi yoksa normal klasörde mi olduğunu çözüyor.
def resolve_path(path):
    try:
        # EXE çalışıyorsa dosyalar sys._MEIPASS içindedir.
        base_path = sys._MEIPASS
    except Exception:
        # Normal Python olarak çalışıyorsa mevcut dizini baz al.
        base_path = os.path.abspath(".")
    return os.path.join(base_path, path)

def run_browser_app():
    # Streamlit sunucusu (Localhost) hemen ayağa kalkmayabilir.
    # Bu yüzden tarayıcıyı açmadan önce 2 saniye bekletiyorum, yoksa "Sayfa bulunamadı" hatası alabiliriz.
    time.sleep(2)
    
    # Uygulamanın çalışacağı yerel adres
    url = "http://localhost:8501"
    
    # Kullanıcıya "Web Sitesi" değil "Masaüstü Uygulaması" hissi vermek için
    # Tarayıcıyı adres çubuğu olmayan "App Mode" (--app) ile başlatıyorum.
    try:
        # İlk tercihim Microsoft Edge çünkü Windows'ta varsayılan olarak var.
        subprocess.Popen(f'start msedge --app={url}', shell=True)
    except:
        # Edge yoksa Chrome deniyoruz.
        try:
            subprocess.Popen(f'start chrome --app={url}', shell=True)
        except:
            # Hiçbiri yoksa (Linux/Mac olabilir) varsayılan tarayıcıda açıyoruz.
            import webbrowser
            webbrowser.open(url)

if __name__ == "__main__":
    # Tarayıcıyı açacak fonksiyonu ayrı bir Thread (iş parçacığı) olarak başlatıyorum.
    # Böylece sunucu çalışırken (bloklanmadan) tarayıcı da açılabilir.
    threading.Thread(target=run_browser_app, daemon=True).start()
    
    # Ana dosyanın yolunu hatasız bulmak için resolve_path kullanıyorum.
    app_path = resolve_path("main.py")
    
    # Streamlit'i komut satırından çalıştırır gibi argümanlarla başlatıyoruz.
    # --server.headless=true : Sunucunun terminalden soru sormasını engeller.
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=false",
        "--server.headless=true", 
        "--server.port=8501",
        "--browser.gatherUsageStats=false"
    ]
    
    # Uygulamayı başlat
    sys.exit(stcli.main())