import pandas as pd

def clean_text_between_markers(file_path, output_path):
    with open(file_path, "r", encoding="utf-8") as file:
        raw_data_new = file.readlines()
    
    skip = False
    filtered_data = []
    for line in raw_data_new:
        # print(line)
        if "contact us" in line.lower():
            # print("SKIP", idx)
            skip = True
            continue
        if "An official website of the United States government" in line:
            print("NOT SKIP")
            skip = False
            continue
        if not skip:
            filtered_data.append(line)
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("".join(filtered_data))

    print(f"Processed file saved to {output_path}")

# 사용 예시
# clean_text_between_markers("raw/crawled_resultsA.csv", "dataset/A.csv")

name = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
for item in name:
    clean_text_between_markers("dataset/" + item + ".csv", "dataset2/" + item + ".csv")