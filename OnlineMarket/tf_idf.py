import psycopg2
from math import *
data={}
conn = psycopg2.connect(database="market", user="abdullah", password="mypass", host="127.0.0.1", port="5432")
cur = conn.cursor()
cur.execute("""SELECT id,name_of_list,description from looking_for ;""")
rows = cur.fetchall()
for i in range(len(rows)):
    data[rows[i][0]] = rows[i][1] + ' ' + rows[i][2]
def tf():
    dataset={}

    inser={}




    for doc in sorted(data):
        list_of = []
        splitdoc = data[doc].lower().split()
        inser[doc]=splitdoc
        for term in inser[doc]:




                        frq=inser[doc].count(term.lower()) / float(len(inser[doc]))
                        list_of.append((term,frq))

                        dataset[doc]=list_of



    return dataset
#print tf()

def idf():

    inser = {}
    list_of=[]

    for doc in sorted(data):
        splitdoc = data[doc].lower().split()
        inser[doc] = splitdoc
        for term in inser[doc]:
            num_texts_with_term = len([True for text in data if term.lower() in data[text].lower().split()])
            try:
                frq=1.0 + log(float(len(data)) /num_texts_with_term)
                list_of.append((term, frq))


            except ZeroDivisionError:return 1.0
    dip=list(set(list_of))
    return dip
#print idf()


def tf_idf():
    final={}
    for key,value in tf().items():
        list_to = []

        for t in value:
            for i in range(len(idf())):
                if t[0]==idf()[i][0]:
                    mu=t[1]*idf()[i][1]
                    list_to.append((t[0],mu))
                    final[key]=list_to
    return final






insert_into=tf_idf()
for key,value in insert_into.items():
    for i in range(len(value)):
        id=key
        word=value[i][0]
        frequency=value[i][1]
        query = "INSERT INTO TF_IDF (id, word, frequency) VALUES (%s, %s, %s);"
        data = (id, word, frequency)
        cur.execute(query, data)

        conn.commit()








