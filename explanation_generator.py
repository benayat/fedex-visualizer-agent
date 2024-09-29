import os
import openai
import pandas as pd

openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_explanation(analysis_result):
    basic_explanation = analysis_result['explanation']
    action_title = analysis_result['action_title']
    measure_type = analysis_result['bin_name']
    bin_representation = analysis_result['bin_representation']
    source_column: pd.Series = analysis_result['source_column']
    result_column: pd.Series = analysis_result['result_column']
    values_to_influence_dict = analysis_result['values_to_influence_dict']
    column_score = analysis_result['column_score']
    # Construct the prompt
    prompt = construct_textual_prompt(basic_explanation, action_title, measure_type,
                                      bin_representation, source_column, result_column, values_to_influence_dict, column_score)

    # Call the OpenAI API
    response = openai.Completion.create(
        engine='gpt4o-mini',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )

    explanation = response.choices[0].text.strip()
    return explanation


def construct_textual_prompt(basic_explanation, action_title, measure_type, bin_representation, source_column, result_column,
                             values_to_influence_dict, column_score):
    # Extract necessary information from the parameters
    col_name = result_column['name']
    source_values_summary = summarize_series(source_column)
    result_values_summary = summarize_series(result_column)

    # Build the prompt
    prompt = f"""
As a data analyst, your mission is to explain the user action, based on the basic explanation and the rest of the data. 
notice changes in the distribution of a specific column between a source dataset and
 a result dataset. You are provided with the following information:

**Information**:

- **Column Name**: {col_name}
- **Measure Type**: {measure_type}
- **Bin Representation**: {bin_representation}
- **Source column Name**: {source_column['name']}
- **Result Dataset Name**: {result_column['name']}
- **Source Column Values**: {source_values_summary}
- **Result Column Values**: {result_values_summary}
- **Result Unique Values and their influence**: {values_to_influence_dict}
- **Column Score**: {column_score}
- **User Action**: {action_title}
- **Basic Explanation**: {basic_explanation}

**Instructions**:

- Write a short paragraph explaining the user action based on the source and result columns.
- Include insights about the bin type and its representation.
- Highlight any significant changes in the unique values between the source and result columns.
- Use professional and clear language that is easy to understand.
- Provide insights into the significance of this change and any potential implications.
- Ensure the explanation is self-contained and comprehensible without additional context.
"""
    return prompt


def summarize_series(series):
    if series.dtype == 'float' or series.dtype == 'int':
        summary = f"mean={series.mean():.2f}, min={series.min()}, max={series.max()}"
    else:
        value_counts = series.value_counts().head(5).to_dict()
        summary = ', '.join([f"{k}: {v}" for k, v in value_counts.items()])
    return summary

def generate_code_instructions(explanation):
    prompt = f"""
You are a senior data analyst reviewing the following explanation:

**Explanation**:
{explanation}

Your task is to translate this explanation into detailed, step-by-step code instructions for a Python developer to create a Matplotlib visualization that reflects the explanation.

**Instructions**:

- Provide clear, unambiguous, and detailed code instructions.
- Specify the type of plot (e.g., bar chart, line plot).
- Include details about data to be plotted (e.g., variables for x and y axes).
- Mention any specific visual elements (e.g., colors, highlighted data points, annotations).
- Include axis labels, plot title, and any legends.
- Do not include any code—only provide instructions.
- Ensure the instructions are sufficient for a developer to write the code without needing additional context.
"""

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )

    instructions = response['choices'][0]['message']['content'].strip()
    return instructions

def generate_matplotlib_code(code_instructions):
    prompt = f"""
You are a Python developer. Based on the following instructions, write Python code using Matplotlib to create the visualization:

**Instructions**:
{code_instructions}

**Requirements**:

- Include all necessary imports (e.g., `import matplotlib.pyplot as plt`).
- Use the data provided in the instructions.
- Implement all visual elements as specified.
- Write clean, well-formatted code following best practices.
- Ensure the code is executable as is.
- Do not include any explanations—only provide the code.
"""

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )

    code = response['choices'][0]['message']['content'].strip()
    return code


def execute_generated_code(code_str):
    # Save the code to a file (optional)
    with open('generated_visualization.py', 'w') as file:
        file.write(code_str)

    # Optionally, execute the code in a restricted namespace
    safe_globals = {'__builtins__': None}
    safe_locals = {}
    exec(code_str, safe_globals, safe_locals)


def visualize_analysis_result(analysis_result):
    explanation = generate_explanation(analysis_result)
    print(explanation)
    code_instructions = generate_code_instructions(explanation)
    print(code_instructions)
    code = generate_matplotlib_code(code_instructions)
    execute_generated_code(code)
    return explanation, code
