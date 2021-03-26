import wikipediaapi
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter.filedialog import askopenfile


root = tk.Tk()
def search_wiki(primary, secondary):
    """search_wiki function takes a primary and secondary argument and uses the primary argument to search a Wikipedia
       page with the the primary argument as the title then stores all paragraphs into a list. Uses the Wikipedia API"""
    find_html = wikipediaapi.Wikipedia(
            language="en",
            extract_format=wikipediaapi.ExtractFormat.HTML
    )
    page_html = find_html.page(primary) # find HTML page with the primary word
    raw = page_html.text # store raw HTML
    soup = BeautifulSoup(raw, 'html.parser') # parse through HTML with Beautiful Soup
    paragraph_list = []
    for paragraph in soup.find_all('p'): # separate paragraphs and add to list
        paragraph_list.append(paragraph)
    return outputcontent(paragraph_list, primary, secondary)


def outputcontent(paragraphs, primary, secondary):
    """outputs the paragraph onto the console. Primary and secondary are used as parameters to find a paragraph that
    contains both words"""
    # make search words lower case to improve search ability
    prim_lower = primary.lower()
    sec_lower = secondary.lower()
    for search in paragraphs:  # iterate through all the paragraphs until both words are found
        if prim_lower and sec_lower in search.text.lower():
            result = search.text  # if both found, return output
            text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
            text_box.insert(1.0, result)
            text_box.grid(column=1, row=10)
            # download file button
            download_button = tk.Button(root, text="Download CSV", command=lambda: outputCSV(primary, secondary, result), font="Arial",
                                        bg="orange", height=1, width=12)
            download_button.grid(column=1, row=11)

def outputCSV(primary, secondary, result):
    """This function outputs the result into a csv file if the download button is pressed"""
    headers = []
    headers.append("input_keywords")
    headers.append("output_content")
    row = []
    row.append(primary + ";" + secondary)
    row.append(result)
    outfile = "contentGenoutput.csv"
    with open(outfile, "w") as csvfile:  # output a csv file containing new output
        csv_write = csv.writer(csvfile)
        csv_write.writerow(headers)  # output header
        csv_write.writerow(row)  # output row
    root.destroy() # close GUI when done


def getCSV():
    """getCSV function reads a CSV file that is uploaded from the user and calls search_wiki function once the primary
    and secondary words are found"""
    file = askopenfile(parent=root, mode="r", title="Choose a file", filetype=[("Csv file", "*.csv")])
    if file is not None:
        headers = []  # empty list for headers
        csv_read = csv.reader(file)
        headers = next(csv_read)  # input headers to the empty list
        for row in csv_read:  # iterate through each row and word within the csv file
            for words in row:
                separate = words.split(";")
                result = search_wiki(separate[0], separate[1])  # perform search


canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(columnspan=3, rowspan=11)

# instructions 1
instructions_1 = tk.Label(root, text="Look Me Up!", font="Arial", fg="orange", width="100")
instructions_1.grid(column=1, row=0)

# instructions 2
instructions_2 = tk.Label(root, text="Want to make a search on your favorite topic? Enter two words below!", font="Arial")
instructions_2.grid(column=1, row=1)

# instructions 3
instructions_3 = tk.Label(root, text="The first word will search the Wikipedia page. The second word will search a paragraph containing both words", font="Arial")
instructions_3.grid(column=1, row=2)

# primary entry
p_entry = tk.Entry(root, font=40)
p_entry.grid(column=1, row=3)

# secondary entry
s_entry = tk.Entry(root, font=40)
s_entry.grid(column=1, row=4)

# generate button
generate_button = tk.Button(root, text="Generate Search", font=50, bg="orange", command=lambda: search_wiki(str(p_entry.get()), str(s_entry.get())))
generate_button.grid(column=1, row=5)

#instructions 5
instructions_5 = tk.Label(root, text="OR you can input your own CSV file!", font="Arial")
instructions_5.grid(column=1, row=6)

# instructions 6
instructions_6 = tk.Label(root, text="The CSV file must contain a header and columns containing TWO search words", font="Arial")
instructions_6.grid(column=1, row=7)

# instructions 7
instructions_7 = tk.Label(root, text='Please separate both search words with a ";"', font="Arial")
instructions_7.grid(column=1, row=8)

# search file button
select_button = tk.Button(root, text="Search File", command=lambda:getCSV(), font="Arial", bg="orange", height=1, width=10)
select_button.grid(column=1, row=9)

root.mainloop()