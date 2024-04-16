def create_compound(tx, compound):
    tx.run(
        "MERGE (c:Compound {id: $id}) "
        "SET c.name = $name, c.formula = $formula, "
        "c.charge = $charge, c.mass = $mass, c.smiles = $smiles",
        id=compound["id"],
        name=compound["name"],
        formula=compound["formula"],
        charge=compound["charge"],
        mass=compound["mass"],
        smiles=compound["smiles"],
        deltag=compound["deltag"],
        pka=compound["pka"],
        pkb=compound["pkb"],
    )


# Function to Create Reaction Nodes
def create_reaction(tx, reaction):
    tx.run(
        "MERGE (r:Reaction {id: $id}) "
        "SET r.name = $name, r.abbreviation = $abbreviation, "
        "r.equation = $equation, r.deltag = $deltag, "
        "r.deltagerr = $deltagerr, r.direction = $direction, "
        "r.ec_numbers = $ec_numbers, r.pathways = $pathways",
        id=reaction["id"],
        name=reaction["name"],
        abbreviation=reaction["abbreviation"],
        equation=reaction["equation"],
        deltag=reaction["deltag"],
        deltagerr=reaction["deltagerr"],
        direction=reaction["direction"],
        ec_numbers=reaction.get("ec_numbers", []),
        pathways=reaction.get("pathways", []),
    )


# Function to Create PARTICIPATES_IN Relationships
def create_participates_in_relationship(tx, compound_id, reaction_id):
    tx.run(
        "MATCH (c:Compound {id: $compound_id}), "
        "(r:Reaction {id: $reaction_id}) "
        "MERGE (c)-[:PARTICIPATES_IN]->(r)",
        compound_id=compound_id,
        reaction_id=reaction_id,
    )


def create_substrate_of_relationship(tx, compound_id, reaction_id, stoichiometry):
    tx.run(
        "MATCH (c:Compound {id: $compound_id}), (r:Reaction {id: $reaction_id}) "
        "MERGE (c)-[:SUBSTRATE_OF {stoichiometry: $stoichiometry}]->(r)",
        compound_id=compound_id,
        reaction_id=reaction_id,
        stoichiometry=stoichiometry,
    )


def create_product_of_relationship(tx, compound_id, reaction_id, stoichiometry):
    tx.run(
        "MATCH (c:Compound {id: $compound_id}), (r:Reaction {id: $reaction_id}) "
        "MERGE (c)-[:PRODUCT_OF {stoichiometry: $stoichiometry}]->(r)",
        compound_id=compound_id,
        reaction_id=reaction_id,
        stoichiometry=stoichiometry,
    )


def create_chemically_similar_relationship(tx, compound1_id, compound2_id, distance):
    tx.run(
        "MATCH (c1:Compound {id: $compound1_id}), (c2:Compound {id: $compound2_id}) "
        "MERGE (c1)-[:CHEMICALLY_SIMILAR {distance: $distance}]->(c2)",
        compound1_id=compound1_id,
        compound2_id=compound2_id,
        distance=distance,
    )
