import customtkinter as ctk
import pygame
import numpy as np
import math

# Initializing this Pygame mixer
pygame.mixer.init()

def generate_sound(frequency=440, duration_ms=100, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)
    tone = np.sin(frequency * 2 * np.pi * t) * 32767 * volume
    tone = tone.astype(np.int16)
    stereo_tone = np.column_stack((tone, tone))  # stereo
    return pygame.sndarray.make_sound(stereo_tone)

click_sound = generate_sound(600, 80)
equal_sound = generate_sound(900, 150)

# Setting initial appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class SKCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SK Calculator")
        self.geometry("380x640")
        self.resizable(False, False)

        # Display Entry
        self.display = ctk.CTkEntry(self, font=("Segoe UI", 26, "bold"),
                                    height=70, width=340, corner_radius=12,
                                    fg_color="#ffffff", text_color="#000000",
                                    justify='right')
        self.display.grid(row=0, column=0, columnspan=4, pady=(20, 10), padx=20)

        # Theme Toggle Switch
        self.theme_switch = ctk.CTkSwitch(self, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.grid(row=1, column=0, columnspan=4, pady=(0, 10))

        # Buttons
        buttons = [
            ("C", self.clear), ("(", lambda: self.append("(")), (")", lambda: self.append(")")), ("/", lambda: self.append("/")),
            ("sin", lambda: self.append("math.sin(")), ("cos", lambda: self.append("math.cos(")), ("tan", lambda: self.append("math.tan(")), ("log", lambda: self.append("math.log10(")),
            ("7", lambda: self.append("7")), ("8", lambda: self.append("8")), ("9", lambda: self.append("9")), ("*", lambda: self.append("*")),
            ("4", lambda: self.append("4")), ("5", lambda: self.append("5")), ("6", lambda: self.append("6")), ("-", lambda: self.append("-")),
            ("1", lambda: self.append("1")), ("2", lambda: self.append("2")), ("3", lambda: self.append("3")), ("+", lambda: self.append("+")),
            ("0", lambda: self.append("0")), (".", lambda: self.append(".")), ("√", lambda: self.append("math.sqrt(")), ("^", lambda: self.append("**")),
            ("=", self.calculate)
        ]

        self.button_widgets = []

        row = 2
        col = 0
        for (text, cmd) in buttons:
            btn = ctk.CTkButton(self, text=text, command=lambda c=cmd: self.on_click(c),
                                font=("Segoe UI", 16, "bold"), width=80, height=55,
                                corner_radius=10, fg_color=self.get_button_color(text),
                                text_color="white", hover_color="#555")
            self.button_widgets.append((btn, text))

            if text == "=":
                btn.grid(row=row, column=0, columnspan=4, padx=15, pady=15, sticky="nsew")
            else:
                btn.grid(row=row, column=col, padx=8, pady=8)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def get_button_color(self, text):
        if text in ("+", "-", "*", "/", "^"):
            return "#f39c12"
        elif text == "C":
            return "#e74c3c"
        elif text in ("sin", "cos", "tan", "log", "√"):
            return "#2980b9"
        elif text == "=":
            return "#27ae60"
        else:
            return "#34495e"

    def toggle_theme(self):
        mode = "dark" if self.theme_switch.get() == 1 else "light"
        ctk.set_appearance_mode(mode)

        if mode == "dark":
            self.display.configure(fg_color="#2e2e2e", text_color="#ffffff")
        else:
            self.display.configure(fg_color="#ffffff", text_color="#000000")

        for btn, text in self.button_widgets:
            btn.configure(fg_color=self.get_button_color(text))

    def on_click(self, cmd):
        if cmd != self.calculate:
            click_sound.play()
        else:
            equal_sound.play()
        cmd()

    def append(self, value):
        self.display.insert(ctk.END, value)

    def clear(self):
        self.display.delete(0, ctk.END)

    def calculate(self):
        expression = self.display.get()
        try:
            result = eval(expression, {"__builtins__": None, "math": math})
            self.display.delete(0, ctk.END)
            self.display.insert(0, str(result))
        except Exception:
            self.display.delete(0, ctk.END)
            self.display.insert(0, "Error")

if __name__ == "__main__":
    app = SKCalculator()
    app.mainloop()
