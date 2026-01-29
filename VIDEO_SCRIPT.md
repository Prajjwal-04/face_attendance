# Video Walkthrough Script (2-3 Minutes)

## Setup Before Recording
- [ ] Install all dependencies
- [ ] Test the system works
- [ ] Prepare 2-3 test users
- [ ] Good lighting setup
- [ ] Clean browser (clear cache)
- [ ] Close unnecessary applications
- [ ] Test audio levels

## Video Structure

### Scene 1: Introduction (0:00 - 0:20)
**Screen**: Main interface showing all three tabs

**Script**:
"Hello! This is my Face Authentication Attendance System for the Medoc Health AI/ML internship assignment. The system provides complete face-based attendance tracking with registration, identification, and spoof detection capabilities. Let me show you how it works."

---

### Scene 2: System Overview (0:20 - 0:35)
**Screen**: Show the three tabs

**Script**:
"The system has three main modules: Registration for enrolling new users, Attendance for marking punch in and out, and Records for viewing attendance history. Let's start with registration."

---

### Scene 3: User Registration (0:35 - 1:15)
**Screen**: Registration tab

**Script**:
"To register a new user, I'll click the Register tab. First, I'll click 'Start Camera' to activate the webcam."

**Action**: Click Start Camera button

**Script**:
"Now I can see myself in the frame. The system requires good lighting and a frontal face view for best results. I'll enter the employee details - name and ID."

**Action**: Type "John Smith" and "EMP001"

**Script**:
"Now I'll click 'Capture & Register' to enroll this user."

**Action**: Click Capture & Register

**Script**:
"Perfect! The system detected the face, generated a 128-dimensional encoding using a pre-trained ResNet model, and stored it in the database. John is now registered."

---

### Scene 4: Face Identification & Attendance (1:15 - 2:15)
**Screen**: Mark Attendance tab

**Script**:
"Now let's mark attendance. I'll switch to the Mark Attendance tab and start the camera."

**Action**: Click Mark Attendance tab, then Start Camera

**Script**:
"The system is now continuously identifying faces. Within seconds, it recognizes me as John Smith with high confidence."

**Action**: Wait for identification to show

**Script**:
"Notice the green indicator showing 'Real Face' - this is our spoof detection system working. It uses texture analysis and motion detection to prevent attacks using printed photos or static images."

**Action**: Point to spoof indicator

**Script**:
"Now I can punch in for the day."

**Action**: Click Punch In button

**Script**:
"The system records the timestamp. At the end of the day, I would simply punch out using the same process."

**Action**: Show the punch-out button

---

### Scene 5: Attendance Records (2:15 - 2:35)
**Screen**: View Records tab

**Script**:
"Finally, let's check the attendance records. The View Records tab shows all attendance data in a clean table format."

**Action**: Switch to View Records tab

**Script**:
"Here we can see John Smith's punch-in time recorded for today. The system tracks punch-in, punch-out, and attendance status for all employees, organized by date."

---

### Scene 6: Technical Highlights (2:35 - 2:50)
**Screen**: Show documentation briefly or stay on records

**Script**:
"The system is built with Python, Flask, and the face_recognition library. It achieves 95-98% accuracy under ideal conditions and includes basic spoof detection with texture and motion analysis. The complete source code, documentation, and GitHub repository are included in my submission."

---

### Scene 7: Closing (2:50 - 3:00)
**Screen**: Main interface

**Script**:
"This system demonstrates practical face authentication with real-world considerations like lighting variations, spoof detection, and user experience. Thank you for watching, and I look forward to discussing the implementation in detail."

---

## Recording Tips

### Video Quality
- Resolution: 1080p minimum
- Frame rate: 30fps
- Format: MP4 (H.264)

### Audio
- Use a good microphone
- Speak clearly and at moderate pace
- Remove background noise

### Screen Recording Settings
- Record entire screen or application window
- Show mouse cursor
- Include system audio (optional)

### Editing Checklist
- [ ] Trim any dead space at start/end
- [ ] Add title card with your name (optional)
- [ ] Ensure audio is clear throughout
- [ ] Check video is under 3 minutes
- [ ] Export in MP4 format

## Software Recommendations

### Free Screen Recording
- **OBS Studio** (Windows/Mac/Linux)
  - Professional quality
  - Free and open-source
  - Excellent for live demos

- **QuickTime Player** (Mac)
  - Built-in, simple
  - Good quality
  - Screen recording feature

- **Xbox Game Bar** (Windows 10/11)
  - Built-in
  - Press Win+G to activate
  - Simple and quick

### Video Editing (Optional)
- **DaVinci Resolve** (Free, professional)
- **iMovie** (Mac, free)
- **Windows Video Editor** (Windows, free)

## Alternative: No-Edit Recording

If you want to do it in one take:
1. Practice 2-3 times before recording
2. Have notes visible on second monitor
3. Prepare users in advance
4. Test all features work
5. Record in one continuous take
6. Add a title card at the beginning (optional)

## Upload Destinations

Recommended platforms for sharing:
- **YouTube** (Unlisted link)
- **Loom** (Easy sharing)
- **Google Drive** (Direct download)
- **Vimeo** (Professional look)

Make sure to:
✅ Set appropriate privacy settings
✅ Generate shareable link
✅ Test link works before submitting
✅ Include link in your submission document

---

## Quick Reference: Key Points to Mention

### Technical
- ✅ Uses face_recognition library with ResNet-34
- ✅ 128-dimensional face embeddings
- ✅ Real-time identification (2-second intervals)
- ✅ Spoof detection (texture + motion)
- ✅ 95-98% accuracy under ideal conditions

### Features
- ✅ User registration with validation
- ✅ Automatic face identification
- ✅ Punch in/out tracking
- ✅ Attendance records by date
- ✅ Web-based interface

### Limitations (Optional to mention)
- ✅ Basic spoof detection (not production-grade)
- ✅ Requires frontal face view
- ✅ Sensitive to extreme lighting

---

Good luck with your recording! 🎬
