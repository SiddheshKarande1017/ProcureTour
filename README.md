# ProcureTour
ProcureTour is a Tour recommendation web app with Restaurant searches using collaborative filtering developed as a part of Microsoft Engage Program'22.The web app include function such as register, login, allow user to give rating, get the recommended places and search Restaurants. Recommendation part is done using KNN machine learning algorithm where rating is provided as a feature to the model. I used cosine similiarity ,matrix to find similiarities between the places that are present in the database. API is developed using flask for recommendation system. Django is used to develop web application.
# System Architecture
![alt text](https://github.com/SiddheshKarande1017/ProcureTour/blob/main/ProcureTour.png?raw=true)
# Installing
1. Create a personal Fork of this repository.
2. Clone the fork with HTTPS, using your local terminal to a preferred location, and cd into the project.
3. Create your virtual environment, and activate it.
   python -m venv env
4. Install dependencies
   pip install -r requirements.txt
5. Run local server
  python manage.py runserver
6. Run app.py
  python app.py
