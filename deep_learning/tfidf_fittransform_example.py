from sklearn.feature_extraction.text import TfidfVectorizer
import os
# with open(r'C:\Users\amrul\Documents\datacamp\nmf\earth.txt', 'r') as fh:
#     earth = fh.readlines()
#
# earth = ' '.join(earth)
#
# with open(r'C:\Users\amrul\Documents\datacamp\nmf\sky.txt', 'r') as fh:
#     sky = fh.readlines()
#
# sky = ' '.join(sky)
#
# articles = [earth, sky]
#
# tfidf = TfidfVectorizer()
# csr_mat = tfidf.fit_transform(articles)
#
# print(csr_mat.toarray())
# tfidf.get_feature_names()

with open(os.path.relpath('../python_scripts/costco_visa_calculator.py','r')) as fh:
    _file_arr=fh.readlines()
    _file_str=' '.join(_file_arr)