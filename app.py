# import cv2
# import os
# import random

# # ------------------- SETTINGS -------------------
# FOLDER_PATH = r"C:\Users\JUNAID TANOLI\OneDrive\Desktop\Bootcamp\pro_roboflow\input_images\s0022"

# SAVE_MAIN = r"C:\Users\JUNAID TANOLI\OneDrive\Desktop\Bootcamp\pro_roboflow\input_images\output"
# LABELS_DIR = os.path.join(SAVE_MAIN, "labels")
# IMAGES_DIR = os.path.join(SAVE_MAIN, "images")
# ANNOTATED_DIR = os.path.join(SAVE_MAIN, "annotated")

# CLASSES = ["1", "2", "3", "4", "5"]
# IMG_SIZE = 640
# HANDLE_SIZE = 10
# # ------------------------------------------------

# # ----------------- STARTUP QUESTIONNAIRE -----------------
# print("Welcome to the Label Tool!")

# # 1. Choose Model
# models = ["YOLO11n", "COCO", "Custom"]
# print("Available models:")
# for i, m in enumerate(models):
#     print(f"{i+1}. {m}")

# model_choice = input("Enter the number of the model you want to use: ")
# try:
#     model_choice = int(model_choice) - 1
#     if 0 <= model_choice < len(models):
#         selected_model = models[model_choice]
#     else:
#         selected_model = models[0]
# except:
#     selected_model = models[0]

# print(f"Selected model: {selected_model}")

# # 2. Subsequence / Resume
# subsequence_choice = input("Do you want to resume from last session? (y/n): ").lower()
# resume = subsequence_choice == 'y'

# # 3. Start index
# images = sorted([f for f in os.listdir(FOLDER_PATH)
#                  if f.lower().endswith(('.jpg', '.png', '.jpeg'))])

# if resume:
#     last_index = input(f"Enter image index to start from (0-{len(images)-1}): ")
#     try:
#         index = int(last_index)
#         if index < 0 or index >= len(images):
#             index = 0
#     except:
#         index = 0
# else:
#     index = 0

# print(f"Starting labeling from image index: {index}")

# # ---------------- MAKE FOLDERS ----------------
# for f in [SAVE_MAIN, LABELS_DIR, IMAGES_DIR, ANNOTATED_DIR]:
#     if not os.path.exists(f):
#         os.makedirs(f)

# # ---------------- VARIABLES ----------------
# editing = False
# drawing = False
# ix, iy = -1, -1
# current_x, current_y = -1, -1
# current_class = 0
# boxes = []  # boxes for current image
# selected_box_index = -1
# resizing = False
# resizing_corner = None
# moving = False
# offset_x, offset_y = 0, 0

# template_boxes = []  # for propagation
# template_applied = False  # flag to track if template was applied

# # ---------------- FUNCTIONS ----------------
# def get_color_for_class(cid):
#     random.seed(cid * 50)
#     return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# def save_yolo(boxes, path):
#     lines = []
#     for (x1, y1, x2, y2, cid) in boxes:
#         xc = (x1 + x2) / 2 / IMG_SIZE
#         yc = (y1 + y2) / 2 / IMG_SIZE
#         ww = abs(x2 - x1) / IMG_SIZE
#         hh = abs(y2 - y1) / IMG_SIZE
#         lines.append(f"{cid} {xc} {yc} {ww} {hh}")
#     with open(path, "w") as f:
#         f.write("\n".join(lines))

# def mouse_event(event, x, y, flags, param):
#     global drawing, ix, iy, current_x, current_y
#     global boxes, editing, current_class, selected_box_index
#     global resizing, resizing_corner, moving, offset_x, offset_y, template_applied

#     if not editing:
#         return

#     # ---------------- RESIZE / MOVE SELECTED BOX ----------------
#     if selected_box_index != -1:
#         x1, y1, x2, y2, cid = boxes[selected_box_index]
#         corners = {'tl': (x1,y1), 'tr': (x2,y1), 'bl': (x1,y2), 'br': (x2,y2)}
#         for c_name, (cx, cy) in corners.items():
#             if abs(x-cx) <= HANDLE_SIZE and abs(y-cy) <= HANDLE_SIZE:
#                 if event == cv2.EVENT_LBUTTONDOWN:
#                     resizing = True
#                     resizing_corner = c_name
#                 break
#         else:
#             if x1 < x < x2 and y1 < y < y2:
#                 if event == cv2.EVENT_LBUTTONDOWN:
#                     moving = True
#                     offset_x = x - x1
#                     offset_y = y - y1

#     # Resizing
#     if resizing and event == cv2.EVENT_MOUSEMOVE:
#         bx = list(boxes[selected_box_index])
#         if resizing_corner == 'tl':
#             bx[0], bx[1] = x, y
#         elif resizing_corner == 'tr':
#             bx[2], bx[1] = x, y
#         elif resizing_corner == 'bl':
#             bx[0], bx[3] = x, y
#         elif resizing_corner == 'br':
#             bx[2], bx[3] = x, y
#         boxes[selected_box_index] = tuple(bx)
#         template_applied = False

#     if resizing and event == cv2.EVENT_LBUTTONUP:
#         resizing = False
#         resizing_corner = None

#     # Moving
#     if moving and event == cv2.EVENT_MOUSEMOVE:
#         w = x2 - x1
#         h = y2 - y1
#         boxes[selected_box_index] = (x - offset_x, y - offset_y, x - offset_x + w, y - offset_y + h, cid)
#         template_applied = False

#     if moving and event == cv2.EVENT_LBUTTONUP:
#         moving = False

#     # ---------------- DRAW NEW BOX ----------------
#     if event == cv2.EVENT_LBUTTONDOWN and not (resizing or moving):
#         drawing = True
#         ix, iy = x, y
#         selected_box_index = -1

#     elif event == cv2.EVENT_MOUSEMOVE and drawing:
#         current_x, current_y = x, y

#     elif event == cv2.EVENT_LBUTTONUP and drawing:
#         drawing = False
#         boxes.append((ix, iy, x, y, current_class))
#         current_x, current_y = -1, -1
#         template_applied = False

#     # ---------------- SELECT BOX ----------------
#     elif event == cv2.EVENT_RBUTTONDOWN:
#         selected_box_index = -1
#         for i, (x1, y1, x2, y2, cid) in enumerate(boxes):
#             if x1 <= x <= x2 and y1 <= y <= y2:
#                 selected_box_index = i
#                 print(f"Selected box {i} -> {CLASSES[cid]}")
#                 break

# # ---------------- MAIN LOOP ----------------
# cv2.namedWindow("Label Tool")
# cv2.setMouseCallback("Label Tool", mouse_event)

# while True:
#     img_path = os.path.join(FOLDER_PATH, images[index])
#     img = cv2.imread(img_path)
#     display_img = img.copy()

#     # Show image name
#     cv2.putText(display_img, images[index], (10, display_img.shape[0]-10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

#     # Draw boxes
#     for i, (x1, y1, x2, y2, cid) in enumerate(boxes):
#         color = get_color_for_class(cid)
#         thickness = 3 if i == selected_box_index else 2
#         cv2.rectangle(display_img, (x1, y1), (x2, y2), color, thickness)
#         cv2.putText(display_img, CLASSES[cid], (x1 + 5, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#         if i == selected_box_index:
#             for cx, cy in [(x1,y1),(x2,y1),(x1,y2),(x2,y2)]:
#                 cv2.circle(display_img, (cx, cy), HANDLE_SIZE, color, -1)

#     # Draw currently drawing box
#     if drawing and current_x != -1:
#         color = get_color_for_class(current_class)
#         cv2.rectangle(display_img, (ix, iy), (current_x, current_y), color, 2)
#         cv2.putText(display_img, CLASSES[current_class], (ix + 5, iy - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#     # Edit mode panel
#     if editing:
#         panel_height = 20 + len(CLASSES)*25
#         panel = cv2.copyMakeBorder(display_img, 0, panel_height, 0, 0,
#                                    cv2.BORDER_CONSTANT, value=(0,0,0))
#         y_start = display_img.shape[0] + 20
#         for i, cls in enumerate(CLASSES):
#             color = get_color_for_class(i)
#             text = f"{i+1} - {cls}"
#             cv2.putText(panel, text, (10, y_start + i*25),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#         display = panel
#     else:
#         display = display_img

#     cv2.imshow("Label Tool", display)
#     key = cv2.waitKey(1) & 0xFF

#     # ---------------- KEY EVENTS ----------------
#     if key == ord('k'):
#         editing = not editing

#     elif key == ord('s'):
#         base_name = images[index].rsplit('.', 1)[0]
#         resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
#         label_path = os.path.join(LABELS_DIR, base_name + ".txt")
#         save_yolo(boxes, label_path)
#         cv2.imwrite(os.path.join(IMAGES_DIR, base_name + ".jpg"), resized_img)

#         annotated = cv2.resize(img.copy(), (IMG_SIZE, IMG_SIZE))
#         for (x1, y1, x2, y2, cid) in boxes:
#             color = get_color_for_class(cid)
#             cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
#             cv2.putText(annotated, CLASSES[cid], (x1 + 5, y1 - 5),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
#         cv2.imwrite(os.path.join(ANNOTATED_DIR, base_name + "_annotated.jpg"), annotated)
#         print(f"\nSaved: {base_name}")

#         # Update template for subsequence propagation
#         if resume:
#             template_boxes = boxes.copy()
#             template_applied = True

#     elif key == ord('n'):
#         selected_box_index = -1
#         index += 1 if index < len(images)-1 else 0
#         # Propagate template if subsequence/resume is ON
#         if resume and template_applied:
#             boxes = [b for b in template_boxes]  # copy template
#         else:
#             boxes = []

#     elif key == ord('b'):
#         selected_box_index = -1
#         index -= 1 if index > 0 else 0
#         boxes = []  # no propagation backward

#     elif key == ord('d') and selected_box_index != -1:
#         print(f"Deleted box {selected_box_index}")
#         boxes.pop(selected_box_index)
#         selected_box_index = -1
#         template_applied = False

#     elif key == 8:  # Backspace key
#         if boxes:
#             removed = boxes.pop(-1)
#             print(f"Deleted last box -> {CLASSES[removed[4]]}")
#             selected_box_index = -1
#             template_applied = False

#     elif ord('1') <= key <= ord('9'):
#         cid = key - ord('1')
#         if cid < len(CLASSES):
#             if selected_box_index != -1:
#                 boxes[selected_box_index] = (*boxes[selected_box_index][:4], cid)
#                 print(f"Box {selected_box_index} class changed to {CLASSES[cid]}")
#             else:
#                 current_class = cid
#                 print("Current class for new boxes:", CLASSES[current_class])
#             template_applied = False

#     elif key == ord('q'):
#         break

# cv2.destroyAllWindows()
import streamlit as st
import cv2
import os
import random
import numpy as np
from PIL import Image
import io

# ------------------- SETTINGS -------------------
CLASSES = ["1", "2", "3", "4", "5"]
IMG_SIZE = 640
HANDLE_SIZE = 10

# ------------------- FUNCTIONS -------------------
def get_color_for_class(cid):
    random.seed(cid * 50)
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

def save_yolo(boxes, path):
    lines = []
    for (x1, y1, x2, y2, cid) in boxes:
        xc = (x1 + x2) / 2 / IMG_SIZE
        yc = (y1 + y2) / 2 / IMG_SIZE
        ww = abs(x2 - x1) / IMG_SIZE
        hh = abs(y2 - y1) / IMG_SIZE
        lines.append(f"{cid} {xc} {yc} {ww} {hh}")
    with open(path, "w") as f:
        f.write("\n".join(lines))

def draw_boxes_on_image(img, boxes, selected_box_index=-1):
    display_img = img.copy()
    for i, (x1, y1, x2, y2, cid) in enumerate(boxes):
        color = get_color_for_class(cid)
        thickness = 3 if i == selected_box_index else 2
        cv2.rectangle(display_img, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
        cv2.putText(display_img, CLASSES[cid], (int(x1) + 5, int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        if i == selected_box_index:
            for cx, cy in [(x1,y1),(x2,y1),(x1,y2),(x2,y2)]:
                cv2.circle(display_img, (int(cx), int(cy)), HANDLE_SIZE, color, -1)
    return display_img

# ------------------- STREAMLIT UI -------------------
st.set_page_config(page_title="YOLO Label Tool", layout="wide")
st.title("🏷️ YOLO Image Labeling Tool")

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.images = []
    st.session_state.current_index = 0
    st.session_state.boxes = []
    st.session_state.selected_box_index = -1
    st.session_state.current_class = 0
    st.session_state.template_boxes = []
    st.session_state.template_applied = False
    st.session_state.resume_mode = False
    st.session_state.folder_path = ""
    st.session_state.save_main = ""

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    models = ["YOLO11n", "COCO", "Custom"]
    selected_model = st.selectbox("Select Model", models)
    
    # Folder paths
    folder_path = st.text_input("Input Folder Path", 
                                value=r"C:\Users\JUNAID TANOLI\OneDrive\Desktop\Bootcamp\pro_roboflow\input_images\s0022")
    
    save_main = st.text_input("Output Folder Path",
                             value=r"C:\Users\JUNAID TANOLI\OneDrive\Desktop\Bootcamp\pro_roboflow\input_images\output")
    
    # Resume mode
    resume_mode = st.checkbox("Resume from last session")
    
    # Initialize button
    if st.button("🚀 Initialize/Load Images"):
        if os.path.exists(folder_path):
            images = sorted([f for f in os.listdir(folder_path)
                           if f.lower().endswith(('.jpg', '.png', '.jpeg'))])
            if images:
                st.session_state.images = images
                st.session_state.folder_path = folder_path
                st.session_state.save_main = save_main
                st.session_state.resume_mode = resume_mode
                st.session_state.initialized = True
                
                # Create output directories
                labels_dir = os.path.join(save_main, "labels")
                images_dir = os.path.join(save_main, "images")
                annotated_dir = os.path.join(save_main, "annotated")
                
                for d in [save_main, labels_dir, images_dir, annotated_dir]:
                    if not os.path.exists(d):
                        os.makedirs(d)
                
                st.success(f"✅ Loaded {len(images)} images!")
            else:
                st.error("❌ No images found in the folder!")
        else:
            st.error("❌ Folder path does not exist!")
    
    st.markdown("---")
    st.subheader("📊 Progress")
    if st.session_state.initialized:
        st.metric("Total Images", len(st.session_state.images))
        st.metric("Current Image", st.session_state.current_index + 1)

# Main content area
if st.session_state.initialized:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"📷 {st.session_state.images[st.session_state.current_index]}")
        
        # Load and display image
        img_path = os.path.join(st.session_state.folder_path, 
                               st.session_state.images[st.session_state.current_index])
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Draw boxes on image
        display_img = draw_boxes_on_image(img_rgb, st.session_state.boxes, 
                                         st.session_state.selected_box_index)
        
        st.image(display_img, use_container_width=True)
        
        # Navigation buttons
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
        
        with nav_col1:
            if st.button("⬅️ Previous (B)"):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
                    st.session_state.boxes = []
                    st.session_state.selected_box_index = -1
                    st.rerun()
        
        with nav_col2:
            if st.button("➡️ Next (N)"):
                if st.session_state.current_index < len(st.session_state.images) - 1:
                    st.session_state.current_index += 1
                    # Propagate template if resume mode is on
                    if st.session_state.resume_mode and st.session_state.template_applied:
                        st.session_state.boxes = [b for b in st.session_state.template_boxes]
                    else:
                        st.session_state.boxes = []
                    st.session_state.selected_box_index = -1
                    st.rerun()
        
        with nav_col3:
            if st.button("💾 Save (S)"):
                base_name = st.session_state.images[st.session_state.current_index].rsplit('.', 1)[0]
                
                # Save label
                labels_dir = os.path.join(st.session_state.save_main, "labels")
                label_path = os.path.join(labels_dir, base_name + ".txt")
                save_yolo(st.session_state.boxes, label_path)
                
                # Save resized image
                resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                images_dir = os.path.join(st.session_state.save_main, "images")
                cv2.imwrite(os.path.join(images_dir, base_name + ".jpg"), resized_img)
                
                # Save annotated image
                annotated = cv2.resize(img.copy(), (IMG_SIZE, IMG_SIZE))
                for (x1, y1, x2, y2, cid) in st.session_state.boxes:
                    color = get_color_for_class(cid)
                    cv2.rectangle(annotated, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                    cv2.putText(annotated, CLASSES[cid], (int(x1) + 5, int(y1) - 5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                annotated_dir = os.path.join(st.session_state.save_main, "annotated")
                cv2.imwrite(os.path.join(annotated_dir, base_name + "_annotated.jpg"), annotated)
                
                # Update template
                if st.session_state.resume_mode:
                    st.session_state.template_boxes = st.session_state.boxes.copy()
                    st.session_state.template_applied = True
                
                st.success(f"✅ Saved: {base_name}")
        
        with nav_col4:
            if st.button("🗑️ Delete Last Box (Backspace)"):
                if st.session_state.boxes:
                    removed = st.session_state.boxes.pop(-1)
                    st.session_state.selected_box_index = -1
                    st.session_state.template_applied = False
                    st.rerun()
    
    with col2:
        st.subheader("🎨 Classes")
        
        # Current class selection
        for i, cls in enumerate(CLASSES):
            color = get_color_for_class(i)
            color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            
            if st.button(f"{i+1} - {cls}", key=f"class_{i}", 
                        use_container_width=True):
                st.session_state.current_class = i
                st.success(f"Current class: {cls}")
        
        st.markdown("---")
        st.subheader("📦 Current Boxes")
        
        if st.session_state.boxes:
            for i, (x1, y1, x2, y2, cid) in enumerate(st.session_state.boxes):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.text(f"Box {i+1}: {CLASSES[cid]}")
                with col_b:
                    if st.button("❌", key=f"del_{i}"):
                        st.session_state.boxes.pop(i)
                        st.session_state.selected_box_index = -1
                        st.session_state.template_applied = False
                        st.rerun()
        else:
            st.info("No boxes yet. Use drawing tools below.")
        
        st.markdown("---")
        st.subheader("✏️ Add Box Manually")
        
        with st.form("add_box_form"):
            x1 = st.number_input("X1", min_value=0, max_value=IMG_SIZE, value=100)
            y1 = st.number_input("Y1", min_value=0, max_value=IMG_SIZE, value=100)
            x2 = st.number_input("X2", min_value=0, max_value=IMG_SIZE, value=200)
            y2 = st.number_input("Y2", min_value=0, max_value=IMG_SIZE, value=200)
            box_class = st.selectbox("Class", range(len(CLASSES)), 
                                    format_func=lambda x: CLASSES[x])
            
            if st.form_submit_button("➕ Add Box"):
                st.session_state.boxes.append((x1, y1, x2, y2, box_class))
                st.session_state.template_applied = False
                st.rerun()
        
        st.markdown("---")
        st.subheader("⌨️ Keyboard Shortcuts")
        st.text("N - Next image")
        st.text("B - Previous image")
        st.text("S - Save annotations")
        st.text("1-5 - Select class")
        st.text("Backspace - Delete last box")

else:
    st.info("👈 Please configure settings and click 'Initialize/Load Images' to start labeling!")
    
    st.markdown("---")
    st.subheader("📖 Instructions")
    st.markdown("""
    1. **Set Input Folder**: Path containing images to label
    2. **Set Output Folder**: Where labeled data will be saved
    3. **Select Model**: Choose your YOLO model type
    4. **Resume Mode**: Enable to propagate boxes to next image
    5. **Initialize**: Click to load images and start labeling
    6. **Add Boxes**: Use the manual box form or draw on image (future feature)
    7. **Save**: Save annotations in YOLO format
    8. **Navigate**: Move between images using Previous/Next buttons
    """)