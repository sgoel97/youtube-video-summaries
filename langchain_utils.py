from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def get_summary_from_transcript(transcript, llm):
    data = Document(page_content=transcript)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    texts = text_splitter.split_documents([data])

    chain = load_summarize_chain(llm, chain_type='map_reduce')
    out = chain.run(texts)
    
    return out.strip()