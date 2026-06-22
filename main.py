import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

languages = [
    "English", "Arabic", "French", "German", "Spanish",
    "Italian", "Portuguese", "Russian", "Chinese", "Japanese",
    "Korean", "Hindi", "Turkish", "Dutch", "Greek",
    "Swedish", "Norwegian", "Danish", "Finnish", "Polish",
    "Czech", "Hungarian", "Romanian", "Ukrainian", "Thai",
    "Vietnamese", "Indonesian", "Malay", "Hebrew", "Persian"
]

while True:
    print("\n===== AI Email Writer =====")

    purpose = input("What is the purpose of the email? ")
    recipient = input("Who is this email for? ")
    sender = input("What is the sender name? ")

    print("\nChoose a language (1-30):")

    for i, language in enumerate(languages, start=1):
        print(f"{i}. {language}")

    try:
        language = languages[int(input("Choose a language: ")) - 1]
    except:
        print("Invalid language choice.")
        continue

    print("\nChoose a tone:")
    print("1. Formal")
    print("2. Friendly")
    print("3. Polite")

    tones = {
        "1": "Formal",
        "2": "Friendly",
        "3": "Polite"
    }

    tone_choice = input("Choose your tone (1-3): ")

    if tone_choice not in tones:
        print("Invalid tone choice.")
        continue

    tone = tones[tone_choice]

    print("\nChoose email length:")
    print("1. Short")
    print("2. Medium")
    print("3. Detailed")

    lengths = {
        "1": "Short",
        "2": "Medium",
        "3": "Detailed"
    }

    length_choice = input("Choose length (1-3): ")

    if length_choice not in lengths:
        print("Invalid length choice.")
        continue

    length = lengths[length_choice]

    prompt = f"""
Write a {length} email in {language}.

Purpose: {purpose}
Recipient: {recipient}
Tone: {tone}
Sender: {sender}

Only write the email.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        if "choices" not in result:
            print("\nAPI Error:")
            print(result)
            continue

        email = result["choices"][0]["message"]["content"]

        print("\n===== Generated Email =====\n")
        print(email)

        print("\nImprove this email?")
        print("1. Make it more professional")
        print("2. Make it friendlier")
        print("3. Make it shorter")
        print("4. Make it more persuasive")
        print("5. Skip")

        improve_choice = input("Choose an option: ")

        improvements = {
            "1": "Make this email more professional.",
            "2": "Make this email friendlier.",
            "3": "Make this email shorter while keeping the main message.",
            "4": "Make this email more persuasive."
        }

        if improve_choice in improvements:

            improve_prompt = f"""
{improvements[improve_choice]}

Email:
{email}

Only return the improved email.
"""

            improve_data = {
                "model": "meta/llama-3.1-8b-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": improve_prompt
                    }
                ],
                "max_tokens": 500
            }

            improve_response = requests.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers=headers,
                json=improve_data
            )

            improve_result = improve_response.json()

            if "choices" in improve_result:
                email = improve_result["choices"][0]["message"]["content"]

                print("\n===== Improved Email =====\n")
                print(email)

        timestamp = datetime.now().strftime("%d/%m/%Y at %I:%M %p")

        print(f"\nGenerated on: {timestamp}")
        print(f"Words: {len(email.split())}")

        save = input("\nSave to file? (yes/no): ")

        if save.lower() == "yes":
            filename = input("Enter file name: ")

            with open(filename + ".txt", "w", encoding="utf-8") as file:
                file.write(email)
                file.write(f"\n\nGenerated on: {timestamp}")

            print("Email saved successfully!")

    except Exception as e:
        print(f"\nError: {e}")

    again = input("\nGenerate another email? (yes/no): ")

    if again.lower() != "yes":
        print("Thank you for using AI Email Writer!")
        break
