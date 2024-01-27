# # BizCardX: Extracting Business Card Data with OCR

## Overview

This project is a Streamlit web application designed to extract and manage business card data using Optical Character Recognition (OCR). Users can upload business card images, extract information, and manage the data in a MySQL database.

## Features

- **Upload Business Card**: Users can upload images of business cards in common formats such as jpg, jpeg, and png.

- **Extract Information**: The app uses the EasyOCR library for OCR to extract text data from the uploaded business card images.

- **Database Integration**: Extracted information is stored in a MySQL database named `bizcard`. The database has a table named `biz_card` to store the business card details.

- **User Interface**: The app features a Streamlit interface with a sidebar for navigation and options.

## Setup

1. **Install Dependencies**: Make sure to install the required Python libraries using the following command:

    ```bash
    pip install -r requirements.txt
    ```

2. **Database Setup**: Ensure that MySQL is installed and running. Update the database connection details in the code (host, user, password, database, port).

3. **Run the App**: Execute the following command to run the Streamlit app:

    ```bash
    streamlit run your_app_file.py
    ```

4. **Access the App**: Open your web browser and navigate to the provided local URL to access the BizCardX app.

## Usage

1. **Upload a Business Card**: Select the "UPLOAD A BUSINESS CARD" option from the sidebar and upload an image of a business card.

2. **Extract Data**: Click the "Extract Image & Save to Database" button to initiate OCR processing and save the extracted data to the database.

3. **Edit Your Card**: Select the "EDIT YOUR CARD" option from the sidebar to edit or delete existing business card entries in the database.

4. **Refresh Table**: Use the "Refresh Table" button to update the displayed database table.

5. **Update Information**: Edit the information fields and click the "Update" button to update the database with the modified details.

6. **Delete Card**: Click the "Delete selected Card" button to remove the selected business card entry from the database.

## Additional Notes

- This app uses the EasyOCR library for Optical Character Recognition. Ensure that the library is correctly installed for accurate text extraction.

- Customize the styling, color schemes, and background images in the Streamlit app based on your preferences.

- Make sure to secure your MySQL database credentials and adjust the permissions accordingly.

## Credits

- [Streamlit](https://streamlit.io/)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)

Feel free to modify and expand this README based on the specific functionalities and features of your app.
