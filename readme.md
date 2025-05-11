# FaceTrack Attendance System

## Overview
FaceTrack Attendance System is a modern solution designed to replace traditional fingerprint attendance systems. Developed specifically for our department to overcome the limitations of fingerprint scanners (such as failures due to sweat), this system uses facial recognition technology to provide a contactless, reliable, and efficient attendance tracking solution.

## Key Features
- **Facial Recognition**: Accurately identifies and verifies personnel using advanced facial recognition algorithms
- **Contactless Operation**: Eliminates issues associated with fingerprint scanners (sweat, dirt, oils)
- **User-Friendly Interface**: Built with Tkinter for an intuitive and accessible user experience
- **Real-time Processing**: Provides immediate attendance verification
- **Secure Database**: Safely stores attendance records and facial data
- **Detailed Reporting**: Generates attendance reports for administrative purposes

## Technologies Used
- **Python**: Core programming language
- **Tkinter**: GUI framework for the user interface
- **Face Recognition API**: Handles facial detection and identification
- **SQLite/MySQL**: Database management (modify as per your actual implementation)
- **OpenCV**: Computer vision functionality

## System Requirements
- Python 3.7+
- Required Python packages (see Installation section)
- Webcam/camera for facial recognition
- Sufficient processing power for real-time facial recognition

## Installation

### Prerequisites
Ensure you have Python 3.7 or newer installed on your system.

### Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/face-recognition.git
   cd face-recognition
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the system parameters in `config.py` (if applicable)

4. Run the application:
   ```
   python main.py
   ```

## Usage
1. Launch the application using the instructions above
2. Register new users through the admin panel
3. Users can mark attendance by facing the camera
4. Access attendance records and reports through the system interface

## Project Structure
- `main.py` - Core application logic and system operations
- `util.py` - Tkinter UI functionality and interface components
- `db/` - Database files and management scripts
- `logs` - It consists of the logs of the student

## Contributing
Contributions to improve FaceTrack Attendance System are welcome. Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---
© 2025 Balaji