# Generated from Cypher.g4 by ANTLR 4.5.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CypherParser import CypherParser
else:
    from CypherParser import CypherParser

# This class defines a complete listener for a parse tree produced by CypherParser.
class CypherListener(ParseTreeListener):

    # Enter a parse tree produced by CypherParser#cypher.
    def enterCypher(self, ctx:CypherParser.CypherContext):
        pass

    # Exit a parse tree produced by CypherParser#cypher.
    def exitCypher(self, ctx:CypherParser.CypherContext):
        pass


    # Enter a parse tree produced by CypherParser#statement.
    def enterStatement(self, ctx:CypherParser.StatementContext):
        pass

    # Exit a parse tree produced by CypherParser#statement.
    def exitStatement(self, ctx:CypherParser.StatementContext):
        pass


    # Enter a parse tree produced by CypherParser#query.
    def enterQuery(self, ctx:CypherParser.QueryContext):
        pass

    # Exit a parse tree produced by CypherParser#query.
    def exitQuery(self, ctx:CypherParser.QueryContext):
        pass


    # Enter a parse tree produced by CypherParser#regularQuery.
    def enterRegularQuery(self, ctx:CypherParser.RegularQueryContext):
        pass

    # Exit a parse tree produced by CypherParser#regularQuery.
    def exitRegularQuery(self, ctx:CypherParser.RegularQueryContext):
        pass


    # Enter a parse tree produced by CypherParser#singleQuery.
    def enterSingleQuery(self, ctx:CypherParser.SingleQueryContext):
        pass

    # Exit a parse tree produced by CypherParser#singleQuery.
    def exitSingleQuery(self, ctx:CypherParser.SingleQueryContext):
        pass


    # Enter a parse tree produced by CypherParser#union.
    def enterUnion(self, ctx:CypherParser.UnionContext):
        pass

    # Exit a parse tree produced by CypherParser#union.
    def exitUnion(self, ctx:CypherParser.UnionContext):
        pass


    # Enter a parse tree produced by CypherParser#clause.
    def enterClause(self, ctx:CypherParser.ClauseContext):
        pass

    # Exit a parse tree produced by CypherParser#clause.
    def exitClause(self, ctx:CypherParser.ClauseContext):
        pass


    # Enter a parse tree produced by CypherParser#match_.
    def enterMatch_(self, ctx:CypherParser.Match_Context):
        pass

    # Exit a parse tree produced by CypherParser#match_.
    def exitMatch_(self, ctx:CypherParser.Match_Context):
        pass


    # Enter a parse tree produced by CypherParser#unwind.
    def enterUnwind(self, ctx:CypherParser.UnwindContext):
        pass

    # Exit a parse tree produced by CypherParser#unwind.
    def exitUnwind(self, ctx:CypherParser.UnwindContext):
        pass


    # Enter a parse tree produced by CypherParser#merge.
    def enterMerge(self, ctx:CypherParser.MergeContext):
        pass

    # Exit a parse tree produced by CypherParser#merge.
    def exitMerge(self, ctx:CypherParser.MergeContext):
        pass


    # Enter a parse tree produced by CypherParser#mergeAction.
    def enterMergeAction(self, ctx:CypherParser.MergeActionContext):
        pass

    # Exit a parse tree produced by CypherParser#mergeAction.
    def exitMergeAction(self, ctx:CypherParser.MergeActionContext):
        pass


    # Enter a parse tree produced by CypherParser#create.
    def enterCreate(self, ctx:CypherParser.CreateContext):
        pass

    # Exit a parse tree produced by CypherParser#create.
    def exitCreate(self, ctx:CypherParser.CreateContext):
        pass


    # Enter a parse tree produced by CypherParser#set_.
    def enterSet_(self, ctx:CypherParser.Set_Context):
        pass

    # Exit a parse tree produced by CypherParser#set_.
    def exitSet_(self, ctx:CypherParser.Set_Context):
        pass


    # Enter a parse tree produced by CypherParser#setItem.
    def enterSetItem(self, ctx:CypherParser.SetItemContext):
        pass

    # Exit a parse tree produced by CypherParser#setItem.
    def exitSetItem(self, ctx:CypherParser.SetItemContext):
        pass


    # Enter a parse tree produced by CypherParser#delete.
    def enterDelete(self, ctx:CypherParser.DeleteContext):
        pass

    # Exit a parse tree produced by CypherParser#delete.
    def exitDelete(self, ctx:CypherParser.DeleteContext):
        pass


    # Enter a parse tree produced by CypherParser#remove.
    def enterRemove(self, ctx:CypherParser.RemoveContext):
        pass

    # Exit a parse tree produced by CypherParser#remove.
    def exitRemove(self, ctx:CypherParser.RemoveContext):
        pass


    # Enter a parse tree produced by CypherParser#removeItem.
    def enterRemoveItem(self, ctx:CypherParser.RemoveItemContext):
        pass

    # Exit a parse tree produced by CypherParser#removeItem.
    def exitRemoveItem(self, ctx:CypherParser.RemoveItemContext):
        pass


    # Enter a parse tree produced by CypherParser#with_.
    def enterWith_(self, ctx:CypherParser.With_Context):
        pass

    # Exit a parse tree produced by CypherParser#with_.
    def exitWith_(self, ctx:CypherParser.With_Context):
        pass


    # Enter a parse tree produced by CypherParser#return_.
    def enterReturn_(self, ctx:CypherParser.Return_Context):
        pass

    # Exit a parse tree produced by CypherParser#return_.
    def exitReturn_(self, ctx:CypherParser.Return_Context):
        pass


    # Enter a parse tree produced by CypherParser#returnBody.
    def enterReturnBody(self, ctx:CypherParser.ReturnBodyContext):
        pass

    # Exit a parse tree produced by CypherParser#returnBody.
    def exitReturnBody(self, ctx:CypherParser.ReturnBodyContext):
        pass


    # Enter a parse tree produced by CypherParser#returnItems.
    def enterReturnItems(self, ctx:CypherParser.ReturnItemsContext):
        pass

    # Exit a parse tree produced by CypherParser#returnItems.
    def exitReturnItems(self, ctx:CypherParser.ReturnItemsContext):
        pass


    # Enter a parse tree produced by CypherParser#returnItem.
    def enterReturnItem(self, ctx:CypherParser.ReturnItemContext):
        pass

    # Exit a parse tree produced by CypherParser#returnItem.
    def exitReturnItem(self, ctx:CypherParser.ReturnItemContext):
        pass


    # Enter a parse tree produced by CypherParser#order.
    def enterOrder(self, ctx:CypherParser.OrderContext):
        pass

    # Exit a parse tree produced by CypherParser#order.
    def exitOrder(self, ctx:CypherParser.OrderContext):
        pass


    # Enter a parse tree produced by CypherParser#skip.
    def enterSkip(self, ctx:CypherParser.SkipContext):
        pass

    # Exit a parse tree produced by CypherParser#skip.
    def exitSkip(self, ctx:CypherParser.SkipContext):
        pass


    # Enter a parse tree produced by CypherParser#limit.
    def enterLimit(self, ctx:CypherParser.LimitContext):
        pass

    # Exit a parse tree produced by CypherParser#limit.
    def exitLimit(self, ctx:CypherParser.LimitContext):
        pass


    # Enter a parse tree produced by CypherParser#sortItem.
    def enterSortItem(self, ctx:CypherParser.SortItemContext):
        pass

    # Exit a parse tree produced by CypherParser#sortItem.
    def exitSortItem(self, ctx:CypherParser.SortItemContext):
        pass


    # Enter a parse tree produced by CypherParser#where.
    def enterWhere(self, ctx:CypherParser.WhereContext):
        pass

    # Exit a parse tree produced by CypherParser#where.
    def exitWhere(self, ctx:CypherParser.WhereContext):
        pass


    # Enter a parse tree produced by CypherParser#pattern.
    def enterPattern(self, ctx:CypherParser.PatternContext):
        pass

    # Exit a parse tree produced by CypherParser#pattern.
    def exitPattern(self, ctx:CypherParser.PatternContext):
        pass


    # Enter a parse tree produced by CypherParser#patternPart.
    def enterPatternPart(self, ctx:CypherParser.PatternPartContext):
        pass

    # Exit a parse tree produced by CypherParser#patternPart.
    def exitPatternPart(self, ctx:CypherParser.PatternPartContext):
        pass


    # Enter a parse tree produced by CypherParser#anonymousPatternPart.
    def enterAnonymousPatternPart(self, ctx:CypherParser.AnonymousPatternPartContext):
        pass

    # Exit a parse tree produced by CypherParser#anonymousPatternPart.
    def exitAnonymousPatternPart(self, ctx:CypherParser.AnonymousPatternPartContext):
        pass


    # Enter a parse tree produced by CypherParser#patternElement.
    def enterPatternElement(self, ctx:CypherParser.PatternElementContext):
        pass

    # Exit a parse tree produced by CypherParser#patternElement.
    def exitPatternElement(self, ctx:CypherParser.PatternElementContext):
        pass


    # Enter a parse tree produced by CypherParser#nodePattern.
    def enterNodePattern(self, ctx:CypherParser.NodePatternContext):
        pass

    # Exit a parse tree produced by CypherParser#nodePattern.
    def exitNodePattern(self, ctx:CypherParser.NodePatternContext):
        pass


    # Enter a parse tree produced by CypherParser#patternElementChain.
    def enterPatternElementChain(self, ctx:CypherParser.PatternElementChainContext):
        pass

    # Exit a parse tree produced by CypherParser#patternElementChain.
    def exitPatternElementChain(self, ctx:CypherParser.PatternElementChainContext):
        pass


    # Enter a parse tree produced by CypherParser#relationshipPattern.
    def enterRelationshipPattern(self, ctx:CypherParser.RelationshipPatternContext):
        pass

    # Exit a parse tree produced by CypherParser#relationshipPattern.
    def exitRelationshipPattern(self, ctx:CypherParser.RelationshipPatternContext):
        pass


    # Enter a parse tree produced by CypherParser#relationshipDetail.
    def enterRelationshipDetail(self, ctx:CypherParser.RelationshipDetailContext):
        pass

    # Exit a parse tree produced by CypherParser#relationshipDetail.
    def exitRelationshipDetail(self, ctx:CypherParser.RelationshipDetailContext):
        pass


    # Enter a parse tree produced by CypherParser#properties.
    def enterProperties(self, ctx:CypherParser.PropertiesContext):
        pass

    # Exit a parse tree produced by CypherParser#properties.
    def exitProperties(self, ctx:CypherParser.PropertiesContext):
        pass


    # Enter a parse tree produced by CypherParser#relationshipTypes.
    def enterRelationshipTypes(self, ctx:CypherParser.RelationshipTypesContext):
        pass

    # Exit a parse tree produced by CypherParser#relationshipTypes.
    def exitRelationshipTypes(self, ctx:CypherParser.RelationshipTypesContext):
        pass


    # Enter a parse tree produced by CypherParser#nodeLabels.
    def enterNodeLabels(self, ctx:CypherParser.NodeLabelsContext):
        pass

    # Exit a parse tree produced by CypherParser#nodeLabels.
    def exitNodeLabels(self, ctx:CypherParser.NodeLabelsContext):
        pass


    # Enter a parse tree produced by CypherParser#nodeLabel.
    def enterNodeLabel(self, ctx:CypherParser.NodeLabelContext):
        pass

    # Exit a parse tree produced by CypherParser#nodeLabel.
    def exitNodeLabel(self, ctx:CypherParser.NodeLabelContext):
        pass


    # Enter a parse tree produced by CypherParser#rangeLiteral.
    def enterRangeLiteral(self, ctx:CypherParser.RangeLiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#rangeLiteral.
    def exitRangeLiteral(self, ctx:CypherParser.RangeLiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#labelName.
    def enterLabelName(self, ctx:CypherParser.LabelNameContext):
        pass

    # Exit a parse tree produced by CypherParser#labelName.
    def exitLabelName(self, ctx:CypherParser.LabelNameContext):
        pass


    # Enter a parse tree produced by CypherParser#relTypeName.
    def enterRelTypeName(self, ctx:CypherParser.RelTypeNameContext):
        pass

    # Exit a parse tree produced by CypherParser#relTypeName.
    def exitRelTypeName(self, ctx:CypherParser.RelTypeNameContext):
        pass


    # Enter a parse tree produced by CypherParser#expression.
    def enterExpression(self, ctx:CypherParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CypherParser#expression.
    def exitExpression(self, ctx:CypherParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CypherParser#expression12.
    def enterExpression12(self, ctx:CypherParser.Expression12Context):
        pass

    # Exit a parse tree produced by CypherParser#expression12.
    def exitExpression12(self, ctx:CypherParser.Expression12Context):
        pass


    # Enter a parse tree produced by CypherParser#expression11.
    def enterExpression11(self, ctx:CypherParser.Expression11Context):
        pass

    # Exit a parse tree produced by CypherParser#expression11.
    def exitExpression11(self, ctx:CypherParser.Expression11Context):
        pass


    # Enter a parse tree produced by CypherParser#expression10.
    def enterExpression10(self, ctx:CypherParser.Expression10Context):
        pass

    # Exit a parse tree produced by CypherParser#expression10.
    def exitExpression10(self, ctx:CypherParser.Expression10Context):
        pass


    # Enter a parse tree produced by CypherParser#expression9.
    def enterExpression9(self, ctx:CypherParser.Expression9Context):
        pass

    # Exit a parse tree produced by CypherParser#expression9.
    def exitExpression9(self, ctx:CypherParser.Expression9Context):
        pass


    # Enter a parse tree produced by CypherParser#expression8.
    def enterExpression8(self, ctx:CypherParser.Expression8Context):
        pass

    # Exit a parse tree produced by CypherParser#expression8.
    def exitExpression8(self, ctx:CypherParser.Expression8Context):
        pass


    # Enter a parse tree produced by CypherParser#expression7.
    def enterExpression7(self, ctx:CypherParser.Expression7Context):
        pass

    # Exit a parse tree produced by CypherParser#expression7.
    def exitExpression7(self, ctx:CypherParser.Expression7Context):
        pass


    # Enter a parse tree produced by CypherParser#expression6.
    def enterExpression6(self, ctx:CypherParser.Expression6Context):
        pass

    # Exit a parse tree produced by CypherParser#expression6.
    def exitExpression6(self, ctx:CypherParser.Expression6Context):
        pass


    # Enter a parse tree produced by CypherParser#expression5.
    def enterExpression5(self, ctx:CypherParser.Expression5Context):
        pass

    # Exit a parse tree produced by CypherParser#expression5.
    def exitExpression5(self, ctx:CypherParser.Expression5Context):
        pass


    # Enter a parse tree produced by CypherParser#expression4.
    def enterExpression4(self, ctx:CypherParser.Expression4Context):
        pass

    # Exit a parse tree produced by CypherParser#expression4.
    def exitExpression4(self, ctx:CypherParser.Expression4Context):
        pass


    # Enter a parse tree produced by CypherParser#expression3.
    def enterExpression3(self, ctx:CypherParser.Expression3Context):
        pass

    # Exit a parse tree produced by CypherParser#expression3.
    def exitExpression3(self, ctx:CypherParser.Expression3Context):
        pass


    # Enter a parse tree produced by CypherParser#expression2.
    def enterExpression2(self, ctx:CypherParser.Expression2Context):
        pass

    # Exit a parse tree produced by CypherParser#expression2.
    def exitExpression2(self, ctx:CypherParser.Expression2Context):
        pass


    # Enter a parse tree produced by CypherParser#atom.
    def enterAtom(self, ctx:CypherParser.AtomContext):
        pass

    # Exit a parse tree produced by CypherParser#atom.
    def exitAtom(self, ctx:CypherParser.AtomContext):
        pass


    # Enter a parse tree produced by CypherParser#literal.
    def enterLiteral(self, ctx:CypherParser.LiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#literal.
    def exitLiteral(self, ctx:CypherParser.LiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:CypherParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:CypherParser.BooleanLiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#listLiteral.
    def enterListLiteral(self, ctx:CypherParser.ListLiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#listLiteral.
    def exitListLiteral(self, ctx:CypherParser.ListLiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#partialComparisonExpression.
    def enterPartialComparisonExpression(self, ctx:CypherParser.PartialComparisonExpressionContext):
        pass

    # Exit a parse tree produced by CypherParser#partialComparisonExpression.
    def exitPartialComparisonExpression(self, ctx:CypherParser.PartialComparisonExpressionContext):
        pass


    # Enter a parse tree produced by CypherParser#parenthesizedExpression.
    def enterParenthesizedExpression(self, ctx:CypherParser.ParenthesizedExpressionContext):
        pass

    # Exit a parse tree produced by CypherParser#parenthesizedExpression.
    def exitParenthesizedExpression(self, ctx:CypherParser.ParenthesizedExpressionContext):
        pass


    # Enter a parse tree produced by CypherParser#relationshipsPattern.
    def enterRelationshipsPattern(self, ctx:CypherParser.RelationshipsPatternContext):
        pass

    # Exit a parse tree produced by CypherParser#relationshipsPattern.
    def exitRelationshipsPattern(self, ctx:CypherParser.RelationshipsPatternContext):
        pass


    # Enter a parse tree produced by CypherParser#filterExpression.
    def enterFilterExpression(self, ctx:CypherParser.FilterExpressionContext):
        pass

    # Exit a parse tree produced by CypherParser#filterExpression.
    def exitFilterExpression(self, ctx:CypherParser.FilterExpressionContext):
        pass


    # Enter a parse tree produced by CypherParser#idInColl.
    def enterIdInColl(self, ctx:CypherParser.IdInCollContext):
        pass

    # Exit a parse tree produced by CypherParser#idInColl.
    def exitIdInColl(self, ctx:CypherParser.IdInCollContext):
        pass


    # Enter a parse tree produced by CypherParser#functionInvocation.
    def enterFunctionInvocation(self, ctx:CypherParser.FunctionInvocationContext):
        pass

    # Exit a parse tree produced by CypherParser#functionInvocation.
    def exitFunctionInvocation(self, ctx:CypherParser.FunctionInvocationContext):
        pass


    # Enter a parse tree produced by CypherParser#functionName.
    def enterFunctionName(self, ctx:CypherParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by CypherParser#functionName.
    def exitFunctionName(self, ctx:CypherParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by CypherParser#listComprehension.
    def enterListComprehension(self, ctx:CypherParser.ListComprehensionContext):
        pass

    # Exit a parse tree produced by CypherParser#listComprehension.
    def exitListComprehension(self, ctx:CypherParser.ListComprehensionContext):
        pass


    # Enter a parse tree produced by CypherParser#patternComprehension.
    def enterPatternComprehension(self, ctx:CypherParser.PatternComprehensionContext):
        pass

    # Exit a parse tree produced by CypherParser#patternComprehension.
    def exitPatternComprehension(self, ctx:CypherParser.PatternComprehensionContext):
        pass


    # Enter a parse tree produced by CypherParser#propertyLookup.
    def enterPropertyLookup(self, ctx:CypherParser.PropertyLookupContext):
        pass

    # Exit a parse tree produced by CypherParser#propertyLookup.
    def exitPropertyLookup(self, ctx:CypherParser.PropertyLookupContext):
        pass


    # Enter a parse tree produced by CypherParser#variable.
    def enterVariable(self, ctx:CypherParser.VariableContext):
        pass

    # Exit a parse tree produced by CypherParser#variable.
    def exitVariable(self, ctx:CypherParser.VariableContext):
        pass


    # Enter a parse tree produced by CypherParser#numberLiteral.
    def enterNumberLiteral(self, ctx:CypherParser.NumberLiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#numberLiteral.
    def exitNumberLiteral(self, ctx:CypherParser.NumberLiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#mapLiteral.
    def enterMapLiteral(self, ctx:CypherParser.MapLiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#mapLiteral.
    def exitMapLiteral(self, ctx:CypherParser.MapLiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#parameter.
    def enterParameter(self, ctx:CypherParser.ParameterContext):
        pass

    # Exit a parse tree produced by CypherParser#parameter.
    def exitParameter(self, ctx:CypherParser.ParameterContext):
        pass


    # Enter a parse tree produced by CypherParser#propertyExpression.
    def enterPropertyExpression(self, ctx:CypherParser.PropertyExpressionContext):
        pass

    # Exit a parse tree produced by CypherParser#propertyExpression.
    def exitPropertyExpression(self, ctx:CypherParser.PropertyExpressionContext):
        pass


    # Enter a parse tree produced by CypherParser#propertyKeyName.
    def enterPropertyKeyName(self, ctx:CypherParser.PropertyKeyNameContext):
        pass

    # Exit a parse tree produced by CypherParser#propertyKeyName.
    def exitPropertyKeyName(self, ctx:CypherParser.PropertyKeyNameContext):
        pass


    # Enter a parse tree produced by CypherParser#integerLiteral.
    def enterIntegerLiteral(self, ctx:CypherParser.IntegerLiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#integerLiteral.
    def exitIntegerLiteral(self, ctx:CypherParser.IntegerLiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#doubleLiteral.
    def enterDoubleLiteral(self, ctx:CypherParser.DoubleLiteralContext):
        pass

    # Exit a parse tree produced by CypherParser#doubleLiteral.
    def exitDoubleLiteral(self, ctx:CypherParser.DoubleLiteralContext):
        pass


    # Enter a parse tree produced by CypherParser#symbolicName.
    def enterSymbolicName(self, ctx:CypherParser.SymbolicNameContext):
        pass

    # Exit a parse tree produced by CypherParser#symbolicName.
    def exitSymbolicName(self, ctx:CypherParser.SymbolicNameContext):
        pass


    # Enter a parse tree produced by CypherParser#leftArrowHead.
    def enterLeftArrowHead(self, ctx:CypherParser.LeftArrowHeadContext):
        pass

    # Exit a parse tree produced by CypherParser#leftArrowHead.
    def exitLeftArrowHead(self, ctx:CypherParser.LeftArrowHeadContext):
        pass


    # Enter a parse tree produced by CypherParser#rightArrowHead.
    def enterRightArrowHead(self, ctx:CypherParser.RightArrowHeadContext):
        pass

    # Exit a parse tree produced by CypherParser#rightArrowHead.
    def exitRightArrowHead(self, ctx:CypherParser.RightArrowHeadContext):
        pass


    # Enter a parse tree produced by CypherParser#dash.
    def enterDash(self, ctx:CypherParser.DashContext):
        pass

    # Exit a parse tree produced by CypherParser#dash.
    def exitDash(self, ctx:CypherParser.DashContext):
        pass


