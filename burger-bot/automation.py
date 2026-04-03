import os
import webbrowser
import screen_brightness_control as sbc
import pywhatkit
from AppOpener import open as open_app
import logging

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

logger = logging.getLogger(__name__)

def set_volume(level):
    """Set system master volume (0-100)."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        vol_level = max(0.0, min(100.0, float(level)))
        scalar = vol_level / 100.0
        volume.SetMasterVolumeLevelScalar(scalar, None)
        logger.info(f"Volume set to {vol_level}%")
        return True
    except Exception as e:
        logger.error(f"Failed to set volume: {e}")
        return False

def set_brightness(level):
    """Set system screen brightness (0-100)."""
    try:
        bright = max(0, min(100, int(level)))
        sbc.set_brightness(bright)
        logger.info(f"Brightness set to {bright}%")
        return True
    except Exception as e:
        logger.error(f"Failed to set brightness: {e}")
        return False

def open_anything(url_or_name):
    """Open a website or application. Falls back to web search if local app is not found."""
    try:
        from AppOpener import give_appnames, open as open_app
        name = url_or_name.lower().strip().replace("open", "").strip()
        
        # 1. Check known explicit web applications
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "instagram": "https://www.instagram.com",
            "facebook": "https://www.facebook.com",
            "whatsapp": "https://web.whatsapp.com",
            "twitter": "https://twitter.com",
            "x": "https://x.com",
            "gmail": "https://mail.google.com",
            "netflix": "https://www.netflix.com",
            "amazon": "https://www.amazon.com",
            "spotify": "https://open.spotify.com",
            "chatgpt": "https://chatgpt.com",
            "claude": "https://claude.ai",
            "maps": "https://maps.google.com"
        }
        
        for key, url in websites.items():
            if key == name or key in name.split():
                webbrowser.open(url)
                logger.info(f"Opened explicit website: {key}")
                return True
                
        # 2. Check if it's a domain literally (e.g., 'open github.com')
        if "." in name and " " not in name:
            webbrowser.open(f"https://{name}")
            return True
            
        # 3. Check Local Desktop Apps using AppOpener
        local_apps = give_appnames()
        app_found = False
        for app in local_apps:
            if name in app or app in name:
                app_found = True
                break
                
        if app_found:
            open_app(name, match_closest=True)
            logger.info(f"Opened local app remotely matching {name}")
            return True
            
        # 4. Universal Fallback: If it's not local and not defined, Google it!
        # This guarantees it opens WHATEVER you ask!
        webbrowser.open(f"https://www.google.com/search?q={name}")
        logger.info(f"Searched Google as fallback for: {name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to open {url_or_name}: {e}")
        return False


def play_music(song_name):
    """Play music on YouTube using pywhatkit."""
    try:
        pywhatkit.playonyt(song_name)
        return True
    except Exception as e:
        logger.error(f"Failed to play music: {e}")
        return False

def search_web(query):
    """Search Google."""
    try:
        pywhatkit.search(query)
        return True
    except Exception as e:
        logger.error(f"Failed to search: {e}")
        return False

# open_application removed, logic merged into open_anything
        
def perform_system_action(action):
    """Shutdown, restart, or sleep."""
    try:
        if action == "shutdown":
            os.system("shutdown /s /t 10")
            return "Shutting down the PC in 10 seconds."
        elif action == "restart":
            os.system("shutdown /r /t 10")
            return "Restarting the PC in 10 seconds."
        elif action == "sleep":
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "Going to sleep."
        elif action == "cancel_shutdown":
            os.system("shutdown /a")
            return "System power action aborted."
        return "Unknown system action."
    except Exception as e:
        logger.error(f"Failed system action {action}: {e}")
        return "Failed to perform system action."
