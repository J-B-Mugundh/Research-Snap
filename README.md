# 🤖 Research Snap

**Research Snap** is a Streamlit application that allows users to generate a concise summary of an academic profile by fetching data from Google Scholar. The app provides insights into an author's publication statistics, including citation counts and trends, while also generating a visual report and exporting it to a PDF.

## Features

- Fetches Google Scholar data for a specified author.
- Displays a summary report of the author's publications.
- Generates visualizations of publication trends and citation counts.
- Exports the publication summary and visualizations to a PDF file.
- Generates concise summaries using Google Generative AI.

## Requirements

To run this application, you need:

- Python 3.7 or higher
- Required Python libraries:
  - `streamlit`
  - `scholarly`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `fpdf`
  - `python-dotenv`
  - `google.generativeai`

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/Research-Snap.git
   cd research-snap
    ```

2. Create a virtual environment (optional but recommended).

3. Install the required libraries.

4. Set up your Google API key: Create a '.env' file in the root directory of the project and add your Google API key.


## Usage

1. Run the Streamlit app 

```bash 
    streamlit run app.py
```
2. Open your web browser and go to 'http://localhost:8501'.

3. Enter the name of the author you wish to summarize in the input field.

4. Click the '🚀 Generate Summary' button to fetch and display the author’s profile summary, publication statistics, and visual reports.

5. The application will generate a PDF report of the author's publications, which can be downloaded.

## Contributing
Contributions are welcome! If you have suggestions for improvements or bug fixes, please create an issue or submit a pull request.

## Acknowledgements
Streamlit
Google Scholar API
Seaborn
Matplotlib
FPDF
