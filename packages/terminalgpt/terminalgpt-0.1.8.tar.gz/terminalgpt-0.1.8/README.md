# TerminalGPT

Welcome to the terminal-based ChatGPT personal assistant app! With the terminalGPT command, you can easily interact with ChatGPT and receive short, easy-to-read answers on your terminal.

ChatGPT is specifically optimized for your machine's operating system, distribution, and chipset architecture, so you can be sure that the information and assistance you receive are tailored to your specific setup.

Whether you need help with a quick question or want to explore a complex topic, TerminalGPT is here to assist you. Simply enter your query and TerminalGPT will provide you with the best answer possible based on its extensive knowledge base.

Thank you for using TerminalGPT, and we hope you find the terminal-based app to be a valuable resource for your day-to-day needs!

# Installation and Usage

1. Install the package with pip install.

```sh
pip install terminalgpt -U
```

2. (Optional) Inject the token to the executable script on your local machine so you don't have to export it every time you open a new terminal

```sh
git clone https://github.com/adamyodinsky/TerminalGPT.git
cd TerminalGPT
export OPENAI_API_KEY=<YOUR_OPEN_AI_KEY>
./inject_token.sh
```

Note: When not using the inject_token.sh script, you will need to export the OPENAI_API_KEY environment variable with your open AI token every time you open a new terminal.

## Usage

```sh
terminalgpt
```
