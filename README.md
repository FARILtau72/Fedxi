# FEDXI - PhotoPro Image Editor 📸

A powerful and user-friendly GUI-based image editor application built with Python. FEDXI - PhotoPro Image Editor provides a range of functionalities, including image loading, display, editing (brightness, contrast, sharpness, color adjustments, and various filters), background removal, user authentication (login/signup), and saving capabilities. It aims to provide a streamlined and intuitive image editing experience for users of all skill levels.

🚀 **Key Features:**

*   **User Authentication:** Secure login and signup functionality with password hashing to protect user accounts.
*   **Image Loading & Display:** Easily load images from your local file system and display them within the application.
*   **Image Adjustments:** Fine-tune your images with brightness, contrast, sharpness, and color adjustments.
*   **Image Filters:** Apply a variety of filters, including grayscale, blur, edge enhancement, emboss, contour, detail, and smooth, to achieve unique effects.
*   **Background Removal:** Intelligently remove backgrounds from images with a single click, powered by the `rembg` library.  This runs in a separate thread to keep the UI responsive.
*   **Image Saving:** Save your edited images in various formats to your desired location.
*   **Intuitive GUI:** A user-friendly graphical interface built with `tkinter` for a seamless editing experience.
*   **Image Reset:** Easily revert back to the original image.

🛠️ **Tech Stack:**

| Category      | Technology                               | Description                                                                    |
|---------------|------------------------------------------|--------------------------------------------------------------------------------|
| **Frontend**  | `tkinter`                                | GUI framework for creating the user interface.                                 |
|               | `tkinter.filedialog`                     | For opening and saving image files.                                            |
|               | `tkinter.messagebox`                     | For displaying message boxes (e.g., error messages).                             |
|               | `tkinter.ttk`                            | Themed widgets (e.g., sliders) for a modern look and feel.                     |
| **Image Processing** | `PIL (Pillow)`                           | Core image processing library for loading, editing, and saving images.         |
|               | `cv2 (OpenCV)`                           | (Potentially) For more advanced image processing features.                       |
|               | `numpy`                                  | Numerical operations, especially when working with image data as arrays.        |
|               | `rembg`                                  | Library for removing backgrounds from images.                                  |
| **Backend**   | `json`                                   | For loading and saving user data in JSON format.                               |
|               | `os`                                     | For file system operations (e.g., checking if a file exists).                  |
|               | `hashlib`                                | For hashing passwords for security.                                            |
|               | `io`                                     | For handling image data in memory.                                             |
|               | `threading`                              | For running background removal in a separate thread.                             |
| **Build Tools** | N/A                                      | No specific build tools are mentioned, indicating a simple execution setup. |

📦 **Getting Started:**

### Prerequisites

*   Python 3.6 or higher
*   Make sure you have `pip` installed

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, install the dependencies individually:

    ```bash
    pip install tkinter pillow numpy rembg opencv-python
    ```

    *Note: `opencv-python` might not be strictly required if you are not using advanced OpenCV features.*

### Running Locally

1.  Navigate to the project directory in your terminal.
2.  Run the `image.py` file:

    ```bash
    python image.py
    ```

💻 **Usage:**

1.  **Login/Signup:** If you are a new user, sign up for an account. Otherwise, log in with your existing credentials.
2.  **Open Image:** Click the "Open Image" button to load an image from your file system.
3.  **Edit Image:** Use the sliders to adjust brightness, contrast, sharpness, and color.
4.  **Apply Filters:** Click the filter buttons to apply various image filters.
5.  **Remove Background:** Click the "Remove Background" button to remove the background from the image.
6.  **Save Image:** Click the "Save Image" button to save the edited image to a file.

📂 **Project Structure:**

```
├── image.py               # Main application file containing the ImageEditorApp class
├── user.txt               # File to store user data (username/password)
├── requirements.txt       # (Optional) Lists the project dependencies
└── README.md              # Project documentation
```

📸 **Screenshots:**
<img width="1920" height="1045" alt="FEDXI - PhotoPro Image Editor 24_10_2025 09_48_18" src="https://github.com/user-attachments/assets/dee01459-1695-490f-b32e-49a18e6ec2a2" />
<img width="1920" height="1045" alt="FEDXI - PhotoPro Image Editor 24_10_2025 09_48_38" src="https://github.com/user-attachments/assets/149c8863-7cc8-4374-935b-83ac50dd21b5" />



🤝 **Contributing:**

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive commit messages.
4.  Push your changes to your fork.
5.  Submit a pull request.

📝 **License:**

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details.

📬 **Contact:**

If you have any questions or suggestions, feel free to contact me at instagram @FR.PROJECT.ID

💖 **Thanks:**

Thank you for checking out FEDXI - PhotoPro Image Editor! I hope you find it useful and enjoyable.

This is written by [readme.ai](https://readme-generator-phi.vercel.app/).
