# doing necessary imports
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
from scrapper import Scrapper
from mongodboperations import MongoOperations
from sqldboperations import SQLOperations
from credentials import Credentials

free_status = True
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        global free_status
        # To maintain the internal server issue on heroku

        if not free_status:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        video_section_link = request.form['content'].replace(" ", "")  # obtaining the searched video section link
        try:
            if video_section_link.rstrip("/").split("/")[-1] != "videos":
                return render_template('home.html', status="No")
        except Exception as e:
            print(e)
            return render_template('home.html', status="No")
        try:
            scrapper_object = Scrapper(video_section_link, video_count=2)
            result = scrapper_object.process_request()
            if result is not None and result[0]:
                return render_template('results.html', rows=result[1])  # show the results to user
            else:
                return redirect(url_for('index'))
        except Exception as e:
            return "No result found"
    else:
        return render_template('home.html',status="")

@app.route('/expand/<document_id>', methods=['GET'])
@cross_origin()
def see_comments(document_id):
    cred_obj = Credentials()
    mongo_obj = MongoOperations(cred_obj.get_mongo_uri())
    sql_obj = SQLOperations(host = cred_obj.get_sql_host(), user=cred_obj.get_sql_user(),
                             password=cred_obj.get_sql_password())
    comments_result = mongo_obj.search_record_from_collection(document_id)
    video_result = sql_obj.fetch_record_by_document_id(document_id)
    results = None
    try:
        results = [video_result[0][0], comments_result.get("comment_data")]
    except Exception as e:
        print(e)
    return render_template('comments.html',result=results)


if __name__ == "__main__":
    app.run()
