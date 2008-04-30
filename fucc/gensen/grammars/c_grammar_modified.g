<float_type> ::= float | double ;;;
<integer_type> ::= char | short | int | long | long long ;;;
<signedness> ::= signed | unsigned ;;;
<numeral_type> ::= <[signedness]>{0.3} <integer_type> | <float_type> %%% (5,2) ;;;

<identifier> ::= <identifier_nondigit>
                 | <identifier><identifier_nondigit> 
                 | <identifier><digit> %%% (1,2,2) ;;;
<identifier_nondigit> ::= <nondigit> ;;;
<nondigit> ::= _ | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o 
               | p | q | r | s | t | u | v | w | x | y | z | A | B | C | D | E
               | F | G | H | I | J | K | L | M | N | O | P | Q | R | S | T | U
               | V | W | X | Y | Z ;;;
<source_character> ::= A | B | C | D | E | F | G | H | I | J | K | L | M | N
                     | O | P | Q | R | S | T | U | V | W | X | Y | Z | a | b
                     | c | d | e | f | g | h | i | j | k | l | m | n | o | p
                     | q | r | s | t | u | v | w | x | y | z | 0 | 1 | 2 | 3 
                     | 4 | 5 | 6 | 7 | 8 | 9 | ! | # | % | & | ( | )
                     | * | + | , | - | . | / | : | ; | < | = | > | ? | [  
                     | ] | ^ | _ | { | } | ~ ;;; 
<digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ;;;

<hexadecimal_digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | a | b | c | d | e | f | A | B | C | D | E | F ;;;

<constant> ::= <integer_constant> | <floating_constant> | <character_constant> ;;;

<integer_constant> ::= <decimal_constant><[integer_suffix]>{0.3} | <octal_constant><[integer_suffix]>{0.3} | <hexadecimal_constant><[integer_suffix]>{0.3} ;;;

<decimal_constant> ::= <nonzero_digit> | <decimal_constant><digit> ;;;

<octal_constant> ::= 0 | <octal_constant><octal_digit> ;;;

<hexadecimal_constant> ::= <hexadecimal_prefix><hexadecimal_digit> | <hexadecimal_constant><hexadecimal_digit> ;;;

<hexadecimal_prefix> ::= 0x | 0X ;;;

<nonzero_digit> ::= 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ;;;

<octal_digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 ;;;

<integer_suffix> ::= <unsigned_suffix><[long_suffix]>{0.2} | <unsigned_suffix><[long_long_suffix]>{0.2} | <long_suffix><[unsigned_suffix]>{0.2} | <long_long_suffix><[unsigned_suffix]>{0.2} ;;;

<unsigned_suffix> ::= u | U ;;;
<long_suffix> ::= l | L ;;;
<long_long_suffix> ::= ll | LL ;;;

<floating_constant> ::= <decimal_floating_constant> | <hexadecimal_floating_constant> ;;;

<decimal_floating_constant> ::= <fractional_constant><[exponent_part]><[floating_suffix]>{0.2} | <digit_sequence><exponent_part><[floating_suffix]>{0.2} ;;;

<hexadecimal_floating_constant> ::= <hexadecimal_prefix><hexadecimal_fractional_constant><binary_exponent_part><[floating_suffix]>{0.2} | <hexadecimal_prefix><hexadecimal_digit_sequence><binary_exponent_part><[floating_suffix]>{0.2} ;;;

<fractional_constant> ::= <[digit_sequence]>{0.9}.<digit_sequence> | <digit_sequence>. ;;;

<exponent_part> ::= e<[sign]>{0.6}<digit_sequence> | E<[sign]>{0.6}<digit_sequence> ;;;

<sign> ::= + | - ;;;

<digit_sequence> ::= <digit> | <digit_sequence><digit> ;;;

<hexadecimal_fractional_constant> ::= <[hexadecimal_digit_sequence]>{0.9}.<hexadecimal_digit_sequence> | <hexadecimal_digit_sequence>. ;;;

<binary_exponent_part> ::= p<[sign]>{0.6}<digit_sequence> | P<[sign]>{0.6}<digit_sequence> ;;;

<hexadecimal_digit_sequence> ::= <hexadecimal_digit> | <hexadecimal_digit_sequence><hexadecimal_digit> ;;;

<floating_suffix> ::= f | L | F | L ;;;

<character_constant> ::= '<c_char>' | L'<c_char>' ;;;

<c_char> ::= <source_character> | <escape_sequence> ;;;

<escape_sequence> ::= <simple_escape_sequence> | <octal_escape_sequence> | <hexadecimal_escape_sequence> ;;;

<simple_escape_sequence> ::= \' | \" | \? | \\ | \a | \b | \f | \n | \r | \t | \v ;;;

<octal_escape_sequence> ::= \<octal_digit> | \<octal_digit><octal_digit> | \<octal_digit><octal_digit><octal_digit> ;;;

<hexadecimal_escape_sequence> ::= \x<hexadecimal_digit> | <hexadecimal_escape_sequence><hexadecimal_digit> ;;;

<mod_operator> ::= % ;;;
<operator> ::= + | - | * | / %%% (3,3,3,1) ;;;
<relational_operator> ::= == | != | >= | > | < | <= ;;;
<existing_value> ::= <constant> ;;;
<operand> ::= <par_expression> | <existing_value> ;;;
<binary_expression> ::= <operand> <operator> <operand> | (((long long)(<operand>)) <mod_operator> ((long long)(<operand>))) %%% (8,1) ;;;
<expression> ::= <existing_value> | <binary_expression> ;;;
<par_expression> ::= (<expression>) | <expression> ;;;
<relational_expression> ::= ! <relational_expression> | <par_expression> <relational_operator> <par_expression> %%% (1,3) ;;;

<type> ::= <numeral_type> ;;;
<decl_list> ::= <decl_list> , <declaration> | <declaration> ;;;
<declaration> ::= <type> <identifier> ;;;
<ass_declaration> ::= <type> <identifier> = <par_expression> ;;;

<ass_to_dec_transition> ::= <ass_declaration> ;;;

<assignment> ::= <identifier> = <par_expression> ;;;


<block_epilogue> ::= printf("--- Block ID epilogue starts here ---\n"); ;;;
<augmented_block_epilogue> ::= printf("--- Block ID epilogue starts here---\n"); ;;;
<augmented_function_prologue> ::= printf("--- Block ID prologue starts here---\n"); ;;;

<block> ::= {
  <local_units>
  <block_epilogue>
}
;;; 


<return> ::= return ;;;

<augmented_function_block> ::= {
  <augmented_function_prologue>
  <local_units>
  <block_epilogue>
  <return>
} ;;;

<augmented_block> ::= {
  <local_units>
  <augmented_block_epilogue>
}
;;;

<while_do> ::= while ( <relational_expression> )<augmented_block> ;;;
<do_while> ::= do <augmented_block> while ( <relational_expression> ); ;;;

<else_clause> ::= else<block>;;;

<if_clause> ::= if ( <relational_expression> )<block>
<[else_clause]>{0.5} ;;; 

<function_definition> ::= <type> <identifier>(<decl_list>)<augmented_function_block> ;;;

<global_unit> ::= <declaration> | <ass_declaration> | <function_definition> %%% (1,0,2)  ;;;
<global_units> ::= <global_unit>; | <global_unit>;
<global_units> %%% (1,1) ;;;

<local_unit> ::= <declaration> | <constant> | <par_expression> | <ass_declaration> | <assignment> | <if_clause> | <while_do> | <do_while>  %%% (0,2,1,2,2,1,1,1) ;;;
<local_units> ::= <local_unit>; | <local_unit>;
  <local_units> %%% (2,1) ;;;

<main_epilogue> ::= printf ("--- Main epilogue starts here ---\n"); ;;;
<global_epilogue> ::= printf ("--- Global epilogue starts here ---\n"); ;;;

<mainfunction> ::= int main(int argc, char *argv[]){
  
  struct sigaction sa;
  memset (&sa, 0, sizeof(sa));
  sa.sa_handler = &handler;
  sigaction(SIGFPE, &sa, NULL);

  struct sigaction sa2;
  memset(&sa2, 0, sizeof(sa2));
  sa2.sa_handler = &handler;
  sigaction(SIGABRT,&sa2, NULL);
  

  <local_units>

  <main_epilogue>

  <global_epilogue>
} ;;;

<program> ::=
// (c) 2008 Petr Muller
// Program generated by gensen, random sentences generator
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <string.h>
#include <stdlib.h>

void handler (int signal_number){
  printf ("System got a signal number %i\n", signal_number);
  exit(128+signal_number);
}

<global_units> 

<mainfunction> ;;;
