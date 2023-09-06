import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
import plotly.express as px
import base64
import openai
import pymongo
import streamlit.components.v1 as components
import json
from streamlit_lottie import st_lottie
import requests

openai.api_key = "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"

myclient=pymongo.MongoClient('mongodb://localhost:27017')

mydb=myclient['pss']
mycol=mydb['projects']
mycol2=mydb['users']

model_engine = "text-davinci-003"
st.set_page_config(page_title="Project Predictor", page_icon="😃", layout="wide")

def show_project(recommended_project,i,level):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"<p style='color:red; margin-bottom:0px;'>PROJECT:</p> {recommended_project['Project_title']}",unsafe_allow_html=True)
        # st.write(f"*Objective:* {recommended_project['Project_domain']}")
        st.write("")
        st.write(f"<p style='color:red; margin-bottom:0px;'>TYPE:</p> {recommended_project['Project_type']}",unsafe_allow_html=True)
    

    c=recommended_project['Project_domain']
    y= c.replace(" ", "+")
    d=recommended_project['Project_title']
    x = d.replace(" ", "+")
    e=recommended_project['Project_type']
    f=recommended_project["Required_Skills"]
    data={ "Project_title":d,'Project_type':e,'Required_Skills':f , 'Project_domain':c }

        
    j=str(i+1000)
    k=str(i+2000)
    l=str(i+3000)
    
    
    with col2:
        st.write("<p style='color:red;'>DESCRIPTION:</p>",unsafe_allow_html=True)
        
        st.write(f" {recommended_project['Description']}")
        co1,co2=st.columns(2)
        with co1:
            st.write("<p style='color:red;'>COMPANY NAME:</p>",unsafe_allow_html=True)
            st.write(f" {recommended_project['Company_name']}")
        with co2:
            st.write("<p style='color:red;'>CONTACT:</p>",unsafe_allow_html=True)
            st.write(f" {recommended_project['Contact']}")
        # b1=st.button("steps to do?", key=j )
        # b2=st.button("startup strategy", key=k )
        
        # b3=st.button("Add to favourites",key=l)
        c1, c2,c3 = st.columns(3)

        with c1:
            b1=st.button("steps to do?", key=j )

        with c2:
            b2=st.button("startup strategy", key=k )

        with c3:
            b3=st.button("Star It",key=l)
        
    
    
    st.markdown(f"[Show Project samples](https://www.google.com/search?q="+x+"+project+using+"+y+"+github)")
    prom="steps to create "+d+" using "+c
    prom2="steps to start buissness startup for "+d+" project"
    if b1:
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prom,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response = completion.choices[0].text
        # print(response)
        st.write(response)
    
    if b2:
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prom2,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        response1 = completion.choices[0].text
        # print(response)
        st.write(response1)
    
    if b3:
        inserted=mycol.insert_one(data)
        st.success("Added to favourites")
    
    # st.write(f"*GitHub:* [{recommended_project['Project_title']}]({recommended_project['GitHub']})")
    st.write("-----")

st.sidebar.title("Enter Your Skills")
# st.sidebar.markdown("Please enter your skills separated by commas.")

st.sidebar.write(" ")
st.sidebar.write(" ")




# Set the app title and sidebar




# Get the user input and transform it into a TF-IDF vector
options = ["HTML & CSS", "React", "Angular","Nodejs","Flask","Flutter","Machine learning","Deep Learning","Data Science","Java","Kotlin","Python","Sql","PyQt5","logistic regression & R"," Apriori and Fp Growth data mining algorithms","blockchain technology and AI","AI and ML","Html & CSS & ASP.NET","Html & CSS & JavaScript & MYSQL.","Html & CSS &  JavaScript & ASP.net","Crypto","3D printing & Bluetooth","Html & CSS & JavaScript & MySQL Database & Django"]

selected_options = st.sidebar.multiselect("Select options:", options)





user_input=""
sta=""
if len(selected_options) > 0:
    for option in selected_options:
        sta=sta+","+option
    # st.write(sta)
    user_input=sta
else:
    
    original_title = '<p class="og" style=" color:Orange; on ">Please select at least one option.</p>'
    st.sidebar.write(original_title, unsafe_allow_html=True)
st.sidebar.write(" ")



level_type=["","Easy","Moderate","Tough"]
level=st.sidebar.selectbox("select level", level_type)

project_df = pd.read_excel("Proj_list.xlsx")

if level == "":
    projects_df=project_df
else:
        # df = df[df['Symbol'] == selected_stock]
    projects_df=project_df[project_df["Difficulty_level"]== level]
    


# Load the project dataset


# Create a TF-IDF vectorizer and fit it to the project skills
tfidf = TfidfVectorizer()
tfidf.fit(projects_df["Required_Skills"])

# user_input = st.sidebar.text_input("", "")
user_skills_tfidf = tfidf.transform([user_input])


ques = st.sidebar.text_input("Enter your query related to project?", "")
st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")

saved=st.sidebar.button("Favourites",key="uni")



# Calculate the cosine similarity between the user skills and the project skills
similarity_scores = cosine_similarity(user_skills_tfidf, tfidf.transform(projects_df["Required_Skills"]))

# Sort the similarity scores and get the top 5 matching projects
top_indices = similarity_scores.argsort()[0][::-1][:25]
top_projects = projects_df.iloc[top_indices]



href=""

# Show the recommended projects
if user_input:
    st.title("Recommended Projects")
    for i, project in top_projects.iterrows():
        show_project(project,i,level)
    recommended_projects_df = pd.DataFrame({
        "Objective": top_projects["Project_domain"],
        "Output": top_projects["Project_title"],
        "Type": top_projects["Project_type"],
        "Desc": top_projects["Description"],
        "Company_name": top_projects["Company_name"],
        "Contact":top_projects["Contact"]
    })
    
    # Add a button to download the recommended projects as a CSV file
    csv = recommended_projects_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="recommended_projects.csv">Download CSV File</a>'
    

elif ques:
    st.title("Answer to your Query")
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=ques,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    # print(response)
    st.write(response)


elif saved:
    st.title("Favourites: ")
    for n in mycol.find():
        
        
        st.write("*Project:* " ,n['Project_title'])
        st.write("*Objective:* " ,n["Project_domain"])
        st.write("*Type:* " ,n["Project_type"])
        st.sidebar.write(" ")
        st.sidebar.write(" ")
        dele=st.button("Delete", key=n["_id"] ) 
        g=n["_id"]
        st.write("-----")
        if dele:
            myquery = { "_id": n["_id"] }
            mycol.delete_one(myquery)


else:
    st.title("Welcome to Project Predictor")
    st.write("Please enter your skills to get project recommendations.")
    a= ""
    components.html(
        """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    * {box-sizing: border-box;}
    body {font-family: Verdana, sans-serif;}
    .mySlides {display: none;}
    img {vertical-align: middle;}

    /* Slideshow container */
    .slideshow-container {
    max-width: 800px;
    position: relative;
    margin: auto;
    margin-left:110px;
    }

    /* Caption text */
    .text {
    color: #f2f2f2;
    font-size: 15px;
    padding: 8px 12px;
    position: absolute;
    bottom: 8px;
    width: 100%;
    text-align: center;
    }

    /* Number text (1/3 etc) */
    .numbertext {
    color: #f2f2f2;
    font-size: 12px;
    padding: 8px 12px;
    position: absolute;
    top: 0;
    }

    /* The dots/bullets/indicators */
    .dot {
    height: 15px;
    width: 15px;
    margin: 0 2px;
    background-color: #bbb;
    border-radius: 50%;
    display: inline-block;
    transition: background-color 0.6s ease;
    }

    .active {
    background-color: #717171;
    }

    /* Fading animation */
    .fade {
    animation-name: fade;
    animation-duration: 1.5s;
    }

    @keyframes fade {
    from {opacity: .4} 
    to {opacity: 1}
    }

    /* On smaller screens, decrease text size */
    @media only screen and (max-width: 300px) {
    .text {font-size: 11px}
    }

    .animate-charcter
    {
    font-size:42px;
    text-transform: uppercase;
     background: -webkit-linear-gradient(#eee, #333);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-left:-120px;
    }

    @keyframes textclip {
    to {
        background-position: 200% center;
    }
    }

    </style>
    </head>
    <body style='background-color:rgb(14, 17, 23);;'>



    <h1 class=animate-charcter style="text-align:center;padding-top: 20px;">Domain:</h1>
    <div class="slideshow-container">
    <h1>"""+a+"""</h1>

    <div class="mySlides fade">
    <div class="numbertext">1 / 6</div>
    <img src="https://dsc.ui.ac.id/wp-content/uploads/2023/02/web-devel.jpg" style="width:685px;height:460px;box-shadow: 7px 7px 15px purple;">
    
    </div>

    <div class="mySlides fade">
    <div class="numbertext">2 / 6</div>
    <img src="https://riseuplabs.com/wp-content/uploads/2021/07/mobile-application-development-guidelines-riseuplabs.jpg" style="width:685px;height:460px;box-shadow: 7px 7px 15px purple;">
    
    </div>

    <div class="mySlides fade">
    <div class="numbertext">3 / 6</div>
    <img src="https://static1.shine.com/l/m/images/blog/Machine_Learning_Interview_Questions.jpg" style="width:685px;height:450px;box-shadow: 7px 7px 15px purple;">

    </div>

    <div class="mySlides fade">
    <div class="numbertext">4 / 6</div>
    <img src="https://www.simplilearn.com/ice9/free_resources_article_thumb/iot-explained-what-it-is-how-it-works-and-its-applications-banner.jpg" style="width:685px;height:450px;box-shadow: 7px 7px 15px purple;">

    </div>

    <div class="mySlides fade">
    <div class="numbertext">5 / 6</div>
    <img src="https://images.livemint.com/img/2021/09/21/1600x900/t1_(2)_1632214319987_1632214326323.jpg" style="width:685px;height:450px;box-shadow: 7px 7px 15px purple;">
    
    </div>

    <div class="mySlides fade">
    <div class="numbertext">6 / 6</div>
    <img src="https://etimg.etb2bimg.com/photo/97787288.cms" style="width:685px;height:450px;box-shadow: 7px 7px 15px purple;">
    
    </div>

    </div>
    <br>

    <div style="text-align:center;margin-left:-140px;">
    <span class="dot"></span> 
    <span class="dot"></span> 
    <span class="dot"></span> 
    <span class="dot"></span> 
    <span class="dot"></span> 
    <span class="dot"></span> 
    </div>

    <script>
    let slideIndex = 0;
    showSlides();

    function showSlides() {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slideIndex++;
    if (slideIndex > slides.length) {slideIndex = 1}    
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
    setTimeout(showSlides, 2000); // Change image every 2 seconds
    }
    </script>

    </body>
    </html> 

        """,
    height=600,
    )
    
st.sidebar.markdown(href, unsafe_allow_html=True)  

# Count of skills in dataset
count_df = pd.DataFrame({
    'skills': tfidf.get_feature_names_out(),
    'count': tfidf.transform(projects_df["Required_Skills"]).sum(axis=0).A1
})
count_df = count_df.sort_values('count', ascending=False)

# Show the skill count graph
st.write("-----")
st.title("Skills Count in Dataset:")
fig = px.bar(count_df[:20], x='skills', y='count')
st.plotly_chart(fig)
st.write("-----")
st.title("About :")
st.write("")



r1,r2,r3=st.columns(3)
with r1:
    components.html("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    .card {
    position: relative;
    width: 220px;
    height: 320px;
    background: mediumturquoise;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: bold;
    border-radius: 15px;
    cursor: pointer;
    }

    .card::before,
    .card::after {
    position: absolute;
    content: "";
    width: 20%;
    height: 20%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: bold;
    background-color: lightblue;
    
    }

    .card::before {
    top: 0;
    right: 0;
    border-radius: 0 15px 0 100%;
    }

    .card::after {
    bottom: 0;
    left: 0;
    border-radius: 0 100%  0 15px;
    }

    .card:hover::before,
    .card:hover:after {
    width: 100%;
    height: 100%;
    border-radius: 15px;
    transition: all 0.5s;
    }

    .card:hover:after {
    content: "The project Recommedation System that matches candidates to suitable projects based on their skills and preferences. The system is designed to be user-friendly and intuitive, allowing candidates to input their skills and preferences and receive a list of recommended projects that match their qualifications. ";
    }
    </style>
    </head>
    <body>
    <div class="card">What</div>
    </body>
    </html>
    """,height=400,)

with r2:
        components.html("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    .card {
    position: relative;
    width: 220px;
    height: 320px;
    background: mediumturquoise;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: bold;
    border-radius: 15px;
    cursor: pointer;
    }

    .card::before,
    .card::after {
    position: absolute;
    content: "";
    width: 20%;
    height: 20%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: bold;
    background-color: lightblue;
    transition: all 0.5s;
    }

    .card::before {
    top: 0;
    right: 0;
    border-radius: 0 15px 0 100%;
    }

    .card::after {
    bottom: 0;
    left: 0;
    border-radius: 0 100%  0 15px;
    }

    .card:hover::before,
    .card:hover:after {
    width: 100%;
    height: 100%;
    border-radius: 15px;
    transition: all 0.5s;
    }

    .card:hover:after {
    content: "The current job market is highly competitive, and it is difficult for candidates to find suitable projects that match their skills and preferences.The project aims to address these challenges by providing a platform that matches candidates to suitable projects based on their skills and preferences. Additionally, the project helps candidates to find meaningful and fulfilling work that matches their skills and preferences.";
    }
    </style>
    </head>
    <body>
    <div class="card">Why</div>
    </body>
    </html>
    """,height=400,)

with r3:
    components.html("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    .card {
    position: relative;
    width: 220px;
    height: 320px;
    background: mediumturquoise;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: bold;
    border-radius: 15px;
    cursor: pointer;
    }

    .card::before,
    .card::after {
    position: absolute;
    content: "";
    width: 20%;
    height: 20%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    font-weight: bold;
    background-color: lightblue;
    transition: all 0.5s;
    }

    .card::before {
    top: 0;
    right: 0;
    border-radius: 0 15px 0 100%;
    }

    .card::after {
    bottom: 0;
    left: 0;
    border-radius: 0 100%  0 15px;
    }

    .card:hover::before,
    .card:hover:after {
    width: 100%;
    height: 100%;
    border-radius: 15px;
    transition: all 0.5s;
    }

    .card:hover:after {
    content: "This involves collecting data on the skills and proficiency levels of candidates, as well as other relevant information such as work experience, education, and certifications. The database can be designed to be flexible and scalable, allowing new candidates and skills to be added as needed";
    }
    </style>
    </head>
    <body>
    <div class="card">How</div>
    </body>
    </html>
    """,height=400,)

st.write("-----")
st.write("<h3>Connect with us:</h3>",unsafe_allow_html=True) 


components.html("""

,
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    .button {
 font-family: inherit;
 font-weight: 400;
 background: #f2295b;
 color: white;
 padding: 0.35em 0;
 font-size: 17px;
 border: none;
 border-radius: 0.7em;
 letter-spacing: 0.08em;
 position: relative;
 display: flex;
 align-content: center;
 align-items: center;
 overflow: hidden;
 height: 2.1em;
 padding-left: 3em;
 padding-right: 0.7em;
 
 
}

.button .icon {
 background: #fff;
 margin-right: 1em;
 height: 2em;
 width: 2em;
 border-radius: 0.5em;
 position: absolute;
 display: flex;
 align-items: center;
 justify-content: center;
 left: 0.3em;
 transition: all .7s;
 margin-left: 80%;
 margin-left: -2px;
 margin-top: 4px;
 margin-bottom: 4px;
}

.shere {
 width: 1.3rem;
 height: 1.3rem;
 
 margin-left: -6px;
 
 
}

.button:hover .icon {
 width: calc(100% - 0.6rem);
 justify-content: space-between;

}

.button:hover .shere {
 width: calc(100% - 0.6rem);
 display: none;
 
}

.button .icon-shere {
 color: #f2295b;
 width: 1.5rem;
 height: 1.5rem;
 display: none;


}

.button:hover .icon .icon-shere {
 display: flex;
 
}
  </style>

</head>
<body>


  <button class="button">
    <div class="icon">
      <a href="https://web.telegram.org/"><svg height="18" width="18" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1024 1024" class="shere">
        <path fill="#f2295b" d="M767.99994 585.142857q75.995429 0 129.462857 53.394286t53.394286 129.462857-53.394286 129.462857-129.462857 53.394286-129.462857-53.394286-53.394286-129.462857q0-6.875429 1.170286-19.456l-205.677714-102.838857q-52.589714 49.152-124.562286 49.152-75.995429 0-129.462857-53.394286t-53.394286-129.462857 53.394286-129.462857 129.462857-53.394286q71.972571 0 124.562286 49.152l205.677714-102.838857q-1.170286-12.580571-1.170286-19.456 0-75.995429 53.394286-129.462857t129.462857-53.394286 129.462857 53.394286 53.394286 129.462857-53.394286 129.462857-129.462857 53.394286q-71.972571 0-124.562286-49.152l-205.677714 102.838857q1.170286 12.580571 1.170286 19.456t-1.170286 19.456l205.677714 102.838857q52.589714-49.152 124.562286-49.152z"></path>
      </svg></a>
      <a href="https://web.telegram.org/z/"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-telegram icon-shere" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.287 5.906c-.778.324-2.334.994-4.666 2.01-.378.15-.577.298-.595.442-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294.26.006.549-.1.868-.32 2.179-1.471 3.304-2.214 3.374-2.23.05-.012.12-.026.166.016.047.041.042.12.037.141-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8.154 8.154 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629.093.06.183.125.27.187.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.426 1.426 0 0 0-.013-.315.337.337 0 0 0-.114-.217.526.526 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09z"></path>
      </svg></a>
      <a href="#"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-instagram icon-shere" viewBox="0 0 16 16">
        <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.917 3.917 0 0 0-1.417.923A3.927 3.927 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.916 3.916 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.926 3.926 0 0 0-.923-1.417A3.911 3.911 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0h.003zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599.28.28.453.546.598.92.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.47 2.47 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.478 2.478 0 0 1-.92-.598 2.48 2.48 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233 0-2.136.008-2.388.046-3.231.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92.28-.28.546-.453.92-.598.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045v.002zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92zm-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217zm0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334z"></path>
      </svg></a>
      <a href="https://www.whatsapp.com/"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-whatsapp icon-shere" viewBox="0 0 16 16">
        <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"></path>
      </svg></a>
    </div>
    <p>Share me</p>
  </button>
</body>
</html>
""",height=600,)

