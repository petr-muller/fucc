# FORMAT:
# TAG : COMMAND
# EXAMPLE
# GCC_O0 : gcc -O0 SOURCE -o OUTPUT

OUTPUT_SUFFIX="output"
RESULT_SUFFIX="result"
RETCODE0_MSG="Success"
RETCODE_NOT0_MSG="Failure"

TAGS = (
    { "name" : "GCC_O0",  "command" : "gcc -O0 SOURCE -o OUTPUT"},
    { "name" : "GCC_O2",  "command" : "gcc -O2 SOURCE -o OUTPUT"},
    { "name" : "TCC",     "command" : "tcc SOURCE -o OUTPUT"},
    { "name" : "GCC_OS",  "command" : "gcc -Os SOURCE -o OUTPUT"},
    { "name" : "GCC_O3",  "command" : "gcc -O3 SOURCE -o OUTPUT"},
    { "name" : "ICC_O0",  "command" : "icc -O0 SOURCE -o OUTPUT"},
    { "name" : "ICC_O2",  "command" : "icc -O2 SOURCE -o OUTPUT"}
)

ACTIONS=("BUILD", "RUN", "READELF")

ADDITIONAL={
    "READELF" : "readelf -a OUTPUT"
    }

