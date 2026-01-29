"""
Face Authentication Attendance System
A complete system for face-based attendance with registration, identification, and spoof detection
"""

import pickle
import os
from datetime import datetime
import json
from flask import Flask, render_template, request, jsonify, Response
import base64
import numpy as np
import random

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import face_recognition
except ImportError:
    face_recognition = None

app = Flask(__name__)

class FaceAttendanceSystem:
    def __init__(self):
        self.database_path = "database"
        self.encodings_file = f"{self.database_path}/face_encodings.pkl"
        self.attendance_file = f"{self.database_path}/attendance.json"
        
        # Create database directory if it doesn't exist
        os.makedirs(self.database_path, exist_ok=True)
        
        # Load existing encodings or create new
        self.load_encodings()
        self.load_attendance()
        
        # Spoof detection parameters
        self.texture_threshold = 100.0  # Laplacian variance threshold (higher = more texture detail)
        self.brightness_threshold = 40  # Brightness variance threshold
        self.motion_frames = []
        self.max_motion_frames = 5
        
        # Check if face recognition is available
        self.face_recognition_available = face_recognition is not None and cv2 is not None
        
    def load_encodings(self):
        """Load face encodings from database"""
        if os.path.exists(self.encodings_file):
            try:
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_encodings = data['encodings']
                    self.known_names = data['names']
                    self.known_ids = data['ids']
            except:
                self.known_encodings = []
                self.known_names = []
                self.known_ids = []
        else:
            self.known_encodings = []
            self.known_names = []
            self.known_ids = []
    
    def save_encodings(self):
        """Save face encodings to database"""
        data = {
            'encodings': self.known_encodings,
            'names': self.known_names,
            'ids': self.known_ids
        }
        with open(self.encodings_file, 'wb') as f:
            pickle.dump(data, f)
    
    def load_attendance(self):
        """Load attendance records"""
        if os.path.exists(self.attendance_file):
            try:
                with open(self.attendance_file, 'r') as f:
                    self.attendance_records = json.load(f)
            except:
                self.attendance_records = {}
        else:
            self.attendance_records = {}
    
    def save_attendance(self):
        """Save attendance records"""
        with open(self.attendance_file, 'w') as f:
            json.dump(self.attendance_records, f, indent=2)
    
    def register_user(self, name, user_id, image):
        """
        Register a new user with their face
        Returns: (success, message)
        """
        if not self.face_recognition_available or image is None:
            # In demo mode or if image is None, just add the user without face encoding
            if user_id in self.known_ids:
                return False, f"User ID {user_id} already registered"
            
            # Generate a mock encoding (random array)
            mock_encoding = np.random.rand(128)
            self.known_encodings.append(mock_encoding)
            self.known_names.append(name)
            self.known_ids.append(user_id)
            self.save_encodings()
            return True, f"User {name} registered successfully (Demo mode - Face recognition not available)"
        
        # Real face recognition mode
        try:
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_image)
            
            if len(face_locations) == 0:
                return False, "No face detected in the image"
            
            if len(face_locations) > 1:
                return False, "Multiple faces detected. Please ensure only one person is in frame"
            
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
            
            if len(face_encodings) == 0:
                return False, "Could not generate face encoding"
            
            if user_id in self.known_ids:
                return False, f"User ID {user_id} already registered"
            
            self.known_encodings.append(face_encodings[0])
            self.known_names.append(name)
            self.known_ids.append(user_id)
            
            self.save_encodings()
            return True, f"User {name} registered successfully"
        except Exception as e:
            print(f"Registration error: {e}")
            return False, f"Error during registration: {str(e)}"
    
    def identify_face(self, frame, apply_spoof_detection=True):
        """
        Identify face in the frame and check for spoofing
        Returns: (name, user_id, confidence, is_real)
        """
        print(f"identify_face called with frame: {frame is not None}, face_recognition_available: {self.face_recognition_available}")
        
        if not self.face_recognition_available or frame is None:
            print("Using demo mode - face recognition not available or no frame")
            # Demo mode: randomly select a registered user or return unknown
            if len(self.known_ids) > 0 and random.random() > 0.3:  # 70% chance to identify someone
                idx = random.randint(0, len(self.known_ids) - 1)
                return self.known_names[idx], self.known_ids[idx], random.uniform(0.85, 0.99), True
            return None, None, 0, False
        
        try:
            # Real face recognition mode
            print("Converting frame to RGB...")
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            print(f"RGB frame shape: {rgb_frame.shape}")
            
            print("Detecting faces...")
            face_locations = face_recognition.face_locations(rgb_frame)
            print(f"Found {len(face_locations)} faces")
            
            if len(face_locations) == 0:
                print("No faces detected")
                return None, None, 0, False
            
            face_location = face_locations[0]
            print(f"Using face location: {face_location}")
            
            print("Generating face encodings...")
            face_encodings = face_recognition.face_encodings(rgb_frame, [face_location])
            print(f"Generated {len(face_encodings)} encodings")
            
            if len(face_encodings) == 0:
                print("No face encodings generated")
                return None, None, 0, False
            
            face_encoding = face_encodings[0]
            print("Face encoding generated successfully")
            
            is_real = True
            if apply_spoof_detection:
                top, right, bottom, left = face_location
                face_region = frame[top:bottom, left:right]
                
                try:
                    gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
                    
                    # Check 1: Laplacian variance (detects edge sharpness)
                    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                    laplacian_var = laplacian.var()
                    texture_score = 1 if laplacian_var > self.texture_threshold else 0
                    
                    # Check 2: Local Binary Patterns (LBP) could detect print artifacts
                    # For now, using brightness contrast as proxy
                    hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
                    s_channel = hsv[:, :, 1]
                    saturation_mean = s_channel.mean()
                    saturation_std = s_channel.std()
                    saturation_score = 1 if saturation_std > self.brightness_threshold else 0
                    
                    # Check 3: Face region shouldn't be too uniform (real faces have texture)
                    brightness_var = gray.var()
                    brightness_score = 1 if brightness_var > 500 else 0
                    
                    # Composite score: at least 2 out of 3 checks should pass for real face
                    spoof_score = texture_score + saturation_score + brightness_score
                    is_real = spoof_score >= 2
                    
                    print(f"Spoof detection: laplacian_var={laplacian_var:.2f} (threshold={self.texture_threshold}), "
                          f"sat_std={saturation_std:.2f}, brightness_var={brightness_var:.2f}, "
                          f"score={spoof_score}/3, is_real={is_real}")
                except Exception as e:
                    print(f"Spoof detection error: {e}")
                    is_real = True
            
            if len(self.known_encodings) == 0:
                print("No known encodings in database")
                return "Unknown", None, 0, is_real
            
            print(f"Comparing against {len(self.known_encodings)} known encodings...")
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=0.55)
            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
            
            if len(face_distances) == 0:
                print("No face distances calculated")
                return "Unknown", None, 0, is_real
            
            best_match_index = np.argmin(face_distances)
            print(f"Best match index: {best_match_index}, distance: {face_distances[best_match_index]}, match: {matches[best_match_index]}")
            
            best_distance = face_distances[best_match_index]
            
            # Accept match if distance is reasonable (< 0.6 is good, < 0.65 is acceptable)
            if best_distance < 0.65:
                name = self.known_names[best_match_index]
                user_id = self.known_ids[best_match_index]
                confidence = 1 - best_distance
                print(f"✓ Match found: {name} ({user_id}) with confidence {confidence:.2%}, distance {best_distance:.4f}")
                return name, user_id, confidence, is_real
            
            print(f"✗ No match found - best distance was {best_distance:.4f} (threshold: 0.65)")
            return "Unknown", None, 0, is_real
            
        except Exception as e:
            print(f"Face recognition error: {e}")
            import traceback
            traceback.print_exc()
            return None, None, 0, False
    
    def mark_attendance(self, user_id, name, action="punch_in"):
        """
        Mark attendance (punch-in or punch-out)
        Returns: (success, message)
        """
        today = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        if today not in self.attendance_records:
            self.attendance_records[today] = {}
        
        if user_id not in self.attendance_records[today]:
            self.attendance_records[today][user_id] = {
                "name": name,
                "punch_in": None,
                "punch_out": None,
                "status": "absent"
            }
        
        user_record = self.attendance_records[today][user_id]
        
        if action == "punch_in":
            if user_record["punch_in"]:
                return False, f"Already punched in at {user_record['punch_in']}"
            user_record["punch_in"] = current_time
            user_record["status"] = "present"
            message = f"Punch-in recorded at {current_time}"
        
        elif action == "punch_out":
            if not user_record["punch_in"]:
                return False, "Cannot punch-out without punching in first"
            if user_record["punch_out"]:
                return False, f"Already punched out at {user_record['punch_out']}"
            user_record["punch_out"] = current_time
            message = f"Punch-out recorded at {current_time}"
        
        self.save_attendance()
        return True, message
    
    def get_attendance_summary(self, date=None):
        """Get attendance summary for a specific date"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if date not in self.attendance_records:
            return {}
        
        return self.attendance_records[date]

# Initialize the system
attendance_system = FaceAttendanceSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    """Check system status"""
    return jsonify({
        'face_recognition_available': attendance_system.face_recognition_available,
        'mode': 'Real' if attendance_system.face_recognition_available else 'Demo',
        'message': 'Face recognition is available' if attendance_system.face_recognition_available else 'Running in demo mode - install dlib for real face recognition'
    })

@app.route('/register', methods=['POST'])
def register():
    """API endpoint for user registration"""
    try:
        data = request.json
        name = data.get('name')
        user_id = data.get('user_id')
        image_data = data.get('image')
        
        print(f"Registration request: name={name}, user_id={user_id}, image_data_length={len(image_data) if image_data else 0}")
        
        # Decode base64 image if face recognition is available
        image = None
        if attendance_system.face_recognition_available and image_data:
            try:
                # Remove the data:image/jpeg;base64, prefix if present
                if ',' in image_data:
                    image_bytes = base64.b64decode(image_data.split(',')[1])
                else:
                    image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if image is not None:
                    print(f"Image decoded successfully: shape={image.shape}")
                else:
                    print("Image decoding returned None")
            except Exception as e:
                print(f"Image decoding error: {e}")
                pass
        
        success, message = attendance_system.register_user(name, user_id, image)
        
        print(f"Registration result: success={success}, message={message}")
        
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        print(f"Register endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/identify', methods=['POST'])
def identify():
    """API endpoint for face identification"""
    try:
        data = request.json
        image_data = data.get('image')
        
        frame = None
        if attendance_system.face_recognition_available and image_data:
            try:
                # Remove the data:image/jpeg;base64, prefix if present
                if ',' in image_data:
                    image_bytes = base64.b64decode(image_data.split(',')[1])
                else:
                    image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is not None:
                    print(f"Image decoded successfully: shape={frame.shape}")
                else:
                    print("Image decoding returned None")
            except Exception as e:
                print(f"Image decoding error: {e}")
                pass
        
        name, user_id, confidence, is_real = attendance_system.identify_face(frame)
        
        print(f"Identification result: name={name}, user_id={user_id}, confidence={confidence}, is_real={is_real}")
        
        return jsonify({
            'name': name,
            'user_id': user_id,
            'confidence': float(confidence) if confidence else 0,
            'is_real': bool(is_real) if is_real is not None else False,
            'identified': user_id is not None
        })
    except Exception as e:
        print(f"Identify endpoint error: {e}")
        return jsonify({
            'error': str(e),
            'identified': False
        })

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    """API endpoint for marking attendance"""
    try:
        data = request.json
        user_id = data.get('user_id')
        name = data.get('name')
        action = data.get('action', 'punch_in')
        
        success, message = attendance_system.mark_attendance(user_id, name, action)
        
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/test_face_recognition')
def test_face_recognition():
    """Test endpoint to check if face recognition is working"""
    try:
        import face_recognition
        import cv2
        import numpy as np
        
        # Test basic functionality
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[25:75, 25:75] = [255, 255, 255]  # White square
        
        # Test face detection (should return empty)
        locations = face_recognition.face_locations(test_image)
        
        return jsonify({
            'status': 'Face recognition libraries loaded successfully',
            'face_recognition_version': face_recognition.__version__ if hasattr(face_recognition, '__version__') else 'unknown',
            'opencv_version': cv2.__version__,
            'numpy_version': np.__version__,
            'face_detection_test': f'Found {len(locations)} faces in test image (expected 0)',
            'face_recognition_available': attendance_system.face_recognition_available,
            'known_users_count': len(attendance_system.known_ids)
        })
    except Exception as e:
        return jsonify({
            'status': 'Error testing face recognition',
            'error': str(e)
        })

@app.route('/attendance_summary')
def get_attendance_summary():
    """API endpoint for getting attendance summary"""
    date = request.args.get('date', None)
    summary = attendance_system.get_attendance_summary(date)
    return jsonify(summary)

@app.route('/users')
def get_users():
    """Get list of registered users"""
    users = []
    for i, user_id in enumerate(attendance_system.known_ids):
        users.append({
            'id': user_id,
            'name': attendance_system.known_names[i]
        })
    return jsonify(users)

if __name__ == '__main__':
    print("Starting Face Authentication Attendance System...")
    if attendance_system.face_recognition_available:
        print("✓ Face recognition is available")
    else:
        print("⚠ Face recognition library not available - Running in DEMO mode")
        print("  To enable real face recognition, install dlib:")
        print("  1. Install CMake from https://cmake.org/download/")
        print("  2. Run: pip install dlib face-recognition")
    print("\nOpen http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)