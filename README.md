# image-labeling-tool-yolo
YOLO Labeler Streamlit 🏷
A simple and interactive image labeling tool built with Streamlit for YOLO-based object detection projects.
Easily label your images, save YOLO-format annotations, and manage annotation sessions efficiently.

Features ✨
Label images for YOLO (YOLO11n, COCO, or Custom)
Resume labeling sessions (propagate boxes to next images)
Save labeled data in YOLO format
Annotated images for verification
Manual box addition and class selection
Keyboard shortcuts for faster labeling
Streamlit web-based interface (works in browser)
Installation ⚙
Clone the repository:
git clone https://github.com/YOUR_USERNAME/yolo-labeler-streamlit.git
cd yolo-labeler-streamlit
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
pip install -r requirements.txt
streamlit run app.py

Set input folder (images to label)

Set output folder (annotations and images will be saved)

Select YOLO model

Enable resume mode if needed

Click Initialize/Load Images to start

Draw boxes or add manually

Save annotations using Save button

Navigate using Next / Previous buttons

Keyboard Shortcuts ⌨

N - Next image

B - Previous image

S - Save annotations

1-5 - Select class

Backspace - Delete last box
Folder Structure 🗂
output/
├── images/          # Resized images
├── labels/          # YOLO .txt annotation files
└── annotated/       # Images with drawn boxes
Screenshots 📸

Contributing 🤝

Feel free to fork and improve features, such as:

Drawing boxes with mouse in Streamlit

Auto-propagation across images

Multiple class support

About
No description, website, or topics provided.
Resources
 Readme
 Activity
Stars
 0 stars
Watchers
 0 watching
Forks
 0 forks
Releases
No releases published
Create a new release
Packages
No packages published
Publish your first package
Footer
