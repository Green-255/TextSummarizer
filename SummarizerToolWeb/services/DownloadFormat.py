from io import StringIO
import csv

def format_csv(input_text, summary_text, summary_type):
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(["Tekstas", "Santrauka", "Santraukos tipas"])
    writer.writerow([input_text, summary_text, summary_type])

    csv_data = output.getvalue().encode('utf-8-sig')
    output.close()

    return csv_data

def format_list_csv(list):
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Input Text', 'Summary Text', 'Summary Type'])
    
    for s in list:
        writer.writerow([s.input_text, s.summary_text, s.summary_type])
    csv_data = output.getvalue().encode('utf-8-sig')
    output.close()
    return csv_data