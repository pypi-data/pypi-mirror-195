def base(self, name):
    '''
    from py2neo import Graph, Node, Relationship, NodeMatcher
    graph = Graph("http://ip:port", auth=("username", "password"))

    #
    Person1 = Node("Person", name="John")
    graph.create(Person1)

    #
    def create_new(person_list):
        for person in person_list:
            Person = Node("Person", name=person)
            graph.create(Person)
    person_list = ["Sally", "Steve", "Mike", "Liz", "Shawn"]
    create_new(person_list)

    #
    def create_new_location(location_list):
        for city, state in location_list:
            Location = Node("Location", city=city, state=state)
            graph.create(Location)
    location_list = [("Miami","Fl"), ("Boston","MA"), ["Lynn", "MA"], ["Portland", "ME"], ["San Francisco", "CA"]]
    create_new_location(location_list)

    #
    matcher = NodeMatcher(graph)
    node_Liz = matcher.match("Person").where(name="Liz").first()
    node_Mike = matcher.match("Person").where(name="Mike").first()
    relation_lize_mike = Relationship(node_Liz, "FRIENDS", node_Mike)
    graph.create(relation_lize_mike)

    relation_lize_mike["since"] = "2021"

    #
    node_Shawn = matcher.match("Person").where(name="Shawn").first()
    node_Sally = matcher.match("Person").where(name="Sally").first()
    relation_shawn_sally = Relationship(node_Shawn, "FRIENDS", node_Sally)
    relation_shawn_sally["since"] = "2001"
    graph.create(relation_shawn_sally)

    #
    def create_new_relation(label1, label2, entity1, entity2, relation, attribute, val):
        node_Shawn = matcher.match(label1).where(name=entity1).first()
        node_Sally = matcher.match(label2).where(name=entity2).first()
    #     node_Sally = matcher.match(label2).where(city=entity2).first()
        relation_shawn_sally = Relationship(node_Shawn, relation, node_Sally)
        relation_shawn_sally[attribute] = val
        graph.create(relation_shawn_sally)
    create_new_relation("Person", "Person", "Shawn", "John", "FRIENDS", "since", "2012")
    create_new_relation("Person", "Person", "Mike", "Shawn", "FRIENDS", "since", "2006")
    create_new_relation("Person", "Person",  "Sally", "Steve", "FRIENDS", "since", "2006")
    create_new_relation("Person", "Person",  "Liz", "John", "MARRIED", "since", "1998")

    #
    def create_new_relation_dif(label1, label2, entity1, entity2, relation, attribute, val):
        node_Shawn = matcher.match(label1).where(name=entity1).first()
        node_Sally = matcher.match(label2).where(city=entity2).first()
        relation_shawn_sally = Relationship(node_Shawn, relation, node_Sally)
        relation_shawn_sally[attribute] = val
        graph.create(relation_shawn_sally)
    create_new_relation_dif("Person", "Location", "John", "Boston", "BORN_IN", "year", "1978")

    #
    create_new_relation_dif("Person", "Location", "Liz", "Boston", "BORN_IN", "year", "1981")
    create_new_relation_dif("Person", "Location", "Mike", "San Francisco", "BORN_IN", "year", "1960")
    create_new_relation_dif("Person", "Location", "Shawn", "Miami", "BORN_IN", "year", "1960")
    create_new_relation_dif("Person", "Location", "Steve", "Lynn", "BORN_IN", "year", "1970")

    #
    query = "MATCH(a:Person)-[:BORN_IN]->(b:Location{city:'Boston'}) RETURN a;"
    iters = graph.run(query)
    for iter in iters:
        print(iter["a"]['name'])

    #
    query = "MATCH (n)-[:MARRIED]-() RETURN n;"
    iters = graph.run(query)
    for iter in iters:
        print(iter)

    #
    query = "CREATE(a:Person{name:'Todd'})-[r:FRIENDS]->(b:Person {name:'Carlos'});"
    graph.run(query)

    #
    query = "MATCH(a:Person{name:'Mike'})-[r1:FRIENDS]-()-[r2:FRIENDS]-(friend_of_a_friend) RETURN friend_of_a_friend.name AS fofName;"
    iters = graph.run(query)
    for iter in iters:
        print(iter)

    #
    query = "MATCH (a:Person {name:'Liz'}) SET a.age=34;"
    graph.run(query)

    query = "MATCH (a:Person {name:'Shawn'}) SET a.age=32;"
    graph.run(query)

    query = "MATCH (a:Person {name:'John'}) SET a.age=44;"
    graph.run(query)

    query = "MATCH (a:Person {name:'Mike'}) SET a.age=25;"
    graph.run(query)

    #
    query = "MATCH (a:Person {name:'Mike'}) SET a.test='test';"
    graph.run(query)
    query = "MATCH (a:Person {name:'Mike'}) REMOVE a.test;"
    graph.run(query)

    #
    query = "MATCH (a:Location {city:'Portland'}) DELETE a;"
    graph.run(query)

    #
    query = "MATCH (a:Person {name:'Todd'})-[rel]-(b:Person) DELETE a,b,rel;"
    graph.run(query)

    #
    query = "MATCH (n) DETACH DELETE n;"
    graph.run(query)

    '''
    return "graph base"

def graph(self, text):
    '''
    from py2neo import Graph, Node, Relationship
    import pandas as pd
    import re
    import os

    path = "data/disease.csv"
    all_data = pd.read_csv(path, encoding='gb18030')

    all_data.head()

    class MedicalGraph:
        def __init__(self):
            self.data_path = "data/disease.csv"
            self.graph = Graph("http://ip:port", auth=("username", "password"))

        def read_file(self):
            # cols = ["name", "alias", "part", "age", "infection", "insurance", "department", "checklist", "symptom",
            #         "complication", "treatment", "drug", "period", "rate", "money"]
            #
            diseases = []  #
            aliases = []  #
            symptoms = []  #
            parts = []  #
            departments = []  #
            complications = []  #
            drugs = []  #

            # ：age, infection, insurance, checklist, treatment, period, rate, money
            diseases_infos = []
            #
            disease_to_symptom = []  #
            disease_to_alias = []  #
            diseases_to_part = []  #
            disease_to_department = []  #
            disease_to_complication = []  #
            disease_to_drug = []  #

            all_data = pd.read_csv(self.data_path, encoding='gb18030').loc[:, :].values
            for data in all_data:
                disease_dict = {}  #
                #
                disease = str(data[0]).replace("...", " ").strip()
                disease_dict["name"] = disease
                #
                line = re.sub("[，、；,.;]", " ", str(data[1])) if str(data[1]) else "WeiZhi"
                for alias in line.strip().split():
                    aliases.append(alias)
                    disease_to_alias.append([disease, alias])
                #
                part_list = str(data[2]).strip().split() if str(data[2]) else "WeiZhi"
                for part in part_list:
                    parts.append(part)
                    diseases_to_part.append([disease, part])
                #
                age = str(data[3]).strip()
                disease_dict["age"] = age
                #
                infect = str(data[4]).strip()
                disease_dict["infection"] = infect
                #
                insurance = str(data[5]).strip()
                disease_dict["insurance"] = insurance
                #
                department_list = str(data[6]).strip().split()
                for department in department_list:
                    departments.append(department)
                    disease_to_department.append([disease, department])
                #
                check = str(data[7]).strip()
                disease_dict["checklist"] = check
                #
                symptom_list = str(data[8]).replace("...", " ").strip().split()[:-1]
                for symptom in symptom_list:
                    symptoms.append(symptom)
                    disease_to_symptom.append([disease, symptom])
                #
                complication_list = str(data[9]).strip().split()[:-1] if str(data[9]) else "WeiZhi"
                for complication in complication_list:
                    complications.append(complication)
                    disease_to_complication.append([disease, complication])
                #
                treat = str(data[10]).strip()[:-4]
                disease_dict["treatment"] = treat
                #
                drug_string = str(data[11]).replace("...", " ").strip()
                for drug in drug_string.split()[:-1]:
                    drugs.append(drug)
                    disease_to_drug.append([disease, drug])
                #
                period = str(data[12]).strip()
                disease_dict["period"] = period
                #
                rate = str(data[13]).strip()
                disease_dict["rate"] = rate
                #
                money = str(data[14]).strip() if str(data[14]) else "WeiZhi"
                disease_dict["money"] = money

                diseases_infos.append(disease_dict)

            return set(diseases), set(symptoms), set(aliases), set(parts), set(departments), set(complications), \
                    set(drugs), disease_to_alias, disease_to_symptom, diseases_to_part, disease_to_department, \
                    disease_to_complication, disease_to_drug, diseases_infos

        def create_node(self, label, nodes):
            count = 0
            for node_name in nodes:
                node = Node(label, name=node_name)
                self.graph.create(node)
                count += 1
                print(count, len(nodes))
            return

        def create_diseases_nodes(self, disease_info):
            count = 0
            for disease_dict in disease_info:
                node = Node("Disease", name=disease_dict['name'], age=disease_dict['age'],
                            infection=disease_dict['infection'], insurance=disease_dict['insurance'],
                            treatment=disease_dict['treatment'], checklist=disease_dict['checklist'],
                            period=disease_dict['period'], rate=disease_dict['rate'],
                            money=disease_dict['money'])
                self.graph.create(node)
                count += 1
                print(count)
            return

        def create_graphNodes(self):
            disease, symptom, alias, part, department, complication, drug, rel_alias, rel_symptom, rel_part, \
            rel_department, rel_complication, rel_drug, rel_infos = self.read_file()
            self.create_diseases_nodes(rel_infos)
            self.create_node("Symptom", symptom)
            self.create_node("Alias", alias)
            self.create_node("Part", part)
            self.create_node("Department", department)
            self.create_node("Complication", complication)
            self.create_node("Drug", drug)

            return

        def create_graphRels(self):
            disease, symptom, alias, part, department, complication, drug, rel_alias, rel_symptom, rel_part, \
            rel_department, rel_complication, rel_drug, rel_infos = self.read_file()

            self.create_relationship("Disease", "Alias", rel_alias, "ALIAS_IS", "BieMing")
            self.create_relationship("Disease", "Symptom", rel_symptom, "HAS_SYMPTOM", "zhengzhuang")
            self.create_relationship("Disease", "Part", rel_part, "PART_IS", "fabingbuwei")
            self.create_relationship("Disease", "Department", rel_department, "DEPARTMENT_IS", "suoshukeshi")
            self.create_relationship("Disease", "Complication", rel_complication, "HAS_COMPLICATION", "bingfazheng")
            self.create_relationship("Disease", "Drug", rel_drug, "HAS_DRUG", "yaopin")

        def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
            count = 0

            set_edges = []
            for edge in edges:
                set_edges.append('###'.join(edge))
            all = len(set(set_edges))
            for edge in set(set_edges):
                edge = edge.split('###')
                p = edge[0]
                q = edge[1]
                query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                    start_node, end_node, p, q, rel_type, rel_name)
                try:
                    self.graph.run(query)
                    count += 1
                    print(rel_type, count, all)
                except Exception as e:
                    print(e)
            return

    handler = MedicalGraph()
    handler.create_graphNodes()
    handler.create_graphRels()

    '''
    return "graph demo"

def dash(self, text):
    '''

    from dash import Dash, html, dcc, Input, Output
    import plotly.express as px
    import pandas as pd

    df = px.data.gapminder()

    app = Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id = 'graph_with_silder'),
        dcc.Slider(
            df.year.min(),
            df.year.max(),
            value = df.year.max(),
            step = None,
            marks = {str(year):str(year)+"年" for year in df['year'].unique()},
            id = 'slider'
        )
    ])

    @app.callback(
        Output('graph_with_silder','figure'),
        Input('slider','value')
    )

    def update_figure(selected_year):
        df_= df[df.year==int(selected_year)]
        # Draw a Scatter Plot Based on Filtered Data
        fig = px.scatter(df_, x='gdpPercap', y='lifeExp', size='pop', size_max=60, color='country', hover_name='country') 
        # Definition of Conversion Speed
        fig.update_layout(transition_duration=200) 
        return fig

    app.run_server(port=11888)
    '''
    return "dash demo"
