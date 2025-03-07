import pandas as pd

def clean_text_between_markers(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        raw_data_new = file.readlines()
    
    skip = True
    filtered_data = []
    skiplist = ["SOURCES\n", "PRINT\n", "SHARE\n" "View All\n", "Program\n", "Articles about Genomics\n", "Genomics Seminars\n", "Sign up for Email Updates\n", "EXPLORE TOPICS\n", "SEARCH\n", "ESPAÑOL\n", "Health Care and Insurance\n", "Disability and Risk Factors\n", "Injuries\n", "Life Stages and Populations\n", "Age Groups\n", "Births\n", "Deaths\n"]
    for line in raw_data_new:
        # print(line)
        skip = False
        for skipline in skiplist:
            if skipline == line:
                skip = True
                break
        if ", 2024" in line:
            skip = True
        if ", 2025" in line:
            skip = True
        if "icon" in line:
            skip = True
        if "ALL PAGES" in line:
            skip = True
        
        if not skip:
            filtered_data.append(line)
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("".join(filtered_data))

    print(f"Processed file saved to {output_path}")

# 사용 예시
# clean_text_between_markers("raw/crawled_resultsA.csv", "dataset/A.csv")

name = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
for item in name:
    clean_text_between_markers("dataset2/" + item + ".csv", "dataset3/" + item + ".csv")