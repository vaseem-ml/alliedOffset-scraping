
from flask import Flask, request, render_template
import pandas as pd
import json


app = Flask(__name__)
projects = pd.read_csv("projects.csv")

@app.route('/')
def hello_world():
    countries = pd.read_csv("countries.csv")
    avgBuyPrice = projects["Price"].mean()
    return render_template('index.html', projects=projects, countries=countries, avgPrice=round(avgBuyPrice, 3))


@app.route("/project/<string:code>")
def project(code):
    try:
        project = projects.loc[projects.Code==int(code)]

        print(project)


        return render_template('project.html', project=project)
    except Exception as e:
        print(e)
        return "Something went wrong"



@app.route('/filtered', methods=['POST'])
def filtered():
    countries = pd.read_csv("countries.csv")
    country = request.form['country']
    print("country", country)
    filteredprojects = projects.loc[projects.CountryCode==country]
    if (country=="All Countries"):
        avgBuyPrice = projects["Price"].mean()
        return render_template('index.html', projects=projects, countries=countries, avgPrice=round(avgBuyPrice, 3))
    else:
        avgBuyPrice = filteredprojects["Price"].mean()
        return render_template('index.html', projects=filteredprojects, countries=countries, avgPrice=round(avgBuyPrice, 3))
    


if __name__ == '__main__':  
    app.run(host="0.0.0.0", port=8000)