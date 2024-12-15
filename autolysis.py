import os
import pandas as pd
import openai
import matplotlib.pyplot as plt

# Configure OpenAI API Key
openai.api_key = "your_api_key_here"

def analyze_and_generate_report(csv_file):
    # Attempt to read the CSV file with UTF-8 encoding
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        # If UTF-8 fails, fall back to ISO-8859-1 encoding
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    # Basic data analysis
    summary = df.describe(include='all').to_string()

    # Generate a plot (example: histogram of the first numeric column)
    numeric_columns = df.select_dtypes(include=['number']).columns
    if not numeric_columns.empty:
        plt.figure(figsize=(10, 6))
        df[numeric_columns[0]].hist(bins=30, color='blue', edgecolor='black')
        plt.title(f"Histogram of {numeric_columns[0]}")
        plt.xlabel(numeric_columns[0])
        plt.ylabel("Frequency")
        plt.savefig("histogram.png")
        plt.close()

    # Generate a Markdown report
    report_content = f"""# Data Analysis Report

## Summary Statistics

{summary}

## Visualizations

![Histogram](histogram.png)
"""

    # Use OpenAI API to generate a story based on the data summary
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates stories based on data analysis."},
                {"role": "user", "content": f"Generate a story or insight based on the following data summary: {summary}"}
            ]
        )
        story = response.choices[0].message.content
        report_content += f"\n## Generated Story\n\n{story}"
    except Exception as e:
        report_content += f"\n## Generated Story\n\nError generating story: {str(e)}"

    # Save the report as a Markdown file
    with open("report.md", "w") as f:
        f.write(report_content)

    print("Report generated: report.md")

# Main function
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <csv_file>")
    else:
        csv_file = sys.argv[1]
        analyze_and_generate_report(csv_file)
