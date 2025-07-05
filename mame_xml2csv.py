# A tool by RetroGameplayer.com - convert MAME XML game list data into .CSV format for easy viewing as a spreadsheet.
# Released under GNU General Public License v3.0

import xml.etree.ElementTree as ET
import csv
import os
import sys
import time

def print_progress(current, total, bar_length=40):
    percent = float(current) / total
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write('\rProcessing: [{0}] {1}% ({2}/{3})'.format(
        arrow + spaces, int(round(percent * 100)), current, total))
    sys.stdout.flush()

# Prompt for XML file
xml_file = input("Enter the MAME XML file, including path (e.g. mame-0.278.xml): ").strip()

# Check if file exists
if not os.path.isfile(xml_file):
    print(f"File '{xml_file}' not found. Please check the path and try again.")
    exit(1)

# Count the number of <machine> entries
print("Counting MAME entries...please wait...")
machine_count = 0
for event, elem in ET.iterparse(xml_file, events=('end',)):
    if elem.tag == 'machine':
        machine_count += 1
    elem.clear()

# Prepare to parse & extract data
print(f"Parsing {machine_count} MAME entries...")

games = []
current = 0
for event, machine in ET.iterparse(xml_file, events=('end',)):
    if machine.tag == 'machine':
        data = {
            'NAME': machine.get('name', ''),
            'DESCRIPTION': '',
            'YEAR': '',
            'MANUFACTURER': '',
            'ROMOF': machine.get('romof', ''),
            'CLONEOF': machine.get('cloneof', ''),
            'ISBIOS': machine.get('isbios', '')
        }
        # Description
        desc = machine.find('description')
        if desc is not None and desc.text:
            data['DESCRIPTION'] = desc.text
        # Year
        year = machine.find('year')
        if year is not None and year.text:
            data['YEAR'] = year.text
        # Manufacturer
        manuf = machine.find('manufacturer')
        if manuf is not None and manuf.text:
            data['MANUFACTURER'] = manuf.text
        games.append(data)
        current += 1
        if current % 100 == 0 or current == machine_count:
            print_progress(current, machine_count)
        machine.clear()

print_progress(machine_count, machine_count)
print("\nWriting CSV file...")

# Write to CSV
output_file = "MAME_Games_List.csv"
with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['NAME', 'DESCRIPTION', 'YEAR', 'MANUFACTURER', 'ROMOF', 'CLONEOF', 'ISBIOS']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for game in games:
        writer.writerow(game)

print(f"Export complete! See '{output_file}' for your .csv file (open with MS Excel or LibreOffice).")
