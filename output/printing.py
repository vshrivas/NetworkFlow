import storage.Node as n
import storage.Relationship as r

def getPropValue(propKey, aspect):
    props = aspect.getProperties()
    for prop in props:
        if prop.getKey() == propKey:
            return prop.getValue()

def printResult(result, nodes, rels, returns, lookingFor):
    # Ok here we go. Printing.
    # First things first, we need a mapping of variable -> Node/Rel.
    # To make this, we need to alter the dictionaries of nodes, rels and results.
    # Reverse the keys/values and change the new keys to just the variable name.
    # If there is no variable name, means it's not getting returned or printed,
    # so we don't need it; don't add it to our new dict.
    varsDict = {}
    if result:
        for (aspect, i) in result:
            if isinstance(aspect, n.Node):
                node = nodes[i]
                if node.varname is not None:
                    varsDict[node.varname] = aspect
            if isinstance(aspect, r.Relationship):
                rel = rels[i]
                if rel.varname is not None:
                    varsDict[rel.varname] = aspect

    # Now we print the things we want to print
    # Loop over the specific things we want from the return statement,
    # and print either of three cases:
    #   - we want a property of a aspect, in which case find the property
    #   - a constant expression from the return statement
    #   - a complete aspect (node or relationship)
    for i in range(len(lookingFor)):
        var = lookingFor[i][0]
        if len(lookingFor[i]) > 1:
            prop = lookingFor[i][1]
            toPrint = getPropValue(prop, varsDict[var])
        # check if we have a constant expression:
        elif var not in varsDict.keys():
            toPrint = var
        else: # good old aspect
            asp = varsDict[var]
            objID = asp.getID()
            props = asp.getProperties()
            propStrings = " {"
            for prop in props:
                # Need to convert this property to a readable format
                propStrings += str(prop.key).strip() + ": " + str(prop.value).strip() + ", "
            propStrings += "}"
            if propStrings == " {{}}":
                propStrings = ""

            if isinstance(asp, n.Node):
                label = asp.getLabels()[0].getLabelStr().strip()
                toPrint = "({}:{}{})".format(objID, label, propStrings)
            if isinstance(asp, r.Relationship):
                relType = asp.getRelType()
                toPrint = "-[{}:{}{}]->".format(objID, relType, propStrings)
        print("{:<29}".format(toPrint), end='|')
    print('')

def printAllResults(results, nodes, rels, returns, matched):
    # Don't forget the first line needs to be the column names.
    lookingFor = []
    firstLine = []
    for (colName, value) in returns:
        toAdd = (value if colName == '' else colName)
        firstLine.append(toAdd)
        # We're going to parse the values as we go through here, since
        # we are iterating through returns anyways.
        # This will help us find what we're actually looking for, whether
        # a node, relationship, or property of them.
        # This if just checks we're not accidentally splitting floats.
        temp = value.split('.')
        if value[0] in '1234567890.':
            temp = value
        lookingFor.append(temp)


    # Now we'll go through the rest of the things we want.
    # Print the first line first:
    for i in range(len(lookingFor)):
        print('-'*29, end='|')
    print('')
    for i in range(len(lookingFor)):
        print('{:<29}'.format(firstLine[i]), end='|')
    print('')
    for i in range(len(lookingFor)):
        print('-'*29, end='|')
    print('')

    # If there are results, then there was a match statement and we should
    # print them.
    if matched and results:
        for result in results:
            printResult(result, nodes, rels, returns, lookingFor)
    elif matched:
        pass
    else:
        printResult(None, nodes, rels, returns, lookingFor)

    for i in range(len(lookingFor)):
        print('-'*29, end='|')
    print('')
