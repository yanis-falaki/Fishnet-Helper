# How to Deploy

## Backend:

0. Run `pip install -r requirements.txt`.

1. Create a `.env` file in the root directory and add the following environment variable:
OPENAI_API_KEY=[Your OpenAI API Key]

Replace `[Your OpenAI API Key]` with your actual OpenAI API key obtained from your OpenAI account.

2. Run `llm.py` to generate the initial knowledge database.

3. Run `flask_server.py` to host the server that the frontend will make API calls to (in debug mode) or else deploy it to production.

## Frontend:

1. Open the `client/src/components/QueryBox.tsx` file in your frontend project.

2. Change the domain in the function getResponse to use whatever domain your backend is hosted on.

3. Deploy the react app user whichever service/method you normally would use.
