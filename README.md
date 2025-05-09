# LLM for Jobs

This repository hosts a series of topics on the Large Language Model(LLM) for Job descriptions and skills. The first part of the repository is focused on the data preparation for the fine-tuning tasks using gpt. The second part is focused on the fine-tuning of the model for different tasks.

It includes mainly two parts:
- **Data Preparation**: How to prepare the data for the fine-tuning tasks using gpt
  - **Translation**: Translate job titles and descriptions from one language to another
  - **Segmentation**: Divide a job description into different segments
  - **standardization**: Standardize job titles and descriptions
  - **Standard Location**: Standardize location names into city region and country level
  - **Skill Extraction**: Extract skills from job descriptions
  - **Skill identification**: Identify the skills from the job description

- **Fine-tuning**: How to fine-tune the model for different tasks


The `GPT-for-jobs` contains the code to use openai api for different tasks on data preparation for different tasks.

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