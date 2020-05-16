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
            elif "b)" in word:
                word1 = word.replace(" b)","")
                album.append(word1)
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


def compute_good_local_community(graph,inp):
    
    teleporting_distribution = {}
    for node_id in graph:
        teleporting_distribution[node_id] = 0
    teleporting_distribution[inp] = 1.
    
    #
    # Computation of the PageRank vector.
  
    pagerank_score = nx.pagerank(graph, alpha=0.85, personalization=teleporting_distribution,weight='weight')
        #
        # Put all nodes in a list and sort the list in descending order of the “normalized_score”.
    normalized_pagerank_score = [(node_id, score / (graph.degree[node_id]))
                                                    for node_id, score in pagerank_score.items()]
    normalized_pagerank_score.sort(key=lambda x: (-x[1], x[0]))
    #
    # LET'S SWEEP!
    min_conductance_value = float("+inf")
    candidate_community = set()
    complement_of_the_candidate_community = set(graph.nodes())
    for sweep_index in range(0, len(normalized_pagerank_score) - 1):
        #
        # Creation of the set of nodes representing the candidate community and
        # its complement to the entire set of nodes in the graph.
        current_node_id = normalized_pagerank_score[sweep_index][0]
        candidate_community.add(current_node_id)
        complement_of_the_candidate_community.remove(current_node_id)
        #
        # Evaluation of the quality of the candidate community according to its conductance value.
        conductance_value = nx.algorithms.cuts.conductance(graph,
                                                        candidate_community,
                                                        complement_of_the_candidate_community)
        #
        # Discard local communities with conductance 0 or 1.
        if conductance_value == 0. or conductance_value == 1.:
            continue
        #
        # Update the values of variables representing the best solution generated so far.
        if conductance_value < min_conductance_value:
            min_conductance_value = conductance_value
            index_set_max_conductance = sweep_index

    # Creation of the set of nodes representing the best local community generated by the sweeping procedure.
        set__node_minimum_conductance = set([node_id for node_id, normalized_score in
                                                    normalized_pagerank_score[
                                                    :index_set_max_conductance + 1]])
    return set__node_minimum_conductance, min_conductance_value


if __name__ == "__main__":
    html_doc = r"../data/j.html"
    soup = openf(html_doc)
    clean_soup = cleanf(soup)
    col = makedict(clean_soup)
    g = create_graph(col)
    print(compute_good_local_community(g,"Glenn Miller "))
    print(len(compute_good_local_community(g,"Glen Miller")[0]))