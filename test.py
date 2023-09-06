# import threading
# import streamlit as st

# from PIL import Image

# import datetime
# curr =0
# image_paths = '<img src="https://www.freecodecamp.org/news/content/images/2022/09/jonatan-pie-3l3RwQdHRHg-unsplash.jpg"  width="700" height="400">'
# image_paths1 = '<img src="https://images.freeimages.com/images/previews/ac9/railway-hdr-1361893.jpg"  width="700" height="400">'
# image_paths2 = '<img src="https://www.shutterstock.com/image-photo/mountains-under-mist-morning-amazing-260nw-1725825019.jpg"  width="700" height="400">'
# curr =0
# Images=[image_paths,image_paths1,image_paths2]
# def set_interval(func, sec): 
#     def func_wrapper():
#         set_interval(func, sec) 
#         func()  
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     now = datetime.datetime.now()
#     seconds = now.second%3
#     return seconds
# def doSomething():
#     # print('op')
#     return 's'
# r = set_interval(doSomething, 2)
# st.markdown(Images[r],unsafe_allow_html=True)

# print("--> ",r)

# # Define a list of image paths
# image_paths = '<img src="https://www.freecodecamp.org/news/content/images/2022/09/jonatan-pie-3l3RwQdHRHg-unsplash.jpg"  width="700" height="400">'
# image_paths1 = '<img src="https://images.freeimages.com/images/previews/ac9/railway-hdr-1361893.jpg"  width="700" height="400">'
# image_paths2 = '<img src="https://www.shutterstock.com/image-photo/mountains-under-mist-morning-amazing-260nw-1725825019.jpg"  width="700" height="400">'
# curr =0
# Images=[image_paths,image_paths1,image_paths2]
# col1,col2,col3,col4,col5,col6=st.columns(6)
# with col1:
#     b1=st.button("1", key='1' )
# with col2:
#     b2=st.button("2", key='2' )
# with col3:
#     b3=st.button("3", key='3')
# with col4:
#     b4=st.button("4", key='4')
# with col5:
#     b5=st.button("5", key='5')
# with col6:
#     b6=st.button("6", key='6')


# if b1:
#    curr = 1
#    print(curr)
# elif b2:
#    curr =0
# #    st.markdown(Images[curr],unsafe_allow_html=True)

# elif b3:
#    curr = 1
# #    st.markdown(Images[2],unsafe_allow_html=True)
# else:
#    curr = 2
# #    st.markdown(Images[0],unsafe_allow_html=True)
# st.markdown(Images[curr],unsafe_allow_html=True)


# # Create a list of image objects from the image paths
# images = [Image.open(path) for path in image_paths]

# # Use the Streamlit slider to create the carousel
# with st.beta_container():
#     index = st.slider("Select an image", 0, len(images)-1)
#     st.image(images[index], width=600)

# <!-- <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta http-equiv="X-UA-Compatible" content="IE=edge">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <style>
#     button {
#   height: 4em;
#   width: 15em;
#   border: none;
#   border-radius: 40px;
#   background-color: #fff;
# }

# button span {
#   z-index: 1;
#   display: inline-block;
#   background-color: black;
#   height: 3em;
#   width: 11.5em;
#   border-radius: 25px;
#   color: #fff;
#   line-height: 55px;
#   font-size: 18px;
#   letter-spacing: 3px;
#   transition: all 0.5s;
#   margin-left: 80%;
# }

# button .container {
#   z-index: -1;
#   width: 0;
#   position: relative;
#   display: flex;
#   justify-content: center;
#   transform: translateY(-50px);
#   transition: all 0.4s;
#   margin-left: 80%;
# }

# button .container a{
#   padding: 0 10px;
  
# }

# button:hover span {
#   width: 0;
# }

# button:hover .container {
#   z-index: 2;
#   width: 100%;
# }
#   </style>
# </head>
# <body>
#   <button>
#     <span>Share</span>
#     <div class="container">
#         <a href="https://www.youtube.com/"><svg height="45" width="45" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1024 1024" class="icon">
#             <path fill="" d="M962.267429 233.179429q-38.253714 56.027429-92.598857 95.451429 0.585143 7.972571 0.585143 23.990857 0 74.313143-21.723429 148.260571t-65.974857 141.970286-105.398857 120.32-147.456 83.456-184.539429 31.158857q-154.843429 0-283.428571-82.870857 19.968 2.267429 44.544 2.267429 128.585143 0 229.156571-78.848-59.977143-1.170286-107.446857-36.864t-65.170286-91.136q18.870857 2.852571 34.889143 2.852571 24.576 0 48.566857-6.290286-64-13.165714-105.984-63.707429t-41.984-117.394286l0-2.267429q38.838857 21.723429 83.456 23.405714-37.741714-25.161143-59.977143-65.682286t-22.308571-87.990857q0-50.322286 25.161143-93.110857 69.12 85.138286 168.301714 136.265143t212.260571 56.832q-4.534857-21.723429-4.534857-42.276571 0-76.580571 53.979429-130.56t130.56-53.979429q80.018286 0 134.875429 58.294857 62.317714-11.995429 117.174857-44.544-21.138286 65.682286-81.115429 101.741714 53.174857-5.705143 106.276571-28.598857z"></path>
#         </svg></a>
#         <a href="#"><svg height="45" width="45" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1024 1024" class="icon">
#             <path fill="" d="M123.52064 667.99143l344.526782 229.708899 0-205.136409-190.802457-127.396658zM88.051421 585.717469l110.283674-73.717469-110.283674-73.717469 0 147.434938zM556.025711 897.627196l344.526782-229.708899-153.724325-102.824168-190.802457 127.396658 0 205.136409zM512 615.994287l155.406371-103.994287-155.406371-103.994287-155.406371 103.994287zM277.171833 458.832738l190.802457-127.396658 0-205.136409-344.526782 229.708899zM825.664905 512l110.283674 73.717469 0-147.434938zM746.828167 458.832738l153.724325-102.824168-344.526782-229.708899 0 205.136409zM1023.926868 356.00857l0 311.98286q0 23.402371-19.453221 36.566205l-467.901157 311.98286q-11.993715 7.459506-24.57249 7.459506t-24.57249-7.459506l-467.901157-311.98286q-19.453221-13.163834-19.453221-36.566205l0-311.98286q0-23.402371 19.453221-36.566205l467.901157-311.98286q11.993715-7.459506 24.57249-7.459506t24.57249 7.459506l467.901157 311.98286q19.453221 13.163834 19.453221 36.566205z"></path>
#         </svg></a>
#         <a href="#"><svg height="45" width="45" xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="0 0 1024 1024" class="icon">
#             <path fill="" d="M950.930286 512q0 143.433143-83.748571 257.974857t-216.283429 158.573714q-15.433143 2.852571-22.601143-4.022857t-7.168-17.115429l0-120.539429q0-55.442286-29.696-81.115429 32.548571-3.437714 58.587429-10.313143t53.686857-22.308571 46.299429-38.034286 30.281143-59.977143 11.702857-86.016q0-69.12-45.129143-117.686857 21.138286-52.004571-4.534857-116.589714-16.018286-5.12-46.299429 6.290286t-52.589714 25.161143l-21.723429 13.677714q-53.174857-14.848-109.714286-14.848t-109.714286 14.848q-9.142857-6.290286-24.283429-15.433143t-47.689143-22.016-49.152-7.68q-25.161143 64.585143-4.022857 116.589714-45.129143 48.566857-45.129143 117.686857 0 48.566857 11.702857 85.723429t29.988571 59.977143 46.006857 38.253714 53.686857 22.308571 58.587429 10.313143q-22.820571 20.553143-28.013714 58.88-11.995429 5.705143-25.746286 8.557714t-32.548571 2.852571-37.449143-12.288-31.744-35.693714q-10.825143-18.285714-27.721143-29.696t-28.306286-13.677714l-11.410286-1.682286q-11.995429 0-16.603429 2.56t-2.852571 6.582857 5.12 7.972571 7.460571 6.875429l4.022857 2.852571q12.580571 5.705143 24.868571 21.723429t17.993143 29.110857l5.705143 13.165714q7.460571 21.723429 25.161143 35.108571t38.253714 17.115429 39.716571 4.022857 31.744-1.974857l13.165714-2.267429q0 21.723429 0.292571 50.834286t0.292571 30.866286q0 10.313143-7.460571 17.115429t-22.820571 4.022857q-132.534857-44.032-216.283429-158.573714t-83.748571-257.974857q0-119.442286 58.88-220.306286t159.744-159.744 220.306286-58.88 220.306286 58.88 159.744 159.744 58.88 220.306286z"></path>
#         </svg></a>
#     </div>
# </button>

# </body>
# </html> -->

import streamlit as st
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the database schema
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    rating = Column(Integer)
    review_text = Column(String)

# Connect to the database
engine = create_engine('sqlite:///reviews.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create the review form
with st.form(key='review_form'):
    st.write('Leave a Review')
    name = st.text_input('Name')
    email = st.text_input('Email')
    rating = st.slider('Rating', 1, 5, 3)
    review_text = st.text_area('Review')
    submitted = st.form_submit_button('Submit')

    # Save the review to the database
    if submitted:
        new_review = Review(name=name, email=email, rating=rating, review_text=review_text)
        session.add(new_review)
        session.commit()

# Display the reviews
reviews = session.query(Review).all()
for review in reviews:
    st.write(review.name)
    st.write(review.email)
    st.write(review.rating)
    st.write(review.review_text)
