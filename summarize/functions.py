# file that contains functions related to logic side

# function to process file upload from input
def handle_uploaded_files(f):
    with open('summarize/static/upload/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
## LangChain functions
from langchain import PromptTemplate, LLMChain
from langchain.llms import Cohere
from langchain.document_loaders import PDFMinerLoader

from .models import Submission

import os

def query_llm():
    
    os.environ["COHERE_API_KEY"] = "XPPJkZ6OHZXtRRvCL17HEgz3y6vLHcNYhkybLeHL"   #!: WARNING API KEY
    llm = Cohere(model='command-xlarge')
    
    query = Submission.objects.last()
    paper_path = query.paper.path
    startSection = query.startSection
    try:
        endSection = query.endSection
    except ValueError:
        endSection = ''
    
    paper_object = PDFMinerLoader(file_path=paper_path)
    paper = paper_object.load()[0].page_content.strip()      # entire pdf is loaded as a single Document
    
    
    start = paper.index(startSection)
    end = paper.index(endSection)

    if startSection == '':
        cleaned_text = paper[:end]
    elif endSection == '':
        cleaned_text = paper[start:]
    else:
        cleaned_text = paper[start:end]
    
    style = """SECTION: name of a section in the text \
    SUMMARY: summary of the text under the SECTION.
    """
    
    template = """
    The following text delimitted by triple backticks is a text taken from a \
    research paper. Each text is corresponding to a certain section in the \
    research paper.
    
    Given this text, return a summary in the following style {style}
    ```
    {text}
    ```
    
    """

    prompt = PromptTemplate(template=template, input_variables=["text", "style"])
    
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    
    input_variables = {
        'text': cleaned_text,
        'style': style
    }
    
    response = llm_chain.run(input_variables)
    
    return response