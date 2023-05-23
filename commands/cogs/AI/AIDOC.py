import os

from langchain import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.llms.openai import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import (CharacterTextSplitter,
                                     RecursiveCharacterTextSplitter)
from langchain.vectorstores import Chroma
from nextcord.ext import commands


class DocumentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.document_text = None
        self.vectorstore = None
        self.memory = None

    @commands.command(name="wupload")
    async def wupload(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please upload a document to summarize.")
            return

        attachment = ctx.message.attachments[0]
        file_path = f"{attachment.filename}"
        await attachment.save(file_path)

        with open(file_path, 'r') as file:
            self.document_text = file.read()

        if os.path.exists(file_path):
            os.remove(file_path)

        await ctx.send("Document uploaded successfully. Now you can run the /wsummarize command.")

    @commands.command(name="wsummarize")
    async def wsummarize(self, ctx):
        if self.document_text is None:
            await ctx.send("Please upload a document first using the /wupload command.")
            return

        llm = OpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=350)
        docs = text_splitter.create_documents([self.document_text])
        chain = load_summarize_chain(llm=llm, chain_type='map_reduce')
        summary = chain.run(docs)

        await ctx.send(summary)

    @commands.command(name="uppers")
    async def uppers(self, ctx):
        if not ctx.message.attachments:
            await ctx.send("Please attach a document to analyze.")
            return

        attachment = ctx.message.attachments[0]
        file_path = f"{attachment.filename}"
        await attachment.save(file_path)

        with open(file_path, 'r', encoding='utf-8') as file:
            document_content = file.read()

        loader = TextLoader(document_content)
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        documents = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma.from_documents(documents, embeddings)

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.memory = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), self.vectorstore.as_retriever(), memory=memory)

        await ctx.send(f"Document '{attachment.filename}' uploaded and processed successfully. You can now ask questions.")


def setup(bot):
    bot.add_cog(DocumentCog(bot))
