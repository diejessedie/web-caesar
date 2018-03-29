from flask import Flask, request, redirect
from caesar import rotate_string
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True

form = """
<!DOCTYPE html>

<html>
    <head>
        <style>
            form {{
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }}
            textarea {{
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }}
        </style>
    </head>
    <body>
        <h1></h1>
        <form method="post">
            <label for="rot">
                Rotate by:
                <input type="text" name="rot" id="rot" value="0">
            </label>
            <textarea name="text">{0}</textarea>
            <input type="submit">

        </form>
    </body>
</html>

"""
@app.route("/", methods=["POST"])
def encrypt():
    rot = request.form["rot"]

    if not rot.isnumeric():
        error = "Please rotate by a numerical value!"
        return redirect("/?error=" + error)

    rot = int(rot)
    text = request.form["text"]
    
    rotated = rotate_string(text, rot)

    template = jinja_env.get_template('caesar-form.html')
        
    return template.render(rotated=rotated)
    

@app.route("/")
def index():
    
    error = request.args.get("error")
    if error:
        error_esc = cgi.escape(error, quote=True)
        error_element = '<p class="error">' + error_esc + '</p>'
    else:
        error_element = ''
    
    template = jinja_env.get_template('caesar-form.html')
        
    return template.render() + error_element

app.run()