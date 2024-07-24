### RockyBot: News Research Tool 📈

<img width="956" alt="Screenshot 2024-07-24 152515" src="https://github.com/user-attachments/assets/6ce39e70-66e4-4f7d-a264-90846905a29e">


##### Overview
RockyBot is a Streamlit application designed to assist users in researching news articles by leveraging the power of AI and natural language processing. This tool allows users to input multiple news article URLs, process their content, and then query the processed information to get insightful answers, along with the sources of those answers.

##### Features
URL Processing: Input up to three news article URLs to fetch and scrape content.
Vector Database Creation: Automatically processes and creates a vector database from the scraped content for efficient searching.
Question Answering: Query the processed content to get detailed answers based on the information from the URLs.
Source Display: View the sources of the answers with correctly formatted URLs.
Technologies Used
Streamlit: For creating the interactive web application.
Requests: For fetching web content.
BeautifulSoup: For parsing and extracting text from HTML.
Langchain: For natural language processing and handling vector stores.
FAISS: For efficient similarity search and indexing.
OpenAI: For embeddings and language model services.
Dotenv: For managing environment variables.

##### Installation
To set up RockyBot locally, follow these steps:

##### Clone the Repository

bash
Copy code
git clone https://github.com/CertifiedAuthur/rockybot.git
cd rockybot

##### Set Up a Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

##### Install Dependencies

bash
Copy code
pip install -r requirements.txt

##### Create a .env File

Create a .env file in the root directory and add your OpenAI API key:

makefile
Copy code
OPENAI_API_KEY=your_openai_api_key_here

##### Run the Application

bash
Copy code
streamlit run app.py
##### Usage
Input URLs: Use the sidebar to enter up to three news article URLs.
Process URLs: Click the "Process URLs" button to scrape and process the content from the entered URLs.
Ask Questions: After processing, input your question about the content in the main area and click "Submit Question" to get answers based on the processed information.
View Answers and Sources: The application will display the answer to your question and list the sources with properly formatted URLs.

##### Example
Input:

URLs:

https://edition.cnn.com/2024/07/21/politics/kamala-harris-biden-endorsement/index.html
[Another URL]
[Another URL]
Question: "Is Biden contesting for president in 2024?"

Output:

Answer: "No, Biden is not contesting for American president. He has announced his decision to not run for re-election in 2024 and is currently serving as the president."
Sources:
[Source URL]

##### Contributing
Feel free to open issues or submit pull requests to enhance the functionality of RockyBot. Contributions and feedback are welcome!

License
This project is licensed under the MIT License. See the LICENSE file for details.
