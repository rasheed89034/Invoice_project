import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from schema import SolorSystemInvoiceForm

load_dotenv()

def extract_invoice_data(transcript: str) -> dict:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
        structured_llm = llm.with_structured_output(SolorSystemInvoiceForm)
        prompt_template = """
        You are an expert data extraction assistant working for a Solar Panel installation company.
        The text provided below is a voice transcript from a salesperson. 
        
        Important Extraction Rules:
        1. The user explicitly says the word "next" to act as a delimiter to jump from one form field to another. Use this to separate the data points.
        2. Carefully analyze the text and extract the values strictly according to the provided schema.
        3. If mathematical calculations (such as 'total_amount', 'remaining_amount', etc.) are required but not explicitly spoken by the user, calculate them yourself based on the provided numerical data (e.g., total_panels * per_panel_price).
        
        Voice Transcript:
        {transcript}
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["transcript"]
        )

        # 4. LangChain Pipeline (Chain)
        chain = prompt | structured_llm

        # 5. Data process karna
        print("AI Brain data extracting...")
        result = chain.invoke({"transcript": transcript})

        # Pydantic object Convert into normal JSON
        return result.model_dump()

    except Exception as e:
        return {"error": f"Error in AI Extraction : {str(e)}"}
