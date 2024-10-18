import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup as bs
import os

# Sorry if the full path causes inconvenience. Sometimes I feel safer using it.
final_folder = "/Users/xinruixie/digital_texts_1/Final/"
epub_folder = "/Users/xinruixie/digital_texts_1/Final/epub_folder"

epub_files = []
tei_headers = []

all_files_in_directory = os.listdir(epub_folder)

for file in all_files_in_directory:
    # Check the file format 
    if file.endswith(".epub"):
        # If it does, add it to the list of epub files
        epub_files.append(file)
print(len(epub_files))

# Process each .epub file
counter = 0
for epub_file in epub_files:
    epub_path = os.path.join(epub_folder, epub_file)
    book = epub.read_epub(epub_path)  # Read the .epub file

    # Extract metadata from the book
    title_metadata = book.get_metadata("DC", "title")
    author_metadata = book.get_metadata("DC", "creator")
    date_metadata = book.get_metadata("DC", "date")

    title = title_metadata[0][0] if title_metadata else "Unknown Title"
    author = author_metadata[0][0] if author_metadata else "Unknown Author"
    date_of_publication = date_metadata[0][0] if date_metadata else "Unknown Date"

    # Determine the output file name based on the .epub file name
    output_file_name = os.path.splitext(epub_file)[0] + ".txt"
    output_path = os.path.join(final_folder, output_file_name)

    # Construct the TEI header
    tei_headers.append(f"""
    <teiHeader>
      <fileDesc>
        <titleStmt>
          <title>{title}</title>
          <author>{author}</author>
        </titleStmt>
        <publicationStmt>
          <date>{date_of_publication}</date>
        </publicationStmt> 
      </fileDesc>
    </teiHeader>
    """)

    with open(output_path, "w", encoding="utf-8") as output:
        output.write(tei_headers[counter] + "\n")  # Write the TEI header to the output file

        # Process each content item in the book
        for content in book.get_items():
            if content.get_type() == ebooklib.ITEM_DOCUMENT:
                html_doc = content.get_content()
            elif content.get_type() == ebooklib.ITEM_UNKNOWN and content.get_name().endswith(".html"):
                html_doc = content.get_content()
            else:
                continue

            soup = bs(html_doc, "xml")
            for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
                output.write(f"<p>{tag.text}</p>\n")
    print(tei_headers[counter])
    counter += 1 

#### Processing from txt to tei
## note: if you see repetitive comments, that is because I adapted the same basic scripts by copy & paste and then adjust based upon that
    
# Strange Tale of Panorama Island 
strange_stopper = "panoramas that he had created."
strange_header = tei_headers[0]
tei_body = ""
with open("Strange Tale of Panorama Island.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "<p>1</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if re.search(r"<p>[1-25]</p>", line):
            if in_div is True:
                tei_body += "</div>"
            line = re.sub(r"<p>([1-25])</p>", r"<div><head>\1</head>", line)
            in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if strange_stopper in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{strange_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Strange Tale of Panorama Island.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# The Edogawa Rampo Reader 
reader_chapter = ["The Daydream", "The Martian Canals", "The Appearance of Osei", "Poison Weeds", "The Stalker in the Attic", "The Air Raid Shelter", "Doctor Mera’s Mysterious Crimes", "The Dancing Dwarf"]

reader_stopper = "dripping from the round object he held in his hands."
reader_header = tei_headers[1]
tei_body = ""
with open("The Edogawa Rampo Reader.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "<p>Tyler, William, ed. Modanizumu: Modernist Fiction from Japan, 1913–1938. Honolulu: U. of Hawaii Press, 2008.</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if any(chapter in line for chapter in reader_chapter):
            if in_div:
                tei_body += "</div>"
                # Escape special characters in chapter title for use in regex
            chapter_name = next((chapter for chapter in reader_chapter if chapter in line), None)
            if chapter_name:
                cleared_title = re.escape(chapter_name)
                line = re.sub(f"{cleared_title}", f"<div><head>{chapter_name}</head>", line, 1)
                in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if reader_stopper in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{reader_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("The Edogawa Rampo Reader.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# Goth
tei_body = ""
goth_header = tei_headers[2]
with open("Goth.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "<p>i</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if re.search(r"<p>[ivxlcm]+</p>", line):
            if in_div is True:
                tei_body += "</div>"
            line = re.sub(r"<p>([ivxlcm]+)</p>", r"<div><head>\1</head>", line)
            in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False
    if "<p>Not that the person walking with her on that path in the woods was a murderer. </p>" in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{goth_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Goth.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# In Ghostly Japan
ghostly_chapter = ["Fragment", "Furisodé", "Incense","A Story of Divination", "Silkworms", "A Passional Karma", "Footprints of the Buddha", "Ululation", "Bits of Poetry", "Japanese Buddhist Proverbs", "Suggestion", "Ingwa-banashi", "Story of a Tengu", "At Yaidzu"] 
ghostly_header = tei_headers[3]
tei_body = ""
with open("In Ghostly Japan.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "<p>Fragment</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if any(chapter in line for chapter in ghostly_chapter):
            if in_div:
                tei_body += "</div>"
                # Escape special characters in chapter title for use in regex
            chapter_name = next((chapter for chapter in ghostly_chapter if chapter in line), None)
            if chapter_name:
                cleared_title = re.escape(chapter_name)
                line = re.sub(f"{cleared_title}", f"<div><head>{chapter_name}</head>", line, 1)
                in_div = True
            tei_body += line
        if re.search(r"<p>([IVXLCM]+)</p>", line):
            line = re.sub(r"<p>([IVXLCM]+)</p>", r"<sec>\1</sec>", line)
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if " THE FULL PROJECT GUTENBERG LICENSE" in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{ghostly_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("In Ghostly Japan.tei", "w") as output_file: 
    output_file.write(soup.prettify())


# Seven Japanese Tales 
seven_chapter = ["A Portrait of Shunkin", "Terror","The Bridge of Dreams", "The Tattooer", "The Thief", "Aguri", "A Blind Man's Tale"]
seven_stopper = "before the night gets any later."
seven_header = tei_headers[4]
seven_starter = re.compile(r"^\s*A Portrait of Shunkin\s*$")
tei_body = ""
with open("Seven Japanese Tales.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False:
        if re.search(seven_starter, line):
            print("Line found.", line.strip())
            in_the_text = True
            tei_body += "<body>\n"
    if in_the_text is True:
        if any(chapter in line for chapter in seven_chapter):
            if in_div:
                tei_body += "</div>"
                # Escape special characters in chapter title for use in regex
            chapter_name = next((chapter for chapter in seven_chapter if chapter in line), None)
            if chapter_name:
                cleared_title = re.escape(chapter_name)
                line = re.sub(f"{cleared_title}", f"<div><head>{chapter_name}</head>", line, 1)
                in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if seven_stopper in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{seven_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Seven Japanese Tales.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# In the Miso Soup
tei_body = ""
miso_header = tei_headers[5]
with open("In The Miso Soup.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "<p>1</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if re.search(r"<p>[1-3]</p>", line):
            if in_div is True:
                tei_body += "</div>"
            line = re.sub(r"<p>([1-3])</p>", r"<div><head>\1</head>", line)
            in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if "<p>“The feather of a swan,” I said.</p>" in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{miso_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("In The Miso Soup.tei", "w") as output_file: 
    output_file.write(soup.prettify())


# Out
out_chapter = ["NIGHT SHIFT", "BATHROOM", "CROWS", "DARK DREAMS", "PIECE WORK", "APARTMENT 412", "EXIT"]
out_stopper = "to be working during the day."
out_header = tei_headers[6]
tei_body = ""
with open("Out.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "APARTMENT 412" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if any(chapter in line for chapter in out_chapter):
            if in_div:
                tei_body += "</div>"
                # Escape special characters in chapter title for use in regex
            chapter_name = next((chapter for chapter in out_chapter if chapter in line), None)
            if chapter_name:
                cleared_title = re.escape(chapter_name)
                line = re.sub(f"{cleared_title}", f"<div><head>{chapter_name}</head>", line, 1)
                in_div = True
            tei_body += line
        if re.search(r"<p>([1-9])</p>", line):
            line = re.sub(r"<p>([1-9])</p>", r"<sec>\1</sec>", line)
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if out_stopper in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{out_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Out.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# kaidan
kaidan_chapter = "THE STORY OF MIMI-NASHI-HŌÏCHI", "OSHIDORI", "THE STORY OF O-TEI", "UBAZAKURA", "DIPLOMACY", "OF A MIRROR AND A BELL", "JIKININKI", "MUJINA", "ROKURO-KUBI", "A DEAD SECRET", "YUKI-ONNA", "THE STORY OF AOYAGI", "JIU-ROKU-ZAKURA", "THE DREAM OF AKINOSUKÉ", "RIKI-BAKA", "HI-MAWARI", "HŌRAI"
kaidan_stopper = "poems and dreams..."
kaidan_header = tei_headers[7]
tei_body = ""
with open("Kaidan.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "<p>THE STORY OF MIMI-NASHI-HŌÏCHI</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if any(chapter in line for chapter in kaidan_chapter):
            if in_div:
                tei_body += "</div>"
                # Escape special characters in chapter title for use in regex
            chapter_name = next((chapter for chapter in kaidan_chapter if chapter in line), None)
            if chapter_name:
                cleared_title = re.escape(chapter_name)
                line = re.sub(f"{cleared_title}", f"<div><head>{chapter_name}</head>", line, 1)
                in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if kaidan_stopper in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{kaidan_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Kaidan.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# Ghastly Tales
tei_body = ""
ghastly_header = tei_headers[8]
with open("Ghastly Tales from the Yotsuya kaidan.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "1 Mino and Densuke" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if re.search(r"<p>\d+\s+.*?<\/p>", line):
            if in_div is True:
                tei_body += "</div>"
            line = re.sub(r"<p>(\d+\s+.*?)<\/p>", r"<div><head>\1</head>", line)
            in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False
    if "<p>5th June–4th July, 1916</p>" in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{ghastly_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Ghastly Tales from the Yotsuya kaidan.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# Shadowing
shadowing_chapter = ["The Reconciliation", "A Legend of Fugen-Bosatsu", "The Screen-Maiden", "The Corpse-Rider", "The Sympathy of Benten", "The Gratitude of the Samébito"]
shadowing_stopper = "and so obtained her in marriage."
shadowing_header = tei_headers[9]
tei_body = ""
with open("Shadowing.txt", encoding = "utf-8") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  for line in input_file:
    if in_the_text is False and "<p>The Reconciliation</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if any(chapter in line for chapter in shadowing_chapter):
            if in_div:
                tei_body += "</div>"
                # Escape special characters in chapter title for use in regex
            chapter_name = next((chapter for chapter in shadowing_chapter if chapter in line), None)
            if chapter_name:
                cleared_title = re.escape(chapter_name)
                line = re.sub(f"{cleared_title}", f"<div><head>{chapter_name}</head>", line, 1)
                in_div = True
            tei_body += line
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
    if shadowing_stopper in line:
        break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{shadowing_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Shadowing.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# Hell Screen
tei_body = ""
hell_header = tei_headers[10]
hell_chapter = ["Hell Screen", "The Spider Thread"]
hell_stopper = "close to noon in Paradise."
with open("Hell Screen.txt", encoding = "utf-8") as input_file:
    in_the_text = False 
    in_div = False 
    in_para = False
    in_hell = False
    test_body = "<body>\n"
    for line in input_file:
        if "<p>Hell Screen</p>" in line:
            in_hell = True
        elif in_hell and "<p>1</p>" in line:
            in_the_text = True  
            tei_body += "<body>\n"
            in_hell = False
        if in_the_text is True: 
            if any(chapter in line for chapter in hell_chapter):
                if in_div:
                    tei_body += "</div>"
                    # Escape special characters in chapter title for use in regex
                chapter_name = next((chapter for chapter in hell_chapter if chapter in line), None)
                if chapter_name:
                    cleared_title = re.escape(chapter_name)
                    line = re.sub(f"{cleared_title}", f"<div><head>{chapter_name}</head>", line, 1)
                    in_div = True
                tei_body += line
            if re.search(r"<p>([1-10])</p>", line):
                line = re.sub(r"<p>([1-10])</p>", r"<sec>\1</sec>", line)
                tei_body += line
            elif re.search(r"\w", line):
                if in_para is False:
                    line = f"<p>\n{line}"
                    in_para = True 
                tei_body += line
            elif not re.search("\w", line) and in_para is True:
                tei_body += "</p>\n"
                in_para = False 
        if hell_stopper in line:
            break
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{hell_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Hell Screen.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# Almost Transparent Blue 
transparent_starter = "It wasn't the sound of an airplane."
tei_body = ""
transparent_header = tei_headers[11]
with open ("Almost Transparent Blue.txt", encoding = "utf-8") as input_file: 
  in_the_text = False  
  in_para = False
  for line in input_file:
    if in_the_text is False and transparent_starter in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif not re.search("\w", line) and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
tei_body += "</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{transparent_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Almost Transparent Blue.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# The Tale of Genji
tei_body = ""
genji_header = tei_headers[12]
genji_stopper = "very deep emotion on both sides."
with open("The Tale of Genji.txt") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  # locate chapter number first 
  chapter_num = r"CHAPTER ([IVXLCM]+)"
  # flag: chapter name
  chapter_found = False
  num_found = "" #store chap numbers found 
  for line in input_file:
    if in_the_text is False and "CHAPTER I" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if chapter_found:
            chapter_name = line.strip()
            if in_div is True:
              tei_body += "</div>"
            title = f"<div><head>{num_found} {chapter_name}</head>"
            in_div = True
            tei_body += title
            chapter_found = False
            continue
        if re.search(chapter_num, line):
            print("found")
            num_found = line.strip()
            chapter_found = True
            continue
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif genji_stopper in line and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{genji_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("The Tale of Genji.tei", "w") as output_file: 
    output_file.write(soup.prettify())

# Japanese Tales from Times Past 
tei_body = ""
past_header = tei_headers[13]
with open("Japanese Tales from Times Past.txt") as input_file:
  in_the_text = False 
  in_div = False 
  in_para = False
  # locate chapter number first 
  chapter_num = r"<p>([1-90])</p>"
  # flag: chapter name
  chapter_found = False
  num_found = "" #store chap numbers found 
  for line in input_file:
    if in_the_text is False and "<p>1</p>" in line:
        in_the_text = True
        tei_body += "<body>\n"
    if in_the_text is True:
        if chapter_found:
            chapter_name = line.strip()
            if in_div is True:
              tei_body += "</div>"
            title = f"<div><head>{num_found} {chapter_name}</head>"
            in_div = True
            tei_body += title
            chapter_found = False
            continue
        if re.search(chapter_num, line):
            print("found")
            num_found = line.strip()
            chapter_found = True
            continue
        elif re.search(r"\w", line):
            if in_para is False:
                line = f"<p>\n{line}"
                in_para = True 
            tei_body += line
        elif "<p>Vol. 31, Tale 37</p>"in line and in_para is True:
            tei_body += "</p>\n"
            in_para = False 
tei_body += "</div>\n</body>\n</text>"
tei = f"<?xml version = '1.0' encoding = 'utf-8'?><TEI>{past_header}{tei_body}</TEI>"
soup = bs(tei, "xml")
with open ("Japanese Tales from Time Past.tei", "w") as output_file: 
    output_file.write(soup.prettify())



tei_folder_name = "tei_folder"
tei_path = os.path.join(final_folder, tei_folder_name)
if not os.path.exists(tei_path):
    os.mkdir(tei_path)

for file in os.listdir(final_folder):
    if file.endswith(".tei"):
       tei_file_path = os.path.join(final_folder, file)
       tei_final_path = os.path.join(tei_path, file)
       os.rename(tei_file_path, tei_final_path)

txt_folder_name = "txt_folder"
txt_path = os.path.join(final_folder, txt_folder_name)
if not os.path.exists(txt_path):
    os.mkdir(txt_path)

for file in os.listdir(final_folder):
    if file.endswith(".txt"):
       txt_file_path = os.path.join(final_folder, file)
       txt_final_path = os.path.join(txt_path, file)
       os.rename(txt_file_path, txt_final_path)