# TDTU eLearning Deadline Scraper

This Python script (`deadLine_widget.py`) automatically scrapes upcoming assignment deadlines from the Tôn Đức Thắng University (TDTU) eLearning system and displays them in a simple widget.

## Features

- Automatically logs into TDTU's eLearning system.
- Extracts upcoming assignment deadlines from all enrolled courses.
- Displays deadlines in a compact GUI.

## Requirements

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver compatible with your Chrome version

## Setup

### 1. Clone the Repository

```bash
https://github.com/roddely/Elearning-Deadline-Scraping.git
cd your-repo-name
```

### 2. Install required Python packages

```bash
pip install -r requirements.txt
```

### 3. Fill in the password.txt file.

Line 1: Your TDTU email or username
Line 2: Your TDTU password
⚠️ Do not include extra spaces or blank lines.


### Running the Script
Make sure Google Chrome is installed and ChromeDriver is available in your system PATH or set explicitly in the code.
Run the script using:
```bash
python deadLine_widget.py
```


### License
This project is for educational use only and is not officially affiliated with TDTU.
