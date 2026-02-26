import cv2
import sys

# Test different URL formats for IP Webcam
urls = [
    "http://10.38.254.194:8080/video",
    "http://10.38.254.194:8080/videofeed",
    "http://10.38.254.194:8080/shot.jpg",
]

print("Testing phone camera connection...")
print("=" * 50)

for url in urls:
    print(f"\nTrying: {url}")
    cap = cv2.VideoCapture(url)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"✓ SUCCESS! Working URL: {url}")
            print(f"  Frame size: {frame.shape}")
            cap.release()
            sys.exit(0)
        else:
            print(f"✗ Opened but couldn't read frame")
    else:
        print(f"✗ Failed to open")
    
    cap.release()

print("\n" + "=" * 50)
print("❌ Could not connect to phone camera")
print("\nTroubleshooting:")
print("1. Make sure IP Webcam app is running on your phone")
print("2. Check that your phone shows 'Video connections: 0'")
print("3. Verify your phone and PC are on the same WiFi network")
print("4. Try opening http://192.168.1.103:8080 in your browser")
print("5. Check if your phone's IP changed")
