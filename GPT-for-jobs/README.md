This folder contains the code to use openai api for different tasks on job descriptions processing:
- Translation
- Job segmentation
- Job classification
- Skill Extraction
- Salary extraction
- Job recommendation

## pre-requisites
- openai account
- openai api key
- python 3.10 or higher

## Usage
- Set the openai api key in the environment variable
"""
export OPENAI_API_KEY=your_api_key
"""

- Run the code with cli arguments, e.g. to translate from english to french:
```bash
python translate.py --from_lang en --to_lang fr --input input.txt --output output.txt
```

