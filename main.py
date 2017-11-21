from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
from database import Base, ShortLink
import random
app = Flask(__name__)

engine = create_engine('sqlite:///smallernatordb.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#this will ensure no collisions
currentSlug = random.randint(0,100000000000000)
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def encode(num, chars):
    if num == 0:
        return chars[0]
    arr = []
    base = len(chars)
    while num:
        num, rem = divmod(num, base)
        arr.append(chars[rem])
    arr.reverse()
    return ''.join(arr)

def decode(string, chars):
    """Decode a Base X encoded string into the number
    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(chars)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += chars.index(char) * (base ** power)
        idx += 1

    return num

def createRandomSlug():
    global currentSlug
    while True:
        slug = encode(currentSlug,chars)
        #check db for slug then break if exists
        if session.query(exists().where(ShortLink.slug==slug)).scalar() == True:
            break
        else:
            return slug

@app.route('/')
def mainPage():
    url = session.query(ShortLink).first()
    if url:
        return render_template('input_field.html', url=url.slug)
    else:
        return render_template('input_field.html', url="")

@app.route('/create', methods=['POST'])
def inputUrl():
    url = session.query(ShortLink).first()
    if request.method == 'POST':
        #take the url and generate a shortlink/slug
        #create redirect with this link
        #add to db
        newSlug = createRandomSlug()
        newLink= ShortLink(destination=request.form['destination'],slug=newSlug)
        session.add(newLink)
        session.commit()
        if url:
            return render_template('input_field.html', url=url.slug)
        else:
            return render_template('input_field.html', url="")

#use var from url example
"""@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username"""


#STORE MANY LINKS 1
#PERSIST FOREVER 2
#RESILIANT TO LOAD SPIKES 3
#USER CAN CHOOSE LINK 4
#THE SHORTER THE BETTER 5
#SHOULD BE FAST 6

# test = ShortLink(id=3, slug='testing', destination='www.dest.com')
# session.add(test)
# session.commit()
# url = session.query(ShortLink).first()
 
# sluga = session.query(exists().where(ShortLink.slug=='ffd')).scalar()
# print sluga
# print url.slug
# print url.id
# print url.destination

