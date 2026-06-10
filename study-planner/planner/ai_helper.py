import os

import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

SUMMARY_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
CHAT_URL = "https://router.huggingface.co/v1/chat/completions"
CHAT_MODEL = "meta-llama/Llama-3.1-8B-Instruct"


def _headers():
    if not HF_API_TOKEN:
        raise RuntimeError("HF_API_TOKEN is not set. Add it to your .env file.")
    return {"Authorization": f"Bearer {HF_API_TOKEN}"}


def query_model(prompt):
    payload = {
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
    }

    resp = requests.post(CHAT_URL, headers=_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        raise RuntimeError(f"Hugging Face API error: {data['error']}")

    return data["choices"][0]["message"]["content"]


def summarize_notes(notes):
    payload = {"inputs": notes}

    resp = requests.post(SUMMARY_URL, headers=_headers(), json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"Hugging Face API error: {data['error']}")

    return data[0]["summary_text"]


def generate_study_plan(subject, topics, time_available):
    if isinstance(topics, (list, tuple)):
        topic_list = ", ".join(topics)
    else:
        topic_list = topics

    prompt = (
        f"Create a study plan for {subject}. "
        f"Topics to cover: {topic_list}. "
        f"Total time available: {time_available} hours. "
        f"Break it into focused study sessions."
    )
    return query_model(prompt)


def suggest_resources(topic):
    prompt = f"Suggest 3 good study resources for learning about {topic}."
    return query_model(prompt)


def generate_flashcards(topic):
    prompt = f"Create 5 flashcards about {topic}. Format each as 'Q: ... A: ...'."
    return query_model(prompt)


def generate_quiz(topic):
    prompt = f"Write 5 short quiz questions to test understanding of {topic}."
    return query_model(prompt)


def optimize_schedule(tasks, time_available):
    names = []
    for t in tasks:
        names.append(getattr(t, "name", str(t)))

    prompt = (
        f"I have {time_available} hours to study these tasks: "
        f"{', '.join(names)}. Suggest how to split the time across them."
    )
    return query_model(prompt)
