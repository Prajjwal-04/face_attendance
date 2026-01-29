# Face Authentication Attendance System

A complete face recognition system for attendance management with spoof detection.

## Quick Start

### Installation

```bash
# Install dependencies
pip install flask opencv-python face-recognition numpy

# Run the application
python app.py
```

### Access the System

Open your browser and navigate to:
```
http://localhost:5000
```

## Features

✅ **Face Registration** - Enroll users with their face data  
✅ **Real-time Identification** - Recognize users instantly  
✅ **Attendance Tracking** - Punch in/out with timestamps  
✅ **Spoof Detection** - Basic protection against fake faces  
✅ **Web Interface** - Clean, modern UI  
✅ **Attendance Reports** - View daily records  

## System Requirements

- Python 3.7+
- Webcam
- Modern web browser (Chrome, Firefox, Safari)
- Good lighting conditions

## How It Works

### 1. Register Users
- Click "Register" tab
- Start camera
- Capture face image
- Enter name and employee ID

### 2. Mark Attendance
- Click "Mark Attendance" tab
- Start camera
- System identifies you automatically
- Click "Punch In" or "Punch Out"

### 3. View Records
- Click "View Records" tab
- Select date
- View attendance table

## Technical Details

### Face Recognition
- Uses dlib-based face_recognition library
- 128-dimensional face embeddings
- 99.38% accuracy on LFW benchmark
- Real-time processing

### Spoof Detection
- Texture analysis (Laplacian variance)
- Motion detection (frame differences)
- ~70% effectiveness against simple attacks

### Data Storage
- Face encodings: `database/face_encodings.pkl`
- Attendance records: `database/attendance.json`

## Project Structure

```
face_attendance_system/
├── app.py                  # Main Flask application
├── templates/
│   └── index.html         # Web interface
├── database/              # Data storage
│   ├── face_encodings.pkl
│   └── attendance.json
├── DOCUMENTATION.md       # Detailed documentation
└── README.md             # This file
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main interface |
| `/register` | POST | Register user |
| `/identify` | POST | Identify face |
| `/mark_attendance` | POST | Mark attendance |
| `/attendance_summary` | GET | Get records |

## Accuracy Expectations

### Ideal Conditions (95-98%)
- Good lighting
- Frontal face
- HD camera

### Real-World (85-92%)
- Variable lighting
- Slight rotation
- Standard webcam

## Known Limitations

❌ **Cannot detect**: Advanced spoofing (video replay, 3D masks)  
❌ **Struggles with**: Identical twins, extreme lighting, face masks  
❌ **Requires**: Frontal face view (±30°)  

## For Production Use

This is a demonstration system. For production deployment:

1. ✅ Add advanced liveness detection
2. ✅ Implement user authentication
3. ✅ Encrypt stored data
4. ✅ Add database backups
5. ✅ Use professional security cameras
6. ✅ Implement audit logging
7. ✅ Add multi-factor authentication

## Troubleshooting

**Camera not working?**
- Check browser permissions
- Try a different browser
- Ensure webcam is connected

**Low accuracy?**
- Improve lighting
- Face camera directly
- Re-register with better image

**Spoof detection issues?**
- Ensure natural movement
- Avoid static poses
- Use real camera input

## Documentation

For detailed information, see [DOCUMENTATION.md](DOCUMENTATION.md) which includes:
- Complete technical architecture
- Model training details
- Accuracy analysis
- Failure case analysis
- Performance benchmarks
- Security considerations

## Demo Video Script

To create your 2-3 minute walkthrough:

1. **Introduction** (15s)
   - Show the main interface
   - Explain the three tabs

2. **Registration Demo** (45s)
   - Show camera starting
   - Capture a face
   - Register a user
   - Show success message

3. **Attendance Demo** (60s)
   - Start attendance camera
   - Show face identification
   - Demonstrate spoof detection indicator
   - Mark punch-in
   - Mark punch-out

4. **Records Demo** (30s)
   - Show attendance table
   - Filter by date
   - Highlight key features

## Video Creation Tips

```bash
# Use screen recording software like:
# - OBS Studio (Free, Windows/Mac/Linux)
# - QuickTime (Mac)
# - Windows Game Bar (Windows)

# Recording checklist:
✅ Test audio before recording
✅ Close unnecessary applications
✅ Prepare sample users
✅ Practice the flow once
✅ Keep it concise and clear
```

## Development

### Local Development
```bash
# Install in development mode
pip install -r requirements.txt

# Run with auto-reload
export FLASK_ENV=development
python app.py
```

### Testing
```bash
# Test registration
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","user_id":"001","image":"..."}'

# Test identification
curl -X POST http://localhost:5000/identify \
  -H "Content-Type: application/json" \
  -d '{"image":"..."}'
```

## Credits

Built using:
- **face_recognition** - Face recognition library
- **OpenCV** - Computer vision
- **Flask** - Web framework
- **dlib** - Machine learning toolkit

## License

Educational and demonstration purposes only.

## Support

For issues or questions:
1. Check DOCUMENTATION.md
2. Review known limitations
3. Verify system requirements

---

**Made for**: Medoc Health AI/ML Intern Assignment  
**Version**: 1.0  
**Date**: January 2026
