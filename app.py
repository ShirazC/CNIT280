from flask import Flask, render_template
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def index():
    title = "Epic Tutorials"
    paragraph = ["wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!","wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!wow I am learning so much great stuff!"]

    try:
        return render_template("index.html", title = title, paragraph=paragraph)
    except Exception as e:
        return str(e)

# @app.route("/home/")
# def home():
#     return("Welcome Back")

@app.route("/home/<string:name>/")
def getUser(name):
    return render_template("user.html", name=name)


if __name__ == '__main__':
    app.run()