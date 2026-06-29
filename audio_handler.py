# import whisper
# import tempfile
# import os

# def transcribe_audio_bytes(audio_bytes: bytes) -> str:
#     time.sleep(1)
#     if not audio_bytes:
#         return "Error: No audio recorded. Please record again."
    
#     try:
#         print("Whisper AI Model is Loading...")
#         model = whisper.load_model("base")

#         # Explicitly naming the file as .wav
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#             temp_audio.write(audio_bytes)
#             temp_path = temp_audio.name

#         print("Transcription Start...")
#         # Use the file path directly
#         result = model.transcribe(temp_path, fp16=False)
#         extracted_text = result["text"].strip()
        
#         # Cleanup
#         os.remove(temp_path)
        
#         print("Transcription Complete")
#         return extracted_text

#     except Exception as e:
#         return f"System Error during transcription: {str(e)}"


import time
import whisper
import tempfile
import os

def transcribe_audio_bytes(audio_bytes: bytes) -> str:
    time.sleep(1)
    if not audio_bytes:
        return "Error: No audio recorded. Please record again."
    
    try:
        print("Whisper AI Model is Loading...")
        model = whisper.load_model("base")

        # Explicitly naming the file as .wav
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_path = temp_audio.name

        print("Transcription Start...")
        result = model.transcribe(temp_path, fp16=False)
        extracted_text = result["text"].strip()
        
        # Cleanup
        os.remove(temp_path)
        
        print("Transcription Complete")
        return extracted_text

    except Exception as e:
        return f"System Error during transcription: {str(e)}"
