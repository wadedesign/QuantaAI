import os
from nextcord.ext import commands

from langchain.chains import  RetrievalQA

from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.llms.openai import OpenAI

from langchain.text_splitter import (RecursiveCharacterTextSplitter)
from langchain.vectorstores import FAISS

class DocumentCog2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.document_embeddings = None
        self.document_docs = None

    @commands.command(name='wupload_embeddings')
    async def wupload_embeddings(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please upload a document to create embeddings.")
            return

        attachment = ctx.message.attachments[0]
        file_path = f"{attachment.filename}"
        await attachment.save(file_path)
        print("File saved.")

        try:
            loader = TextLoader(file_path)
            doc = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=400)
            docs = text_splitter.split_documents(doc)

            embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
            self.document_embeddings = FAISS.from_documents(docs, embeddings)
            self.document_docs = docs

            if os.path.exists(file_path):
                os.remove(file_path)
                print("File removed.")

        except Exception as e:
            print(f"Error: {e}")
            await ctx.send(f"An error occurred: {e}")
            return

        await ctx.send("Document uploaded and embeddings created successfully. Now you can run the !wask command with your question.")
        print("Confirmation sent.")

    @commands.command(name="wask")
    async def wask(self, ctx, *, question: str):
        if self.document_embeddings is None or self.document_docs is None:
            await ctx.send("Please upload a document first using the /wupload_embeddings command.")
            return

        llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
        qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=self.document_embeddings.as_retriever())
        answer = qa.run(question)

        await ctx.send(answer)

def setup(bot):
    bot.add_cog(DocumentCog2(bot))
