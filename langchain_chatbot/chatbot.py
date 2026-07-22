import os
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


class YouTubeChatBot:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            groq_api_key=groq_api_key,
            temperature=0
        )

        self.retriever = None

    def get_video_id(self, url):

        if "watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]

        if "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]

        return url

    def load_video(self, url):

        video_id = self.get_video_id(url)

        transcript = YouTubeTranscriptApi().fetch(video_id)

        text = ""

        for line in transcript:
            text += line.text + " "

        documents = [
            Document(page_content=text)
        ]

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.split_documents(documents)

        vectorstore = FAISS.from_documents(
            docs,
            self.embeddings
        )

        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k":5}
        )

def ask(self, question):

    docs = self.retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    print("Context Length:", len(context))

    prompt = f"""
You are an AI assistant.

Use ONLY the transcript below.

Transcript:
{context}

Question:
{question}

Answer the question directly.

If the answer exists in the transcript, answer it.

Only if it does NOT exist, reply:

I couldn't find that information in this video.
"""

    response = self.llm.invoke(prompt)

    return response.content