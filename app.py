import json
import re

import streamlit as st

from kg_summarizer.ai import general_summarize_abstracts
from kg_summarizer.trapi import GraphContainer, query_knowledge_graph
from kg_summarizer.queries import CREATIVE_QUERY_GRAPH_LIST, LOOKUP_QUERY_GRAPH_LIST


def graph_str_to_json(gs):
    p = re.compile('(?<!\\\\)\'')
    gs = p.sub('\"', gs)
    return json.loads(gs)

def submit_query(query_graph, target):
    rjson = query_knowledge_graph(query_graph, target=target)
    n_results = len(rjson['message']['results'])
    st.write(f"Returned {n_results} results")

    if n_results == 0:
        raise Exception('Query failed to return results')    
    
    st.session_state['query_graph'] = query_graph
    st.session_state['target'] = target
    st.session_state['rjson'] = rjson
    st.session_state['n_results'] = n_results

@st.cache_data(show_spinner='Querying target...')
def cached_query(query_graph, target):
    return query_knowledge_graph(query_graph, target=target)

@st.cache_data(show_spinner="Fetching publications...")
def setup_container(query_graph, rjson, result_idx):
    return GraphContainer(query_graph, rjson, verbose=False, result_idx=result_idx)

def display_edge(edge, summarization_type, sentence):
    if summarization_type == 'None':
        for pub in edge['publications']:
            ((pubid, abstract),) = pub.items()
            st.write(f"{pubid}: {abstract}\n\n")
    elif summarization_type == 'General':
        with st.spinner('Summarizing abstracts...'):
            summaries, text = general_summarize_abstracts(edge, sentence)
        st.write(text)
        
        st.write(summaries)
    elif summarization_type == 'Specific':
        pass
    
with st.sidebar:
    target = st.selectbox('Query Target', ('aragorn', 'robokop', 'strider'))
    query_type = st.selectbox('Query Type', ('lookup', 'creative'))

    if query_type == 'lookup':
        graph_list = LOOKUP_QUERY_GRAPH_LIST
    else:
        graph_list = CREATIVE_QUERY_GRAPH_LIST

    query_idx = st.selectbox('Example Number', range(len(graph_list)))
    query_graph = graph_list[query_idx]
    st.write('Query Graph')
    st.json(query_graph)
    st.button('Submit Query', on_click=submit_query, args=(query_graph, target, ))

if 'rjson' in st.session_state:
    with st.form('results'):
        result_idx = st.selectbox('Result Number', range(st.session_state['n_results']), key='result_idx')
        summarization_type = st.selectbox('Summarization Type', ('None', 'General', 'Specific'))
        submitted = st.form_submit_button('Display Result')

        if submitted:
            g = setup_container(query_graph, st.session_state['rjson'], result_idx)

            if query_type == 'creative':
                sub, pred, obj = g.edges[0]['subject'], g.edges[0]['predicate'], g.edges[0]['object']
                st.write(f"Inferred relationship: {sub} {pred} {obj}")

                st.write("Support Graphs")
                for sentence, edge_list in g.edges[0]['support_graphs'].items():
                    with st.expander(sentence):
                        for edge in edge_list:
                            if edge['publications']:
                                display_edge(edge, summarization_type, sentence)
                            else:
                                st.write('No publication evidence')
            else:
                for edge in g.edges:
                    sub, pred, obj = edge['subject'], edge['predicate'], edge['object']
                    sentence = f"{sub} {pred} {obj}"
                    with st.expander(sentence):
                        if edge['publications']:
                            display_edge(edge, summarization_type, sentence)
                        else:
                            st.write('No publication evidence')

