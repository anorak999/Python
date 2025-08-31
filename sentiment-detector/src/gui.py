from tkinter import Tk, Label, Entry, Button, Text, END, messagebox, StringVar, OptionMenu
from sentiment import SentimentAnalyzer

class SentimentDetectorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sentiment Detector")

        self.label = Label(master, text="Enter text for sentiment analysis:")
        self.label.pack()

        self.text_input = Text(master, height=10, width=50)
        self.text_input.pack()

        # Dropdown for analysis mode
        self.mode_var = StringVar(master)
        self.mode_var.set("Simple")
        self.mode_label = Label(master, text="Select analysis mode:")
        self.mode_label.pack()
        self.mode_menu = OptionMenu(master, self.mode_var, "Simple", "Advanced")
        self.mode_menu.pack()

        self.analyze_button = Button(master, text="Analyze Sentiment", command=self.analyze_sentiment)
        self.analyze_button.pack()

        self.result_label = Label(master, text="")
        self.result_label.pack()

        self.confidence_label = Label(master, text="")
        self.confidence_label.pack()

    def analyze_sentiment(self):
        text = self.text_input.get("1.0", END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        analyzer = SentimentAnalyzer()
        mode = self.mode_var.get()
        sentiment, confidence = analyzer.analyze_sentiment(text, mode=mode)
        self.result_label.config(text=f"Sentiment: {sentiment}")
        self.confidence_label.config(text=f"Confidence: {confidence}")

if __name__ == "__main__":
    root = Tk()
    gui = SentimentDetectorGUI(root)
    root.mainloop()