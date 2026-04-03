import customtkinter as ctk
import tkinter as tk
from config import Config
import logging

logger = logging.getLogger(__name__)

class AdminPanel(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("🍔 Burger Bot Settings")
        self.geometry("500x750")
        self.attributes("-topmost", True)
        
        # Load current profile
        self.profile = Config.get_user_profile()
        
        # UI Setup
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(self, text="⚙️ Personalization Dashboard", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=460, height=600)
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # --- User Info Section ---
        self.create_section_label(self.scrollable_frame, "IDENTIFICATION & CONTEXT", 0)
        
        self.user_name_entry = self.create_input_field(self.scrollable_frame, "Your Name", self.profile.get("user_name"), 1)
        self.hobbies_entry = self.create_input_field(self.scrollable_frame, "Interests / Hobbies", self.profile.get("hobbies"), 2, placeholder="Coding, Fitness, Pizza...")
        self.location_entry = self.create_input_field(self.scrollable_frame, "Current Location", self.profile.get("location", ""), 3, placeholder="City, Country")
        
        self.bio_label = ctk.CTkLabel(self.scrollable_frame, text="Professional Background", anchor="w")
        self.bio_label.grid(row=8, column=0, padx=10, pady=(10, 0), sticky="w")
        self.bio_text = tk.Text(self.scrollable_frame, height=3, bg="#2b2b2b", fg="#e0e0e0", font=("Arial", 12), insertbackground="white", bd=0)
        self.bio_text.insert("1.0", self.profile.get("professional_bio", ""))
        self.bio_text.grid(row=9, column=0, padx=10, pady=(0, 10), sticky="ew")

        # --- Assistant Persona ---
        self.create_section_label(self.scrollable_frame, "BURGER'S PERSONALITY", 10)
        
        self.assistant_name_entry = self.create_input_field(self.scrollable_frame, "Assistant Call-sign (Nickname)", self.profile.get("assistant_name"), 6)
        
        self.personality_label = ctk.CTkLabel(self.scrollable_frame, text="Desired Behavior / Vibe", anchor="w")
        self.personality_label.grid(row=13, column=0, padx=10, pady=(10, 0), sticky="w")
        self.personality_text = tk.Text(self.scrollable_frame, height=3, bg="#2b2b2b", fg="#e0e0e0", font=("Arial", 12), insertbackground="white", bd=0)
        self.personality_text.insert("1.0", self.profile.get("personality", "Professional and Helpful"))
        self.personality_text.grid(row=14, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        # --- Advanced Section ---
        self.create_section_label(self.scrollable_frame, "ENGINE CONFIGURATION", 15)
        self.api_key_entry = self.create_input_field(self.scrollable_frame, "Cohere API Authorization Key", self.profile.get("cohere_api_key", ""), 9, show="*")
        
        # Note on creator
        self.creator_label = ctk.CTkLabel(self.scrollable_frame, text="Developer: Kunal Chauhan", font=ctk.CTkFont(size=10, slant="italic"), text_color="#555555")
        self.creator_label.grid(row=18, column=0, pady=(20, 0))

        # --- Footer Buttons ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.save_button = ctk.CTkButton(self.button_frame, text="Apply Changes", command=self.save_settings, fg_color="#FF9800", text_color="black", font=ctk.CTkFont(weight="bold"))
        self.save_button.grid(row=0, column=0, padx=10, pady=0, sticky="ew")
        
        self.cancel_button = ctk.CTkButton(self.button_frame, text="Close", command=self.destroy, fg_color="#333333")
        self.cancel_button.grid(row=0, column=1, padx=10, pady=0, sticky="ew")

    def create_section_label(self, parent, text, row):
        label = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=12, weight="bold"), text_color="#777777")
        label.grid(row=row, column=0, padx=10, pady=(20, 5), sticky="w")
        
    def create_input_field(self, parent, label_text, default_value, row, show=None, placeholder=""):
        label = ctk.CTkLabel(parent, text=label_text, anchor="w")
        label.grid(row=row*2+1, column=0, padx=10, pady=(10, 0), sticky="w")
        entry = ctk.CTkEntry(parent, width=400, show=show, placeholder_text=placeholder)
        entry.insert(0, default_value if default_value else "")
        entry.grid(row=row*2+2, column=0, padx=10, pady=(0, 10), sticky="ew")
        return entry

    def save_settings(self):
        new_profile = {
            "user_name": self.user_name_entry.get(),
            "assistant_name": self.assistant_name_entry.get(),
            "creator_name": "Kunal Chauhan", # Locked
            "personality": self.personality_text.get("1.0", "end-1c"),
            "hobbies": self.hobbies_entry.get(),
            "location": self.location_entry.get(),
            "professional_bio": self.bio_text.get("1.0", "end-1c"),
            "language_preference": self.profile.get("language_preference", "Hinglish"),
            "cohere_api_key": self.api_key_entry.get()
        }
        
        if Config.save_user_profile(new_profile):
            logger.info("AdminPanel: Professional settings saved.")
            self.save_button.configure(text="Changes Applied ✅")
            self.after(1500, self.destroy)
        else:
            logger.error("AdminPanel: Failed to save profile.")
            tk.messagebox.showerror("Error", "Could not write to profile storage!")

if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw() # Hide the main root window
    panel = AdminPanel(app)
    app.mainloop()
