"""
Demo Script - Face Authentication Attendance System
This script demonstrates the core functionality without the web interface
"""

import cv2
import numpy as np
from app import FaceAttendanceSystem
import time

def main():
    print("=" * 60)
    print("Face Authentication Attendance System - Demo")
    print("=" * 60)
    
    # Initialize the system
    system = FaceAttendanceSystem()
    
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("\nDemo Instructions:")
    print("1. Press 'R' to enter Registration mode")
    print("2. Press 'A' to enter Attendance mode")
    print("3. Press 'Q' to quit")
    print("4. Press 'S' to show statistics")
    print("\n")
    
    mode = None
    user_name = None
    user_id = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Display mode
        display_frame = frame.copy()
        
        if mode == "register":
            cv2.putText(display_frame, "REGISTRATION MODE", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(display_frame, "Press SPACE to capture", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        elif mode == "attendance":
            cv2.putText(display_frame, "ATTENDANCE MODE", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Try to identify
            name, uid, confidence, is_real = system.identify_face(frame, apply_spoof_detection=True)
            
            if uid:
                status_text = f"{name} (ID: {uid})"
                conf_text = f"Confidence: {confidence*100:.1f}%"
                spoof_text = f"Real: {'Yes' if is_real else 'NO - SPOOF!'}"
                
                color = (0, 255, 0) if is_real else (0, 0, 255)
                
                cv2.putText(display_frame, status_text, (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                cv2.putText(display_frame, conf_text, (10, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                cv2.putText(display_frame, spoof_text, (10, 130),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                cv2.putText(display_frame, "Press 'I' for Punch In", (10, 170),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(display_frame, "Press 'O' for Punch Out", (10, 195),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            else:
                cv2.putText(display_frame, "No face recognized", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        else:
            cv2.putText(display_frame, "Press R=Register | A=Attendance | Q=Quit", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Show the frame
        cv2.imshow('Face Attendance Demo', display_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\nExiting demo...")
            break
        
        elif key == ord('r'):
            mode = "register"
            print("\n--- Registration Mode ---")
            user_name = input("Enter name: ")
            user_id = input("Enter employee ID: ")
            print("Position your face and press SPACE to capture")
        
        elif key == ord('a'):
            mode = "attendance"
            print("\n--- Attendance Mode ---")
            print("Face the camera to be identified")
        
        elif key == ord('s'):
            print("\n--- System Statistics ---")
            print(f"Registered Users: {len(system.known_names)}")
            if len(system.known_names) > 0:
                print("Users:")
                for i, name in enumerate(system.known_names):
                    print(f"  - {name} (ID: {system.known_ids[i]})")
            print()
        
        elif key == ord(' ') and mode == "register":
            if user_name and user_id:
                print(f"Capturing image for {user_name}...")
                success, message = system.register_user(user_name, user_id, frame)
                print(message)
                if success:
                    mode = None
                    user_name = None
                    user_id = None
                time.sleep(1)
        
        elif key == ord('i') and mode == "attendance":
            name, uid, confidence, is_real = system.identify_face(frame)
            if uid and is_real:
                success, message = system.mark_attendance(uid, name, "punch_in")
                print(message)
                time.sleep(1)
            elif uid and not is_real:
                print("Cannot mark attendance - spoof detected!")
            else:
                print("No user identified")
        
        elif key == ord('o') and mode == "attendance":
            name, uid, confidence, is_real = system.identify_face(frame)
            if uid and is_real:
                success, message = system.mark_attendance(uid, name, "punch_out")
                print(message)
                time.sleep(1)
            elif uid and not is_real:
                print("Cannot mark attendance - spoof detected!")
            else:
                print("No user identified")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print("\nDemo completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
