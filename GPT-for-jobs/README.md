This folder contains the code to use openai api for different tasks on job descriptions processing:
- Translation: Translate titles and descriptions from/to different languages
- Segment Job: divide a job description into different segments
- Standardize Job: standardize job titles and descriptions
- Standardize Location: standardize location names into city, region and country level

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
