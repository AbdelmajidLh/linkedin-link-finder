# LinkedIn URL Finder

# Hello, c'est [Abdelmajid][linkedin] 👋
[![My Website](https://img.shields.io/website?style=for-the-badge&url=https%3A%2F%2Fabdelmajidlh.github.io%2FePortfolio%2F)][website] [![LinkedIn](https://img.shields.io/badge/LinkedIn-Abdelmajid%20EL%20HOU-blue?style=for-the-badge&logo=linkedin&logoColor=blue)][linkedin]

[website]: https://abdelmajidlh.github.io/ePortfolio/
[linkedin]: https://www.linkedin.com/in/aelhou/

## Overview

LinkedIn URL Finder is a Python-based tool designed to automate the process of searching and retrieving LinkedIn profile URLs for a list of individuals. This tool is particularly useful for professionals in recruitment, sales, and marketing who require a quick and efficient way to gather LinkedIn information.

## Features

- **Automated Search**: Automatically performs Google searches to find LinkedIn profiles.
- **Error Handling**: Implements exponential backoff strategy to handle HTTP 429 (Too Many Requests) errors.
- **Parallel Processing**: Utilizes multi-threading to speed up the search process across multiple data chunks.
- **Configurable**: Allows customization through a JSON configuration file.
- **Logging**: Provides detailed logs for monitoring the program's progress and troubleshooting issues.
- **Integration with ChatGPT**: Uses OpenAI's ChatGPT to process text data from PDF files into structured Excel files.
- **Easy to Use**: You can run the script on your Windows machine without installing Python.

## Requirements

- Python 3.6 ou supérieur
- `pandas` library
- `openpyxl` library
- `requests` library
- `PyPDF2` library
- `openai` library
- `python-dotenv` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AbdelmajidLh/linkedin-link-finder.git
   ```
2. Navigate to the project directory:
   ```bash
   cd linkedin-link-finder
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   ```

## Configuration

Edit the `conf/config.json` file to set up your configuration:

```json
{
    "api_key_path": "conf/api_key.txt",
    "excel_file_path": "data/input_file.xlsx",
    "output_file_path": "res/output_file.xlsx",
    "pdf_path": "data/company_organigramme.pdf",
    "prompt_template_path": "prompts/prompt_template.txt",
    "nrow": 60,
    "time_sleep": 15,
    "lang": "fr",
    "num": 10,
    "max_retries": 1,
    "start": 0,
    "stop": 1,
    "pause": 3,
    "ignore_gpt_if_excel_exists": true
}
```

- `api_key_path`: [optional if you have an Excel file] The path to the file containing your OpenAI API key.
- `excel_file_path`: [optional] The path to the Excel file containing the data (on Windows, use the slash `/` instead of backslash `\`).
- `output_file_path`: [optional] The path where the output Excel file with LinkedIn URLs will be saved.
- `pdf_path`: [mondatory if Excel file is not provided] The path to the PDF file containing the organizational chart.
- `prompt_template_path`: [do not delete] The path to the prompt template file.
- `nrow`: Number of rows per chunk for processing.
- `time_sleep`: Number of seconds to wait between processing chunks.
- `ignore_gpt_if_excel_exists`: Boolean flag to skip GPT processing if the Excel file is already provided.

## Usage

### Unix or Windows with Python installed

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the main script from the command line:
   ```bash
   python main.py
   ```

3. On VSCode, right-click and run script (see screenshot)
![Run in VSCode](src/img/run_vscode.png)

### On Windows

Double-click on the Python application `main.exe`.

The program will read the Excel file, process the data in chunks, and save the results with LinkedIn URLs in the specified output file (`res/output_file.xlsx`).

To generate the `exe` file, double-click on the `Windows/apk_builder.bat` file.

## Logging

Logs are saved in the `log` directory. Check the logs for detailed information about the program's execution and any errors encountered.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or create issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
This project is licensed for personal use only, not for commercial use. See the [LICENSE](LICENSE) for details.



**Note**: This tool is intended for legitimate purposes and should be used responsibly following LinkedIn's terms of service. The developers are not responsible for any misuse of this tool.

For any questions or support, please contact [abdelmajid.elhou@gmail.com](mailto:abdelmajid.elhou@gmail.com).