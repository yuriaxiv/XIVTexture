import os
import streamlit as st
from PIL import Image
import tempfile
import io
import webbrowser


# Helper functions

def get_image_files(folder):
    return [os.path.join(folder, filename) for filename in os.listdir(folder) if
            os.path.isfile(os.path.join(folder, filename))]


def get_subfolders(folder):
    return [subfolder for subfolder in os.listdir(folder) if os.path.isdir(os.path.join(folder, subfolder))]


def filter_subfolders(subfolders, filter_option):
    return set(subfolders) & set(filter_option)


# Helper function to overlay images
def overlay_images(image_path_a, image_path_b):
    # Open the images
    image_a = Image.open(image_path_a)
    image_b = Image.open(image_path_b)

    try:
        # Resize the larger image to fit the size of the smaller image
        image_a.thumbnail(image_b.size)
        image_b.thumbnail(image_a.size)

        # Overlay the images
        overlay_image = Image.alpha_composite(image_b.convert("RGBA"), image_a.convert("RGBA"))
        return overlay_image

    except ValueError:
        st.error("Operation failure, please choose an image with the same aspect ratio.")
        return None


# Image Overlay App

def image_overlay_app():
    st.title("XIV Texture - Overlay Images")
    st.write("#### Presets (Optional)")

    overlay_folder = "overlay_texture"
    base_folder = "base_texture"

    # Get subfolders for race (female only)
    subfolders_race = get_subfolders(overlay_folder)
    selected_subfolder_race = st.selectbox("Presets (female only):", sorted(subfolders_race))

    # Get subfolders for race options (female only)
    subfolders_options = get_subfolders(os.path.join(overlay_folder, selected_subfolder_race))
    sorted_subfolders_options = sorted(subfolders_options)

    filter_option = st.selectbox("Preset options:", sorted_subfolders_options)

    selected_subfolders_options = [filter_option]

    # Fetch image files for all selected subfolders
    all_image_files_overlay = []
    all_image_files_base = []
    for subfolder in selected_subfolders_options:
        folder_race_sub = os.path.join(overlay_folder, selected_subfolder_race, subfolder)
        all_image_files_overlay.extend(get_image_files(folder_race_sub))

        folder_base_sub = os.path.join(base_folder, selected_subfolder_race, subfolder)
        all_image_files_base.extend(get_image_files(folder_base_sub))

    st.write("#### Combine Textures")

    col1, col2 = st.columns(2)

    uploaded_image_base = col1.file_uploader("Upload a base image:",
                                             type=["png", "dds", "jpg", "jpeg", "bmp"])
    if uploaded_image_base is not None:
        col1.image(uploaded_image_base, caption="Uploaded Image for Base Folder", use_column_width=True)
        selected_image_base = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        selected_image_base.write(uploaded_image_base.read())
        selected_image_base = selected_image_base.name
    else:
        selected_image_base = col1.selectbox("OR Select a preset base:", all_image_files_base,
                                             format_func=lambda x: os.path.basename(x))
        if selected_image_base:
            col1.image(Image.open(selected_image_base), caption="Base Preview",
                       use_column_width=True)

    uploaded_image_overlay = col2.file_uploader("Upload an overlay:",
                                                type=["png", "dds", "jpg", "jpeg", "bmp"])
    if uploaded_image_overlay is not None:
        col2.image(uploaded_image_overlay, caption="Uploaded Image for Overlay Folder", use_column_width=True)
        selected_image_overlay = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        selected_image_overlay.write(uploaded_image_overlay.read())
        selected_image_overlay = selected_image_overlay.name
    else:
        selected_image_overlay = col2.selectbox("OR Select an overlay:", all_image_files_overlay,
                                                format_func=lambda x: os.path.basename(x))
        if selected_image_overlay:
            col2.image(Image.open(selected_image_overlay), caption="Overlay Preview",
                       use_column_width=True)

    if (uploaded_image_overlay or selected_image_overlay) and (uploaded_image_base or selected_image_base):
        overlay_button = st.button("Overlay Images", key="overlay_button")
        if overlay_button:
            overlay_image = overlay_images(selected_image_overlay, selected_image_base)
            st.image(overlay_image, caption="Combined Image", use_column_width=True)

            # Convert the overlay_image to bytes and enable image download as PNG with custom filename
            img_bytes = io.BytesIO()
            overlay_image.save(img_bytes, format="PNG")

            # Offer the download link as a Streamlit-styled button
            st.download_button(
                label="Download Combined Image",
                data=img_bytes.getvalue(),
                file_name="texture.png",
                mime="image/png"
            )

            # How to import into your game section
            with st.expander("How do I import this into my game?"):
                col1, col2 = st.columns(2)

                if col1.button("Penumbra"):
                    webbrowser.open_new_tab("https://loosetexturecompiler.zip")

                if col2.button("Textools"):
                    webbrowser.open_new_tab(
                        "https://media.discordapp.net/attachments/994181303522041906/1065732743985647777/makeup.png")


# Multi-Page App

def about_page():
    st.title("About XIV Texture")
    # About page
    st.write("A simple application made to overlay images. Eventually I hope to expand functionality to convert "
             "images into Penumbra modpacks.")
    st.write("This is designed as a shortcut for people not familiar with image editing tools. It will not work for "
             "things like Atramentum Luminis, or anything else requiring an edited alpha channel.")
    st.write("")
    st.markdown("[Created By: Yuria](https://yuriamods.com)")

    st.write("")
    st.write("### Texture Credits")
    st.write("Au Ra Textures - To be released (Yuria's Upscales)")
    st.markdown("[Miqo'te Textures](https://www.xivmodarchive.com/modid/70736)")
    st.markdown("[Viera Textures](https://www.xivmodarchive.com/modid/70766)")
    st.markdown("[NB Textures](https://www.deviantart.com/bizuart/art/Gen-2-NB-Scales-905047991)")
    st.markdown("[Body Textures](https://www.xivmodarchive.com/modid/29029)")
    st.write("If using for a release, please check the original mod page for credits.")

    st.write("")
    st.write("### Contact")
    st.write("I'm always open to suggestions & help, you can contact me through my Discord.")
    st.write("Please send suggestions to the 'suggestions' channel, and help to the 'technical help' channel.")
    if st.button("Contact Me"):
        st.markdown("[Contact Me](https://discord.gg/lunartear)")


def privacy_policy_page():
    st.title("Privacy Policy")
    # Privacy Policy
    st.write("**Last updated:** 31/08/2023")
    st.write("")
    st.write(
        "We understand the importance of your privacy and are committed to protecting it. This Privacy Policy explains how we collect, use, and safeguard your information when you use our app.")
    st.write("")
    st.write("**Information We Collect**")
    st.write(
        "We do not collect any personal information or user data through our app. We do not use cookies or any other tracking technologies to gather information about your activities.")
    st.write("")
    st.write("**Use of Your Information**")
    st.write(
        "Since we do not collect any personal information or user data, we do not use your information for any purpose.")
    st.write("")
    st.write("**Third-Party Services**")
    st.write(
        "Our app does not use any third-party services, plugins, or tools that might collect or process user data.")
    st.write("")
    st.write("**Changes to this Privacy Policy**")
    st.write(
        "We reserve the right to update or modify this Privacy Policy at any time, and changes will be effective upon "
        "posting the updated Privacy Policy. We encourage you to review this Privacy Policy periodically to stay "
        "informed about how we are protecting your information.")
    st.write("")
    st.write("This Privacy Policy was last updated on 31/08/2023.")


def main():
    pages = {
        "XIV Texture": image_overlay_app,
        "About This Website": about_page,
        "Privacy Policy": privacy_policy_page,
    }

    page = st.sidebar.selectbox("Select a page:", list(pages.keys()))

    # Execute the selected page's function
    pages[page]()


if __name__ == "__main__":
    main()
