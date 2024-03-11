import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import send_file

def validate_email(email):
  regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') 
  if re.fullmatch(regex, email):  
      return 1 
  return 0
def valid_password(password):
  pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&+=]).*$"
  result = re.findall(pattern, password)
  if result:
    return 1
  return 0
def line_plot(data):
    plt.plot([3, 2, 1], data)
    plt.xlabel("Users - Months before")
    plt.ylabel("Number of users registered")
    plt.xticks([3, 2, 1])
    plt.savefig('static/3month-users.png')
    plt.close()  # Close the figure to release resources

    # Return the image file as a response
    return send_file('static/3month-users.png', mimetype='image/png')
def song_plot(data):
    plt.plot([3, 2, 1], data)
    plt.xlabel("Users - Months before")
    plt.ylabel("Number of users registered")
    plt.xticks([3, 2, 1])
    plt.savefig('static/3month-songs.png')
    plt.close()  # Close the figure to release resources

    # Return the image file as a response
    return send_file('static/3month-songs.png', mimetype='image/png')
# def line_plot(data):
#    plt.plot([3,2,1], data) 
#    plt.xlabel("Users - Months before")  # add X-axis label 
#    plt.ylabel("Number of users registered")
#    plt.savefig('static/3month-users.png')