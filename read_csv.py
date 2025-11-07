import csv


with open('transactions.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)