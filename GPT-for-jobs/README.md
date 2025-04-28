This folder contains the code to use openai api for different tasks on job descriptions processing:
- Translations: Translate titles and descriptions from/to different languages
- classify Sentences: Classify sentences from job descriptions into different categories
- Standardize Job Titles: Standardize job titles and descriptions
- Standardize Locations: Standardize location names into city, region and country level
- Extract Skills: Extract skills from job descriptions

## pre-requisites
- openai account
- openai api key
- python 3.10 or higher

## Usage
- Set the openai api key in the environment variable
"""
export OPENAI_API_KEY=your_api_key
"""

- Run the script
```bash
python translate.py
```

See examples in `examples.ipynb` notebook.
