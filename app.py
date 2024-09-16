from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate required Midterm and Final grades
def calculate_required_grades(prelim):
    passing_grade = 75
    prelim_contribution = prelim * 0.20

    if prelim_contribution + (0.30 * 100) + (0.50 * 100) < passing_grade:
        return None, None

    remaining = passing_grade - prelim_contribution
    required_midterm = max(0, (remaining - (0.50 * 100)) / 0.30)
    required_final = max(0, (remaining - (0.30 * 100)) / 0.50)
    
    return required_midterm, required_final

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        try:
            prelim = float(request.form["prelim"])
            if 0 <= prelim <= 100:
                midterm, final = calculate_required_grades(prelim)
                if midterm is None:
                    result = "It is impossible to pass."
                else:
                    result = f"You need at least a Midterm grade of {midterm:.2f} and a Final grade of {final:.2f} to pass."
            else:
                result = "Please enter a Prelim grade between 0 and 100."
        except ValueError:
            result = "Invalid input. Please enter a valid number."
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
