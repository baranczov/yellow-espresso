from flask import Flask, render_template, request
from config import DEBUG
from methods import get_weather

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_city = request.form.get("start")
        end_city = request.form.get("end")

        start_weather = get_weather(start_city, get_cached=DEBUG)
        end_weather = get_weather(end_city, get_cached=DEBUG)

        return render_template(
            "weather.html",
            start=start_weather["name"],
            end=end_weather["name"],
            weather_from=start_weather["data"],
            weather_to=end_weather["data"],
            good_from=start_weather["good"],
            good_to=end_weather["good"],
            errors_from=start_weather["errors"],
            errors_to=end_weather["errors"],
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=DEBUG)
