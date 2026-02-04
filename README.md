# DODO

Dodo AI is a simple, personal voice assistant built with Python. It listens to your voice commands, processes them intelligently, and responds with useful information and actions.

## Features

- **Voice Recognition**: Uses speech recognition to understand voice commands in English and Urdu
- **Text-to-Speech**: Responds with natural-sounding speech output
- **Multi-Language Support**: Supports translation between English and Urdu
- **Web Integration**: Can search Wikipedia, YouTube, and other web resources
- **Information Retrieval**: Provides weather, jokes, and general knowledge answers
- **Contact Management**: Stores and manages user contacts
- **Smart Command Processing**: Understands and executes various voice commands

## Project Structure

```
Dodo/
├── main.py           # Main chatbot logic and command processing
├── speech.py         # Text-to-speech module
├── contacts.txt      # Stored contacts database
└── README.md         # This file
```

## Requirements

- Python 3.x
- **Dependencies:**
  - `pyttsx3` - Text-to-speech engine
  - `speech_recognition` - Voice recognition
  - `pywhatkit` - YouTube and WhatsApp integration
  - `wikipedia` - Wikipedia search
  - `googletrans` - Language translation
  - `mtranslate` - Multi-language translation
  - `pyjokes` - Joke generation
  - `requests` - HTTP library

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saoodmasood1/DodoAI.git
cd DodoAI
```

Or download the repository as a ZIP file and extract it to your desired location.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Script

```bash
python main.py
```

### Prerequisites

- **Python 3.6+** installed on your system
- **pip** (Python package manager)
- **Microphone** for voice input
- **Internet connection** for voice recognition and web searches


## Running the Application

Run the main script to start Dodo AI:

```bash
python main.py
```

Dodo AI will:
1. Initialize and greet you with "Hello, I am Dodo AI. How can I help you?"
2. Wait for your voice input (up to 15 seconds for speech to start, 8 seconds max capture)
3. Process your command
4. Provide an audio response

## Example Commands

Try saying a few of the following commands.

- "Tell me something about the University of Oxford?" or "What is Metaphysics?" 
- "What is the weather in Lahore?" 
- "send a message to [contact name] saying that [your message]" 
- "Play the song [song name] of [singer name] on YouTube" or "Play the song Tu Jane Na of Atif Aslam on Youtube" 
- "Translate [enter your text] to [name language]" 
- "Search for [person name] on instagram/facebook/tiktok/etc."
- "Define [a topic in physics/bio/chemistry/CS/Maths]." 
- "Google that [enter you topic or question]."  
- "Open instagram/google/facebook/whatsapp."
- "What is 10 + 40 - 30?" or "What is 39098 / 45?"
- "What time is it?"
- "Play Aljazeera News"
- "Play the movie Veer"
- "Tell me a joke"
- "Tell me a story"
- "Say some poetry?"


## Configuration

You can adjust voice properties in `main.py`:

- **Voice Rate**: Change `engine.setProperty('rate', 170)` to adjust speaking speed
- **Volume**: Modify `engine.setProperty('volume', 1.0)` to change volume level
- **Voice Gender**: Change `voices[0].id` to `voices[1].id` for different voice options

## Contacts

Store your contacts in `contacts.txt` in the following format:

```
name, phone number
```

Example:
```
John Doe, 1234567890
Jane Smith, 0987654321
```


## Features in Development

- Advanced natural language processing
- More language support
- Calendar and reminder integration
- Custom command scripting

## License

This project is open source and available for personal use.

## Author

Created as a personal AI assistant project.


