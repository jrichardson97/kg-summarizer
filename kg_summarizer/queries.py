# TRAPI Query Graphs

# Chemicals that might ameliorate Huntington's Disease.
query_graph_0 = {
  "message": {
    "query_graph": {
      "nodes": {
        "n0": {
          "categories": [
            "biolink:ChemicalEntity"
          ],
          "name": "Chemical Entity"
        },
        "n1": {
          "name": "Huntington disease",
          "categories": [
            "biolink:Disease"
          ],
          "ids": [
            "MONDO:0007739"
          ]
        }
      },
      "edges": {
        "e0": {
          "subject": "n0",
          "object": "n1",
          "predicates": [
            "biolink:ameliorates"
          ]
        }
      }
    }
  }
}


# query_graph_0 = {
#     "nodes": {
#         "n0": {
#             "categories": [
#                 "biolink:ChemicalEntity"
#             ],
#             "name": "Chemical Entity"
#         },
#         "n1": {
#             "name": "Huntington disease",
#             "categories": [
#                 "biolink:Disease"
#             ],
#             "ids": [
#                 "MONDO:0007739"
#             ]
#         }
#     },
#     "edges": {
#         "e0": {
#             "subject": "n0",
#             "object": "n1",
#             "predicates": [
#                 "biolink:ameliorates"
#             ]
#         }
#     }
# }
# Chemicals that interact with a Gene related to Castleman's Disease.
query_graph_1 = {
    "nodes": {
        "n0": {
            "categories": [
                "biolink:ChemicalEntity"
            ],
            "name": "Chemical Entity"
        },
        "n1": {
            "categories": [
                "biolink:Gene"
            ],
            "name": "Gene"
        },
        "n2": {
            "name": "Castleman disease",
            "categories": [
                "biolink:DiseaseOrPhenotypicFeature",
                "biolink:BiologicalEntity",
                "biolink:NamedThing",
                "biolink:Entity",
                "biolink:ThingWithTaxon",
                "biolink:Disease"
            ],
            "ids": [
                "MONDO:0015564"
            ]
        }
    },
    "edges": {
        "e0": {
            "subject": "n0",
            "object": "n1",
            "predicates": [
            "biolink:interacts_with"
            ]
        },
        "e1": {
            "subject": "n1",
            "object": "n2",
            "predicates": [
            "biolink:related_to"
            ]
        }
    }
}

# Genes involved in histone H3 deacetylation.
query_graph_2 = {
    "nodes": {
        "n0": {
            "name": "histone H3 deacetylation",
            "categories": [
                "biolink:BiologicalProcessOrActivity",
                "biolink:BiologicalEntity",
                "biolink:NamedThing",
                "biolink:Entity",
                "biolink:Occurrent",
                "biolink:OntologyClass",
                "biolink:ThingWithTaxon",
                "biolink:PhysicalEssenceOrOccurrent",
                "biolink:BiologicalProcess"
            ],
            "ids": [
                "GO:0070932"
            ]
        },
        "n1": {
            "categories": [
                "biolink:Gene"
            ],
            "name": "Gene"
        }
    },
    "edges": {
        "e0": {
            "subject": "n0",
            "object": "n1",
            "predicates": [
                "biolink:related_to"
            ]
        }
    }
}

# Genes and Chemicals related to GLUT1 deficiency, and to each other.
query_graph_3 = {
    "nodes": {
        "n0": {
            "categories": [
                "biolink:ChemicalEntity"
            ],
            "name": "Chemical Entity"
        },
        "n1": {
            "categories": [
                "biolink:Gene"
            ],
            "name": "Gene"
        },
        "n2": {
            "name": "GLUT1 deficiency syndrome",
            "categories": [
                "biolink:DiseaseOrPhenotypicFeature",
                "biolink:BiologicalEntity",
                "biolink:NamedThing",
                "biolink:Entity",
                "biolink:ThingWithTaxon",
                "biolink:Disease"
            ],
            "ids": [
                "MONDO:0000188"
            ]
        }
    },
    "edges": {
        "e0": {
            "subject": "n0",
            "object": "n1",
            "predicates": [
                "biolink:related_to"
            ]
        },
        "e1": {
            "subject": "n1",
            "object": "n2",
            "predicates": [
                "biolink:related_to"
            ]
        },
        "e2": {
            "subject": "n2",
            "object": "n0",
            "predicates": [
                "biolink:related_to"
            ]
        }
    }
}

# Diseases associated with 2,3,7,8-tetrochlorodibenzo-p-dioxin
query_graph_4 = {
    "nodes": {
        "n0": {
            "name": "2,3,7,8-Tetrachlorodibenzo-P-dioxin",
            "categories": [
                "biolink:MolecularEntity",
                "biolink:ChemicalEntity",
                "biolink:NamedThing",
                "biolink:Entity",
                "biolink:PhysicalEssence",
                "biolink:ChemicalOrDrugOrTreatment",
                "biolink:ChemicalEntityOrGeneOrGeneProduct",
                "biolink:ChemicalEntityOrProteinOrPolypeptide",
                "biolink:PhysicalEssenceOrOccurrent",
                "biolink:SmallMolecule"
            ],
            "ids": [
                "PUBCHEM.COMPOUND:15625"
            ]
        },
    "n1": {
        "categories": [
            "biolink:Disease"
        ],
        "name": "Disease"
    }
    },
    "edges": {
        "e0": {
            "subject": "n0",
            "object": "n1",
            "predicates": [
                "biolink:associated_with"
            ]
        }
    }
}

query_graph_5 = {
    "nodes": {
        "n0": {
            "name": "Bisphenol A",
            "categories": [
                "biolink:SmallMolecule",
                "biolink:MolecularEntity",
                "biolink:ChemicalEntity",
                "biolink:NamedThing",
                "biolink:Entity",
                "biolink:PhysicalEssence",
                "biolink:ChemicalOrDrugOrTreatment",
                "biolink:ChemicalEntityOrGeneOrGeneProduct",
                "biolink:ChemicalEntityOrProteinOrPolypeptide",
                "biolink:PhysicalEssenceOrOccurrent"
            ],
            "ids": [
                "PUBCHEM.COMPOUND:6623"
            ]
        },
        "n1": {
            "categories": [
                "biolink:Gene"
            ],
            "name": "Gene"
        },
        "n2": {
            "categories": [
                "biolink:SequenceVariant"
            ],
            "name": "Sequence Variant"
        },
        "n3": {
            "name": "autism",
            "categories": [
                "biolink:Disease",
                "biolink:DiseaseOrPhenotypicFeature",
                "biolink:BiologicalEntity",
                "biolink:NamedThing",
                "biolink:Entity",
                "biolink:ThingWithTaxon"
            ],
            "ids": [
            "MONDO:0005260"
            ]
        }
        },
        "edges": {
        "e0": {
            "subject": "n0",
            "object": "n1",
            "predicates": [
                "biolink:related_to"
            ]
        },
        "e1": {
            "subject": "n1",
            "object": "n2",
            "predicates": [
                "biolink:related_to"
            ]
        },
        "e2": {
            "subject": "n2",
            "object": "n3",
            "predicates": [
                "biolink:related_to"
            ]
        }
    }
}


LOOKUP_QUERY_GRAPH_LIST = [
    query_graph_0,
    query_graph_1,
    query_graph_2,
    query_graph_3,
    query_graph_4,
    query_graph_5,
]

query_graph_0 = {
    "nodes": {
        "disease": {
            "ids": [
                "MONDO:0015564"
            ]
        },
        "chemical": {
            "categories": [
                "biolink:ChemicalEntity"
            ]
        }
    },
    "edges": {
        "t_edge": {
            "object": "disease",
            "subject": "chemical",
            "predicates": [
                "biolink:treats"
            ],
            "knowledge_type": "inferred"
        }
    }
}

query_graph_1 = {
    "nodes": {
        "gene": {
            "categories": [
                "biolink:Gene"
            ],
            "ids": [
                "NCBIGene:477"
            ]
        },
        "chemical": {
            "categories": [
                "biolink:ChemicalEntity"
            ]
        }
    },
    "edges": {
        "t_edge": {
            "object": "gene",
            "subject": "chemical",
            "predicates": [
                "biolink:affects"
            ],
            "qualifier_constraints": [
                {
                    "qualifier_set": [
                        {
                            "qualifier_type_id": "biolink:object_aspect_qualifier",
                            "qualifier_value": "activity_or_abundance"
                        },
                        {
                            "qualifier_type_id": "biolink:object_direction_qualifier",
                            "qualifier_value": "increased"
                        }
                    ]
                }
            ],
            "knowledge_type": "inferred"
        }
    }
}

CREATIVE_QUERY_GRAPH_LIST = [
    query_graph_0,
    query_graph_1,
]