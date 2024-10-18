import os
import pandas as pd 
import spacy 
from bs4 import BeautifulSoup as bs
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_sm")
final_folder = "/Users/xinruixie/digital_texts_1/Final/"
extracted_titles = []
extracted_text = []

tei_path = "/Users/xinruixie/digital_texts_1/Final/tei_folder"

for file in os.scandir(tei_path):
    if file.name.endswith(".tei"):
        with open(file.path, "r", encoding = "utf-8") as tei_file:
            soup = bs(tei_file, "xml")

            title_match = soup.find("title")
            if title_match:
                title = title_match.getText(strip = True)
                extracted_titles.append(title)

            body_match = soup.find("body")
            if body_match:
                body = body_match.getText(separator = " ", strip = True)

                doc = nlp(body)
                extracted_words = []
            
                for token in doc:
                    # remove stopwords based on built-in stopwords list 
                    if not token.is_stop and token.pos_ in ["NOUN", "ADJ", "VERB"]and not token.ent_type_ in ["LOC", "PERSON", "ORG", "TIME", "QUANTITY", "MONEY", "DATE"]:
                        extracted_words.append(token.lemma_)
                string = " ".join(extracted_words)
                extracted_text.append(string)

vectorizer = TfidfVectorizer(max_df=0.6, min_df=2)
vectorized_texts = vectorizer.fit_transform(extracted_text)
indices_to_word = vectorizer.get_feature_names_out()
document_term_matrix = pd.DataFrame(vectorized_texts.toarray(), index = extracted_titles, columns = indices_to_word)
print(document_term_matrix)

# prepare: write them in their respective folder 
top_20_folder = os.path.join(final_folder, "top_20_words")
top_3_folder = os.path.join(final_folder, "top_3_similar")

os.mkdir(top_20_folder)
os.mkdir(top_3_folder)
#retrieve top 20 words for each work
for extracted_title, df_row in document_term_matrix.iterrows():
    print(f"\n## Doc {extracted_title} weights")
    for word, weight in df_row.sort_values(ascending = False).head(20).items():
        print (word, weight)
        filename = os.path.join(top_20_folder, f"{extracted_title}_top_20.txt")

        with open(filename, "w", encoding = "utf-8") as file:
            for word, weight in df_row.sort_values(ascending = False).head(20).items():
                file.write(f"{word}:{weight}\n")
    
# compare using cosine similarity 
similarity_results = cosine_similarity(vectorized_texts)
similarity_matrix = pd.DataFrame(similarity_results, index = extracted_titles, columns = extracted_titles)
for extracted_title, df_row in similarity_matrix.iterrows():
    sort = df_row.sort_values(ascending = False)
    top_3 = sort.iloc[1:4] # eliminate the one comparing with the file per se

    filename = os.path.join(top_3_folder, f"{extracted_title}_top_3.txt")
    with open (filename, "w", encoding = "utf-8") as file:
        for top_title, similar_text in top_3.items():
            file.write(f"{top_title}:{similar_text}\n")

