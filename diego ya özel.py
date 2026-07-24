import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import mouse
import time
import threading
import ctypes
import win32api
import win32con

class MakroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ALT Tuşu Makro")
        self.root.geometry("450x420")
        self.root.resizable(False, False)
        
        # Stil ayarları
        self.root.configure(bg='#2b2b2b')
        style = ttk.Style()
        style.theme_use('clam')
        
        # Değişkenler
        self.is_running = False
        self.stop_flag = False
        self.repeat_mode = tk.StringVar(value="1")
        
        # Ana frame
        main_frame = tk.Frame(root, bg='#2b2b2b')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Başlık
        title_label = tk.Label(
            main_frame, 
            text="ALT Tuşu Makro Kontrol Paneli",
            font=('Arial', 14, 'bold'),
            bg='#2b2b2b',
            fg='#ffffff'
        )
        title_label.pack(pady=(0, 20))
        
        # Koordinat bilgileri frame'i
        coord_frame = tk.Frame(main_frame, bg='#3c3c3c', relief='ridge', bd=2)
        coord_frame.pack(fill='x', pady=10)
        
        # Koordinat 1
        coord1_label = tk.Label(
            coord_frame,
            text="1. Tıklama: 1296, 849",
            font=('Arial', 10),
            bg='#3c3c3c',
            fg='#00ff00'
        )
        coord1_label.pack(pady=5)
        
        # Koordinat 2
        coord2_label = tk.Label(
            coord_frame,
            text="2. Tıklama: 1093, 531",
            font=('Arial', 10),
            bg='#3c3c3c',
            fg='#00ff00'
        )
        coord2_label.pack(pady=5)
        
        # Süre bilgisi
        sure_label = tk.Label(
            coord_frame,
            text="ALT tuşu basılı kalma süresi: 2 saniye",
            font=('Arial', 10),
            bg='#3c3c3c',
            fg='#00ff00'
        )
        sure_label.pack(pady=5)
        
        # Tekrar modu seçimi
        repeat_frame = tk.Frame(main_frame, bg='#3c3c3c', relief='ridge', bd=2)
        repeat_frame.pack(fill='x', pady=10)
        
        repeat_label = tk.Label(
            repeat_frame,
            text="Tekrar Modu:",
            font=('Arial', 11, 'bold'),
            bg='#3c3c3c',
            fg='#ffffff'
        )
        repeat_label.pack(pady=(10, 5))
        
        # Radio butonlar için frame
        radio_frame = tk.Frame(repeat_frame, bg='#3c3c3c')
        radio_frame.pack(pady=5)
        
        # Tek seferlik
        rb_single = tk.Radiobutton(
            radio_frame,
            text="Tek Sefer",
            variable=self.repeat_mode,
            value="1",
            bg='#3c3c3c',
            fg='#ffffff',
            selectcolor='#2b2b2b',
            font=('Arial', 10)
        )
        rb_single.pack(side='left', padx=10)
        
        # Sınırsız tekrar
        rb_infinite = tk.Radiobutton(
            radio_frame,
            text="Sınırsız (Ü tuşu ile durdur)",
            variable=self.repeat_mode,
            value="infinite",
            bg='#3c3c3c',
            fg='#ffffff',
            selectcolor='#2b2b2b',
            font=('Arial', 10)
        )
        rb_infinite.pack(side='left', padx=10)
        
        # Durum göstergesi
        self.status_label = tk.Label(
            main_frame,
            text="● Hazır",
            font=('Arial', 12, 'bold'),
            bg='#2b2b2b',
            fg='#00ff00'
        )
        self.status_label.pack(pady=10)
        
        # Sayaç label
        self.counter_label = tk.Label(
            main_frame,
            text="Tekrar: 0",
            font=('Arial', 10),
            bg='#2b2b2b',
            fg='#cccccc'
        )
        self.counter_label.pack(pady=5)
        
        # Tuş bilgileri frame'i
        key_frame = tk.Frame(main_frame, bg='#2b2b2b')
        key_frame.pack(pady=10)
        
        # Başlatma/Durdurma tuşu
        toggle_key_label = tk.Label(
            key_frame,
            text="Başlat/Durdur: Ü tuşu",
            font=('Arial', 10, 'bold'),
            bg='#2b2b2b',
            fg='#ffaa00'
        )
        toggle_key_label.pack(pady=3)
        
        # Durdurma tuşu
        stop_key_label = tk.Label(
            key_frame,
            text="Acil Durdurma: ESC tuşu",
            font=('Arial', 10),
            bg='#2b2b2b',
            fg='#ff4444'
        )
        stop_key_label.pack(pady=3)
        
        # Butonlar frame'i
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(pady=20)
        
        # Toggle butonu
        self.toggle_button = tk.Button(
            button_frame,
            text="Başlat (Ü)",
            command=self.toggle_makro,
            bg='#00aa00',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2,
            width=15,
            height=2
        )
        self.toggle_button.pack(side='left', padx=5)
        
        # Kapat butonu
        close_button = tk.Button(
            button_frame,
            text="Programı Kapat",
            command=self.quit_app,
            bg='#666666',
            fg='white',
            font=('Arial', 10),
            relief='raised',
            bd=2,
            width=15,
            height=2
        )
        close_button.pack(side='left', padx=5)
        
        # Footer
        footer_label = tk.Label(
            main_frame,
            text="Not: Program yönetici olarak çalıştırılmalıdır",
            font=('Arial', 8),
            bg='#2b2b2b',
            fg='#888888'
        )
        footer_label.pack(side='bottom', pady=10)
        
        # ESC tuşu dinleyicisi (acil durdurma)
        keyboard.add_hotkey('esc', self.emergency_stop)
        
        # 'ü' tuşu dinleyicisini başlat
        self.start_listener()
        
        self.tekrar_sayisi = 0
    
    def click_at(self, x, y):
        """Windows API kullanarak tıklama yap"""
        # Fareyi hareket ettir
        ctypes.windll.user32.SetCursorPos(x, y)
        time.sleep(0.05)
        
        # Sol tıklama yap (bas ve bırak)
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Sol bas
        time.sleep(0.02)
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Sol bırak
        time.sleep(0.05)
    
    def single_makro(self):
        """Tek bir makro döngüsü çalıştır"""
        try:
            # ALT tuşuna bas
            keyboard.press('alt')
            time.sleep(0.1)  # ALT tuşunun tam basıldığından emin ol
            
            # İlk koordinata tıkla (ALT basılıyken)
            self.click_at(1296, 849)
            time.sleep(0.2)
            
            # İkinci koordinata tıkla (ALT basılıyken)
            self.click_at(1093, 531)
            time.sleep(0.2)
            
            # 2 saniye dolana kadar bekle
            for i in range(15):  # 1.5 saniye bekle
                if self.stop_flag:
                    break
                time.sleep(0.1)
            
            # ALT tuşunu bırak
            keyboard.release('alt')
            time.sleep(0.1)
            
            return True
            
        except Exception as e:
            print(f"Hata: {e}")
            keyboard.release('alt')  # Hata durumunda ALT'ı bırak
            return False
    
    def makro_loop(self):
        """Makro döngüsü - tek veya sınırsız"""
        self.stop_flag = False
        self.tekrar_sayisi = 0
        
        while not self.stop_flag and self.is_running:
            self.tekrar_sayisi += 1
            self.root.after(0, self.update_counter)
            
            success = self.single_makro()
            
            if not success:
                break
            
            # Tek seferlik modda ise döngüden çık
            if self.repeat_mode.get() == "1":
                break
                
            time.sleep(0.3)  # Döngüler arası kısa bekleme
        
        # ALT tuşunun bırakıldığından emin ol
        keyboard.release('alt')
        self.is_running = False
        self.root.after(0, self.update_status_stopped)
    
    def toggle_makro(self):
        """Ü tuşu ile aç/kapat"""
        if self.is_running:
            self.stop_makro()
        else:
            self.start_makro()
    
    def start_makro(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.stop_flag = False
        self.tekrar_sayisi = 0
        
        self.status_label.config(text="● Çalışıyor...", fg='#ffaa00')
        self.toggle_button.config(text="Durdur (Ü)", bg='#ff4444')
        self.counter_label.config(text="Tekrar: 0")
        
        # Makroyu ayrı thread'de çalıştır
        thread = threading.Thread(target=self.makro_loop, daemon=True)
        thread.start()
    
    def stop_makro(self):
        if self.is_running:
            self.stop_flag = True
            self.is_running = False
            keyboard.release('alt')  # ALT tuşunu bırak
            self.root.after(0, self.update_status_stopped)
    
    def emergency_stop(self):
        """ESC tuşu ile acil durdurma"""
        print("ESC ile acil durdurma!")
        self.stop_makro()
    
    def update_status_stopped(self):
        self.status_label.config(text="● Hazır", fg='#00ff00')
        self.toggle_button.config(text="Başlat (Ü)", bg='#00aa00')
    
    def update_counter(self):
        self.counter_label.config(text=f"Tekrar: {self.tekrar_sayisi}")
    
    def start_listener(self):
        def on_u_press(event):
            # Ü tuşuna basıldığında toggle yap
            time.sleep(0.1)  # Tuş basımının tam algılanması için
            self.root.after(0, self.toggle_makro)
        
        keyboard.on_press_key('ü', on_u_press)
    
    def quit_app(self):
        self.stop_makro()
        keyboard.release('alt')
        time.sleep(0.2)
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    # Gerekli kütüphaneleri kontrol et
    try:
        import win32api
        import win32con
    except ImportError:
        print("pywin32 kütüphanesi yüklü değil. Yüklemek için: pip install pywin32")
        exit(1)
    
    root = tk.Tk()
    app = MakroApp(root)
    
    # Pencereyi ekranın ortasına konumlandır
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Pencere kapatıldığında
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    
    root.mainloop()
