import pandas as pd
from transformers import pipeline
import datetime
from flask import Flask, render_template, request


app = Flask(__name__)

# Set up the AI model for text generation
generator = pipeline("text-generation", model="gpt2")

def generate_plan(goal, duration):

    # Formulate inputs for the model
    input_text = f"How to learn {goal} in {duration} months."

    # Generate the time-based plan using the model
    response = generator(input_text, max_length=300, num_return_sequences=1)[0]['generated_text']

    # Split the response into lines (each line represents a weekly activity or plan)
    plan_lines = response.split('\n')

    # Return the list of plan lines
    return plan_lines

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        goal = request.form.get("goal")
        duration = request.form.get("duration")
        
        # Ensure duration is an integer
        try:
            duration = int(duration)
        except ValueError:
            return render_template("home.html", error="Please enter a valid number for the duration.")
        
        # Generate the plan
        plan_lines = generate_plan(goal, duration)
        
        # Pass the plan to the template
        return render_template("home.html", plan_lines=plan_lines, goal=goal, duration=duration)
    
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
