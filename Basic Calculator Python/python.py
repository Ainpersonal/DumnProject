import customtkinter as ctk
import re

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AInCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AIn Calculator")
        self.geometry("350x550")
        self.resizable(True, True)
        
        self.colors = {
            "bg": "#1a1a2e",
            "display_bg": "#16213e",
            "btn_num": "#0f3460",
            "btn_num_hover": "#1e4d8c",
            "btn_op": "#e94560",
            "btn_op_hover": "#ff6b81",
            "btn_clear": "#533483",
            "btn_clear_hover": "#7a4ebf",
            "text": "#ffffff"
        }
        
        self.configure(fg_color=self.colors["bg"])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)

        self.expression = ""
        self.input_text = ctk.StringVar()
        
        self.button_map = {}

        self.create_display()
        self.create_buttons()
        self.bind('<Key>', self.handle_keypress)

    def create_display(self):
        self.display_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.display_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        
        self.display = ctk.CTkEntry(
            self.display_frame, 
            textvariable=self.input_text, 
            font=("Roboto Medium", 40),
            width=300, 
            height=80,
            border_width=0,
            fg_color=self.colors["display_bg"],
            text_color=self.colors["text"],
            justify="right",
            corner_radius=15
        )
        self.display.pack(expand=True, fill="both")

    def create_buttons(self):
        self.btns_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btns_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)

        for i in range(4):
            self.btns_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.btns_frame.grid_rowconfigure(i, weight=1)

        buttons = [
            ('AC', 0, 0, 2, self.colors["btn_clear"], self.colors["btn_clear_hover"], self.btn_clear),
            ('DEL', 0, 2, 1, self.colors["btn_clear"], self.colors["btn_clear_hover"], self.btn_delete),
            ('/', 0, 3, 1, self.colors["btn_op"], self.colors["btn_op_hover"], lambda: self.btn_click('/')),
            
            ('7', 1, 0, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('7')),
            ('8', 1, 1, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('8')),
            ('9', 1, 2, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('9')),
            ('*', 1, 3, 1, self.colors["btn_op"], self.colors["btn_op_hover"], lambda: self.btn_click('*')),
            
            ('4', 2, 0, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('4')),
            ('5', 2, 1, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('5')),
            ('6', 2, 2, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('6')),
            ('-', 2, 3, 1, self.colors["btn_op"], self.colors["btn_op_hover"], lambda: self.btn_click('-')),
            
            ('1', 3, 0, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('1')),
            ('2', 3, 1, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('2')),
            ('3', 3, 2, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('3')),
            ('+', 3, 3, 1, self.colors["btn_op"], self.colors["btn_op_hover"], lambda: self.btn_click('+')),
            
            ('0', 4, 0, 2, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('0')),
            ('.', 4, 2, 1, self.colors["btn_num"], self.colors["btn_num_hover"], lambda: self.btn_click('.')),
            ('=', 4, 3, 1, self.colors["btn_op"], self.colors["btn_op_hover"], self.btn_equal),
        ]

        for text, r, c, span, col, h_col, cmd in buttons:
            self.create_btn(text, r, c, span, col, h_col, cmd)

    def create_btn(self, text, row, col, span, color, hover_color, cmd):
        btn = ctk.CTkButton(
            self.btns_frame, 
            text=text, 
            font=("Arial", 20, "bold"),
            fg_color=color, 
            hover_color=hover_color, 
            command=cmd,
            corner_radius=15,
            height=60
        )
        btn.grid(row=row, column=col, columnspan=span, padx=5, pady=5, sticky="nsew")
        self.button_map[text] = btn

    def animate_button_press(self, btn_text):
        if btn_text in self.button_map:
            btn = self.button_map[btn_text]
            original_color = btn.cget("fg_color")
            pressed_color = btn.cget("hover_color")
            btn.configure(fg_color=pressed_color)
            self.after(100, lambda: btn.configure(fg_color=original_color))

    def btn_click(self, item):
        self.animate_button_press(item)
        current_val = self.expression
        operators = ['+', '-', '*', '/']

        if item == '.':
            if not current_val or current_val[-1] in operators:
                self.expression += "0."
            else:
                parts = re.split(r'[\+\-\*\/]', current_val)
                if '.' not in parts[-1]:
                    self.expression += "."
            self.input_text.set(self.expression)
            return

        if item in operators:
            if not current_val: return
            if current_val[-1] in operators:
                self.expression = current_val[:-1] + item
            elif current_val[-1] == '.':
                 self.expression = current_val[:-1] + item
            else:
                self.expression += item
            self.input_text.set(self.expression)
            return

        self.expression = str(self.expression) + str(item)
        self.input_text.set(self.expression)

    def btn_clear(self):
        self.animate_button_press('AC')
        self.expression = ""
        self.input_text.set("")

    def btn_delete(self):
        self.animate_button_press('DEL')
        self.expression = self.expression[:-1]
        self.input_text.set(self.expression)

    def btn_equal(self):
        self.animate_button_press('=')
        try:
            if self.expression and self.expression[-1] in ['+', '-', '*', '/']:
                 self.expression = self.expression[:-1]
            result = str(eval(self.expression)) 
            if '.' in result:
                f_result = float(result)
                result = "{:.10f}".format(f_result).rstrip('0').rstrip('.')
            self.expression = result
            self.input_text.set(result)
        except:
            self.input_text.set("Error")
            self.expression = ""

    def handle_keypress(self, event):
        key = event.char
        if key in '0123456789.': self.btn_click(key)
        elif key in '+-*/': self.btn_click(key)
        elif key == '\r': self.btn_equal()
        elif key == '\x08': self.btn_delete()
        elif key.lower() == 'c' or key == '\x1b': self.btn_clear()

if __name__ == "__main__":
    app = AInCalculator()
    app.mainloop()