import streamlit as st
import json
import datetime
from PIL import Image
import numpy as np
from streamlit_webrtc import webrtc_streamer, WebRtcMode
# import numpy as np
from pyzbar.pyzbar import decode
import cv2
# from helpers import change

# File paths for data
inventory_file = "inventory.json"
restocking_file = "restocking.json"

# Initialize files
def initialize_file(file_path, default_content):
    try:
        with open(file_path, "r") as file:
            json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(file_path, "w") as file:
            json.dump(default_content, file)

initialize_file(inventory_file, [])
initialize_file(restocking_file, [])

# Load and save JSON data
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)



def decode_barcode_from_image(image):
    # Convert the image to grayscale for better barcode detection
    
    # Decode barcodes
    barcodes = decode(image)
    print(barcodes)
    decoded_info = []
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        decoded_info.append(barcode_data)
        
        # Draw a rectangle around the barcode
        pts = np.array(barcode.polygon, dtype=np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], True, (0, 255, 0), 5)
    
    return decoded_info, image

def manage_inventory_page():
    st.header("Manage Inventory")
    action = st.radio("Choose an action:", ["Add Item", "Edit/Delete Item"])
    inventory = load_data(inventory_file)

    if action == "Add Item":
        st.subheader("Add New Item")
        st.write("Upload the image of the item to scan the barcode.")

        # Image upload field
        uploaded_image = st.file_uploader("Upload Item Image", type=["png", "jpg", "jpeg"])

        if uploaded_image:
            # Read the uploaded image
            file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)



            # Decode barcode from the uploaded image
            decoded_info, image_with_bboxes = decode_barcode_from_image(image)

            # Display the image with bounding boxes
            st.image(image_with_bboxes, caption="Image with Barcode", use_column_width=True)

            if decoded_info:
                st.success(f"Barcode detected: {decoded_info[0]}")
                # Allow the user to enter item details manually
                name = st.text_input("Enter Item Name")
                aisle = st.number_input("Enter Aisle Number (1-8):", min_value=1, max_value=8, step=1)
                cases = st.number_input("Number of Cases:", min_value=0, step=1)
                
                if st.button("Add Item"):
                    if not name:
                        st.error("Please provide the item name.")
                    else:
                        new_item = {
                            "barcode": decoded_info[0],
                            "name": name,
                            "aisle": aisle,
                            "cases": cases,
                        }
                        inventory.append(new_item)
                        save_data(inventory_file, inventory)
                        st.success(f"Item '{name}' added successfully!")
            else:
                st.warning("No barcode detected. Please try another image.")

    elif action == "Edit/Delete Item":
        st.subheader("Edit or Delete Items")
        search_query = st.text_input("Search by Name or Barcode")
        matching_items = [
            item for item in inventory
            if search_query.lower() in item["name"].lower() or search_query == item["barcode"]
        ]

        if matching_items:
            for item in matching_items:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(item.get("image_path", None), use_column_width=True)
                with col2:
                    st.write(f"**{item['name']}** (Barcode: {item['barcode']})")
                    new_cases = st.number_input(
                        f"Update Cases for {item['name']}",
                        min_value=0,
                        value=item["cases"],
                        step=1,
                        key=f"cases_{item['barcode']}",
                    )
                    if st.button("Update", key=f"update_{item['barcode']}"):
                        item["cases"] = new_cases
                        save_data(inventory_file, inventory)
                        st.success(f"Updated '{item['name']}' cases to {new_cases}.")
                    if st.button("Delete", key=f"delete_{item['barcode']}"):
                        inventory.remove(item)
                        save_data(inventory_file, inventory)
                        st.warning(f"Deleted '{item['name']}'.")
        else:
            st.warning("No matching items found.")
# Streamlit interface for Add Inventory page
# def manage_inventory_page():
#     st.header("Manage Inventory")
#     action = st.radio("Choose an action:", ["Add Item", "Edit/Delete Item"])
#     inventory = load_data(inventory_file)
#     if action == "Add Item":
#         st.subheader("Add New Item")
#         st.write("Click to scan the barcode of the item.")

#         # Set up the WebRTC component for camera access
#         webrtc_ctx = webrtc_streamer(
#             key="add_inventory_video",
#             mode=WebRtcMode.SENDRECV,
#             video_frame_callback=video_frame_callback,
#             media_stream_constraints={"video": True},
#         )

#         # Display the barcode and allow manual item entry after scanning
#         if webrtc_ctx.video_receiver:
#             barcode = None
#             for obj in decode(webrtc_ctx.video_receiver.get_frame()):

#                 barcode = obj.data.decode("utf-8")
#                 if barcode:
#                     break
            
#             if barcode:
#                 st.success(f"Barcode detected: {barcode}")
#                 name = st.text_input("Enter Item Name")
#                 aisle = st.number_input("Enter Aisle Number (1-8):", min_value=1, max_value=8, step=1)
#                 cases = st.number_input("Number of Cases:", min_value=0, step=1)
#                 image_file = st.file_uploader("Upload Item Image", type=["png", "jpg", "jpeg"])

#                 if st.button("Add Item"):
#                     if not name or not image_file:
#                         st.error("Please provide all required fields.")
#                     else:
#                         image_path = f"static/{barcode}.jpg"
#                         with open(image_path, "wb") as f:
#                             f.write(image_file.getbuffer())

#                         new_item = {
#                             "barcode": barcode,
#                             "name": name,
#                             "aisle": aisle,
#                             "cases": cases,
#                             "image_path": image_path,
#                         }
#                         inventory.append(new_item)
#                         save_data(inventory_file, inventory)
#                         st.success(f"Item '{name}' added successfully!")
#             else:
#                 st.warning("No barcode detected. Please try again.")

#     elif action == "Edit/Delete Item":
#         st.subheader("Edit or Delete Items")
#         search_query = st.text_input("Search by Name or Barcode")
#         matching_items = [
#             item for item in inventory
#             if search_query.lower() in item["name"].lower() or search_query == item["barcode"]
#         ]

#         if matching_items:
#             for item in matching_items:
#                 col1, col2 = st.columns([1, 2])
#                 with col1:
#                     st.image(item["image_path"], use_column_width=True)
#                 with col2:
#                     st.write(f"**{item['name']}** (Barcode: {item['barcode']})")
#                     new_cases = st.number_input(
#                         f"Update Cases for {item['name']}",
#                         min_value=0,
#                         value=item["cases"],
#                         step=1,
#                         key=f"cases_{item['barcode']}",
#                     )
#                     if st.button("Update", key=f"update_{item['barcode']}"):
#                         item["cases"] = new_cases
#                         save_data(inventory_file, inventory)
#                         st.success(f"Updated '{item['name']}' cases to {new_cases}.")
#                     if st.button("Delete", key=f"delete_{item['barcode']}"):
#                         inventory.remove(item)
#                         save_data(inventory_file, inventory)
#                         st.warning(f"Deleted '{item['name']}'.")
#         else:
#             st.warning("No matching items found.")


def restock_page():
    st.header("Restock Aisle")
    aisle = st.number_input("Enter Aisle Number (1-8):", min_value=1, max_value=8, step=1)
    st.title(f"Restocking in Aisle {aisle}")
    inventory = load_data(inventory_file)

    items_in_aisle = [item for item in inventory if item["aisle"] == aisle]

    if not items_in_aisle:
        st.warning(f"No items found in Aisle {aisle}.")
        return
    background_color = ""
    restocking_list = []
    item_status = {}
    for item in items_in_aisle:
        col1, col2, col3,col4 = st.columns([1, 2, 2,1])
        with col1:
            st.image(item["image_path"], use_column_width=True)
        with col2:
            st.write(f"**{item['name']}** (Barcode: {item['barcode']})")
        with col3:
            status = st.radio(
                f"Status for {item['name']}",
                ["Fully Stocked", "Needs Restocking"],
                index=None,
            )
            if status == "Needs Restocking":
                restocking_list.append(item)
                print("Here stocked")

                col4.empty()
                with col4:
                    dummy = np.zeros((60,60,3))
                    if status == "Needs Restocking":
                        dummy[:,:,0] = 1
                    else:
                        dummy[:,:,1] = 1
                    
                    st.image(dummy, use_column_width=True)
            elif status == "Fully Stocked":
                col4.empty()
                with col4:
                    dummy = np.zeros((60,60,3))
                    if status == "Needs Restocking":
                        dummy[:,:,0] = 1
                    else:
                        dummy[:,:,1] = 1
                    
                    st.image(dummy, use_column_width=True)
            
        # with col4:
        #     dummy = np.ones((60,60,3))
            
        #     st.image(dummy, use_column_width=True)


    if st.button("Finalize Restocking"):
        restocking_data = load_data(restocking_file)
        restocking_data.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "items": restocking_list
        })
        save_data(restocking_file, restocking_data)
        st.success("Restocking list saved!")
        st.json(restocking_list)


# Main Menu
st.sidebar.title("Menu")
option = st.sidebar.selectbox("Choose an option:", ["Restock", "Manage Inventory"])

if option == "Restock":
    restock_page()
elif option == "Manage Inventory":
    manage_inventory_page()