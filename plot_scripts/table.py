import re
import pandas as pd
from pylatexenc.latex2text import LatexNodes2Text
import matplotlib.pyplot as plt

# Define a function to extract table content
def extract_latex_table(latex_str):
    # Use regex to find the table content between \begin{tabular} and \end{tabular}
    table_regex = re.compile(r'\\begin{tabular}{[^}]+}(.+?)\\end{tabular}', re.DOTALL)
    table_match = table_regex.search(latex_str)
    
    if not table_match:
        raise ValueError("No tabular environment found in the given LaTeX string.")
    
    table_content = table_match.group(1).strip()

    # Remove \hline and split the rows
    rows = table_content.replace('\\hline', '').strip().split('\\\\')
    rows = [row.strip() for row in rows if row.strip()]

    # Extract headers and data
    headers = [header.strip() for header in rows[0].split('&')]
    data = []
    for row in rows[1:]:
        data.append([item.strip() for item in row.split('&')])
    
    return headers, data

# Read the LaTeX file
latex_file = 'table.txt'  # Replace with your LaTeX file path

with open(latex_file, 'r') as file:
    latex_str = file.read()

# Extract headers and data
headers, data = extract_latex_table(latex_str)

# Convert to DataFrame
df = pd.DataFrame(data, columns=headers)

# Convert numerical columns to appropriate data types
df['Wolne pola'] = df['Wolne pola'].astype(int)
df['Czas wykonania (s)'] = df['Czas wykonania (s)'].astype(float)
df['Liczba osiągalnych stanów'] = df['Liczba osiągalnych stanów'].apply(lambda x: float(x.replace('e+', 'E')))
df['Użycie pamięci BDD (MB)'] = df['Użycie pamięci BDD (MB)'].astype(float)

# Plotting the data
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Wolne pola vs Czas wykonania
axs[0, 0].plot(df['Wolne pola'], df['Czas wykonania (s)'], marker='o')
axs[0, 0].set_title('Wolne pola vs Czas wykonania')
axs[0, 0].set_xlabel('Wolne pola')
axs[0, 0].set_ylabel('Czas wykonania (s)')
axs[0, 0].xaxis.set_major_locator(plt.MaxNLocator(integer=True))

# Plot 2: Wolne pola vs Liczba osiągalnych stanów
axs[0, 1].plot(df['Wolne pola'], df['Liczba osiągalnych stanów'], marker='o')
axs[0, 1].set_title('Wolne pola vs Liczba osiągalnych stanów')
axs[0, 1].set_xlabel('Wolne pola')
axs[0, 1].set_ylabel('Liczba osiągalnych stanów')
axs[0, 1].xaxis.set_major_locator(plt.MaxNLocator(integer=True))

# Plot 3: Wolne pola vs Użycie pamięci BDD
axs[1, 0].plot(df['Wolne pola'], df['Użycie pamięci BDD (MB)'], marker='o')
axs[1, 0].set_title('Wolne pola vs Użycie pamięci BDD')
axs[1, 0].set_xlabel('Wolne pola')
axs[1, 0].set_ylabel('Użycie pamięci BDD (MB)')
axs[1, 0].xaxis.set_major_locator(plt.MaxNLocator(integer=True))

# Plot 4: Wolne pola vs Użycie pamięci BDD
axs[1, 1].plot(df['Wolne pola'], df['Użycie pamięci BDD (MB)'], marker='o')
axs[1, 1].set_title('Wolne pola vs Użycie pamięci BDD')
axs[1, 1].set_xlabel('Wolne pola')
axs[1, 1].set_ylabel('Użycie pamięci BDD (MB)')
axs[1, 1].xaxis.set_major_locator(plt.MaxNLocator(integer=True))

plt.savefig('../figures/wykres_wyniki_mcmas_1.png')  # Save the figure as a PNG file
plt.show()
