import csv
import os

def read_csv(filename): 
    
    with open(filename) as f:
        reader = csv.reader(f)
        data = list(reader)

    return data
    

if __name__ == "__main__":
    filepath = os.path.join(os.getcwd(),"Day9", "NIFTY.csv")
    data = read_csv(filepath)
    low=data[1][2]
    for row in data:
         if row[2] < low:
             low = row[2]
             Date = row[1]

    print(f"The lowest price of {Date} is {low}")          
        