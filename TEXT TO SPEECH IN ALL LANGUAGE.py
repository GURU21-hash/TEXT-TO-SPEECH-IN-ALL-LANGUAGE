import requests
import edge_tts
import asyncio
import os
from playsound3 import playsound


# ==========================================
# LANGUAGES
# ==========================================

languages = {
    "english": {
        "code": "en",
        "voice": "en-US-AriaNeural"
    },

    "tamil": {
        "code": "ta",
        "voice": "ta-IN-PallaviNeural"
    },

    "hindi": {
        "code": "hi",
        "voice": "hi-IN-SwaraNeural"
    },

    "telugu": {
        "code": "te",
        "voice": "te-IN-ShrutiNeural"
    },

    "malayalam": {
        "code": "ml",
        "voice": "ml-IN-SobhanaNeural"
    },

    "kannada": {
        "code": "kn",
        "voice": "kn-IN-SapnaNeural"
    },

    "bengali": {
        "code": "bn",
        "voice": "bn-IN-TanishaaNeural"
    },

    "marathi": {
        "code": "mr",
        "voice": "mr-IN-AarohiNeural"
    },

    "gujarati": {
        "code": "gu",
        "voice": "gu-IN-DhwaniNeural"
    },

    "punjabi": {
        "code": "pa",
        "voice": "pa-IN-OjasNeural"
    },

    "urdu": {
        "code": "ur",
        "voice": "ur-PK-AsadNeural"
    },

    "french": {
        "code": "fr",
        "voice": "fr-FR-DeniseNeural"
    },

    "german": {
        "code": "de",
        "voice": "de-DE-KatjaNeural"
    },

    "spanish": {
        "code": "es",
        "voice": "es-ES-ElviraNeural"
    },

    "italian": {
        "code": "it",
        "voice": "it-IT-ElsaNeural"
    },

    "japanese": {
        "code": "ja",
        "voice": "ja-JP-NanamiNeural"
    },

    "korean": {
        "code": "ko",
        "voice": "ko-KR-SunHiNeural"
    },

    "chinese": {
        "code": "zh-CN",
        "voice": "zh-CN-XiaoxiaoNeural"
    },

    "arabic": {
        "code": "ar",
        "voice": "ar-SA-ZariyahNeural"
    },

    "russian": {
        "code": "ru",
        "voice": "ru-RU-SvetlanaNeural"
    }
}


# ==========================================
# TRANSLATION
# ==========================================

def translate_text(text, target_language):

    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": text,
        "langpair": "en|" + target_language
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    data = response.json()

    return data["responseData"]["translatedText"]


# ==========================================
# TEXT TO SPEECH
# ==========================================

async def create_speech(text, voice):

    filename = "my_speech.mp3"

    communicate = edge_tts.Communicate(
        text,
        voice
    )

    await communicate.save(filename)

    return filename


# ==========================================
# MAIN PROGRAM
# ==========================================

print("======================================")
print("       TEXT TO SPEECH TRANSLATOR")
print("======================================")

text = input("\nEnter the text: ")

print("\nAvailable languages:")

for language in languages:
    print("-", language)

language = input(
    "\nWhich language should I speak? "
).lower().strip()


# Check selected language
if language not in languages:

    print("\nERROR: Language not found.")

else:

    target_code = languages[language]["code"]

    voice = languages[language]["voice"]

    print("\nTranslating...")

    translated_text = translate_text(
        text,
        target_code
    )

    if translated_text is None:

        print("\nTranslation failed.")

    else:

        print("\nTranslated text:")
        print(translated_text)

        print("\nSpeaking...")

        # Create speech
        filename = asyncio.run(
            create_speech(
                translated_text,
                voice
            )
        )

        # PLAY DIRECTLY THROUGH SPEAKER
        playsound(filename)

        # Delete temporary MP3
        if os.path.exists(filename):
            os.remove(filename)

        print("\nFinished.")
