# Generated from Cypher.g4 by ANTLR 4.7
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CypherParser import CypherParser
else:
    from CypherParser import CypherParser

# This class defines a complete generic visitor for a parse tree produced by CypherParser.

class CypherVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by CypherParser#cypher.
    def visitCypher(self, ctx:CypherParser.CypherContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#statement.
    def visitStatement(self, ctx:CypherParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#query.
    def visitQuery(self, ctx:CypherParser.QueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#regularQuery.
    def visitRegularQuery(self, ctx:CypherParser.RegularQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#singleQuery.
    def visitSingleQuery(self, ctx:CypherParser.SingleQueryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#union.
    def visitUnion(self, ctx:CypherParser.UnionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#clause.
    def visitClause(self, ctx:CypherParser.ClauseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#match_.
    def visitMatch_(self, ctx:CypherParser.Match_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#unwind.
    def visitUnwind(self, ctx:CypherParser.UnwindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#merge.
    def visitMerge(self, ctx:CypherParser.MergeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#mergeAction.
    def visitMergeAction(self, ctx:CypherParser.MergeActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#create.
    def visitCreate(self, ctx:CypherParser.CreateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#set_.
    def visitSet_(self, ctx:CypherParser.Set_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#setItem.
    def visitSetItem(self, ctx:CypherParser.SetItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#delete.
    def visitDelete(self, ctx:CypherParser.DeleteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#remove.
    def visitRemove(self, ctx:CypherParser.RemoveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#removeItem.
    def visitRemoveItem(self, ctx:CypherParser.RemoveItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#inQueryCall.
    def visitInQueryCall(self, ctx:CypherParser.InQueryCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#standaloneCall.
    def visitStandaloneCall(self, ctx:CypherParser.StandaloneCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#yieldItems.
    def visitYieldItems(self, ctx:CypherParser.YieldItemsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#yieldItem.
    def visitYieldItem(self, ctx:CypherParser.YieldItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#with_.
    def visitWith_(self, ctx:CypherParser.With_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#return_.
    def visitReturn_(self, ctx:CypherParser.Return_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#returnBody.
    def visitReturnBody(self, ctx:CypherParser.ReturnBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#returnItems.
    def visitReturnItems(self, ctx:CypherParser.ReturnItemsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#returnItem.
    def visitReturnItem(self, ctx:CypherParser.ReturnItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#order.
    def visitOrder(self, ctx:CypherParser.OrderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#skip.
    def visitSkip(self, ctx:CypherParser.SkipContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#limit.
    def visitLimit(self, ctx:CypherParser.LimitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#sortItem.
    def visitSortItem(self, ctx:CypherParser.SortItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#where.
    def visitWhere(self, ctx:CypherParser.WhereContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#pattern.
    def visitPattern(self, ctx:CypherParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#patternPart.
    def visitPatternPart(self, ctx:CypherParser.PatternPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#anonymousPatternPart.
    def visitAnonymousPatternPart(self, ctx:CypherParser.AnonymousPatternPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#patternElement.
    def visitPatternElement(self, ctx:CypherParser.PatternElementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#nodePattern.
    def visitNodePattern(self, ctx:CypherParser.NodePatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#patternElementChain.
    def visitPatternElementChain(self, ctx:CypherParser.PatternElementChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#relationshipPattern.
    def visitRelationshipPattern(self, ctx:CypherParser.RelationshipPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#relationshipDetail.
    def visitRelationshipDetail(self, ctx:CypherParser.RelationshipDetailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#properties.
    def visitProperties(self, ctx:CypherParser.PropertiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#relationshipTypes.
    def visitRelationshipTypes(self, ctx:CypherParser.RelationshipTypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#nodeLabels.
    def visitNodeLabels(self, ctx:CypherParser.NodeLabelsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#nodeLabel.
    def visitNodeLabel(self, ctx:CypherParser.NodeLabelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#rangeLiteral.
    def visitRangeLiteral(self, ctx:CypherParser.RangeLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#labelName.
    def visitLabelName(self, ctx:CypherParser.LabelNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#relTypeName.
    def visitRelTypeName(self, ctx:CypherParser.RelTypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#expression.
    def visitExpression(self, ctx:CypherParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#orExpression.
    def visitOrExpression(self, ctx:CypherParser.OrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#xorExpression.
    def visitXorExpression(self, ctx:CypherParser.XorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#andExpression.
    def visitAndExpression(self, ctx:CypherParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#notExpression.
    def visitNotExpression(self, ctx:CypherParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#comparisonExpression.
    def visitComparisonExpression(self, ctx:CypherParser.ComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#addOrSubtractExpression.
    def visitAddOrSubtractExpression(self, ctx:CypherParser.AddOrSubtractExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#multiplyDivideModuloExpression.
    def visitMultiplyDivideModuloExpression(self, ctx:CypherParser.MultiplyDivideModuloExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#powerOfExpression.
    def visitPowerOfExpression(self, ctx:CypherParser.PowerOfExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#unaryAddOrSubtractExpression.
    def visitUnaryAddOrSubtractExpression(self, ctx:CypherParser.UnaryAddOrSubtractExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#stringListNullOperatorExpression.
    def visitStringListNullOperatorExpression(self, ctx:CypherParser.StringListNullOperatorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#propertyOrLabelsExpression.
    def visitPropertyOrLabelsExpression(self, ctx:CypherParser.PropertyOrLabelsExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#atom.
    def visitAtom(self, ctx:CypherParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#literal.
    def visitLiteral(self, ctx:CypherParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:CypherParser.BooleanLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#listLiteral.
    def visitListLiteral(self, ctx:CypherParser.ListLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#partialComparisonExpression.
    def visitPartialComparisonExpression(self, ctx:CypherParser.PartialComparisonExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#parenthesizedExpression.
    def visitParenthesizedExpression(self, ctx:CypherParser.ParenthesizedExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#relationshipsPattern.
    def visitRelationshipsPattern(self, ctx:CypherParser.RelationshipsPatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#filterExpression.
    def visitFilterExpression(self, ctx:CypherParser.FilterExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#idInColl.
    def visitIdInColl(self, ctx:CypherParser.IdInCollContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#functionInvocation.
    def visitFunctionInvocation(self, ctx:CypherParser.FunctionInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#functionName.
    def visitFunctionName(self, ctx:CypherParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#explicitProcedureInvocation.
    def visitExplicitProcedureInvocation(self, ctx:CypherParser.ExplicitProcedureInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#implicitProcedureInvocation.
    def visitImplicitProcedureInvocation(self, ctx:CypherParser.ImplicitProcedureInvocationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#procedureResultField.
    def visitProcedureResultField(self, ctx:CypherParser.ProcedureResultFieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#procedureName.
    def visitProcedureName(self, ctx:CypherParser.ProcedureNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#listComprehension.
    def visitListComprehension(self, ctx:CypherParser.ListComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#patternComprehension.
    def visitPatternComprehension(self, ctx:CypherParser.PatternComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#propertyLookup.
    def visitPropertyLookup(self, ctx:CypherParser.PropertyLookupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#caseExpression.
    def visitCaseExpression(self, ctx:CypherParser.CaseExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#caseAlternatives.
    def visitCaseAlternatives(self, ctx:CypherParser.CaseAlternativesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#variable.
    def visitVariable(self, ctx:CypherParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#numberLiteral.
    def visitNumberLiteral(self, ctx:CypherParser.NumberLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#mapLiteral.
    def visitMapLiteral(self, ctx:CypherParser.MapLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#parameter.
    def visitParameter(self, ctx:CypherParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#propertyExpression.
    def visitPropertyExpression(self, ctx:CypherParser.PropertyExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#propertyKeyName.
    def visitPropertyKeyName(self, ctx:CypherParser.PropertyKeyNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#integerLiteral.
    def visitIntegerLiteral(self, ctx:CypherParser.IntegerLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#doubleLiteral.
    def visitDoubleLiteral(self, ctx:CypherParser.DoubleLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#schemaName.
    def visitSchemaName(self, ctx:CypherParser.SchemaNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#reservedWord.
    def visitReservedWord(self, ctx:CypherParser.ReservedWordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#symbolicName.
    def visitSymbolicName(self, ctx:CypherParser.SymbolicNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#leftArrowHead.
    def visitLeftArrowHead(self, ctx:CypherParser.LeftArrowHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#rightArrowHead.
    def visitRightArrowHead(self, ctx:CypherParser.RightArrowHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CypherParser#dash.
    def visitDash(self, ctx:CypherParser.DashContext):
        return self.visitChildren(ctx)



del CypherParser