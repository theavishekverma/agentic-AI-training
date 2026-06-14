import json
import os
import csv

def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data



if __name__ == "__main__":
    filepath = os.path.join(os.getcwd(),"Day9", "college.json")
    data = read_file(filepath)
    with open("college.csv","w", newline='') as f:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    