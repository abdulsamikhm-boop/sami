import csv
import os
from datetime import datetime

CSV_FILE = 'expense.csv'
FEILDNAMES = ['ammount','category','description']

def initiative_csv():
    '''CREATION OF A FILE NAMES EXPENSE TRACKER'''
    if not os.path.exists(CSV_FILE):
        with open (CSV_FILE,mode='w',newline='',encoding='utf-8') as file:
            writer = csv.DictWriter(file,fieldnames=FEILDNAMES)
            writer.writeheader()

def add_ammount():
    """adding ammount and also tasks"""
    print('--adding the ammount--')
    while True:
        try:
            ammount = float(input('enter the ammount: '))
            if ammount <= 0:
                print('ammount cannot be smaller than 0')
                continue
            break
        except ValueError:
            print('enter a valid number of ammount!')

    category = input('enter the category (food,furniture,random): ').lower().strip()
    if not category:
        category = 'others'

    description = input ('enter the breif description: ').lower().strip()
    if not description:
        description = 'e/d'

    with open (CSV_FILE,mode='a',newline='',encoding='utf-8') as file:
        writer = csv.DictWriter(file,fieldnames=FEILDNAMES)
        writer.writerow({
            'ammount':ammount,
            'category':category,
            'description':description
        })
    print(f'added successfully {ammount} under {category}')

def sumarize():
    """summarize about"""
    print('summarize')
    if not os.path.exists(CSV_FILE):
        return print('not specific data is available to show !!')
    category_total = {}

    with open (CSV_FILE,mode='r',encoding='utf-8') as file:
        for row in csv.DictWriter(file):
            cat =row['category']
            if cat not in category_total:
                category_total[cat] = 0.0

            category_total[cat] += float(row['ammount']) 

        print('total summary of the expenses')
        for cat, total in category_total.items():
            print(f'{cat}: {total}')

        print(f'total something {sum(category_total.values()):.2f}')

def main():
    initiative_csv()
    while True:
        print('choose between 1-3')
        print(1,'add ammount')
        print(2,'view sumary')
        print(3,'choose to exit')

        user = input('enter the choice: ').lower().strip()
        if user == '1':
            add_ammount()
        elif user == '2':
            sumarize()
        elif user == '3':
            print('byee')
            break
        else:
            print('invalid choice , please choose between 1 to 3')

if __name__ == '__main__':
    main()



