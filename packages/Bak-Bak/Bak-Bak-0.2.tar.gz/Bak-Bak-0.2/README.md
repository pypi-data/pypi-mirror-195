# Bak-Bak
 Python library for speech synthesis using SAPI.SpVoice, which is the Microsoft Speech API that allows Windows applications to use voice synthesis and recognition functionality. With Bak-Bak, you can easily add text-to-speech capabilities to your Python applications on Windows.

## Installation

To install Bak-Bak, use pip:

```bash
pip install Bak-Bak
```
Bak-Bak is a Python library for speech synthesis using SAPI.SpVoice, which is the Microsoft Speech API that allows Windows applications to use voice synthesis and recognition functionality. With Bak-Bak, you can easily add text-to-speech capabilities to your Python applications on Windows.

Features:
- Simple API for synthesizing speech from text
- Supports multiple voices
- Ability to save synthesized speech as a WAV file

## Usage
To use Bak-Bak, simply import the speak function from the bakbak module and call it with the message you want to speak:
```bash
import bakbak

bakbak.speak("Hello, world!")
```
By default, Bak-Bak uses the first available voice on your system. You can specify a different voice using the speaker_number parameter. You can also use the speak function to save the synthesized speech as a WAV file:
```bash
import bakbak
```
# Use the third voice and save the speech as a file
```bash
bakbak.speak("Hello, world!", speaker_number=2, filename="hello.wav")
```
Bak-Bak also provides a get_voices function that returns a list of available voices on your system:
```bash
import bakbak

voices = bakbak.get_voices()
for i, voice in enumerate(voices):
    print(f"{i + 1}. {voice['name']}")
```
## Requirements
- Python 3.6 or higher
- pypiwin32 package
## License
Bak-Bak is released under the MIT License. See the LICENSE file for more details.

