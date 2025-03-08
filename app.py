from flask import Flask, render_template, request
import wikipedia
import requests


app = Flask(__name__)

# Hugging Face API Key (Replace with your actual key)
HUG_API_KEY = "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"

def fetch_wikipedia_content(topic):
    """Fetch research data from Wikipedia based on a given topic."""
    try:
        summary = wikipedia.summary(topic, sentences=3)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "No Wikipedia page found for this topic."
    except Exception as e:
        return f"Error fetching Wikipedia data: {e}"

def generate_blog(topic):
    """Generates a blog on a given topic using Hugging Face API and Wikipedia research."""

    # Fetch research content from Wikipedia
    research_content = fetch_wikipedia_content(topic)

    # Blog structure prompt
    prompt = f"""
    Generate a well-structured blog post on "{topic}". Follow this format:

    1. **Heading**: Clearly define the topic.
    2. **Introduction**: Provide an engaging introduction.
    3. **Content**: Present detailed and informative content with research.
    4. **Summary**: Summarize key points.

    Research Data:
    {research_content}

    Keep the writing engaging, structured, and professional.
    """

    # **Use a Free Hugging Face Model**
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": f"Bearer {HUG_API_KEY}"}

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.json()}"

@app.route("/", methods=["GET", "POST"])
def index():
    blog_output = ""
    if request.method == "POST":
        topic = request.form["topic"]
        blog_output = generate_blog(topic)
    return render_template("index.html", blog=blog_output)

if __name__ == "__main__":
    app.run(debug=True)
