/*
 * Copyright (c) 2015-2017 "Neo Technology,"
 * Network Engine for Objects in Lund AB [http://neotechnology.com]
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
grammar Cypher;

cypher : SP? statement ( SP? ';' )? SP? ;

statement : query ;

query : regularQuery
      | standaloneCall
      ;

regularQuery : singleQuery ( SP? union )* ;

singleQuery : clause ( SP? clause )* ;

union : ( UNION SP ALL SP? singleQuery )
      | ( UNION SP? singleQuery )
      ;

UNION : ( 'U' | 'u' ) ( 'N' | 'n' ) ( 'I' | 'i' ) ( 'O' | 'o' ) ( 'N' | 'n' )  ;

ALL : ( 'A' | 'a' ) ( 'L' | 'l' ) ( 'L' | 'l' )  ;

clause : match_
       | unwind
       | merge
       | create
       | set_
       | delete
       | remove
       | inQueryCall
       | with_
       | return_
       ;

match_ : ( OPTIONAL SP )? MATCH SP? pattern ( SP? where )? ;

OPTIONAL : ( 'O' | 'o' ) ( 'P' | 'p' ) ( 'T' | 't' ) ( 'I' | 'i' ) ( 'O' | 'o' ) ( 'N' | 'n' ) ( 'A' | 'a' ) ( 'L' | 'l' )  ;

MATCH : ( 'M' | 'm' ) ( 'A' | 'a' ) ( 'T' | 't' ) ( 'C' | 'c' ) ( 'H' | 'h' )  ;

unwind : UNWIND SP? expression SP AS SP variable ;

UNWIND : ( 'U' | 'u' ) ( 'N' | 'n' ) ( 'W' | 'w' ) ( 'I' | 'i' ) ( 'N' | 'n' ) ( 'D' | 'd' )  ;

AS : ( 'A' | 'a' ) ( 'S' | 's' )  ;

merge : MERGE SP? patternPart ( SP mergeAction )* ;

MERGE : ( 'M' | 'm' ) ( 'E' | 'e' ) ( 'R' | 'r' ) ( 'G' | 'g' ) ( 'E' | 'e' )  ;

mergeAction : ( ON SP MATCH SP set_ )
            | ( ON SP CREATE SP set_ )
            ;

ON : ( 'O' | 'o' ) ( 'N' | 'n' )  ;

CREATE : ( 'C' | 'c' ) ( 'R' | 'r' ) ( 'E' | 'e' ) ( 'A' | 'a' ) ( 'T' | 't' ) ( 'E' | 'e' )  ;

create : CREATE SP? pattern ;

set_ : SET SP? setItem ( ',' setItem )* ;

SET : ( 'S' | 's' ) ( 'E' | 'e' ) ( 'T' | 't' )  ;

setItem : ( propertyExpression SP? '=' SP? expression )
        | ( variable SP? '=' SP? expression )
        | ( variable SP? '+=' SP? expression )
        | ( variable SP? nodeLabels )
        ;

delete : ( DETACH SP )? DELETE SP? expression ( SP? ',' SP? expression )* ;

DETACH : ( 'D' | 'd' ) ( 'E' | 'e' ) ( 'T' | 't' ) ( 'A' | 'a' ) ( 'C' | 'c' ) ( 'H' | 'h' )  ;

DELETE : ( 'D' | 'd' ) ( 'E' | 'e' ) ( 'L' | 'l' ) ( 'E' | 'e' ) ( 'T' | 't' ) ( 'E' | 'e' )  ;

remove : REMOVE SP removeItem ( SP? ',' SP? removeItem )* ;

REMOVE : ( 'R' | 'r' ) ( 'E' | 'e' ) ( 'M' | 'm' ) ( 'O' | 'o' ) ( 'V' | 'v' ) ( 'E' | 'e' )  ;

removeItem : ( variable nodeLabels )
           | propertyExpression
           ;

inQueryCall : CALL SP explicitProcedureInvocation ( SP? YIELD SP yieldItems )? ;

CALL : ( 'C' | 'c' ) ( 'A' | 'a' ) ( 'L' | 'l' ) ( 'L' | 'l' )  ;

YIELD : ( 'Y' | 'y' ) ( 'I' | 'i' ) ( 'E' | 'e' ) ( 'L' | 'l' ) ( 'D' | 'd' )  ;

standaloneCall : CALL SP ( explicitProcedureInvocation | implicitProcedureInvocation ) ( SP YIELD SP yieldItems )? ;

yieldItems : ( yieldItem ( SP? ',' SP? yieldItem )* )
           | '-'
           ;

yieldItem : ( procedureResultField SP AS SP )? variable ;

with_ : WITH ( SP? DISTINCT )? SP returnBody ( SP? where )? ;

WITH : ( 'W' | 'w' ) ( 'I' | 'i' ) ( 'T' | 't' ) ( 'H' | 'h' )  ;

DISTINCT : ( 'D' | 'd' ) ( 'I' | 'i' ) ( 'S' | 's' ) ( 'T' | 't' ) ( 'I' | 'i' ) ( 'N' | 'n' ) ( 'C' | 'c' ) ( 'T' | 't' )  ;

return_ : RETURN ( SP? DISTINCT )? SP returnBody ;

RETURN : ( 'R' | 'r' ) ( 'E' | 'e' ) ( 'T' | 't' ) ( 'U' | 'u' ) ( 'R' | 'r' ) ( 'N' | 'n' )  ;

returnBody : returnItems ( SP order )? ( SP skip )? ( SP limit )? ;

returnItems : ( '*' ( SP? ',' SP? returnItem )* )
            | ( returnItem ( SP? ',' SP? returnItem )* )
            ;

returnItem : ( expression SP AS SP variable )
           | expression
           ;

order : ORDER SP BY SP sortItem ( ',' SP? sortItem )* ;

ORDER : ( 'O' | 'o' ) ( 'R' | 'r' ) ( 'D' | 'd' ) ( 'E' | 'e' ) ( 'R' | 'r' )  ;

BY : ( 'B' | 'b' ) ( 'Y' | 'y' )  ;

skip : L_SKIP SP expression ;

L_SKIP : ( 'S' | 's' ) ( 'K' | 'k' ) ( 'I' | 'i' ) ( 'P' | 'p' )  ;

limit : LIMIT SP expression ;

LIMIT : ( 'L' | 'l' ) ( 'I' | 'i' ) ( 'M' | 'm' ) ( 'I' | 'i' ) ( 'T' | 't' )  ;

sortItem : expression ( SP? ( ASCENDING | ASC | DESCENDING | DESC ) )? ;

ASCENDING : ( 'A' | 'a' ) ( 'S' | 's' ) ( 'C' | 'c' ) ( 'E' | 'e' ) ( 'N' | 'n' ) ( 'D' | 'd' ) ( 'I' | 'i' ) ( 'N' | 'n' ) ( 'G' | 'g' )  ;

ASC : ( 'A' | 'a' ) ( 'S' | 's' ) ( 'C' | 'c' )  ;

DESCENDING : ( 'D' | 'd' ) ( 'E' | 'e' ) ( 'S' | 's' ) ( 'C' | 'c' ) ( 'E' | 'e' ) ( 'N' | 'n' ) ( 'D' | 'd' ) ( 'I' | 'i' ) ( 'N' | 'n' ) ( 'G' | 'g' )  ;

DESC : ( 'D' | 'd' ) ( 'E' | 'e' ) ( 'S' | 's' ) ( 'C' | 'c' )  ;

where : WHERE SP expression ;

WHERE : ( 'W' | 'w' ) ( 'H' | 'h' ) ( 'E' | 'e' ) ( 'R' | 'r' ) ( 'E' | 'e' )  ;

pattern : patternPart ( SP? ',' SP? patternPart )* ;

patternPart : ( variable SP? '=' SP? anonymousPatternPart )
            | anonymousPatternPart
            ;

anonymousPatternPart : patternElement ;

patternElement : ( nodePattern ( SP? patternElementChain )* )
               | ( '(' patternElement ')' )
               ;

nodePattern : '(' SP? ( variable SP? )? ( nodeLabels SP? )? ( properties SP? )? ')' ;

patternElementChain : relationshipPattern SP? nodePattern ;

relationshipPattern : ( leftArrowHead SP? dash SP? relationshipDetail? SP? dash SP? rightArrowHead )
                    | ( leftArrowHead SP? dash SP? relationshipDetail? SP? dash )
                    | ( dash SP? relationshipDetail? SP? dash SP? rightArrowHead )
                    | ( dash SP? relationshipDetail? SP? dash )
                    ;

relationshipDetail : '[' SP? ( variable SP? )? ( relationshipTypes SP? )? rangeLiteral? ( properties SP? )? ']' ;

properties : mapLiteral
           | parameter
           ;

relationshipTypes : ':' SP? relTypeName ( SP? '|' ':'? SP? relTypeName )* ;

nodeLabels : nodeLabel ( SP? nodeLabel )* ;

nodeLabel : ':' SP? labelName ;

rangeLiteral : '*' SP? ( integerLiteral SP? )? ( '..' SP? ( integerLiteral SP? )? )? ;

labelName : schemaName ;

relTypeName : schemaName ;

expression : orExpression ;

orExpression : xorExpression ( SP OR SP xorExpression )* ;

OR : ( 'O' | 'o' ) ( 'R' | 'r' )  ;

xorExpression : andExpression ( SP XOR SP andExpression )* ;

XOR : ( 'X' | 'x' ) ( 'O' | 'o' ) ( 'R' | 'r' )  ;

andExpression : notExpression ( SP AND SP notExpression )* ;

AND : ( 'A' | 'a' ) ( 'N' | 'n' ) ( 'D' | 'd' )  ;

notExpression : ( NOT SP? )* comparisonExpression ;

NOT : ( 'N' | 'n' ) ( 'O' | 'o' ) ( 'T' | 't' )  ;

comparisonExpression : addOrSubtractExpression ( SP? partialComparisonExpression )* ;

addOrSubtractExpression : multiplyDivideModuloExpression ( ( SP? '+' SP? multiplyDivideModuloExpression ) | ( SP? '-' SP? multiplyDivideModuloExpression ) )* ;

multiplyDivideModuloExpression : powerOfExpression ( ( SP? '*' SP? powerOfExpression ) | ( SP? '/' SP? powerOfExpression ) | ( SP? '%' SP? powerOfExpression ) )* ;

powerOfExpression : unaryAddOrSubtractExpression ( SP? '^' SP? unaryAddOrSubtractExpression )* ;

unaryAddOrSubtractExpression : ( ( '+' | '-' ) SP? )* stringListNullOperatorExpression ;

stringListNullOperatorExpression : propertyOrLabelsExpression ( ( SP? '[' expression ']' ) | ( SP? '[' expression? '..' expression? ']' ) | ( ( ( SP? '=~' ) | ( SP IN ) | ( SP STARTS SP WITH ) | ( SP ENDS SP WITH ) | ( SP CONTAINS ) ) SP? propertyOrLabelsExpression ) | ( SP IS SP NULL ) | ( SP IS SP NOT SP NULL ) )* ;

IN : ( 'I' | 'i' ) ( 'N' | 'n' )  ;

STARTS : ( 'S' | 's' ) ( 'T' | 't' ) ( 'A' | 'a' ) ( 'R' | 'r' ) ( 'T' | 't' ) ( 'S' | 's' )  ;

ENDS : ( 'E' | 'e' ) ( 'N' | 'n' ) ( 'D' | 'd' ) ( 'S' | 's' )  ;

CONTAINS : ( 'C' | 'c' ) ( 'O' | 'o' ) ( 'N' | 'n' ) ( 'T' | 't' ) ( 'A' | 'a' ) ( 'I' | 'i' ) ( 'N' | 'n' ) ( 'S' | 's' )  ;

IS : ( 'I' | 'i' ) ( 'S' | 's' )  ;

NULL : ( 'N' | 'n' ) ( 'U' | 'u' ) ( 'L' | 'l' ) ( 'L' | 'l' )  ;

propertyOrLabelsExpression : atom ( SP? ( propertyLookup | nodeLabels ) )* ;

atom : literal
     | parameter
     | caseExpression
     | ( COUNT SP? '(' SP? '*' SP? ')' )
     | listComprehension
     | patternComprehension
     | ( FILTER SP? '(' SP? filterExpression SP? ')' )
     | ( EXTRACT SP? '(' SP? filterExpression SP? ( SP? '|' expression )? ')' )
     | ( ALL SP? '(' SP? filterExpression SP? ')' )
     | ( ANY SP? '(' SP? filterExpression SP? ')' )
     | ( NONE SP? '(' SP? filterExpression SP? ')' )
     | ( SINGLE SP? '(' SP? filterExpression SP? ')' )
     | relationshipsPattern
     | parenthesizedExpression
     | functionInvocation
     | variable
     ;

COUNT : ( 'C' | 'c' ) ( 'O' | 'o' ) ( 'U' | 'u' ) ( 'N' | 'n' ) ( 'T' | 't' )  ;

FILTER : ( 'F' | 'f' ) ( 'I' | 'i' ) ( 'L' | 'l' ) ( 'T' | 't' ) ( 'E' | 'e' ) ( 'R' | 'r' )  ;

EXTRACT : ( 'E' | 'e' ) ( 'X' | 'x' ) ( 'T' | 't' ) ( 'R' | 'r' ) ( 'A' | 'a' ) ( 'C' | 'c' ) ( 'T' | 't' )  ;

ANY : ( 'A' | 'a' ) ( 'N' | 'n' ) ( 'Y' | 'y' )  ;

NONE : ( 'N' | 'n' ) ( 'O' | 'o' ) ( 'N' | 'n' ) ( 'E' | 'e' )  ;

SINGLE : ( 'S' | 's' ) ( 'I' | 'i' ) ( 'N' | 'n' ) ( 'G' | 'g' ) ( 'L' | 'l' ) ( 'E' | 'e' )  ;

literal : numberLiteral
        | StringLiteral
        | booleanLiteral
        | NULL
        | mapLiteral
        | listLiteral
        ;

booleanLiteral : TRUE
               | FALSE
               ;

TRUE : ( 'T' | 't' ) ( 'R' | 'r' ) ( 'U' | 'u' ) ( 'E' | 'e' )  ;

FALSE : ( 'F' | 'f' ) ( 'A' | 'a' ) ( 'L' | 'l' ) ( 'S' | 's' ) ( 'E' | 'e' )  ;

listLiteral : '[' SP? ( expression SP? ( ',' SP? expression SP? )* )? ']' ;

partialComparisonExpression : ( '=' SP? addOrSubtractExpression )
                            | ( '<>' SP? addOrSubtractExpression )
                            | ( '<' SP? addOrSubtractExpression )
                            | ( '>' SP? addOrSubtractExpression )
                            | ( '<=' SP? addOrSubtractExpression )
                            | ( '>=' SP? addOrSubtractExpression )
                            ;

parenthesizedExpression : '(' SP? expression SP? ')' ;

relationshipsPattern : nodePattern ( SP? patternElementChain )+ ;

filterExpression : idInColl ( SP? where )? ;

idInColl : variable SP IN SP expression ;

functionInvocation : functionName SP? '(' SP? ( DISTINCT SP? )? ( expression SP? ( ',' SP? expression SP? )* )? ')' ;

functionName : symbolicName
             | EXISTS
             ;

EXISTS : ( 'E' | 'e' ) ( 'X' | 'x' ) ( 'I' | 'i' ) ( 'S' | 's' ) ( 'T' | 't' ) ( 'S' | 's' )  ;

explicitProcedureInvocation : procedureName SP? '(' SP? ( expression SP? ( ',' SP? expression SP? )* )? ')' ;

implicitProcedureInvocation : procedureName ;

procedureResultField : symbolicName ;

procedureName : symbolicName ;

listComprehension : '[' SP? filterExpression ( SP? '|' SP? expression )? SP? ']' ;

patternComprehension : '[' SP? ( variable SP? '=' SP? )? relationshipsPattern SP? ( WHERE SP? expression SP? )? '|' SP? expression SP? ']' ;

propertyLookup : '.' SP? ( propertyKeyName ) ;

caseExpression : ( ( CASE ( SP? caseAlternatives )+ ) | ( CASE SP? expression ( SP? caseAlternatives )+ ) ) ( SP? ELSE SP? expression )? SP? END ;

CASE : ( 'C' | 'c' ) ( 'A' | 'a' ) ( 'S' | 's' ) ( 'E' | 'e' )  ;

ELSE : ( 'E' | 'e' ) ( 'L' | 'l' ) ( 'S' | 's' ) ( 'E' | 'e' )  ;

END : ( 'E' | 'e' ) ( 'N' | 'n' ) ( 'D' | 'd' )  ;

caseAlternatives : WHEN SP? expression SP? THEN SP? expression ;

WHEN : ( 'W' | 'w' ) ( 'H' | 'h' ) ( 'E' | 'e' ) ( 'N' | 'n' )  ;

THEN : ( 'T' | 't' ) ( 'H' | 'h' ) ( 'E' | 'e' ) ( 'N' | 'n' )  ;

variable : symbolicName ;

StringLiteral : ( '"' ( ~["\\] | EscapedChar )* '"' )
              | ( '\'' ( ~['\\] | EscapedChar )* '\'' )
              ;

EscapedChar : '\\' ( '\\' | '\'' | '"' | ( 'B' | 'b' ) | ( 'F' | 'f' ) | ( 'N' | 'n' ) | ( 'R' | 'r' ) | ( 'T' | 't' ) | ( ( 'U' | 'u' ) ( HexDigit HexDigit HexDigit HexDigit ) ) | ( ( 'U' | 'u' ) ( HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit HexDigit ) ) ) ;

numberLiteral : doubleLiteral
              | integerLiteral
              ;

mapLiteral : '{' SP? ( propertyKeyName SP? ':' SP? expression SP? ( ',' SP? propertyKeyName SP? ':' SP? expression SP? )* )? '}' ;

parameter : '$' ( symbolicName | DecimalInteger ) ;

propertyExpression : atom ( SP? propertyLookup )+ ;

propertyKeyName : schemaName ;

integerLiteral : HexInteger
               | OctalInteger
               | DecimalInteger
               ;

HexInteger : '0x' ( HexDigit )+ ;

DecimalInteger : ZeroDigit
               | ( NonZeroDigit ( Digit )* )
               ;

OctalInteger : ZeroDigit ( OctDigit )+ ;

HexLetter : ( 'A' | 'a' )
          | ( 'B' | 'b' )
          | ( 'C' | 'c' )
          | ( 'D' | 'd' )
          | ( 'E' | 'e' )
          | ( 'F' | 'f' )
          ;

HexDigit : Digit
         | HexLetter
         ;

Digit : ZeroDigit
      | NonZeroDigit
      ;

NonZeroDigit : NonZeroOctDigit
             | '8'
             | '9'
             ;

NonZeroOctDigit : '1'
                | '2'
                | '3'
                | '4'
                | '5'
                | '6'
                | '7'
                ;

OctDigit : ZeroDigit
         | NonZeroOctDigit
         ;

ZeroDigit : '0' ;

doubleLiteral : ExponentDecimalReal
              | RegularDecimalReal
              ;

ExponentDecimalReal : ( ( Digit )+ | ( ( Digit )+ '.' ( Digit )+ ) | ( '.' ( Digit )+ ) ) ( ( 'E' | 'e' ) | ( 'E' | 'e' ) ) '-'? ( Digit )+ ;

RegularDecimalReal : ( Digit )* '.' ( Digit )+ ;

schemaName : symbolicName
           | reservedWord
           ;

reservedWord : ALL
             | ASC
             | ASCENDING
             | BY
             | CREATE
             | DELETE
             | DESC
             | DESCENDING
             | DETACH
             | EXISTS
             | LIMIT
             | MATCH
             | MERGE
             | ON
             | OPTIONAL
             | ORDER
             | REMOVE
             | RETURN
             | SET
             | L_SKIP
             | WHERE
             | WITH
             | UNION
             | UNWIND
             | AND
             | AS
             | CONTAINS
             | DISTINCT
             | ENDS
             | IN
             | IS
             | NOT
             | OR
             | STARTS
             | XOR
             | FALSE
             | TRUE
             | NULL
             | CONSTRAINT
             | DO
             | FOR
             | REQUIRE
             | UNIQUE
             | CASE
             | WHEN
             | THEN
             | ELSE
             | END
             ;

CONSTRAINT : ( 'C' | 'c' ) ( 'O' | 'o' ) ( 'N' | 'n' ) ( 'S' | 's' ) ( 'T' | 't' ) ( 'R' | 'r' ) ( 'A' | 'a' ) ( 'I' | 'i' ) ( 'N' | 'n' ) ( 'T' | 't' )  ;

DO : ( 'D' | 'd' ) ( 'O' | 'o' )  ;

FOR : ( 'F' | 'f' ) ( 'O' | 'o' ) ( 'R' | 'r' )  ;

REQUIRE : ( 'R' | 'r' ) ( 'E' | 'e' ) ( 'Q' | 'q' ) ( 'U' | 'u' ) ( 'I' | 'i' ) ( 'R' | 'r' ) ( 'E' | 'e' )  ;

UNIQUE : ( 'U' | 'u' ) ( 'N' | 'n' ) ( 'I' | 'i' ) ( 'Q' | 'q' ) ( 'U' | 'u' ) ( 'E' | 'e' )  ;

symbolicName : UnescapedSymbolicName
             | EscapedSymbolicName
             | HexLetter
             | COUNT
             | FILTER
             | EXTRACT
             | ANY
             | ALL
             | NONE
             | SINGLE
             ;

UnescapedSymbolicName : IdentifierStart ( IdentifierPart )* ;

/**
 * Based on the unicode identifier and pattern syntax
 *   (http://www.unicode.org/reports/tr31/)
 * And extended with a few characters.
 */
IdentifierStart : ID_Start
                | Pc
                ;

/**
 * Based on the unicode identifier and pattern syntax
 *   (http://www.unicode.org/reports/tr31/)
 * And extended with a few characters.
 */
IdentifierPart : ID_Continue
               | Sc
               ;

/**
 * Any character except "`", enclosed within `backticks`. Backticks are escaped with double backticks. */
EscapedSymbolicName : ( '`' ( EscapedSymbolicName_0 )* '`' )+ ;

SP : ( WHITESPACE )+ ;

WHITESPACE : SPACE
           | TAB
           | LF
           | VT
           | FF
           | CR
           | FS
           | GS
           | RS
           | US
           | ' '
           | '᠎'
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | ' '
           | '　'
           | ' '
           | ' '
           | ' '
           | Comment
           ;

Comment : ( '/*' ( Comment_1 | ( '*' Comment_2 ) )* '*/' )
        | ( '//' ( Comment_3 )* CR? ( LF | EOF ) )
        ;

leftArrowHead : '<' ;

rightArrowHead : '>' ;

dash : '-' ;

fragment FF : [\f] ;

fragment EscapedSymbolicName_0 : [\u0000-_a-\uFFFF] ;

fragment RS : [\u001E] ;

fragment ID_Continue : [0-9A-Z_a-z] ;

fragment Comment_1 : [\u0000-)+-\uFFFF] ;

fragment StringLiteral_1 : [\u0000-&(-[\]-\uFFFF] ;

fragment Comment_3 : [\u0000-\t\u000B-\f\u000E-\uFFFF] ;

fragment Comment_2 : [\u0000-.0-\uFFFF] ;

fragment GS : [\u001D] ;

fragment FS : [\u001C] ;

fragment CR : [\r] ;

fragment Sc : [$\u00A2-\u00A5\u058F\u060B\u09F2-\u09F3\u09FB\u0AF1\u0BF9\u0E3F\u17DB\u20A0-\u20BA\uA838\uFDFC\uFE69\uFF04\uFFE0-\uFFE1\uFFE5-\uFFE6] ;

fragment SPACE : [ ] ;

fragment Pc : [_\u203F-\u2040\u2054\uFE33-\uFE34\uFE4D-\uFE4F\uFF3F] ;

fragment TAB : [\t] ;

fragment StringLiteral_0 : [^"] ;

fragment LF : [\n] ;

fragment VT : [\u000B] ;

fragment US : [\u001F] ;

fragment ID_Start : [A-Za-z];