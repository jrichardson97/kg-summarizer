from dataclasses import dataclass, field

import json
import requests
import pathlib
from time import time

from kg_summarizer.utils import normalize_list, cached_get_pubmed_abstract, unique_name_from_str

def cache_query_knowledge_graph(query_graph, target='aragorn'): 
    file_str = str(query_graph) + target
    filename = f"{unique_name_from_str(file_str)}.json"

    cache_dir = pathlib.Path('./query_cache')
    cache_dir.mkdir(parents=True, exist_ok=True)

    cached_queries = [s.name for s in cache_dir.glob('*.json')]
    if filename in cached_queries:
        print('Loading from cache...')
        with open(cache_dir/filename, 'r') as openfile:
            rjson = json.load(openfile)
    else:
        [response, response_time] = query_knowledge_graph(query_graph, target=target)
        rjson = response.json()

        with open(cache_dir/filename, 'w') as outfile:
            json.dump(rjson, outfile)

    return rjson

def query_knowledge_graph(query_graph, answer_coalesce=False, async_query=False, target='aragorn'):
    start_time = time()

    if target == 'aragorn':
        print('Querying Aragorn...')
        url = (
            'https://aragorn.renci.org/aragorn/{qtype}'
            # 'https://aragorn.renci.org/aragorn/{qtype}?answer_coalesce_type={actype}'
        ).format(
            qtype = 'asyncquery' if async_query else 'query',
            # actype = 'all' if answer_coalesce else 'none',
        )
        callback = 'https://aragorn.renci.org/1.2/aragorn_callback' if async_query else ''
    elif target == 'robokop':
        print('Querying Robokop...')
        url = (
            'https://aragorn.renci.org/robokop/{qtype}?answer_coalesce_type={actype}'
        ).format(
            qtype = 'asyncquery' if async_query else 'query',
            actype = 'all' if answer_coalesce else 'none',
        )
        # url = 'https://robokop-ara.apps.renci.org/#/reasoner/lookup_query_post'
        # url = 'https://robokop-ara.apps.renci.org/query'
        callback = ''
    elif target == 'strider':
        print('Querying Strider...')
        url = 'https://strider.renci.org/1.4/query/'
        callback = ''
    else:
        raise ValueError(f"Target '{target}' not defined")

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    trapi_query = dict(
        callback = callback,
        message = dict(query_graph = query_graph),
    )

    r = requests.post(url, headers=headers, json=trapi_query)
    finish_time =  time()
    runtime = round(finish_time-start_time,2)

    rjson = r.json()
    return rjson

@dataclass
class GraphContainer:
    query_graph: dict
    response: dict
    verbose: bool = True
    result_idx: int = 0
    graph_type: str = field(init=False) # lookup or creative
    sorted_results: list = field(default_factory=list, init=False)
    result: dict = field(default_factory=dict, init=False)
    nodes: dict = field(default_factory=dict, init=False)
    edges: list = field(default_factory=list, init=False)

    def __post_init__(self):
        # Check graph type from query graph
        self.graph_type = 'creative' if 't_edge' in self.query_graph['edges'] else 'lookup'

        # Remove top layer of response dictionary (assumes the query worked)
        self.response = self.response['message']

        # Sort results by score
        self.sorted_results = sorted(
            self.response['results'], key=lambda d: d['analyses'][0]['score'], reverse=True
        )

        # Set current result as top result
        self.set_result(self.result_idx)

    def set_result(self, idx):
        self.result_idx = idx
        self.result = self.sorted_results[idx]
        self.get_node_info()
        self.get_edge_info()
        self.vprint(f"Result: \n{self.result}\n")

    def vprint(self, msg):
        if self.verbose:
            print(msg)

    def get_node_info(self):
        def parse_node_attributes(attr_list_of_dicts, node_norm_name):
            node_attr_data = {
                'description': '',
                'publications': [],
                'same_as': [],
                'smiles': '',
            }

            for attr_dict in attr_list_of_dicts:
                atid = attr_dict['attribute_type_id']

                if atid == 'biolink:same_as':
                    same_as_norm_names = normalize_list(attr_dict['value'])
                    node_attr_data['same_as'].extend([n[1] for n in same_as_norm_names.values() if n[1] != node_norm_name])

                if atid == 'biolink:synonym':
                    node_attr_data['same_as'].extend(attr_dict['value'])

                if (atid == 'biolink:id') and (attr_dict.get('original_attribute_name') == 'standardized_smiles'):
                    node_attr_data['smiles'] = attr_dict['value']

                if atid in ['biolink:description', 'dct:description']:
                    node_attr_data['description'] = attr_dict['value']

                if atid == 'biolink:publications': 
                    # Sometimes there are multiple publication attributes so extend list then fetch non-duplicates at the end
                    publication_ids = attr_dict['value']
                    node_attr_data['publications'].extend(publication_ids)

            # Remove duplicates
            node_attr_data['publications'] = list(set(node_attr_data['publications']))
            node_attr_data['same_as'] = list(set(node_attr_data['same_as']))

            # Fetch publications
            node_attr_data['publications'] = get_publications(node_attr_data['publications'])

            return node_attr_data

        for qnode_name, id_list in self.result['node_bindings'].items():
            for id_dict in id_list: 
                curie = id_dict.get('id')
                node_norm_name = normalize_list([curie])[curie][1]

                node_info = self.response['knowledge_graph']['nodes'][curie]

                self.nodes[node_norm_name] = parse_node_attributes(node_info['attributes'], node_norm_name)

                qcurie = id_dict.get('qnode_id')
                if qcurie is not None:
                    qnode_norm_name = normalize_list([curie])[curie][1]
                    qnode_info = self.response['knowledge_graph']['nodes'][qcurie]
                    self.nodes[node_norm_name]['subclass_of'] = {
                        qnode_norm_name: parse_node_attributes(qnode_info['attributes'], qnode_norm_name),
                    }

    def get_edge_info(self, fetch_pubs=True):
        def parse_edge_attributes(attr_list_of_dicts, fetch_pubs=True):
            edge_attr_data = {
                'publications': [],
            }

            for attr_dict in attr_list_of_dicts:
                atid = attr_dict['attribute_type_id']

                if atid == 'biolink:publications': 
                    # Sometimes there are multiple publication attributes so extend list then fetch non-duplicates at the end
                    publication_ids = attr_dict['value']
                    edge_attr_data['publications'].extend(publication_ids)

                if atid == 'biolink:support_graphs':
                    edge_attr_data['support_graphs'] = attr_dict['value']

            # Remove duplicates
            edge_attr_data['publications'] = list(set(edge_attr_data['publications']))

            if fetch_pubs:
                edge_attr_data['publications'] = get_publications(edge_attr_data['publications'])

            return edge_attr_data

        self.edges = []
        edge_list = []

        if self.graph_type == 'creative':
            for id_dict in self.result['analyses'][0]['edge_bindings']['t_edge']:
                eid = id_dict['id']
                t_edge = self.response['knowledge_graph']['edges'][eid]

                t_sub, t_pred, t_obj = format_spo(t_edge)
                t_edge_attr_data = parse_edge_attributes(t_edge['attributes'], fetch_pubs=fetch_pubs)

                support_graphs = {}
                for sgid in t_edge_attr_data.pop('support_graphs', []):
                    spo_path_sentence = ''
                    sg_edge_list = self.response['auxiliary_graphs'][sgid]['edges']
                    n_edges = len(sg_edge_list)
                    sg_edge_info_list = []
                    for seid_idx, seid in enumerate(sg_edge_list):
                        edge = self.response['knowledge_graph']['edges'][seid]
                        sub, pred, obj = format_spo(edge)
                        edge_attr_data = parse_edge_attributes(edge['attributes'], fetch_pubs=fetch_pubs)

                        sg_edge_info_list.append(dict(
                            subject=sub,
                            object=obj,
                            predicate=pred,
                            **edge_attr_data
                        ))

                        if n_edges == 1:
                            spo_path_sentence += f"{sub} {pred} {obj}."
                        elif seid_idx == n_edges - 1:
                            spo_path_sentence += f"and {sub} {pred} {obj}."
                        else:
                            spo_path_sentence += f"{sub} {pred} {obj}, "

                    support_graphs[spo_path_sentence] = sg_edge_info_list

                edge_list.append(dict(
                    subject=t_sub,
                    object=t_obj,
                    predicate=t_pred,
                    **t_edge_attr_data,
                    support_graphs=support_graphs,
                ))    

            self.edges = edge_list            
            
        else:
            for eid, id_list in self.result['analyses'][0]['edge_bindings'].items():
                id_list = [d['id'] for d in id_list]
                for id in id_list:
                    edge = self.response['knowledge_graph']['edges'][id]
                    sub, pred, obj = format_spo(edge)
                    edge_attr_data = parse_edge_attributes(edge['attributes'], fetch_pubs=False)

                    edge_list.append(dict(
                        subject=sub,
                        object=obj,
                        predicate=pred,
                        **edge_attr_data
                    ))

            self.edges = merge_dicts(edge_list)

            if fetch_pubs:
                for edge in self.edges:
                    edge['publications'] = get_publications(edge['publications'])

    def print_results(self, top_n=5):
        for idx in range(top_n):
            self.result = self.sorted_results[idx]
            print(f"\nResult idx: {idx}")
            try:
                self.get_edge_info(fetch_pubs=False)
            except Exception:
                print('Failed to normalize')
            else:
                for edge in self.edges:
                    print(f"{edge['subject']} {edge['predicate']} {edge['object']}")

        self.set_result(self.result_idx)

    def print_node_info(self, nid, print_biolink_attrs=False):
        if type(nid) == int:
            node_names = [d[0]['id'] for d in self.result['node_bindings'].values()]
            nid = node_names[nid]

        node_info = self.response['knowledge_graph']['nodes'][nid]
        print(125*'*')
        print(node_info.keys())
        print('\n')
        print(node_info['categories'])
        print('\n')
        print(node_info['name'])
        print('\n')

        for attr_dict in node_info['attributes']:
            if (attr_dict['attribute_type_id'] == 'biolink:Attribute') and (not print_biolink_attrs):
                continue
            print(attr_dict)
            print('\n')

            if attr_dict['attribute_type_id'] == 'biolink:same_as':
                print(normalize_list(attr_dict['value']))

    def print_support_graphs(self, sg_list, print_full_edge=True):
        for sg in sg_list:
            print(self.response['auxiliary_graphs'][sg])
            print()
            for eid in self.response['auxiliary_graphs'][sg]['edges']:
                edge = self.response['knowledge_graph']['edges'][eid]
                print_edge(edge, print_full_edge=print_full_edge)
                print()
            print('\n' + 100*'*' + '\n')

    def print_edge_info(self):
        if self.graph_type == 'creative':
            for id_dict in self.result['analyses'][0]['edge_bindings']['t_edge']:
                edge_binding = id_dict['id']
                t_edge = self.response['knowledge_graph']['edges'][edge_binding]

                print_edge(t_edge)

                for attr_dict in t_edge['attributes']:
                    atid = attr_dict['attribute_type_id']

                    if atid == 'biolink:support_graphs':
                        t_edge_support_graphs = attr_dict['value']
                        print(f"\n{125*'*'}\n* Support Graphs\n{125*'*'}")
                        self.print_support_graphs(t_edge_support_graphs)
        else:
            for eid, id_list in self.result['analyses'][0]['edge_bindings'].items():
                id_list = [d['id'] for d in id_list]
                for id in id_list:
                    edge = self.response['knowledge_graph']['edges'][id]
                    print(edge.keys())

                    atid = [attribute['attribute_type_id'] for attribute in edge['attributes']]
                    print(atid)
                        
                    print_edge(edge)
                    print()

        cooccur_support_graphs = self.result['analyses'][0].get('support_graphs', [])
        print(f"\n{125*'*'}\n* Literature Co-Occurrence Support Graphs\n{125*'*'}")
        self.print_support_graphs(cooccur_support_graphs, print_full_edge=False)

def merge_dicts(lod):
    merged_dict = {}
    for entry in lod:
        key = (entry['subject'], entry['object'], entry['predicate'])
        if key in merged_dict:
            merged_dict[key]['publications'].extend(entry['publications'])
        else:
            merged_dict[key] = entry.copy()

    merged_list = list(merged_dict.values())
    return merged_list

def format_spo(edge):
    sub, obj, pred = edge['subject'], edge['object'], edge['predicate']
    ndict = normalize_list([sub, obj])
    nlist = [n[1] for n in ndict.values()]
    if len(nlist) != 2:
        raise Exception(f"Failed to normalize nodes.\nIDs to normalize: {sub}, {obj}\nReturned normalization {ndict}")
    sub, obj = nlist[0], nlist[1]
    pred = pred.split(':')[1].replace('_', ' ')
    return sub, pred, obj

def print_edge(edge, print_full_edge=True):
    sub, pred, obj = format_spo(edge)
    print(f"{sub} {pred} {obj}")
    if print_full_edge:
        print(edge)

def get_publications(pub_id_list):
    pub_list = []
    for pubid in pub_id_list:
        if pubid.startswith('PMID:'):
            abstract = cached_get_pubmed_abstract(pubid)
            if abstract is not None:
                pub_list.append({pubid: abstract})

    return pub_list