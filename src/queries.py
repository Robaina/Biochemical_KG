from neo4j import GraphDatabase


def find_negative_deltag_reactions_of_compound(uri, user, password, compound_id):
    def get_reactions(tx):
        query = (
            "MATCH (c:Compound {id: $compound_id})-[:PARTICIPATES_IN]->(r:Reaction) "
            "WHERE r.deltag < 0 "
            "RETURN r.id, r.name, r.deltag"
        )
        result = tx.run(query, compound_id=compound_id)
        return [
            (record["r.id"], record["r.name"], record["r.deltag"]) for record in result
        ]

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        reactions = session.execute_read(get_reactions)

    driver.close()
    return reactions


def find_chemically_similar_compounds(uri, user, password, compound_id):
    def get_similar_compounds(tx):
        query = (
            "MATCH (c:Compound {id: $compound_id})-[:CHEMICALLY_SIMILAR]->(similar:Compound) "
            "RETURN similar.id, similar.name, similar.smiles"
        )
        result = tx.run(query, compound_id=compound_id)
        return [
            (record["similar.id"], record["similar.name"], record["similar.smiles"])
            for record in result
        ]

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        similar_compounds = session.execute_read(get_similar_compounds)

    driver.close()
    return similar_compounds


def find_reactions_with_similar_product_compounds(
    uri, user, password, target_compound_id
):
    driver = GraphDatabase.driver(uri, auth=(user, password))

    def get_reactions(tx):
        query = (
            "MATCH (c:Compound {id: $target_compound_id})-[:CHEMICALLY_SIMILAR]->(similar:Compound), "
            "(similar)-[:PRODUCT_OF]->(r:Reaction) "
            "RETURN r.id AS reaction_id, r.name AS reaction_name, similar.id AS similar_compound_id, "
            "similar.name AS similar_compound_name, similar.smiles AS similar_compound_smiles"
        )
        result = tx.run(query, target_compound_id=target_compound_id)
        return [
            (
                record["reaction_id"],
                record["reaction_name"],
                record["similar_compound_id"],
                record["similar_compound_name"],
                record["similar_compound_smiles"],
            )
            for record in result
        ]

    with driver.session() as session:
        reactions = session.execute_read(get_reactions)
    driver.close()
    return reactions


def find_reactions_involving_compounds(uri, user, password, compound_ids):
    def get_reactions(tx):
        query = (
            "MATCH (c:Compound)-[:PARTICIPATES_IN]->(r:Reaction) "
            "WHERE c.id IN $compound_ids "
            "RETURN r.id, r.name, collect(c.id) as involved_compounds"
        )
        result = tx.run(query, compound_ids=compound_ids)
        return [
            (record["r.id"], record["r.name"], record["involved_compounds"])
            for record in result
        ]

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        reactions = session.execute_read(get_reactions)

    driver.close()
    return reactions


def find_pathways_of_reaction(uri, user, password, reaction_id):
    def get_pathways(tx):
        query = "MATCH (r:Reaction {id: $reaction_id}) " "RETURN r.pathways"
        result = tx.run(query, reaction_id=reaction_id)
        return result.single()[0]

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        pathways = session.execute_read(get_pathways)

    driver.close()
    return pathways
