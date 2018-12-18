import json
import math


filename = "../InputFolder/unigram_inverted_indexJSON.json"
MU = 1500

invertedIndex = {}

def loadJson(filename):
    global invertedIndex
    with open(filename) as f:
        invertedIndex = json.load(f)

#|C|
def calculate_total_corpus_size():
    #unique terms in corpus
    total_number_of_terms_in_corpus = 0


    #total_number_of_terms_in_corpus = len(invertedIndex.keys())#total number of unique terms in corpus(uncomment it if you want unique terms)


    for key in invertedIndex.keys(): #total number of terms in corpus (*not unique)
        for list in invertedIndex[key]:
            total_number_of_terms_in_corpus = total_number_of_terms_in_corpus+list[1]


    print("the total number of terms in corpus is: ",total_number_of_terms_in_corpus)
    return total_number_of_terms_in_corpus



#|D|
def calculate_total_number_of_terms_in_a_document(docId):
    # unique number of terms in a document
    number_of_terms_in_document = 0
    for key in invertedIndex.keys():
        for listOfDocs in invertedIndex[key]:
            if listOfDocs[0] == docId:
                #number_of_terms_in_document = number_of_terms_in_document + 1 # number of unique terms (uncomment it if you want unique terms)
                number_of_terms_in_document = number_of_terms_in_document + listOfDocs[1]

    print("the total number of terms in the document "+docId+" is: ", number_of_terms_in_document)
    return number_of_terms_in_document


#c(qi)
def occurance_of_query_term_in_collection(query_term):

    list_of_docs_where_query_term_is_present = invertedIndex[query_term]
    number_of_occurances_in_corpus = 0
    for doc in list_of_docs_where_query_term_is_present:
        number_of_occurances_in_corpus = number_of_occurances_in_corpus + doc[1] #seems wrong. why not unique?

    print("the total occurance of term ",query_term," is: ",number_of_occurances_in_corpus)
    return number_of_occurances_in_corpus

#f(qi, D)
def frequency_of_the_term_in_a_given_document(query_term, docId):

    frequency = 0
    for list in invertedIndex[query_term]:
        if list[0] == docId:
            frequency = list[1]

    print("the frequency of the term ", query_term, " in doc ",docId," is: ", frequency)
    return frequency


def probablity(fqi,cqi,C,D):
    score = (fqi+(MU*(cqi/C)))/(D+MU)
    return math.log10(score)


def find_list_of_total_documents():
    list_of_total_documents = []
    for key in invertedIndex.keys():
        for list in invertedIndex[key]:
            if list[0] not in list_of_total_documents:
                list_of_total_documents.append(list[0])
    return list_of_total_documents


def task2(queryId, query):

    document_scores = {}
    loadJson(filename)
    C = calculate_total_corpus_size()
    list_of_docs = find_list_of_total_documents()
    for docId in list_of_docs:
        score = 0
        D = calculate_total_number_of_terms_in_a_document(docId)
        query_term = query.split(" ")
        for term in query_term:
            fqi = frequency_of_the_term_in_a_given_document(term, docId)
            cqi = occurance_of_query_term_in_collection(term)
            score = score + probablity(fqi,cqi,C,D)
            print("the score of the document for term ",term,"is: ",score)

        document_scores[docId] = score

    sorted_smoothing_score = sorted(document_scores.items(), key=lambda kv: kv[1], reverse=True)

    f = open("../OutputFolder/sorted_smoothing_list_"+query+".txt", 'w')

    rank = 1
    for item in sorted_smoothing_score:
        if rank == 100:
            break;
        f.write(str(queryId)+" Q0 "+item[0]+" "+str(rank)+" "+str(item[1])+" LMDirichlet\n")
        rank += 1





# This is the main method.
def main():
    listOfQuery = {1:"carbon emission", 2:"cutting carbon emission", 3:"flexible dieting",
                   4:"flexible dieting and vegetarianism", 5:"information on pest control in greenhouse",
                   6:"pest control greenhouse", 7:"greenhouse apples apple", 8:"green house apples apple"}

    for queryId in listOfQuery.keys():
        task2(queryId,listOfQuery[queryId])

    #



if __name__ == '__main__':
    main();