from bs4 import BeautifulSoup
import string
import re 
import networkx as nx




def openf(path):
    '''Open the file html and create soup object'''
    with open(html_doc,encoding ='utf8') as f:
        html = f.read()
        soup = BeautifulSoup(html,'html.parser')
    return soup


def cleanf(soup):
    '''this function takes in input soup object and clena data.
    it return a list that contains lists where each one is the set of artists that have collaboreted to an album'''
    lista = []
    for psg in soup.find_all('p'):
        if psg.find('strong'):
            if  "Rec." in psg.find('strong').text:
                text = psg.find('strong').text.replace(' and ',',')
                tex = text.replace(' plus ',',')
                te = tex.replace('/', ',')
                lista.append(te.split(','))
#######################################
    for lis in lista:
        for j in range(len(lis)):
            nome = lis[j]
            for i in range(len(nome)):
                if nome[i] == "(":
                    nome1 = nome[:i-1]
                    lis[j] = nome1
####################################     
    set_album = []
    for lis in lista:
        album = []
        for i in range(len(lis)):
            word = lis[i]

            if word == "":
                pass
            elif word[0] == " ":
                    if word[1].isupper():
                        if "Rec." in word:
                            pass
                        else:
                            album.append(word.strip())
            elif  word[0].islower():
                    pass
                    
                    
            elif word[0].isupper():
                if "Rec." in word:
                    pass
                else:
                    album.append(word.strip())
        set_album.append(album)
    return set_album


def makedict(set_album):
    '''This function takes in input the all set of albums and returns a dictionary where keys are tuples of two artists and value the number of collaborations '''
    final_list = []
    tot_coll = dict()
    for album in set_album:
        for i in range(len(album)-1):
            for j  in range(i+1,len(album)):
                couple = list()
                couple.append(album[i])
                couple.append(album[j])
                couple.sort()
                final_list.append(tuple(couple))
    for coll in final_list:
        if coll in list(tot_coll.keys()):
            tot_coll[coll] += 1
        else:
            tot_coll[coll] = 1
    
    return tot_coll


def create_graph(dic):
    "make a graph where nodes are artist and number of collaboration are the weight of the edges"
    G = nx.Graph()
    for val in dic:
        G.add_edge(val[0], val[1], weight=dic[val])
    return G


if __name__ == "__main__":
    html_doc = r"../data/j.html"
    soup = openf(html_doc)
    clean_soup = cleanf(soup)
    col = makedict(clean_soup)
    g = create_graph(col)
    print(len(list(col.keys())))
    print(g.number_of_edges())