import tkinter as tk
from tkinter import scrolledtext, filedialog

class ChatbotGUI:
    def __init__(self, send_callback, observation_mode_callback, feedback_callback):
        self.send_callback = send_callback
        self.observation_mode_callback = observation_mode_callback
        self.feedback_callback = feedback_callback
        self.observation_mode = False

        self.window = tk.Tk()
        self.window.title("JaACKIE - AI Chatbot")

        # Chat display
        self.chat_display = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD, width=50, height=20)
        self.chat_display.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # Text input
        self.input_box = tk.Entry(self.window, width=40)
        self.input_box.grid(row=1, column=0, padx=10, pady=10)
        self.input_box.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)

        # Feedback buttons
        self.positive_button = tk.Button(self.window, text="+", command=lambda: self.give_feedback("positive"))
        self.positive_button.grid(row=1, column=2, padx=5, pady=10)

        self.negative_button = tk.Button(self.window, text="-", command=lambda: self.give_feedback("negative"))
        self.negative_button.grid(row=1, column=3, padx=5, pady=10)

        # Observation Mode Toggle Button
        self.observation_button = tk.Button(self.window, text="Enable Observation Mode", command=self.toggle_observation_mode)
        self.observation_button.grid(row=2, column=0, columnspan=5, pady=10)

        # Observation mode buttons (hidden initially)
        self.user1_button = tk.Button(self.window, text="User 1", command=lambda: self.manual_entry("User 1"))
        self.user1_button.grid(row=3, column=0, padx=5, pady=5)
        self.user1_button.grid_remove()

        self.user2_button = tk.Button(self.window, text="User 2", command=lambda: self.manual_entry("User 2"))
        self.user2_button.grid(row=3, column=1, padx=5, pady=5)
        self.user2_button.grid_remove()

        self.paste_button = tk.Button(self.window, text="Paste Conversation", command=self.paste_conversation)
        self.paste_button.grid(row=3, column=2, columnspan=2, padx=5, pady=5)
        self.paste_button.grid_remove()

    def send_message(self, event=None):
        if not self.observation_mode:
            user_input = self.input_box.get()
            if user_input.strip():
                self.display_message("User", user_input, "black")
                response = self.send_callback(user_input)
                if response:
                    self.display_message("JaACKIE", response, "blue")
            self.input_box.delete(0, tk.END)

    def give_feedback(self, feedback_type):
        user_input, bot_response = self.get_last_interaction()
        if user_input and bot_response:
            corrected_response = self.feedback_callback(feedback_type, user_input, bot_response)
            if feedback_type == "negative" and corrected_response:
                self.display_message("JaACKIE (Revised)", corrected_response, "blue")

    def toggle_observation_mode(self):
        self.observation_mode = not self.observation_mode
        self.observation_mode_callback(self.observation_mode)
        self.update_mode(self.observation_mode)  # Pass the observation_mode argument

    def update_mode(self, observation_mode):
        self.observation_mode = observation_mode
        if self.observation_mode:
            self.input_box.config(state='disabled')
            self.send_button.config(state='disabled')
            self.user1_button.grid()
            self.user2_button.grid()
            self.paste_button.grid()
            self.observation_button.config(text="Disable Observation Mode")
        else:
            self.input_box.config(state='normal')
            self.send_button.config(state='normal')
            self.user1_button.grid_remove()
            self.user2_button.grid_remove()
            self.paste_button.grid_remove()
            self.observation_button.config(text="Enable Observation Mode")

    def manual_entry(self, user_type):
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Manual Entry - {user_type}")
        label = tk.Label(dialog, text=f"Enter {user_type} message:")
        label.pack(padx=10, pady=5)
        entry = tk.Entry(dialog, width=50)
        entry.pack(padx=10, pady=5)

        def save_message():
            message = entry.get()
            if message.strip():
                self.display_message(user_type, message, "purple")
                self.send_callback(message)  # Log the message
            dialog.destroy()

        save_button = tk.Button(dialog, text="Save", command=save_message)
        save_button.pack(pady=10)

    def paste_conversation(self):
        file_path = filedialog.askopenfilename(title="Select Conversation File", filetypes=(("Text Files", "*.txt"),))
        if file_path:
            with open(file_path, "r") as file:
                conversation = file.read()
            self.display_message("System", "Pasted conversation:\n" + conversation, "purple")
            self.send_callback(conversation)  # Log the entire conversation

    def display_message(self, sender, message, color):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n", (color,))
        self.chat_display.tag_config(color, foreground=color)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def get_last_interaction(self):
        lines = self.chat_display.get("1.0", tk.END).strip().split("\n")
        user_line, bot_line = None, None
        for line in reversed(lines):
            if line.startswith("JaACKIE:") and not bot_line:
                bot_line = line.split(":", 1)[1].strip()
            elif line.startswith("User:") and not user_line:
                user_line = line.split(":", 1)[1].strip()
            if user_line and bot_line:
                break
        return user_line, bot_line

    def run(self):
        self.window.mainloop()