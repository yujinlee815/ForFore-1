# run_app.py
import subprocess, sys, time, threading
import webview  # pywebview

PORT = "8501"

def start_streamlit():
    # --server.headless=true 로 콘솔만 띄우고, 브라우저 자동 오픈은 막음
    cmd = [sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
           "--server.headless=true", "--server.port", PORT]
    subprocess.Popen(cmd)

def open_window():
    # 스트림릿 서버가 뜨길 잠깐 기다렸다가 네이티브 창으로 열기
    time.sleep(2)
    webview.create_window("Chatbot", f"http://localhost:{PORT}", width=1100, height=800)
    webview.start()

if __name__ == "__main__":
    threading.Thread(target=start_streamlit, daemon=True).start()
    open_window()