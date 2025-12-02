# Avoiding paying for ChatGPT Plus

This is scripts I've gathered to avoid paying for ChatGPT Plus, and instead use the API for things I want. 

Benefits for me are

- Pay for what i use
- I typically spend less than $20/mo
- Tighter control on image generation

## How to use this repo

There's three scripts in here for now. Before you run any of them you have to set the `OPENAI_API_KEY` to a API key on your account. If you want to use the newer models, you also need to "verify your organization" or whatever they're calling it nowadays.

### image-generate.py

You'll need to set

- `OPENAI_API_KEY` env var
- the `COST_CHOICE` variable in the code
- create a file called `image-generate-prompt.txt` and put your prompt in there

Then you just run the script and it should output two files

- `{date_str}_generated_image.png`
- `{date_str}_prompt.txt`

### image-modify.py

You'll need to set

- `OPENAI_API_KEY` env var
- the `COST_CHOICE` variable in the code
- create a file called `image-modify-prompt.txt` and put your prompt in there
- create a file called `image.jpg` as the modified image
    - of course you can just change the path to whatever image you want, extension, etc.

Then you just run the script and it should output two files

- `{date_str}_modified_image.png`
- `{date_str}_prompt.txt`

### models-list.py

You'll need to set

- `OPENAI_API_KEY` env var

I don't think it actually calls any API nor does it cost any money to run this, but it still requires an API key to run. It should just print out the different model choices in the console.