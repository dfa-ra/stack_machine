;_import_
;    "lib/math.forth"

_data_
5 VAR var_a

_text_

LOOP
    1 !i 4 <= 1
    WHILE
        var_a 10 + !var_a
        LOOP
            1 !j 4 <= 1
            WHILE
                var_a j + !var_a
            REPEAT
        var_a 1 + !var_a
    REPEAT
HALT
