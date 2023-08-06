from ShExJSG import Schema, ShExC, ShExJ
from ShExJSG.ShExJ import Shape, IRIREF, TripleConstraint, NodeConstraint, ShapeOr, EachOf, ShapeExternal, ShapeDecl, Annotation, ObjectLiteral
from pyshex.utils.schema_loader import SchemaLoader
import graphviz

symbol = dict()
symbol["class"] = "oval"
symbol["datatype"] = "octagon"
symbol["literal"] = "rectangle"
symbol["iri"]="diamond"
symbol["bnode"]='point'
symbol["oneof"]='record'

shex = """
PREFIX : <http://placeholder.semscape.org/source_data/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX acr: <http://publications.europa.eu/resource/authority/access-right/>
PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>

start = @:source

:source {
    rdf:type [dcat:Dataset] ;
    dcat:keyword ["triple-negative breast cancer" "glioblastoma" "tuberculosis"] ;
    dcat:mediaType ["application/csv"];
    dcat:contactPoint @dtdata:contact + ;
    dcat:accessURL xsd:string;
    dct:issued xsd:date;
    dct:modified xsd:date;
    dct:accessRights [acr:PUBLIC acr:RESTRICTED acr:INFORMATIVE acr:CONFIDENTIAL] ;
}

:contact {
    rdf:type [vcard:Individual] ;
    vcard:fn xsd:string ;
    vcard:hasEmail xsd:string ;
}
  """

def shex2dot(shex, graphviz_name, format="png", rankdir="LR"):
    def process_tc(tc, shape_id):
        dotschema.node(startshape.replace(":", ""), startshape, shape=symbol["iri"])
        if isinstance(tc, TripleConstraint):
            if isinstance(tc.valueExpr, IRIREF):
                node = tc.valueExpr
                predicate = tc.predicate
                for key in prefixmap.keys():
                    node = node.replace(key, prefixmap[key])
                    predicate = predicate.replace(key, prefixmap[key] + ":")
                dotschema.node(node, node, shape=symbol["iri"])
                dotschema.edge(shape.id.split("/")[-1], node, label=predicate)
            elif isinstance(tc.valueExpr, NodeConstraint):

                if tc.valueExpr.datatype:
                    datatype = tc.valueExpr.datatype
                    predicate = tc.predicate
                    for key in prefixmap.keys():
                        datatype = datatype.replace(key, prefixmap[key] + ":")
                        predicate = predicate.replace(key, prefixmap[key] + ":")
                    dotschema.node(
                        shape.id.split("/")[-1] + tc.valueExpr.datatype.split("/")[-1] + tc.predicate.split("/")[-1],
                        datatype, shape=symbol["datatype"])
                    dotschema.edge(shape.id.split("/")[-1],
                                   shape.id.split("/")[-1] + tc.valueExpr.datatype.split("/")[-1] +
                                   tc.predicate.split("/")[
                                       -1], label=predicate)
                elif tc.valueExpr.values:
                    oneofs = []
                    predicate = tc.predicate
                    for value in tc.valueExpr.values:
                        if isinstance(value, ObjectLiteral):
                            oneofs.append(value.value)
                        else:
                            for key in prefixmap.keys():
                                try:
                                    value = value.replace(key, prefixmap[key] + ":")
                                except:
                                    value = "a"
                            oneofs.append(value)
                    for key in prefixmap.keys():
                        predicate = predicate.replace(key, prefixmap[key] + ":")
                    dotschema.node(
                        shape.id.split("/")[-1] + "|".join(oneofs).replace(":", "") + tc.predicate.split("/")[-1],
                        "{" + "|".join(oneofs) + "}", shape=symbol["oneof"])
                    dotschema.edge(shape.id.split("/")[-1],
                                   shape.id.split("/")[-1] + "|".join(oneofs).replace(":", "") +
                                   tc.predicate.split("/")[
                                       -1], label=predicate)

                elif tc.valueExpr.nodeKind:
                    dotschema.node(tc.valueExpr.nodeKind, tc.valueExpr.nodeKind.split("/")[-1],
                                   shape=symbol[tc.valueExpr.nodeKind])
                    dotschema.edge(shape.id.split("/")[-1], tc.valueExpr.nodeKind.split("/")[-1],
                                   label=tc.predicate.split("/")[-1])
                elif tc.valueExpr.xone:

                    dotschema.node(tc.valueExpr.xone[0].id, tc.valueExpr.xone[0].id.split("/")[-1],
                                   shape=symbol["oneof"])
                    dotschema.edge(shape.id.split("/")[-1], tc.valueExpr.xone[0].id.split("/")[-1],
                                   label=tc.predicate.split("/")[-1])
                else:
                    pass
                    # print("No valueExpr")
            else:
                pass
                # print("No valueExpr")
    dotschema = graphviz.Digraph(graphviz_name, format="png")
    dotschema.attr(rankdir=rankdir)
    prefixmap = dict()
    for line in shex.splitlines():
        if line.startswith("PREFIX"):
            line = line.replace("PREFIX", "")
            prefix, uri = line.split(": ")
            prefix = prefix.strip()
            uri = uri.strip()
            prefixmap[uri.replace("<", "").replace(">", "")] = prefix
            dotschema.node(prefix, uri, shape="none", style="invis")

    loader = SchemaLoader()
    schema = loader.loads(shex)

    for shape in schema.shapes:
        if id in (dir(shape)):
            continue
        startshape = shape.id
        for key in prefixmap.keys():
            startshape = startshape.replace(key, prefixmap[key]+":")
        if "expressions" in dir(shape.expression):
            for tc in shape.expression.expressions:
                process_tc(tc, startshape)
        else:
            tc = shape.expression
            process_tc(tc, startshape)

    return dotschema

def view_graphviz(dotschema):
    return dotschema.view()

def save_graphviz(dotschema, filename):
    return dotschema.render(filename)


view_graphviz(shex2dot(shex, "bloembloem"))

