import tkinter as tk
import time
import math
import threading

class BurgerUI(tk.Tk):
    def __init__(self, start_voice_engine, command_handler_fn, open_settings_fn):
        super().__init__()
        self.title("BURGER")
        self.geometry("400x500")
        
        # Make transparent and borderless
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.wm_attributes("-transparentcolor", "#000000")
        self.configure(bg="#000000")
        
        # Center window loosely on desktop right edge
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        self.geometry(f"+{screen_w - 500}+{screen_h - 600}")

        self.canvas = tk.Canvas(self, width=400, height=450, bg="#000000", highlightthickness=0)
        self.canvas.pack()
        
        self.state = "IDLE"
        self.text_status = "Sleeping... (Say 'Burger')"
        self.t = 0
        self.mouth_open = False
        
        self.status_label = tk.Label(self, text=self.text_status, fg="#FF9800", bg="#111111", font=("Consolas", 12), wraplength=380)
        self.status_label.pack(fill="x", pady=10)
        
        # Draggable Support
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        
        # Context menu (right click)
        self.canvas.bind("<Button-3>", self.on_right_click)

        # Callbacks setup
        self.start_voice_engine = start_voice_engine
        self.command_handler_fn = command_handler_fn
        self.open_settings_fn = open_settings_fn
        
        # Context Menu object
        self.menu = tk.Menu(self, tearoff=0, bg="#212121", fg="white", activebackground="#FF9800", font=("Arial", 10))
        self.menu.add_command(label="⚙️ Settings", command=self.open_settings_fn)
        self.menu.add_separator()
        self.menu.add_command(label="❌ Exit", command=self.destroy)

        self.draw_burger()
        self.animate()
        
        # Start background threads 500ms after UI launch
        self.after(500, self.start_voice_engine)

    def on_drag_start(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag_motion(self, event):
        x = self.winfo_x() - self._drag_start_x + event.x
        y = self.winfo_y() - self._drag_start_y + event.y
        self.geometry(f"+{x}+{y}")
        
    def on_right_click(self, event):
        """Right click to show context menu."""
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def update_state(self, state, text):
        """Update character state and UI label. Called from any thread."""
        def _update():
            self.state = state
            self.text_status = text
            if state == "SPEAKING":
                color = "#00ff9d"
            elif state == "LISTENING":
                color = "#FFEB3B" 
            elif state == "THINKING":
                color = "#00d4ff"
            else:
                color = "#FF9800"
            self.status_label.config(text=f"[{state}] {text}", fg=color)
        
        # Ensure label update happens in main thread
        self.after(0, _update)

    def draw_burger(self):
        """Draw the animated character based on state and timer (t)."""
        self.canvas.delete("all")
        cx = 200
        cy = 250 + math.sin(self.t) * 12 # Hovering effect
        
        # Inner backdrop glow if listening
        if self.state == "LISTENING":
            glow_radius = 110 + math.sin(self.t * 8) * 15
            self.canvas.create_oval(cx - glow_radius, cy - glow_radius, cx + glow_radius, cy + glow_radius, fill="#4c2700", outline="")
            glow_radius2 = 90 + math.sin(self.t * 8) * 10
            self.canvas.create_oval(cx - glow_radius2, cy - glow_radius2, cx + glow_radius2, cy + glow_radius2, fill="#7a3f00", outline="")

        # Top Bun
        self.canvas.create_arc(cx - 80, cy - 80, cx + 80, cy, start=0, extent=180, fill="#E49B0F", outline="")
        # Lettuce
        self.canvas.create_polygon(cx-85, cy-5, cx-60, cy+5, cx-40, cy-5, cx-20, cy+5, cx, cy-5, cx+20, cy+5, cx+40, cy-5, cx+60, cy+5, cx+85, cy-5, cx+80, cy+15, cx-80, cy+15, fill="#4CAF50", outline="", smooth=True)
        # Tomato
        self.canvas.create_rectangle(cx-75, cy+5, cx+75, cy+15, fill="#F44336", outline="", width=0)
        # Cheese
        self.canvas.create_polygon(cx-80, cy+15, cx-60, cy+35, cx-40, cy+15, cx-20, cy+35, cx, cy+15, cx+20, cy+35, cx+40, cy+15, cx+60, cy+35, cx+80, cy+15, fill="#FFEB3B", outline="")
        # Patty
        self.canvas.create_rectangle(cx-85, cy+20, cx+85, cy+45, fill="#5D4037", outline="", width=0)
        # Bottom Bun
        self.canvas.create_arc(cx - 80, cy + 15, cx + 80, cy + 95, start=180, extent=180, fill="#E49B0F", outline="")
        
        # Eyes
        if self.state == "THINKING":
            r1, r2 = 3, 3 # Squinting up
            eyey = cy - 40
        else:
            # Blink animation
            if math.sin(self.t * 1.5) > 0.96:
                r1, r2 = 1, 1 
            else:
                r1, r2 = 5, 6
            eyey = cy - 35
            
        # Left eye
        self.canvas.create_oval(cx - 35, eyey - 10, cx - 15, eyey + 10, fill="white")
        self.canvas.create_oval(cx - 25 - r1, eyey - r2, cx - 25 + r1, eyey + r2, fill="black")
        
        # Right eye
        self.canvas.create_oval(cx + 15, eyey - 10, cx + 35, eyey + 10, fill="white")
        self.canvas.create_oval(cx + 25 - r1, eyey - r2, cx + 25 + r1, eyey + r2, fill="black")
        
        # Mouth
        mouth_y = cy - 10
        if self.state == "SPEAKING" and self.mouth_open:
            # Open mouth
            self.canvas.create_oval(cx - 15, mouth_y - 5, cx + 15, mouth_y + 15, fill="#3E2723")
        elif self.state == "SPEAKING":
            # Closed mouth / mid speech
            self.canvas.create_oval(cx - 10, mouth_y + 2, cx + 10, mouth_y + 8, fill="#3E2723")
        elif self.state == "LISTENING":
            # Smiling slightly
            self.canvas.create_arc(cx - 15, mouth_y-5, cx + 15, mouth_y + 10, start=180, extent=180, outline="#3E2723", width=3, style=tk.ARC)
        elif self.state == "THINKING":
            # Thoughtful mouth (straight line slightly off)
            self.canvas.create_line(cx - 8, mouth_y + 5, cx + 8, mouth_y + 2, fill="#3E2723", width=3)
        else:
            # Idle tiny smile
            self.canvas.create_arc(cx - 10, mouth_y, cx + 10, mouth_y + 10, start=180, extent=180, outline="#3E2723", width=2, style=tk.ARC)

        # Thinking Animation (spinning dots above head)
        if self.state == "THINKING":
            ang1 = self.t * 5
            ang2 = self.t * 5 + math.pi
            r_spin = 25
            lx1 = cx + math.cos(ang1) * r_spin
            ly1 = cy - 100 + math.sin(ang1) * r_spin
            lx2 = cx + math.cos(ang2) * r_spin
            ly2 = cy - 100 + math.sin(ang2) * r_spin
            
            # Center ball
            self.canvas.create_oval(cx-4, cy-104, cx+4, cy-96, fill="#FFEB3B")
            # Spinning orbits
            self.canvas.create_oval(lx1-4, ly1-4, lx1+4, ly1+4, fill="#00d4ff")
            self.canvas.create_oval(lx2-4, ly2-4, lx2+4, ly2+4, fill="#FF4081")

    def animate(self):
        """Animation loop that runs every 50ms in the Tkinter thread."""
        self.t += 0.1
        if self.state == "SPEAKING":
            # Quick toggle for mouth open/close to simulate speaking
            if (self.t * 10) % 3 < 1.5:
                self.mouth_open = True
            else:
                self.mouth_open = False
        else:
            self.mouth_open = False
            
        self.draw_burger()
        self.after(50, self.animate)
