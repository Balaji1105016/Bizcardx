import streamlit as st
import easyocr
import numpy as np
import re
import mysql.connector as sql
import pandas as pd
import os
from streamlit_option_menu import option_menu
from PIL import Image, ImageDraw

# Title:
Title_pic_img_path = r"C:\Users\Balaji\Music\Personal_Pic\Title3.jpg"
Title_pic = Image.open(Title_pic_img_path)
st.image(Title_pic)


# HTML code for the video
video_html = '<div style="position: relative; overflow: hidden; padding-top: 56.25%;"><iframe src="https://share.synthesia.io/embeds/videos/0f462ad2-2009-4a72-9029-baeaff5f609e" loading="lazy" title="Synthesia video player - Your AI video" allow="encrypted-media; fullscreen;" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0; margin: 0; overflow:hidden;"></iframe></div>'

# Display the video using st.components.v1.html
st.components.v1.html(video_html, width=480, height=280)

# Login and Logout Section:
if 'login_status' not in st.session_state:
    st.session_state.login_status = False
    
username = st.text_input("User Name")
password = st.text_input("Password",type = 'password')
if st.button("Login"):
    if username == "Balaji" and password == "Balaji@123":
        st.session_state.login_status = True
        st.success("Login Successful!")
    
    else:
        st.session_state.login_status = False
        st.error("Invalid Credentials. Please try again.")

if st.session_state.login_status:      
    logout = st.sidebar.button("Logout")
    if logout:
        if 'login_status' in st.session_state:
            st.session_state.login_status = False
            st.experimental_rerun()

                
    # SQL Database connection:
    db = sql.connect(host="127.0.0.1", user="root", password="test", database="Biz_Card")
    cur = db.cursor(buffered=True)

    cur.execute("""
                Create Table IF NOT EXISTS Biz_Card_Details(Id int PRIMARY KEY AUTO_INCREMENT,
                                                                Company TEXT,
                                                                Card_Holder_Name TEXT,
                                                                Designation TEXT,
                                                                MOB VARCHAR(50),
                                                                Email TEXT,
                                                                Website TEXT,
                                                                Area TEXT,
                                                                City TEXT,
                                                                State TEXT,
                                                                Pincode VARCHAR(10),
                                                                Card_Pic LONGBLOB                                                                     
                )
                """)


    # Creating the EasyOCR Reader:
    r_1 = easyocr.Reader(['en'], gpu=False)

    with st.sidebar:
        menu_sel = option_menu("Menu", ["Home","Data Extraction","Data Modification","Data Deletion","Resources"], 
                    icons=["house","play","list-task", "exclamation-circle"],
                    styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-1px", "--hover-color": "#6F36AD"},
                            "nav-link-selected": {"background-color": "#6F36AD"}})

    if menu_sel == "Home":
        st.header("Vision - THINK ABOUT FUTURE")
        st.subheader("By")
        Personal_pic_img_path = r"C:\Users\Balaji\Music\Personal_Pic\Balaji_pic.jpeg"
        pic = Image.open(Personal_pic_img_path)
        st.image(pic, caption="""BALAJI BALAKRISHNAN(Data Engineer)""")
        st.write("""
                Note: This application will be helpfull in extracting the Business Card data with OCR
                """)
        st.subheader("Application Process")
        st.write("""
                    1. Installing the required packages: We will need to install Python, Streamlit,
                       easyOCR, and a database management system like SQLite or MySQL.\n
                    2. Designing the user interface: We are creating a simple and intuitive user interface using
                       Streamlit that guides users through the process of uploading the business
                       card image and extracting its information. We are using widgets like file
                       uploader, buttons, and text boxes to make the interface more interactive.\n
                    3. Implementing the image processing and OCR: Using easyOCR to extract the
                       relevant information from the uploaded business card image. We are using
                       image processing techniques like resizing, cropping, and thresholding to
                       enhance the image quality before passing it to the OCR engine.\n
                    4. Displaying the extracted information: Once the information has been extracted,We are
                       displaying it in a clean and organized manner in the Streamlit GUI. We are using
                       widgets like tables, text boxes, and labels to present the information.\n
                    5. Implementing database integration: Using a database management system like
                       SQLite or MySQL we are storing the extracted information along with the uploaded
                       business card image. We are using SQL queries to create tables, insert data,
                       and retrieve data from the database, Update the data and allowing the users to
                       delete the data through the streamlit UI.\n
                    6. Testing the application: Testing the application thoroughly to ensure that it works as
                       expected. We are running the application on our local machine by running the
                       command streamlit run Bizcard.py in the terminal, where Bizcard.py is the name of
                       our Streamlit application file.\n
                    7. Improving the application: Continuously improving the application by adding new
                       features, optimizing the code, and fixing bugs.\n
                """)
        


    if menu_sel == "Data Extraction":
        st.header("Data Extraction Section")
        st.subheader("Data Upload")
        file_up = st.file_uploader("Upload the BizCard", type=["PNG", "JPEG", "JPG"])
        
        if file_up is not None:
            
            with open(os.path.join("uploaded_cards", file_up.name), "wb") as file:#--> Creating the file path by joining the dir uploaded_cards
                #file_up.name -->if the user uploads the file name as Bizcard.PNG then it will save in the same file name locally. 
                    file.write(file_up.getbuffer())#-->saving the binary content of the image in the local file dir uploaded_cards 
            
            image = Image.open(file_up)
            st.image(image, caption='Uploaded Bizcard', use_column_width=True)
            
            # Data Extraction Section:
            Extract_Data = st.button("Extract Data")
            if Extract_Data:
                st.subheader("Data Extraction and Data Storage in DB")
                array = np.array(image)
                read = r_1.readtext(array)
                # st.write(read)
                draw = ImageDraw.Draw(image)
                # Making a Reactangle:
                for bounding_box, detect_text, confidence_score in read:
                    top_left, top_right, bottom_right, bottom_left = bounding_box
                    top_left = tuple(map(int, top_left))#-->Converting the floating point numbers to integers
                    bottom_right = tuple(map(int, bottom_right))
                    draw.rectangle([top_left, bottom_right], outline="green", width=2)
                # st.write(bounding_box)
                # # st.write(detect_text)
                # st.write(confidence_score)
                    
                # Displaying the annotated image
                st.image(image, caption='Annotated Bizcard', use_column_width=True)
                
                local_Biz_Card_Path = os.getcwd() + "\\" + "uploaded_cards" + "\\" + file_up.name#--> Forming the file Path of the uploaded Business Card
                local_Biz_Card_result = r_1.readtext(local_Biz_Card_Path,detail = 0,paragraph=False)#reading the text of the locally saved business card,detail=0-->only the text,Paragraph = False in the sense it should not be treated as paragraph and it will contain the list of text strings.
                with open(local_Biz_Card_Path, 'rb') as file: #-->Reading the Binary File
                        bi_D = file.read()
                        
                result = {"Company":[],"Card_Holder_Name":[],"Designation":[],"MOB":[],"Email":[],"Website":[],"Area":[],"City":[],"State":[],"Pincode":[],"Card_Pic":bi_D}
            
                for index,j in enumerate(local_Biz_Card_result):
                    # Website URL:
                    if "www" in j.lower() or "WWW" in j or "www." in j or "Www." in j or "WWw." in j:
                        result["Website"].append(j)
                    # Email:
                    elif "@" in j:
                        result["Email"].append(j)
                    # Mobile Number:
                    elif "+" in j or "-" in j:
                        result["MOB"].append(j)
                        if len(result["MOB"])==2:
                            result["MOB"]=" , ".join(result["MOB"]) 
                    # Company Name:
                    elif index == len(local_Biz_Card_result) - 1:
                        result["Company"].append(j)
                    # Card Holder Name:
                    elif index==0:
                        result["Card_Holder_Name"].append(j)
                    #Designation:
                    elif index == 1:
                        result["Designation"].append(j)
                    #Pincode:
                    if len(j)==6 and j.isdigit():
                        result["Pincode"].append(j)
                    elif re.findall("[a-zA-Z]{9} +[0-9]",j):
                        #a-z --> Characters starting with a-z small letters
                        #A-Z --> Characters starting with A-Z small letters
                        #{9} --> exactly 9 charactes -->For TamilNadu State
                        #+ --> One or More Spaces
                        #[0-9] ---> Zero to nine numbers
                        result["Pincode"].append(j[10:])
                    # State:
                    state = re.findall("[a-zA-Z]{9} +[0-9]", j)
                    if state:
                        result["State"].append(j[:9])
                    elif re.findall("^[0-9].+, ([a-zA-Z]+);", j):
                    # #     #^ --> Start of the String
                    # #     #[0-9] --> 0-9 Characters
                    # #     #.+ -->  one or more occurences of any character(except for a new line)
                    # #     #([a-zA-Z]+) --> 
                    # #     #() --> Used to capture and remember the matched content within the parenthesis
                        result["State"].append(j.split()[-1])# Appending the state alone if it is present with city
                    elif len(result["State"]) == 2:
                        result["State"].pop(0)#--> Used to avoid the city name coming with state
                    # Area:
                    if re.findall("^[0-9].+, [a-zA-Z]+", j):
                        result["Area"].append(j.split(",")[0])
                    elif re.findall("[0-9] [a-zA-Z]+", j):
                        result["Area"].append(j)
                    #City:
                    m1 = re.findall('.+St , ([a-zA-Z]+).+', j)
                    m2 = re.findall('.+St,, ([a-zA-Z]+).+', j)
                    m3 = re.findall('^[E].*',j)
                    if m1:
                        result["City"].append(m1[0])
                    elif m2:
                        result["City"].append(m2[0])
                    elif m3:
                        result["City"].append(m3[0])
                        
                # st.write(result)
                df = pd.DataFrame(result)
                st.dataframe(df)
                st.dataframe(df).balloons()
                df1 = pd.DataFrame(result)
                
                for k,l in df1.iterrows():
                    # Duplicate Record Check:
                    check_query = """SELECT * FROM Biz_Card_Details WHERE Email = %s ORDER BY ID DESC LIMIT 1"""
                    cur.execute(check_query, (l['Email'],))
                    existing_record = cur.fetchone()
                    if not existing_record:
                    #  if it is not an existing record:
                        insert_query = """INSERT INTO Biz_Card_Details(Company,Card_Holder_Name,Designation,MOB,Email,Website,Area,City,State,Pincode,Card_Pic) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                        cur.execute(insert_query, tuple(l))
                        st.success(f"Record for {l['Email']} inserted successfully.")
                    else:
                        st.warning(f"Record already exists. Skipping the insertion.")
                db.commit()
                    
    
                #     Query = """INSERT INTO Biz_Card_Details(Company,Card_Holder_Name,Designation,MOB,Email,Website,Area,City,State,Pincode,Card_Pic) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                #     cur.execute(Query,tuple(l))
                # db.commit()
                # st.success("""Data Is Saved Successfully Extracted And Stored In DB""")
                

    if menu_sel == "Data Modification":
        with st.sidebar:
            Mod = option_menu("Modification Menu", ['Company Modification', 'Card Holder Name Modification', 'Designation Modification','MOB Modification','Email Modification','Website URL Modification','Area Modification','City Modification','State Modification','Pincode Modification'], 
                        styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-1px", "--hover-color": "#6F36AD"},
                                "nav-link-selected": {"background-color": "#6F36AD"}})
            
        
        if Mod == "Company Modification":
            st.header("Data Modification Section")
            st.subheader("Company Modification")
            st.success("""
                            1)In this section you need to provide the id and the corresponding company name which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                    """)
            
            id = st.text_input("Enter the ID")
            company = st.text_input("Enter the Company Name")
            submit_button_1 = st.button("Submit Button")
            if submit_button_1:
                q3 = f"""
                        update biz_card.biz_card_details set Company = "{company}" where ID  = {id}
                        """
                cur.execute(q3)
                db.commit()
                q4 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q4)
                res_2 = cur.fetchall()
                df_3 = pd.DataFrame(res_2, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_3)
                st.dataframe(df_3).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Company Name For Your Bizcard...!!!!
                        """)
                
                
                
        if Mod == "Card Holder Name Modification":
            st.header("Data Modification Section")
            st.subheader("Card Holder Name Modification")
            st.success("""
                            1)In this section you need to provide the id and the corresponding card holder name which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                    """)
            id = st.text_input("Enter the ID")
            Card_Holder_Name = st.text_input("Enter the Card Holder Name")
            submit_button_2 = st.button("Submit Button")
            if submit_button_2:
                q5 = f"""
                        update biz_card.biz_card_details set Card_Holder_Name = "{Card_Holder_Name}" where ID  = {id}
                        """
                cur.execute(q5)
                db.commit()
                q6 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q6)
                res_3 = cur.fetchall()
                df_4 = pd.DataFrame(res_3, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_4)
                st.dataframe(df_4).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Card Holder Name For Your Bizcard...!!!!
                        """)
                
        if Mod == "Designation Modification":
            st.header("Data Modification Section")
            st.subheader("Designation Modification")
            st.success("""
                            1)In this section you need to provide the id and the corresponding designation name which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                    """)
            
            id = st.text_input("Enter the ID")
            Designation = st.text_input("Enter the Designation Name")
            submit_button_3 = st.button("Submit Button")
            if submit_button_3:
                q7 = f"""
                        update biz_card.biz_card_details set Designation = "{Designation}" where ID  = {id}
                        """
                cur.execute(q7)
                db.commit()
                q8 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q8)
                res_4 = cur.fetchall()
                df_5 = pd.DataFrame(res_4, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_5)
                st.dataframe(df_5).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Designation Name For Your Bizcard...!!!!
                        """)
                
        if Mod == "MOB Modification":
            st.header("Data Modification Section")
            st.subheader("Mobile Number Modification")
            st.success(""" 
                            1)In this section you need to provide the id and the Mobile Number which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                        """) 
            id = st.text_input("Enter the ID")
            Mobile_Number = st.text_input("Enter the Mobile Number")
            submit_button_4 = st.button("Submit Button")
            if submit_button_4:
                q9 = f"""
                        update biz_card.biz_card_details set MOB = "{Mobile_Number}" where ID  = {id}
                        """
                cur.execute(q9)
                db.commit()
                q10 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q10)
                res_5 = cur.fetchall()
                df_6 = pd.DataFrame(res_5, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_6)
                st.dataframe(df_6).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Mobile Number For Your Bizcard...!!!!
                        """)
        
        if Mod == "Email Modification":
            st.header("Data Modification Section")
            st.subheader("Email Modification")
            st.success(""" 
                            1)In this section you need to provide the id and provide the Email which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                        """)
            
            id = st.text_input("Enter the ID")
            Email = st.text_input("Enter the Email ID")
            submit_button_5 = st.button("Submit Button")
            if submit_button_5:
                q11 = f"""
                        update biz_card.biz_card_details set Email = "{Email}" where ID  = {id}
                        """
                cur.execute(q11)
                db.commit()
                q12 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q12)
                res_6 = cur.fetchall()
                df_7 = pd.DataFrame(res_6, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_7)
                st.dataframe(df_7).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Email ID For Your Bizcard...!!!!
                        """)
        
        if Mod == "Website URL Modification":
            st.header("Data Modification Section")
            st.subheader("Website URL Modification")
            st.success(""" 
                            1)In this section you need to provide the id and provide the Website URL which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                        """)
            id = st.text_input("Enter the ID")
            url = st.text_input("Enter the Website URL as text")
            submit_button_6 = st.button("Submit Button")
            if submit_button_6:
                q13 = f"""
                        update biz_card.biz_card_details set Website = "{url}" where ID  = {id}
                        """
                cur.execute(q13)
                db.commit()
                q14 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q14)
                res_7 = cur.fetchall()
                df_8 = pd.DataFrame(res_7, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_8)
                st.dataframe(df_8).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Website URL For Your Bizcard...!!!!
                        """)
                
        if Mod == "Area Modification":
            st.header("Data Modification Section")
            st.subheader("Area Modification")
            st.success(""" 
                            1)In this section you need to provide the id and provide the area information which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                        """)
            id = st.text_input("Enter the ID")
            Area = st.text_input("Enter the Area")
            submit_button_7 = st.button("Submit Button")
            if submit_button_7:
                q14 = f"""
                        update biz_card.biz_card_details set Area = "{Area}" where ID  = {id}
                        """
                cur.execute(q14)
                db.commit()
                q15 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q15)
                res_8 = cur.fetchall()
                df_9 = pd.DataFrame(res_8, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_9)
                st.dataframe(df_9).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Area Information For Your Bizcard...!!!!
                        """)
        
        if Mod == "City Modification":
            st.header("Data Modification Section")
            st.subheader("City Modification")
            st.success(""" 
                            1)In this section you need to provide the id and provide the City information which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                        """)
            id = st.text_input("Enter the ID")
            City = st.text_input("Enter the City")
            submit_button_8 = st.button("Submit Button")
            if submit_button_8:
                q16 = f"""
                        update biz_card.biz_card_details set City = "{City}" where ID  = {id}
                        """
                cur.execute(q16)
                db.commit()
                q17 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q17)
                res_9 = cur.fetchall()
                df_10 = pd.DataFrame(res_9, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_10)
                st.dataframe(df_10).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The City Information For Your Bizcard...!!!!
                        """)
        
        if Mod == "State Modification":
            st.header("Data Modification Section")
            st.subheader("State Modification")
            st.success(""" 
                            1)In this section you need to provide the id and provide the State information which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                        """)
            id = st.text_input("Enter the ID")
            State = st.text_input("Enter the State")
            submit_button_9 = st.button("Submit Button")
            if submit_button_9:
                q18 = f"""
                        update biz_card.biz_card_details set State = "{State}" where ID  = {id}
                        """
                cur.execute(q18)
                db.commit()
                q19 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q19)
                res_10 = cur.fetchall()
                df_11 = pd.DataFrame(res_10, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_11)
                st.dataframe(df_11).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The State Information For Your Bizcard...!!!!
                        """)
                
        if Mod == "Pincode Modification":
            
            st.header("Data Modification Section")
            st.subheader("Pincode Modification")
            st.success(""" 
                            1)In this section you need to provide the id and provide the Pincode information which you want to modify for your Bizcard.\n
                            2)To Provide your inputs properly,please refer the resource section.
                        """)
            id = st.text_input("Enter the ID")
            Pincode = st.text_input("Enter the Pincode")
            submit_button_10 = st.button("Submit Button")
            if submit_button_10:
                q20 = f"""
                        update biz_card.biz_card_details set Pincode = "{Pincode}" where ID  = {id}
                        """
                cur.execute(q20)
                db.commit()
                q21 = f"""
                        select * from biz_card.biz_card_details where ID  = {id}
                        """
                cur.execute(q21)
                res_11 = cur.fetchall()
                df_12 = pd.DataFrame(res_11, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
                st.subheader("Modified DB Data")
                st.dataframe(df_12)
                st.dataframe(df_12).balloons()
                st.success("""
                        !!!!!....Congrats😃....You Have Successfully Modified The Pincode Information For Your Bizcard...!!!!
                        """)

    if menu_sel == "Data Deletion":
        st.header("Data Deletion")
        st.warning("""
                    Note: This Module will be helpfull in deleting the data from the DB,Make sure that you are providing the proper ID for deletion.To refer your Bizcard ID please go to the Resource section. Once the data is deleted you need to extract the data again to add in the DB. For available data in DB also you can refer the Resource section. 
                """)
        id = st.text_input("Enter the ID")
        deletion_button = st.button("Data Deletion")
        if deletion_button:
            q22 = f"""Delete from biz_card.biz_card_details where ID = {id} """
            cur.execute(q22)
            db.commit()
            st.subheader("Available Data in DB After Deletion")
            q23 = f"select * from biz_card.biz_card_details"
            cur.execute(q23)
            res_13 = cur.fetchall()
            df_14 = pd.DataFrame(res_13, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
            
            if df_14.empty:
                st.warning("""
                        You deleted the last data in the DB,please try to extract some more Bizcard so that it will get stored in the DB automatically.
                        """)
            else:
                st.dataframe(df_14)
                st.dataframe(df_14).balloons()
                st.success("!!!!...You Have Successfully Deleted The Data....!!!!")

        
    if menu_sel == "Resources":
        st.subheader("Available Data in DB")
        q24 = f"select * from biz_card.biz_card_details"
        cur.execute(q24)
        res_14 = cur.fetchall()
        df_15 = pd.DataFrame(res_14, columns=[ "ID", "Company", "Card_Holder_Name", "Designation", "MOB","Email","Website","Area","City","State","Pincode","Card_Pic"])
        
        if df_15.empty:
            st.error("There are no Data in the DB as of now, So please extact the Bizcard so that it will get automatically stored in the DB and it will get reflected in this Resource section also")
        else:
            st.dataframe(df_15)
            st.dataframe(df_15).balloons()
