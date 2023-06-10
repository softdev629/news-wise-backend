from fastapi import APIRouter
from langchain.document_loaders import WebBaseLoader
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import AnalyzeDocumentChain

router = APIRouter(prefix="/api/summarize", tags=["summarize"])


@router.get("/news", description="summarize news")
async def summarize_news(url: str):
    loader = WebBaseLoader(url)
    data = loader.load()
    llm = OpenAI(temperature=0)
    summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
    summarize_document_chain = AnalyzeDocumentChain(
        combine_docs_chain=summary_chain)
    summary = summarize_document_chain.run(data[0].page_content)
    return {"summary": summary}
