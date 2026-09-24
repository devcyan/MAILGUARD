from flask import Flask, render_template, request

from predict import predict_email


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    analysis = None

    email_text = ""
    header_text = ""

    if request.method == "POST":

        email_text = request.form.get(
            "email",
            ""
        ).strip()

        header_text = request.form.get(
            "headers",
            ""
        ).strip()

        if email_text:

            analysis = predict_email(
                email_text,
                header_text
            )

    return render_template(
        "index.html",
        analysis=analysis,
        email_text=email_text,
        header_text=header_text
    )


if __name__ == "__main__":
    app.run(debug=True)