import csv


def html_reports():
    # Open the CSV file for reading
    with open('testresult.csv', 'r') as file:
        # Create a CSV reader object
        reader = list(csv.reader(file))
        # Create the HTML table
        html = '''<!DOCTYPE html>
    <html>
    <head>
    <title>USB Test Result</title>
    <style>
    table, th, td
        {
            border: 1px solid black;
            font-family: "Helvetica Neue", monospace;
        }
    h1
    {
        font-family: Verdana, sans-serif;
        font-size: 35px;
        font-weight: normal;
        font-style: normal;
    }
    </style>
    </head>
    <body>
    
        <h1>USB TestSuite Results</h1>
    
        <table style="width:60%">
        '''
        # Add a row to the table
        html += '<tr>\n'
        for header in reader[0]:
            html += f'\t\t<td style="background-color:lightgrey;text-align:center;"><b>{header}</b></td>\n'

        html += f'\t</tr>\n'

        # Loop through each row in the CSV file
        for row in reader[1:len(reader) - 3]:
            # Add a row to the table
            html += '\t<tr>\n'

            # Loop through each cell in the row
            for cell in row:
                if cell.lower() == 'pass':
                    # Add a cell to the row
                    html += '\t\t<td style="color:green;text-align:center;">{}</td>\n'.format(cell)

                elif cell.lower() == 'fail':
                    # Add a cell to the row
                    html += '\t\t<td style="color:red;text-align:center;">{}</td>\n'.format(cell)
                else:
                    html += '\t\t<td style="color:black;text-align:center">{}</td>\n'.format(cell)

            # Close the row
            html += '\t</tr>\n'
        html += '</table>\n<br>\n'
        # opening the Table
        html += '<table>\n'
        for result in reader[len(reader) - 3:]:
            html += '<tr>\n'
            for cell in result:
                if "Pass" in cell.split():
                    html += f'\t\t<td style="color:black;background-color:rgba(0, 128, 0, 0.5)"><b>{cell}</b></td>\n'
                elif "Fail" in cell.split():
                    html += f'\t\t<td style="color:black;background-color:rgba(500, 127, 127, 1)"><b>{cell}</b></td>\n'
                else:
                    html += f'\t\t<td style="text-align:center ;color:black;width:70%"><b>{cell}</b></td>\n'
            html += '\t</tr>'

        # Close the table
        html += '''</table>
        <p></p>
        <h3>log file of above Test cases result: 
        <a href='./results/output.log'>output.log_file</a></h3>
        </body>'''

    # Write the HTML code to a file
    with open('./result.html', 'w') as file:
        file.write(html)
