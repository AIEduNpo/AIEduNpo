import os
import requests
import time
import random

# ================= CONFIGURATION =================
WIDTH = 768
HEIGHT = 1024
OUTPUT_FOLDER = "fake_images"
# =================================================

# The full list of 8 prompts
all_prompts = [
    # 1. Beer Toast
    "A slightly blurry smartphone photo taken at night inside a noisy Taiwanese 熱炒店 in Taipei. A group of local friends are casually clinking beer glasses over a messy round table with empty plates, cigarette ashtray, and sauce bottles. Uneven fluorescent lighting, motion blur from people moving, one face partially cut off by the frame. Background shows red plastic stools and handwritten Chinese menu signs on the wall. Feels unposed and accidental.",
    # 2. Hiking 101
    "A front-camera selfie taken on a smartphone by a Taiwanese woman hiking on 象山 (Elephant Mountain). Taipei 101 appears slightly off-center in the background, partially blocked by trees. The sky is cloudy and flat, lighting is dull. The photo is a bit tilted, with sweat on her forehead and messy hair. One finger slightly visible on the edge of the lens. Looks like a quick photo sent to friends, not social media polished.",
    # 3. Scooter Dog
    "A casual smartphone photo of a Shiba Inu sitting on the footrest of an old scooter parked in a narrow Taiwanese alley. The scooter has scratches and faded stickers. Background includes barred windows, stacked buckets, potted plants, and exposed pipes. Lighting is uneven with hard shadows. Slight noise and soft focus, like taken quickly without adjusting camera settings.",
    # 4. Bubble Tea POV
    "A close-up smartphone photo of a hand holding a half-finished bubble tea with condensation and fingerprints on the plastic cup. The straw is slightly bent. Background is a busy Taipei street but heavily blurred due to shallow focus and motion. The framing is awkward, cutting off part of the cup. Natural daylight, no stylized colors, looks like a quick snapshot before crossing the street.",
    # 5. Hotpot Family
    "A realistic indoor smartphone photo of a Taiwanese family eating hotpot at home around a crowded round table. Steam partially fogs the camera lens. Bowls, chopsticks, tissue box, and random plastic containers clutter the table. Lighting is warm but uneven from a ceiling lamp. One person is mid-bite, another slightly out of focus. The image is slightly grainy, like taken at night without flash.",
    # 6. Night Market
    "A handheld smartphone photo taken at a Taiwanese night market. People walking past food stalls selling fried chicken and stinky tofu. Steam and smoke partially obscure the scene. Red lanterns appear overexposed. Motion blur from moving crowds, uneven exposure, high ISO noise. Feels chaotic and unplanned, like taken while walking.",
    # 7. Rainy 7-Eleven
    "A rainy evening smartphone photo taken while standing at a Taipei crosswalk. Dozens of scooters waiting at a red light, some riders wearing ponchos. Wet road reflects traffic lights and a 7-Eleven sign in the background. Raindrops visible on the camera lens. Slight blur from hand movement. Neutral colors, no dramatic contrast.",
    # 8. Apartment Cat
    "A casual smartphone photo of a cat sleeping on an old Taiwanese terrazzo tile floor inside an apartment. The floor pattern is worn and faded. A standing fan, slippers, and tangled extension cords appear in the background. Indoor lighting is slightly yellow and flat. Framing is imperfect, cutting off part of the cat’s tail. Feels like a random moment at home."
]

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def generate_vertical_flux(prompt, file_number):
    seed = random.randint(1, 999999)
    url = f"https://pollinations.ai/p/{prompt}?width={WIDTH}&height={HEIGHT}&seed={seed}&model=flux&nologo=true"

    try:
        print(f"[{file_number}] Generating: {prompt[:30]}...")
        response = requests.get(url, timeout=60) # Set a timeout
        
        if response.status_code == 200:
            filename = f"{OUTPUT_FOLDER}/taiwan_fake_{file_number}.jpg"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"   ✅ Saved to {filename}")
        else:
            print(f"   ⚠️ Server Busy (Error {response.status_code}). Try again later.")

    except Exception as e:
        print(f"   ❌ Failed: {e}")

# --- MAIN MENU ---
print("--- Flux Generator (Batch Mode) ---")
print("1. Generate Photos 1 to 4")
print("2. Generate Photos 5 to 8")
choice = input("Enter 1 or 2: ")

if choice == "1":
    selected_prompts = all_prompts[:4] # First 4
    start_index = 1
elif choice == "2":
    selected_prompts = all_prompts[4:] # Last 4
    start_index = 5
else:
    print("Invalid choice, running Batch 1.")
    selected_prompts = all_prompts[:4]
    start_index = 1

print(f"\n--- Starting Batch {choice} ---")

for i, prompt in enumerate(selected_prompts):
    # Calculate the actual file number (1,2,3,4 OR 5,6,7,8)
    current_file_num = start_index + i
    
    generate_vertical_flux(prompt, current_file_num)
    
    # Wait 5 seconds between images to prevent Error 502/524
    if i < len(selected_prompts) - 1:
        print("   Thinking... (waiting 5s)")
        time.sleep(5)

print("\n--- Batch Complete! ---")