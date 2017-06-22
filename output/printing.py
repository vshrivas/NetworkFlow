import storage.Node as n
import storage.Relationship as r

def printResult(result):
    # Results are composed of "aspects", each of which is either a Node or
    # a Relationship. Well, results are actually (aspect, index) 2-tuples,
    # but we don't actually need the index here except for error checking.
    for (aspect, i) in result:
        objID = aspect.getID()
        props = aspect.getProperties()
        propStrings = " {"
        for prop in props:
            # Need to convert this property to a readable format
            propStrings += prop.key.strip() + ": " + prop.value.strip() + ", "
        propStrings += "}"
        if propStrings == " {{}}":
            propStrings = ""

        if isinstance(aspect, n.Node):
            label = aspect.getLabels()[0].getLabelStr().strip()
            print("({}:{}{})".format(objID, label, propStrings))
        if isinstance(aspect, r.Relationship):
            relType = aspect.getRelType()
            print("-[{}:{}{}]->".format(objID, relType, propStrings))
