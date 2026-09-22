from flask import Flask, render_template, request
from predict import predict_email

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    confidence = None
    email_text = ""

    if request.method == "POST":

        email_text = request.form.get("email", "").strip()

        if email_text:
            result, confidence = predict_email(email_text)

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        email_text=email_text
    )


if __name__ == "__main__":
    app.run(debug=True)