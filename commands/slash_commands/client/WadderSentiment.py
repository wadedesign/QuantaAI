import nextcord
from nextcord.ext import commands
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
#own cog
# Initialize NLTK modules
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

# Function to perform sentiment analysis on text
def perform_sentiment_analysis(text):
    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    
    # Tokenize the text and remove stop words
    tokens = [word.lower() for word in word_tokenize(text) if word.lower() not in stopwords.words('english')]
    
    # Stem the tokens
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    
    # Calculate the sentiment score
    sentiment_scores = sia.polarity_scores(' '.join(stemmed_tokens))
    return sentiment_scores

# Slash command to perform NLP tasks on text
def setup(bot):
    
    @bot.slash_command(name="nlp", description="Performs natural language processing tasks on text")
    async def perform_nlp(interaction: nextcord.Interaction, text: str):
        # Perform sentiment analysis on the text
        sentiment_scores = perform_sentiment_analysis(text)
        sentiment_score = sentiment_scores['compound']
        
        # Classify the text based on sentiment score
        if sentiment_score > 0.5:
            sentiment_class = "positive"
        elif sentiment_score < -0.5:
            sentiment_class = "negative"
        else:
            sentiment_class = "neutral"
        
        # Create an embed with the sentiment analysis results
        embed = nextcord.Embed(title="Sentiment Analysis Results", description=f"Text: {text}\nSentiment score: {sentiment_score:.2f}\nSentiment class: {sentiment_class}")
        
        # Send the embed to the user
        await interaction.response.send_message(embed=embed)
