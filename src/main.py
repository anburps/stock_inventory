import threading
import webview
import os
import sys
import time
from waitress import serve
from django.core.wsgi import get_wsgi_application

# --- Configure Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock.settings')  # change 'myapp' to your Django project name
application = get_wsgi_application()

def start_server():
    """Run the Django app silently using Waitress."""
    serve(application, host='127.0.0.1', port=8000)

if __name__ == "__main__":
    # Start Django server in the background
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Give the server a moment to start
    time.sleep(2)

    # Open the desktop window
    webview.create_window("Stock Inventory System", "http://127.0.0.1:8000", width=1200, height=800)
    webview.start()
