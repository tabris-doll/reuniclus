import tkinter as tk
from tkinter import ttk, font
import random
import json
import os
from datetime import datetime

# ---------------------------- CONSTANTS & STYLING ----------------------------
BG_COLOR = "#FFF5F5"  # Soft pinkish-white
PRIMARY_COLOR = "#E75480"  # Romantic pink (like sakura 🌸)
SECONDARY_COLOR = "#6A5ACD"  # Royal purple
TEXT_COLOR = "#333333"
CORRECT_COLOR = "#4CAF50"  # Soft green
INCORRECT_COLOR = "#F44336"  # Soft red
BUTTON_FONT = ("Nunito", 12, "bold")  # Changed to Nunito for better readability
TITLE_FONT = ("Nunito", 28, "bold")  # Increased size, changed to Nunito
CARD_FONT_LARGE = ("Nunito", 80, "bold")  # Increased size, changed to Nunito
CARD_FONT_SMALL = ("Nunito", 20)  # Increased size, changed to Nunito
APP_NAME = "Reuniclus"  # Official app name
APP_TAGLINE = "Hiragana Learning Studio"  # Added tagline

# ---------------------------- MAIN APP ----------------------------
class ReuniclusApp:  # Renamed class to reflect the official name
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} - {APP_TAGLINE}")
        self.root.geometry("900x750")  # Increased window size for better spacing
        self.root.configure(bg=BG_COLOR)
        
        # Try to load custom fonts
        try:
            # Attempt to load Nunito font if available on system
            font.nametofont("TkDefaultFont").configure(family="Nunito", size=11)
        except:
            # Fallback to system fonts if Nunito is not available
            pass
        
        # App data
        self.flashcards = self.initialize_flashcards()
        self.current_card = None
        self.stats = self.load_stats()
        self.session_correct = 0
        self.session_total = 0
        self.multiple_choice_mode = False
        self.practice_mode = None  # Initialize practice_mode
        self.practice_cards = []  # Initialize practice_cards
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("TButton", 
                            font=BUTTON_FONT, 
                            foreground="white", 
                            background=PRIMARY_COLOR,
                            padding=12)  # Increased padding
        self.style.map("TButton",
                      background=[("active", SECONDARY_COLOR)],
                      foreground=[("active", "white")])
        
        # Main container with increased padding
        self.main_frame = ttk.Frame(root, padding=(40, 30))  # Increased padding
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create main menu
        self.create_main_menu()
        
        # Bind Escape key to return to main menu
        self.root.bind('<Escape>', lambda e: self.create_main_menu())

    # ---------------------------- FLASHCARD DATA ----------------------------
    def initialize_flashcards(self):
        """Create the hiragana flashcard dictionary"""
        return [
            {"hiragana": "あ", "romaji": "a"}, {"hiragana": "い", "romaji": "i"}, 
            {"hiragana": "う", "romaji": "u"}, {"hiragana": "え", "romaji": "e"}, 
            {"hiragana": "お", "romaji": "o"}, {"hiragana": "か", "romaji": "ka"}, 
            {"hiragana": "き", "romaji": "ki"}, {"hiragana": "く", "romaji": "ku"}, 
            {"hiragana": "け", "romaji": "ke"}, {"hiragana": "こ", "romaji": "ko"}, 
            {"hiragana": "さ", "romaji": "sa"}, {"hiragana": "し", "romaji": "shi"}, 
            {"hiragana": "す", "romaji": "su"}, {"hiragana": "せ", "romaji": "se"}, 
            {"hiragana": "そ", "romaji": "so"}, {"hiragana": "た", "romaji": "ta"}, 
            {"hiragana": "ち", "romaji": "chi"}, {"hiragana": "つ", "romaji": "tsu"}, 
            {"hiragana": "て", "romaji": "te"}, {"hiragana": "と", "romaji": "to"}, 
            {"hiragana": "な", "romaji": "na"}, {"hiragana": "に", "romaji": "ni"}, 
            {"hiragana": "ぬ", "romaji": "nu"}, {"hiragana": "ね", "romaji": "ne"}, 
            {"hiragana": "の", "romaji": "no"}, {"hiragana": "は", "romaji": "ha"}, 
            {"hiragana": "ひ", "romaji": "hi"}, {"hiragana": "ふ", "romaji": "fu"}, 
            {"hiragana": "へ", "romaji": "he"}, {"hiragana": "ほ", "romaji": "ho"}, 
            {"hiragana": "ま", "romaji": "ma"}, {"hiragana": "み", "romaji": "mi"}, 
            {"hiragana": "む", "romaji": "mu"}, {"hiragana": "め", "romaji": "me"}, 
            {"hiragana": "も", "romaji": "mo"}, {"hiragana": "や", "romaji": "ya"}, 
            {"hiragana": "ゆ", "romaji": "yu"}, {"hiragana": "よ", "romaji": "yo"}, 
            {"hiragana": "ら", "romaji": "ra"}, {"hiragana": "り", "romaji": "ri"}, 
            {"hiragana": "る", "romaji": "ru"}, {"hiragana": "れ", "romaji": "re"}, 
            {"hiragana": "ろ", "romaji": "ro"}, {"hiragana": "わ", "romaji": "wa"}, 
            {"hiragana": "を", "romaji": "wo"}, {"hiragana": "ん", "romaji": "n"}
        ]

    # ---------------------------- STATS HANDLING ----------------------------
    def load_stats(self):
        """Load previous statistics from file"""
        try:
            if os.path.exists("reuniclus_stats.json"):  # Updated filename
                with open("reuniclus_stats.json", "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        
        # Default stats structure
        default_stats = {
            "total_correct": 0,
            "total_attempts": 0,
            "hiragana_stats": {},
            "streak": 0,
            "longest_streak": 0,
            "last_session": None
        }
        
        # Initialize stats for each hiragana character
        for card in self.flashcards:
            default_stats["hiragana_stats"][card["hiragana"]] = {"correct": 0, "attempts": 0}
            
        return default_stats
    
    def save_stats(self):
        """Save statistics to file"""
        try:
            self.stats["last_session"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("reuniclus_stats.json", "w", encoding="utf-8") as f:  # Updated filename
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Could not save stats:", e)

    # ---------------------------- MAIN MENU ----------------------------
    def create_main_menu(self):
        """Create the main menu interface with improved spacing"""
        self.clear_frame()
        self.root.unbind('<Return>')
        
        # Logo and title with elegant spacing
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=40)  # Increased top padding
        
        # Main title with app name
        tk.Label(title_frame, 
                text=f"✨ {APP_NAME} ✨", 
                font=TITLE_FONT, 
                fg=PRIMARY_COLOR, 
                bg=BG_COLOR).pack(pady=(0, 5))
        
        # Tagline
        tk.Label(title_frame, 
                text=APP_TAGLINE, 
                font=("Nunito", 16, "italic"),  # Stylish tagline font
                fg=SECONDARY_COLOR, 
                bg=BG_COLOR).pack(pady=(0, 15))
        
        # Mode toggle with better spacing (multiple choice checkbox)
        mode_frame = ttk.Frame(self.main_frame)
        mode_frame.pack(pady=15)  # Increased padding
        
        self.multiple_choice_var = tk.BooleanVar(value=self.multiple_choice_mode)
        mc_check = tk.Checkbutton(mode_frame, 
                                 text="Multiple Choice Mode", 
                                 variable=self.multiple_choice_var,
                                 command=self.toggle_multiple_choice,
                                 font=("Nunito", 12),  # Updated font
                                 bg=BG_COLOR,
                                 activebackground=BG_COLOR,
                                 fg=TEXT_COLOR,
                                 selectcolor=BG_COLOR)
        mc_check.pack(pady=8)  # Increased padding
        
        # Practice buttons with improved spacing
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=25)  # Increased padding
        
        study_button = ttk.Button(button_frame, 
                                 text="Study Hiragana → Romaji", 
                                 command=lambda: self.start_practice("hiragana_to_romaji"))
        study_button.pack(pady=15, fill=tk.X, padx=70)  # Increased padding and width
        
        reverse_button = ttk.Button(button_frame, 
                                   text="Study Romaji → Hiragana", 
                                   command=lambda: self.start_practice("romaji_to_hiragana"))
        reverse_button.pack(pady=15, fill=tk.X, padx=70)  # Increased padding and width
        
        reference_button = ttk.Button(button_frame, 
                                     text="Hiragana Reference Chart", 
                                     command=self.show_reference)
        reference_button.pack(pady=15, fill=tk.X, padx=70)  # Increased padding and width
        
        # Stats display with improved spacing
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(pady=30, fill=tk.X, padx=70)  # Increased padding
        
        # Add a decorative line above stats
        separator = ttk.Separator(stats_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 15))
        
        accuracy = 0
        if self.stats["total_attempts"] > 0:
            accuracy = (self.stats["total_correct"] / self.stats["total_attempts"]) * 100
            
        stats_text = f"🎯 {self.stats['total_correct']}/{self.stats['total_attempts']} correct ({accuracy:.1f}%)"
        streak_text = f"🔥 Streak: {self.stats['streak']} (Best: {self.stats['longest_streak']})"
        
        tk.Label(stats_frame, 
                 text=stats_text, 
                 font=("Nunito", 14),  # Updated font and size
                 bg=BG_COLOR).pack(pady=8)  # Increased padding
        tk.Label(stats_frame, 
                 text=streak_text, 
                 font=("Nunito", 14),  # Updated font and size
                 bg=BG_COLOR).pack(pady=8)  # Increased padding
        
        # Exit button (small and subtle)
        exit_button = ttk.Button(self.main_frame, 
                                text="Exit", 
                                command=self.root.destroy)
        exit_button.pack(pady=20)  # Increased padding

    # ---------------------------- PRACTICE MODE ----------------------------
    def start_practice(self, mode):
        """Start practice session with selected mode"""
        self.practice_mode = mode
        self.practice_cards = self.flashcards.copy()
        random.shuffle(self.practice_cards)
        self.session_correct = 0
        self.session_total = 0
        self.show_next_card()

    def show_next_card(self):
        """Show the next flashcard with improved spacing"""
        self.clear_frame()
        
        if not self.practice_cards:
            self.show_session_results()
            return
        
        self.current_card = self.practice_cards.pop(0)
        
        # Header with session info
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(10, 30))
        
        # Show practice mode and card count
        mode_text = "Hiragana → Romaji" if self.practice_mode == "hiragana_to_romaji" else "Romaji → Hiragana"
        cards_remaining = len(self.practice_cards) + 1
        
        tk.Label(header_frame, 
                text=f"{APP_NAME} - {mode_text}",
                font=("Nunito", 14, "bold"),
                fg=SECONDARY_COLOR,
                bg=BG_COLOR).pack(side=tk.LEFT, padx=20)
        
        tk.Label(header_frame, 
                text=f"Cards: {cards_remaining}/{len(self.flashcards)}",
                font=("Nunito", 12),
                fg=TEXT_COLOR,
                bg=BG_COLOR).pack(side=tk.RIGHT, padx=20)
        
        # Question display (centered card) with improved spacing
        card_frame = ttk.Frame(self.main_frame)
        card_frame.pack(expand=True, pady=50)
        
        if self.practice_mode == "hiragana_to_romaji":
            question = self.current_card["hiragana"]
            answer_label = "Romaji:"
        else:
            question = self.current_card["romaji"]
            answer_label = "Hiragana:"
        
        # Card container with visual border effect
        card_container = tk.Frame(card_frame, 
                                 bd=2, 
                                 relief=tk.RIDGE, 
                                 bg=BG_COLOR,
                                 highlightbackground=PRIMARY_COLOR,
                                 highlightthickness=2)
        card_container.pack(padx=40, pady=20, ipadx=40, ipady=40)
        
        # Large hiragana/romaji display
        tk.Label(card_container, 
                text=question, 
                font=CARD_FONT_LARGE, 
                fg=PRIMARY_COLOR, 
                bg=BG_COLOR).pack(pady=20)
        
        if self.multiple_choice_mode:
            self.show_multiple_choice()
        else:
            self.show_free_answer(answer_label)

    def show_free_answer(self, answer_label):
        """Elegant free-answer input with improved spacing"""
        answer_frame = ttk.Frame(self.main_frame)
        answer_frame.pack(pady=30)  # Increased padding
        
        tk.Label(answer_frame, 
                text=answer_label, 
                font=("Nunito", 14, "bold"),  # Updated font
                fg=TEXT_COLOR, 
                bg=BG_COLOR).pack(side=tk.LEFT, padx=10)  # Increased padding
        
        self.answer_var = tk.StringVar()
        answer_entry = ttk.Entry(answer_frame, 
                                textvariable=self.answer_var, 
                                font=CARD_FONT_SMALL, 
                                width=18)  # Increased width
        answer_entry.pack(side=tk.LEFT, padx=10)  # Increased padding
        answer_entry.focus()
        
        # Buttons (centered) with improved spacing
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=40)  # Increased padding
        
        ttk.Button(button_frame, 
                  text="Check Answer (Enter)", 
                  command=self.check_answer).pack(side=tk.LEFT, padx=15)  # Increased padding
        
        ttk.Button(button_frame, 
                  text="Back to Menu (Esc)", 
                  command=self.create_main_menu).pack(side=tk.LEFT, padx=15)  # Increased padding
        
        self.root.bind('<Return>', lambda e: self.check_answer())

    def show_multiple_choice(self):
        """Stylish multiple-choice buttons with improved spacing"""
        if self.practice_mode == "hiragana_to_romaji":
            correct_answer = self.current_card["romaji"]
            all_answers = [card["romaji"] for card in self.flashcards if card["romaji"] != correct_answer]
        else:
            correct_answer = self.current_card["hiragana"]
            all_answers = [card["hiragana"] for card in self.flashcards if card["hiragana"] != correct_answer]
        
        # Select 3 incorrect answers
        options = random.sample(all_answers, min(3, len(all_answers))) + [correct_answer]
        random.shuffle(options)
        
        # Grid of choice buttons with improved spacing
        choice_frame = ttk.Frame(self.main_frame)
        choice_frame.pack(pady=40, padx=60)  # Increased padding
        
        # Configure columns with equal weight
        choice_frame.columnconfigure(0, weight=1)
        choice_frame.columnconfigure(1, weight=1)
        
        for i, option in enumerate(options):
            btn = ttk.Button(choice_frame, 
                            text=option, 
                            command=lambda o=option: self.check_answer(o))
            btn.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="nsew")  # Increased padding
        
        # Navigation buttons with improved spacing
        nav_frame = ttk.Frame(self.main_frame)
        nav_frame.pack(pady=30)  # Increased padding
        
        ttk.Button(nav_frame, 
                  text="Skip (Space)", 
                  command=self.show_next_card).pack(side=tk.LEFT, padx=15)  # Increased padding
        
        ttk.Button(nav_frame, 
                  text="Back to Menu (Esc)", 
                  command=self.create_main_menu).pack(side=tk.LEFT, padx=15)  # Increased padding
        
        self.root.bind('<space>', lambda e: self.show_next_card())

    def check_answer(self, user_answer=None):
        """Check the user's answer against the correct answer"""
        if user_answer is None:  # Free answer mode
            user_answer = self.answer_var.get().strip().lower()
        
        if self.practice_mode == "hiragana_to_romaji":
            correct_answer = self.current_card["romaji"]
        else:  # romaji_to_hiragana
            correct_answer = self.current_card["hiragana"]
        
        is_correct = (str(user_answer).lower() == str(correct_answer).lower())
        self.show_answer(is_correct, user_answer)

    def show_answer(self, is_correct=False, user_answer=""):
        """Luxe answer feedback screen with improved spacing"""
        self.clear_frame()
        self.root.unbind('<Return>')
        self.root.unbind('<space>')
        
        # Update stats
        self.session_total += 1
        card_hiragana = self.current_card["hiragana"]
        
        if card_hiragana not in self.stats["hiragana_stats"]:
            self.stats["hiragana_stats"][card_hiragana] = {"correct": 0, "attempts": 0}
            
        self.stats["hiragana_stats"][card_hiragana]["attempts"] += 1
        self.stats["total_attempts"] += 1
        
        if is_correct:
            self.session_correct += 1
            self.stats["total_correct"] += 1
            self.stats["hiragana_stats"][card_hiragana]["correct"] += 1
            self.stats["streak"] += 1
            self.stats["longest_streak"] = max(self.stats["streak"], self.stats["longest_streak"])
            result_text = "✅ Correct!"
            result_color = CORRECT_COLOR
        else:
            self.stats["streak"] = 0
            result_text = "❌ Incorrect"
            result_color = INCORRECT_COLOR
        
        # Header with app name
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(10, 30))
        
        tk.Label(header_frame, 
                text=APP_NAME,
                font=("Nunito", 14, "bold"),
                fg=SECONDARY_COLOR,
                bg=BG_COLOR).pack(side=tk.LEFT, padx=20)
        
        # Result display (centered) with improved spacing
        result_frame = ttk.Frame(self.main_frame)
        result_frame.pack(expand=True, pady=20) 
        
        tk.Label(result_frame, 
                text=result_text, 
                font=("Nunito", 28, "bold"),  # Updated font and size 
                fg=result_color, 
                bg=BG_COLOR).pack(pady=25)  # Increased padding
        
        # Card details (as a neat "card") with improved styling
        card_border = tk.Frame(result_frame, 
                             bd=2, 
                             relief=tk.RIDGE, 
                             bg=BG_COLOR,
                             highlightbackground=SECONDARY_COLOR,
                             highlightthickness=1)
        card_border.pack(pady=20, padx=60, fill=tk.X)
        
        detail_frame = ttk.Frame(card_border)
        detail_frame.pack(pady=20, padx=30, fill=tk.X)
        
        tk.Label(detail_frame, 
                text=f"Hiragana: {self.current_card['hiragana']}", 
                font=("Nunito", 22),  # Updated font and size
                bg=BG_COLOR).pack(pady=8)  # Increased padding
        
        tk.Label(detail_frame, 
                text=f"Romaji: {self.current_card['romaji']}", 
                font=("Nunito", 18),  # Updated font and size
                bg=BG_COLOR).pack(pady=8)  # Increased padding
        
        tk.Label(detail_frame, 
                text=f"Your answer: {user_answer}", 
                font=("Nunito", 16),  # Updated font and size
                bg=BG_COLOR).pack(pady=12)  # Increased padding
        
        # Next card button (big and inviting) with improved spacing
        ttk.Button(result_frame, 
                  text="Next Card (Space)", 
                  command=self.show_next_card).pack(pady=30)  # Increased padding
        
        self.root.bind('<space>', lambda e: self.show_next_card())
        self.save_stats()

    # ---------------------------- REFERENCE CHART ----------------------------
    def show_reference(self):
        """Fancy scrollable reference chart with improved spacing"""
        self.clear_frame()
        
        # Header with title and back button
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=15)  # Increased padding
        
        tk.Label(header_frame, 
                text=f"{APP_NAME} - 📖 Hiragana Reference", 
                font=("Nunito", 20, "bold"),  # Updated font and size
                fg=SECONDARY_COLOR, 
                bg=BG_COLOR).pack(side=tk.LEFT, padx=25)  # Increased padding
        
        ttk.Button(header_frame, 
                  text="Back (Esc)", 
                  command=self.create_main_menu).pack(side=tk.RIGHT, padx=25)  # Increased padding
        
        # Scrollable canvas
        canvas = tk.Canvas(self.main_frame, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))  # Added padding
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))  # Added padding
        
        # Frame inside canvas
        chart_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=chart_frame, anchor="nw")
        
        # Add section headers
        tk.Label(chart_frame, 
                text="Basic Hiragana Characters", 
                font=("Nunito", 16, "bold"),
                fg=PRIMARY_COLOR, 
                bg=BG_COLOR).grid(row=0, column=0, sticky="w", padx=60, pady=(20, 10))
        
        # Add flashcards in a grid with improved spacing
        for i, card in enumerate(self.flashcards):
            # Add section headers at appropriate places
            if i == 5:  # Before "ka" row
                tk.Label(chart_frame, 
                        text="K-row Characters", 
                        font=("Nunito", 16, "bold"),
                        fg=PRIMARY_COLOR, 
                        bg=BG_COLOR).grid(row=i+1, column=0, sticky="w", padx=60, pady=(20, 10))
                i += 1
            elif i == 10 + 1:  # Before "sa" row (adjusted for header)
                tk.Label(chart_frame, 
                        text="S-row Characters", 
                        font=("Nunito", 16, "bold"),
                        fg=PRIMARY_COLOR, 
                        bg=BG_COLOR).grid(row=i+1, column=0, sticky="w", padx=60, pady=(20, 10))
                i += 1
            # Add more section headers as needed for other rows
            
            row_frame = ttk.Frame(chart_frame)
            row_frame.grid(row=i+2, column=0, sticky="ew", padx=60, pady=8)  # Increased padding
            
            # Add character card with border
            char_frame = tk.Frame(row_frame, 
                                bd=1, 
                                relief=tk.RIDGE, 
                                bg=BG_COLOR)
            char_frame.pack(side=tk.LEFT, padx=20)
            
            tk.Label(char_frame, 
                    text=card["hiragana"], 
                    font=("Nunito", 40),  # Updated font and size
                    width=2, 
                    bg=BG_COLOR,
                    padx=10,
                    pady=5).pack()
            
            tk.Label(row_frame, 
                    text=card["romaji"], 
                    font=("Nunito", 18),  # Updated font and size
                    bg=BG_COLOR).pack(side=tk.LEFT, padx=15)  # Increased padding
        
        # Update scrollregion
        chart_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Mousewheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # ---------------------------- HELPER FUNCTIONS ----------------------------
    def clear_frame(self):
        """Destroy all widgets in main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def toggle_multiple_choice(self):
        """Toggle multiple choice mode"""
        self.multiple_choice_mode = self.multiple_choice_var.get()

    def show_session_results(self):
        """Show the results of the practice session with improved spacing"""
        self.clear_frame()
        self.root.unbind('<space>')  # Unbind space from answer screen
        
        # Header with app name
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(10, 30))
        
        tk.Label(header_frame, 
                text=APP_NAME,
                font=("Nunito", 14, "bold"),
                fg=SECONDARY_COLOR,
                bg=BG_COLOR).pack(side=tk.LEFT, padx=20)
        
        # Results title with improved spacing
        title_label = tk.Label(self.main_frame, 
                              text="Session Results", 
                              font=("Nunito", 28, "bold"),  # Updated font and size
                              fg=PRIMARY_COLOR, 
                              bg=BG_COLOR)
        title_label.pack(pady=25)  # Increased padding
        
        # Results card with border
        results_card = tk.Frame(self.main_frame, 
                              bd=2, 
                              relief=tk.RIDGE, 
                              bg=BG_COLOR,
                              highlightbackground=SECONDARY_COLOR,
                              highlightthickness=1)
        results_card.pack(pady=20, padx=80, fill=tk.X)
        
        results_content = ttk.Frame(results_card)
        results_content.pack(pady=25, padx=30)  # Increased padding
        
        # Results stats with improved spacing
        if self.session_total > 0:
            accuracy = (self.session_correct / self.session_total) * 100
            
            tk.Label(results_content, 
                    text=f"Cards studied: {self.session_total}", 
                    font=("Nunito", 16),  # Updated font and size
                    bg=BG_COLOR).pack(pady=8)  # Increased padding
            
            tk.Label(results_content, 
                    text=f"Correct answers: {self.session_correct}", 
                    font=("Nunito", 16),  # Updated font and size
                    bg=BG_COLOR).pack(pady=8)  # Increased padding
            
            tk.Label(results_content, 
                    text=f"Accuracy: {accuracy:.1f}%", 
                    font=("Nunito", 16, "bold"),  # Updated font and size, made bold
                    bg=BG_COLOR).pack(pady=8)  # Increased padding
            
            # Feedback based on accuracy with improved styling
            if accuracy >= 90:
                feedback = "🌸 Excellent! You're mastering hiragana!"
                feedback_color = CORRECT_COLOR
            elif accuracy >= 75:
                feedback = "🎌 Great job! Keep practicing!"
                feedback_color = CORRECT_COLOR
            elif accuracy >= 60:
                feedback = "💮 Good progress! Regular practice will help you improve."
                feedback_color = SECONDARY_COLOR
            else:
                feedback = "🍃 Keep studying! You'll get better with practice."
                feedback_color = PRIMARY_COLOR
            
            # Separator before feedback
            separator = ttk.Separator(results_content, orient='horizontal')
            separator.pack(fill=tk.X, pady=15)
            
            tk.Label(results_content, 
                    text=feedback, 
                    font=("Nunito", 16),  # Updated font and size
                    fg=feedback_color,
                    bg=BG_COLOR).pack(pady=12)  # Increased padding
        else:
            tk.Label(results_content, 
                    text="No cards were studied in this session.", 
                    font=("Nunito", 16),  # Updated font and size
                    bg=BG_COLOR).pack(pady=10)  # Increased padding
        
        # Buttons with improved spacing
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=40)  # Increased padding
        
        menu_button = ttk.Button(button_frame, 
                                text="Return to Menu (Esc)", 
                                command=self.create_main_menu)
        menu_button.pack(side=tk.LEFT, padx=15)  # Increased padding
        
        practice_again_button = ttk.Button(button_frame, 
                                         text="Practice Again", 
                                         command=lambda: self.start_practice(self.practice_mode))
        practice_again_button.pack(side=tk.LEFT, padx=15)  # Increased padding

# ---------------------------- RUN THE APP ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ReuniclusApp(root)  # Updated class name
    root.mainloop()