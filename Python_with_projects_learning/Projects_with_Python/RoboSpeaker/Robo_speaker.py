
import os
import platform
import subprocess

if __name__ == '__main__':
    print("Welcome to the Robo Speaker!")

    system = platform.system()

    while True:
        x = input("Enter what you want me to pronounce: ")

        if x.lower() == 'z':
            x = "Bye Bye Friend"
            exit_program = True
        else:
            exit_program = False

        if system == "Darwin":  # macOS
            subprocess.run(["say", x])

        elif system == "Windows":
            # Use Windows built-in text-to-speech
            escaped_text = x.replace("'", "''")
            command = (
                "Add-Type -AssemblyName System.Speech; "
                "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                f"$speaker.Speak('{escaped_text}')"
            )
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                check=False
            )

        else:
            print("This version supports Windows and macOS only.")

        if exit_program:
            break
