import pandas as pd
import streamlit as st
# from streamlit_option_menu import option_menu
import easyocr
import mysql.connector as mysql
import os
import re

import io

# INITIALIZING THE EASYOCR READER IN ENGLISH LANGUAGE
reader = easyocr.Reader(['en'])

# CONNECTING MYSQL DATABASE
mydb = mysql.connect(
    host="localhost", 
    user="root", 
    password="", 
    database="bizcard", 
    port =3306
    )

mycursor = mydb.cursor(buffered=True)

# CREATING TABLE IN DATABASE

mycursor.execute("""CREATE TABLE IF NOT EXISTS biz_card (
                 id INTEGER PRIMARY KEY AUTO_INCREMENT,
                 company_name TEXT,
                 card_holder TEXT,
                 designation TEXT,
                 mobile_number VARCHAR(50),
                 email_id TEXT,
                 website_URL TEXT,
                 area TEXT,
                 city TEXT,
                 state TEXT,
                 pincode VARCHAR(10),image BLOB                            
                 )
""")

# PAGE SETUP USING STREAMLIT


st.set_page_config(page_title= "BizCardX: Extracting Business Card Data with OCR",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   )
background_color = "!Important"  # Replace this with your desired color code
page_bg = f"""
    <style>
        .main {{
            background-color: {background_color};
        }}
    </style>
"""
# PAGE BACKGROUND FUNCTION
def bgm():
    
    st.markdown(f""" <style>.stApp {{
                            background: url("https://picsum.photos/seed/picsum/536/354");
                            background-size: cover}}
                         </style>""", unsafe_allow_html=True)

bgm()

# st.markdown(page_bg, unsafe_allow_html=True)
# st.sidebar.markdown("<h1 style='color: #391c59;  font-size: 30px;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <style>
        div[data-testid="stSidebarContent"] {
            background-color: #eddaec; 
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("<h1 style='color: #52aec4;  font-size: 30px;'>BizCardX: Extracting Business Card Data with OCR</h1>", unsafe_allow_html=True)
# Your Streamlit app content goes here
st.title("Streamlit Sidebar Color Change")
st.sidebar.header("Sidebar Section")

welcome_css = """
    <style>
            .welcome-message {
            font-size: 26px;
            color: #333;
            text-align: center;
            padding: 10px;
            background-color: YELLOW ;
            border-radius:100px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
"""

# CUSTOM CSS AND WELCOME MESSAGE
st.markdown(welcome_css, unsafe_allow_html=True)
 
st.markdown("<div class='welcome-message'>Welcome to Your Business Card App!</div>", unsafe_allow_html=True)

with st.sidebar:
    selected = st.selectbox(
        "SELECT AN OPTION",
        ["UPLOAD A BUSINESS CARD","EDIT YOUR CARD"],
        index=0
        )
if not os.path.exists("uploaded_file") :
     os.makedirs("uploaded_file")   
if selected == "UPLOAD A BUSINESS CARD" :
    st.markdown("#### Upload your Business Card")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])   
    
    if uploaded_file is not None:
        
        def save_image(uploaded_file):
            with open(os.path.join( "uploaded_file",uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())              

                return

        # CALLING SAVE IMAGE
        save_image(uploaded_file)
        st.success("Image saved successfully!")

        if st.button("Extract Image & Save to Database"):
            with st.spinner("Extracting image Please wait ..."):
                if uploaded_file is not None:
                    st.image(uploaded_file, caption="Uploaded Image", width=500)
                    image_data = uploaded_file.read()

                    # OCR PROCESSING IMAGE TO READ DATA
                    reader = easyocr.Reader(['en'])
                    extracted_text = reader.readtext(image_data)

                    # SAVING EXTRACTED FILES TO LIST
                    card_data=[]
                    for text_info in extracted_text: 
                        card_data.append(text_info[1])

                    # REARRANGING THE DATA IN CARD
                    if card_data[4]=="WWW":
                        concatenated_value = card_data[4].lower() + '.'+card_data[5]                       
                        card_data[4] = concatenated_value                        
                        card_data.pop(5)
                        concatenated_value_cn = card_data[7] + ' '+card_data[9]
                        concatenated_value_str =  card_data[5] + ','+card_data[10] +card_data[6]
                        card_data[7] = concatenated_value_cn 
                        card_data[5] = concatenated_value_str
                        card_data[10]=concatenated_value_cn
                    if len(card_data) >8:    
                        if  card_data[8]== "Restaurant":
                            concatenated_value_cn = card_data[6] + ' '+card_data[8]
                            card_data[8] = concatenated_value_cn
                            card_data[7]=card_data[7].lower()
                            card_data[5]=card_data[5].lower()                        
                    if len(card_data ) >8:
                        if  card_data[8]=="AIRLINES" :
                            concatenated_value_cn = card_data[7] + ' '+card_data[8]
                            card_data[8] = concatenated_value_cn
                    if len(card_data ) >8:
                        if card_data[0]== "Selva":
                            concatenated_value_cn = card_data[0] + ' '+ card_data[9]
                            card_data[9]=concatenated_value_cn 
                    #                            # 
                    image_uploaded = os.getcwd()+"//"+"uploaded_file" + "//" + uploaded_file.name
                    result = reader.readtext(image_uploaded,detail = 0, paragraph = False)

                    # BINARY READ OPERATION
                    def read_binary_image(image_path):
                        with open(image_path, 'rb') as file:
                            binary_data = file.read()
                        return binary_data
                    # INITIALIZING DICTIONARY 
                    image_info = {"company_name": [],
                                "card_holder": [],
                                "designation": [],
                                "mobile_number": [],
                                "email": [],
                                "website": [],
                                "area": [],
                                "city": [],
                                "state": [],
                                "pin_code": [],
                                "image": read_binary_image(image_uploaded)
                                } 
                    # FUNCTION FOR EXTRACT VALUES FROM CARD DATA
                    def extract_data (data):                        
                        for index, element in enumerate(data):                        
                            
                            #EXTRACTING CARD HOLDER VALUE
                            if index == 0:
                                image_info["card_holder"].append(element) 

                            #EXTRACTING COMPANY NAME VALUE                                
                            elif index == len(data) - 1 :                         
                                image_info["company_name"].append(element) 
                            
                            #EXTRACTING DESIGNATION VALUE 
                            elif index == 1:                            
                                image_info["designation"].append(element) 

                            #EXTRACTING WEBSITE VALUE 
                            if "www" in element.lower() or "www." in element.lower():                              
                                image_info["website"].append(element)                              
                            elif "wWW" in element.lower() :
                                image_info["website"].append(element)   
                                   

                            #EXTRACTING MOBILE NUMBER VALUE 
                            elif "-" in element or "+"  in element:
                                image_info["mobile_number"].append(element)
                                if len(image_info["mobile_number"])>1:
                                    image_info["mobile_number"] = " & ".join(image_info["mobile_number"]) 

                            #EXTRACTING EMAIL-ID VALUE
                            elif  "@"  in element :
                                image_info["email"].append(element) 
                                
                            #EXTRACTING AREA VALUE
                            if re.findall('^[0-9].+, [a-zA-Z]',element):
                                image_info["area"].append(element.split(',')[0])
                            elif re.findall('[0-9] [a-zA-z]+',element):
                                image_info["area"].append(element)

                            #EXTRACTING STREET VALUE
                            if "St ," in element or "St." in element:                                                            
                                address = [address.strip() for address in element.split(',')]                                
                                if len(address) >3:
                                    image_info["city"] = address[2]                                 
                                else: 
                                    image_info["city"] = address[1]                      
                                                
                            if "St,," in element:
                                address = [address.strip() for address in element.split(',')]                                
                                if len(address) >3:
                                    image_info["city"] = address[2]                                 
                                else: 
                                    image_info["city"] = address[1]  

                            #EXTRACTING STATE VALUE
                            state_match = re.findall('[a-zA-Z]{9} +[0-9]', element)
                            if state_match:
                                image_info["state"].append(element[:9])
                            elif re.findall('^[0-9].+, ([a-zA-Z]+);', element):
                                image_info["state"].append(element.split()[-1])
                            if len(image_info["state"]) == 2:
                                image_info["state"].pop(0)

                            #EXTRACTING PINCODE VALUE
                            if len(element) >= 6 and element.isdigit():
                                image_info["pin_code"].append(element)
                            elif re.findall('[a-zA-Z]{9} +[0-9]', element):
                                image_info["pin_code"].append(element[10:])   
                    #CALLING EXTRACTION FUNCTION 
                    extract_data(card_data) 

                    # FUNCTION FOR SHOWING THE EXTRACTED DATA 
                    def create_df(image_info):                        
                        df = pd.DataFrame(image_info)                       
                        return df                    
                    df = create_df(image_info)                    
                    st.success("### Extracted Data ")                
                    st.write(df)
                    # INSERTING EXTRACTED VALUES TO DATABASE USING MYSQL 
                    for element,row in df.iterrows():
                        sql = """INSERT INTO biz_card(company_name,card_holder,designation,mobile_number,email_id,website_URL,area,city,state,pincode,image)
                                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""                 
                        
                        mycursor.execute(sql, tuple(row))
                        mydb.commit()                        
                    st.success("#### Uploaded to database successfully!")

# BEGING OF NEXT OPTION:EDIT YOUR CARD
else:
    
    st.markdown("## Select Your ID ") 
    st.markdown("#### Card Details in Database")  
    mycursor.execute("Select * FROM biz_card")
    result = mycursor.fetchall()

    # FUNCTION FOR REFRESHING TABLE
    def refresh():        
            col = ['Id','Company Name','Card Holder','Designation','Mobile Number','Email ID','Website','Area','City','State','Pincode','Image']
            df = pd.DataFrame(result,columns = col )
            st.table(df)
    refresh()        
    if st.button("Refresh Table"):
        st.experimental_rerun()         
        refresh()
    # SETTING ID SELECTBOX  
    cards = {}
    for row in result:
        cards[row[0]]=row[0]
    selected_card = st.selectbox(" SELECT PROPER ID FROM ABOVE DATABASE TABLE", list(cards.keys()))
    mycursor.execute(
            "select company_name,card_holder,designation,mobile_number,email_id,website_URL,area,city,state,pincode from biz_card WHERE id=%s",(selected_card,))
    result = mycursor.fetchone()  
 
# TEXT INPUT DISPLAY FEILD
    
    company_name = st.text_input("Company Name", result[0] if result else "")
    card_holder = st.text_input("Card Holder", result[1] if result else "")
    designation = st.text_input("Designation", result[2] if result else "")
    mobile_number = st.text_input("Mobile Number", result[3] if result else "")
    email_id = st.text_input("Email", result[4] if result else "")
    website_URL = st.text_input("Website", result[5] if result else "")
    area = st.text_input("Area", result[6] if result else "")
    city = st.text_input("City", result[7] if result else "")
    state = st.text_input("State", result[8] if result else "")
    pincode = st.text_input("Pin Code", result[9] if result else "")

    #  BUTTON FOR DATA UPDATION
    if st.button("Update"):        
        mycursor.execute("""UPDATE biz_card SET company_name=%s,card_holder=%s,designation=%s,mobile_number=%s,email_id=%s,website_URL=%s,area=%s,city=%s,state=%s,pincode=%s
                                    WHERE id=%s""", (
        company_name, card_holder, designation, mobile_number, email_id, website_URL, area, city, state, pincode,
        selected_card))
        mydb.commit()
        st.success("Information updated in database successfully.")        
        st.success("Refresh the Table!") 
    #  BUTTON FOR SELECTED CARD
    if st.button("Delete selected Card"):
        with st.spinner("Please wait ..."):
            mycursor.execute(f"DELETE FROM biz_card WHERE id ='{selected_card}'")
            mydb.commit()
            st.success("Deleted !!!  Refresh the Table! .")  
    

             
                
               
     
                     
        
        

    

    

    