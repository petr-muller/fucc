<keyword> ::= auto | break | case | char | const | continue | default | do 
              | double | else | enum | extern | float | for | goto | if 
              | inline | int | long | register | restrict | return | short
              | signed | sizeof | static | struct | switch | typedef | union
              | unsigned | void | volatile | while | _Bool | _Complex
              | _Imaginary ;;;
<identifier> ::= <identifier_nondigit>
                 | <identifier><identifier_nondigit> 
                 | <identifier><digit> ;;;
<identifier_nondigit> ::= <nondigit> | <universal_character_name> ;;;
<nondigit> ::= _ | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o 
               | p | q | r | s | t | u | v | w | x | y | z | A | B | C | D | E
               | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U
               | V | W | X | Y | Z ;;;
<source_character> ::= A | B | C | D | E | F | G | H | I | J | K | L | M | N
                     | O | P | Q | R | S | T | U | V | W | X | Y | Z | a | b
                     | c | d | e | f | g | h | i | j | k | l | m | n | o | p
                     | q | r | s | t | u | v | w | x | y | z | 0 | 1 | 2 | 3 
                     | 4 | 5 | 6 | 7 | 8 | 9 | ! | # | % | & | ( | )
                     | * | + | , | - | . | / | : | ; | LTSIGN | = | GTSIGN | ? | [  
                     | ] | ^ | _ | { | } | ~ ;;; 
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ;;;

<universal_character_name> ::= \u<hex_quad> | \U<hex_quad><hex_quad> ;;;

<hex_quad> ::= <hexadecimal_digit><hexadecimal_digit><hexadecimal_digit><hexadecimal_digit> ;;;

<hexadecimal_digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | A | B | C | D | E | F ;;;

<constant> ::= <integer_constant> | <floating_constant> | <enumeration_constant> | <character_constant> ;;;

<integer_constant> ::= <decimal_constant><[integer_suffix]> | <octal_constant><[integer_suffix]> | <hexadecimal_constant><[integer_suffix]> ;;;

<decimal_constant> ::= <nonzero_digit> | <decimal_constant><digit> ;;;

<octal_constant> ::= 0 | <octal_constant><octal_digit> ;;;

<hexadecimal_constant> ::= <hexadecimal_prefix><hexadecimal_digit> | <hexadecimal_constant><hexadecimal_digit> ;;;

<hexadecimal_prefix> ::= 0x | 0X ;;;

<nonzero_digit> ::= 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ;;;

<octal_digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 ;;;

<integer_suffix> ::= <unsigned_suffix><[long_suffix]> | <unsigned_suffix><[long_long_suffix]> | <long_suffix><[unsigned_suffix]> | <long_long_suffix><[unsigned_suffix]> ;;;

<unsigned_suffix> ::= u | U ;;;
<long_suffix> ::= l | L ;;;
<long_long_suffix> ::= ll | LL ;;;

<floating_constant> ::= <decimal_floating_constant> | <hexadecimal_floating_constant> ;;;

<decimal_floating_constant> ::= <fractional_constant><[exponent_part]><[floating_suffix]> | <digit_sequence><exponent_part><[floating_suffix]> ;;;

<hexadecimal_floating_constant> ::= <hexadecimal_prefix><hexadecimal_fractional_constant><binary_exponent_part><[floating_suffix]> | <hexadecimal_prefix><hexadecimal_digit_sequence><binary_exponent_part><[floating_suffix]> ;;;

<fractional_constant> ::= <[digit_sequence]>.<digit_sequence> | <digit_sequence>. ;;;

<exponent_part> ::= e<[sign]><digit_sequence> | E<[sign]><digit_sequence> ;;;

<sign> ::= + | - ;;;

<digit_sequence> ::= <digit> | <digit_sequence><digit> ;;;

<hexadecimal_fractional_constant> ::= <[hexadecimal_digit_sequence]>.<hexadecimal_digit_sequence> | <hexadecimal_digit_sequence>. ;;;

<binary_exponent_part> ::= p<[sign]><digit_sequence> | P<[sign]><digit_sequence> ;;;

<hexadecimal_digit_sequence> ::= <hexadecimal_digit> | <hexadecimal_digit_sequence><hexadecimal_digit> ;;;

<floating_suffix> ::= f | L | F | L ;;;

<enumeration_constant> ::= <identifier> ;;;

<character_constant> ::= '<c_char_sequence>' | L'<c_char_sequence>' ;;;

<c_char_sequence> ::= <c_char> | <c_char_sequence><c_char> ;;;

<c_char> ::= <source_character> | <escape_sequence> ;;;

<escape_sequence> ::= <simple_escape_sequence> | <octal_escape_sequence> | <hexadecimal_escape_sequence> | <universal_character_name> ;;;

<simple_escape_sequence> ::= \' | \" | \? | \\ | \a | \b | \f | \n | \r | \t | \v ;;;

<octal_escape_sequence> ::= \<octal_digit> | \<octal_digit><octal_digit> | \<octal_digit><octal_digit><octal_digit> ;;;

<hexadecimal_escape_sequence> ::= \x<hexadecimal_digit> | <hexadecimal_escape_sequence><hexadecimal_digit> ;;;

<string_literal> ::= "<[s_char_sequence]>" | L"<[s_char_sequence]>" ;;;

<s_char_sequence> ::= <s_char> | <s_char_sequence><s_char> ;;;

<s_char> ::= <source_character> | <escape_sequence> ;;;

<punctuator> ::= [ | ] | ( | ) | { | } | . | -GTSIGN | ++ | -- | & | * | + | - | ~ | ! 
                   | / | % | LTSIGNLTSIGN | GTSIGNGTSIGN | LTSIGN | GTSIGN | LTSIGN= | GTSIGN= | == | != | ^ | && | || | ? | : 
                   | ; | ... | = | *= | /= | %= | += | -= | LTSIGNLTSIGN= | GTSIGNGTSIGN= | &= | ^= 
                   | |= | , | # | ## | LTSIGN: | :GTSIGN | LTSIGN% | %GTSIGN | %: | %:%: ;;;

<header_name> ::= LTSIGN<h_char_sequence>GTSIGN | "<h_char_sequence>" ;;;

<h_char_sequence> ::= <h_char> | <h_char_sequence><h_char> ;;;

<h_char> ::= <source_character> ;;;

<q_char_sequence> ::= <q_char> | <q_char_sequence><q_char> ;;;

<q_char> ::= <source_character> ;;;

<primary_expression> ::= <identifier> | <constant> | <string_literal> | {<expression>} ;;;

<postfix_expression> ::= <primary_expression> | <postfix_expression>[<expression>] 
                       | <postfix_expression>(<[argument_expression_list]>) 
                       | <postfix_expression>.<identifier> 
                       | <postfix_expression>-GTSIGN<identifier> 
                       | <postfix_expression>++ | <postfix_expression>-- 
                       | ( <type_name>) { <initializer_list> } 
                       | ( <type_name>) { <initializer_list>, } ;;;

<argument_expression_list> ::= <assignment_expression> | <argument_expression_list>,<assignment_expression> ;;;

<unary_expression> ::= <postfix_expression> | ++<unary_expression> 
                     | --<unary_expression> | <unary_operator><cast_expression> 
                     | sizeof<unary_expression> | sizeof(<type_name>) ;;;

<unary_operator> ::= & | * | + | - | ~ | ! ;;;

<cast_expression> ::= <unary_expression> | (<type_name>)<cast_expression> ;;;

<multiplicative_expression> ::= <cast_expression>
                              | <multiplicative_expression>*<cast_expression>
                              | <multiplicative_expression>/<cast_expression>
                              | <multiplicative_expression>%<cast_expression> ;;;
<additive_expression> ::= <multiplicative_expression>
                        | <additive_expression> + <multiplicative_expression> 
                        | <additive_expression> - <multiplicative_expression> ;;;
<shift_expression> ::= <additive_expression>  
                     | <shift_expression> LTSIGNLTSIGN <additive_expression> 
                     | <shift_expression> GTSIGNGTSIGN <additive_expression> ;;;
<relational_expression> ::= <shift_expression> 
                          | <relational_expression> LTSIGN <shift_expression>
                          | <relational_expression> GTSIGN <shift_expression>
                          | <relational_expression> LTSIGN= <shift_expression>
                          | <relational_expression> GTSIGN= <shift_expression> ;;;
<equality_expression> ::= <relational_expression> 
                        | <equality_expression> == <relational_expression> 
                        | <equality_expression> != <equality_expression> ;;;
<AND_expression> ::= <equality_expression> | <AND_expression> & <equality_expression> ;;;
<exclusive_OR_expression> ::= <AND_expression> 
                            | <exclusive_OR_expression> ^ <AND_expression> ;;;
<inclusive_OR_expression> ::= <exclusive_OR_expression>
                            | <inclusive_OR_expression>|<exclusive_OR_expression> ;;;
<logical_AND_expression> ::= <inclusive_OR_expression>
                           | <logical_AND_expression>&&<inclusive_OR_expression> ;;;
<logical_OR_expression> ::= <logical_AND_expression> 
                          | <logical_OR_expression> || <logical_AND_expression> ;;;
<conditional_expression> ::= <logical_OR_expression> 
                           | <logical_OR_expression> ? <expression> : <conditional_expression> ;;;

<assignment_expression> ::= <conditional_expression>
                          | <unary_expression><assignment_operator><assignment_expression> ;;;

<assignment_operator> ::= = | *= | /= | %= | += | -= | LTSIGNLTSIGN= | GTSIGNGTSIGN= | &= | ^= | |= ;;;

<expression> ::= <assignment_expression> | <expression>,<assignment_expression> ;;;

<constant_expression> ::= <conditional_expression> ;;;

<declaration> ::= <declaration_specifiers> <[init_declarator_list]> ; ;;;

<declaration_specifiers> ::= <storage_class_specifier> <[declaration_specifiers]>
                           | <type_specifier> <[declaration_specifiers]>
                           | <type_qualifier> <[declaration_specifiers]>
                           | <function_specifier><[declaration_specifiers]> ;;;
<init_declarator_list> ::= <init_declarator> | <init_declarator_list>,<init_declarator> ;;;

<init_declarator> ::= <declarator> | <declarator> = <initializer> ;;;

<storage_class_specifier> ::= typedef | extern | static | auto | register ;;;
<type_specifier> ::= void | char | short | int | long | float | double | signed
                   | unsigned | _Bool | _Complex | <struct_or_union_specifier> 
                   | <enum_specifier> | <typedef_name> ;;;

<struct_or_union_specifier> ::= <struct_or_union> <[identifier]>{<struct_declaration_list>} | <struct_or_union> <identifier> ;;;

<struct_or_union> ::= struct | union ;;;

<struct_declaration_list> ::= <struct_declaration> | <struct_declaration_list><struct_declaration> ;;;

<struct_declaration> ::= <specifier_qualifier_list> <struct_declarator_list> ; ;;;

<specifier_qualifier_list> ::= <type_specifier> <[specifier_qualifier_list]>
                             | <type_qualifier><[specifier_qualifier_list]> ;;;

<struct_declarator_list> ::= <struct_declarator>
                           | <struct_declarator_list>,<struct_declarator> ;;;
<struct_declarator> ::= <declarator> | <[declarator]>:<constant_expression> ;;;

<enum_specifier> ::= enum <[identifier]>{<enumerator_list>}
                   | enum <[identifier]>{<enumerator_list>,}
                   | enum <identifier> ;;;

<enumerator_list> ::= <enumerator> | <enumerator_list>,<enumerator> ;;;

<enumerator> ::= <enumeration_constant> | <enumeration_constant> = <constant_expression> ;;;

<type_qualifier> ::= const | restrict | volatile ;;;

<function_specifier> ::= inline ;;;

<declarator> ::= <[pointer]><direct_declarator> ;;;

<direct_declarator> ::= <identifier> | (<declarator>)
                      | <direct_declarator>[<[type_qualifier_list]><[assignment_expression]>]
                      | <direct_declarator>[<type_qualifier_list> static <assignment_expression>]
                      | <direct_declarator>[static <[type_qualifier_list]><assignment_expression>]
                      | <direct_declarator>[<[type_qualifier_list]>*]
                      | <direct_declarator>(<parameter_type_list>)
                      | <direct_declarator>(<[identifier_list]>) ;;;

<pointer> ::= * <[type_qualifier_list]> | * <[type_qualifier_list]><pointer> ;;;

<type_qualifier_list> ::= <type_qualifier> | <type_qualifier_list><type_qualifier> ;;;

<parameter_type_list> ::= <parameter_list> | <parameter_list>, ... ;;;

<parameter_list> ::= <parameter_declaration> | <parameter_list>,<parameter_declaration> ;;;

<parameter_declaration> ::= <declaration_specifiers><declarator> 
                          | <declaration_specifiers><[abstract_declarator]> ;;;

<identifier_list> ::= <identifier> | <identifier_list>,<identifier> ;;;

<type_name> ::= <specifier_qualifier_list><[abstract_declarator]> ;;;

<abstract_declarator> ::= <pointer> | <[pointer]><direct_abstract_declarator> ;;;

<direct_abstract_declarator> ::= (<abstract_declarator>)
                               | <[direct_abstract_declarator]>[<[type_qualifier_list]><[assignment_expression]>
                               | <[direct_abstract_declarator]>[ static <[type_qualifier_list]><assignment_expression> ]
                               | <[direct_abstract_declarator]>[ <type_qualifier_list> static <assignment_expression> 
                               | <[direct_abstract_declarator]>[ * ] 
                               | <[direct_abstract_declarator]>(<[parameter_type_list]>) ;;;

<typedef_name> ::= <identifier> ;;;

<initializer> ::= <assignment_expression> | { <initializer_list> } 
                | { <initializer_list>, } ;;;

<initializer_list> ::= <[designation]><initializer> 
                     | <initializer_list>,<[designation]><initializer> ;;;

<designation> ::= <designator_list> = ;;;

<designator_list> ::= <designator> | <designator_list><designator> ;;;

<designator> ::= [ <constant_expression> ] | .<identifier> ;;;

<statement> ::= <labeled_statement> | <compound_statement> | <expression_statement>
              | <selection_statement> | <iteration_statement> | <jump_statement> ;;;

<labeled_statement> ::= <identifier>: <statement>
                      | case <constant_expression>: <statement>
                      | default: <statement> ;;;
<compound_statement> ::= { <[block_item_list]> } ;;;
<block_item_list> ::= <block_item> | <block_item_list> <block_item> ;;;
<block_item> ::= <declaration> | <statement> ;;;
<expression_statement> ::= <[expression]> ; ;;;
<selection_statement> ::= if ( <expression> ) <statement> 
                        | if ( <expression> ) <statement> else <statement>
                        | switch ( <expression> ) <statement> ;;;
<iteration_statement> ::= while ( <expression> ) <statement> 
                        | do <statement> while ( <expression> );
                        | for ( <[expression]>; <[expression]>; <[expression]> ) <statement> 
                        | for ( <declaration> <[expression]> ; <[expression]> ) <statement> ;;;

<jump_statement> ::= goto <identifier>; | continue; | break; | return <[expression]>; ;;;

<declaration_list> ::= <declaration> | <declaration_list> <declaration> ;;;

<function_definition> ::= <declaration_specifiers> <declarator> <[declaration_list]> <compound_statement> ;;;

<external_declaration> ::= <function_definition> | <declaration> ;;;

<translation_unit> ::= <external_declaration> | <translation_unit> <external_declaration> ;;;
