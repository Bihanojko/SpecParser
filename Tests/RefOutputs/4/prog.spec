{"Comments": [{"AP": [["! 0%{?first_if:1}", 1], ["druhej_if", 1]], "block_type": 5, "content": "# comment jak svina"}, {"AP": [["! 0%{?first_if:1}", 1]], "block_type": 5, "content": "# problem 1"}, {"AP": [["! 0%{?first_if:1}", 1], ["treti_if", 1]], "block_type": 5, "content": "# treti comment"}, {"AP": [["! 0%{?first_if:1}", 1], ["ctvrty_if", 1]], "block_type": 5, "content": "#posledni comment"}, {"AP": [["! 0%{?first_if:1}", 1]], "block_type": 5, "content": "# taky patri do prvni urovne"}], "Conditions": [{"block_type": 6, "else_body": [], "else_keyword": null, "end_keyword": "endif", "expression": "! 0%{?first_if:1}", "keyword": "if"}, {"AP": [["! 0%{?first_if:1}", 1]], "block_type": 6, "else_body": [], "else_keyword": null, "end_keyword": "endif", "expression": "druhej_if", "keyword": "if"}, {"AP": [["! 0%{?first_if:1}", 1]], "block_type": 6, "else_body": [], "else_keyword": null, "end_keyword": "endif", "expression": "treti_if", "keyword": "if"}, {"AP": [["! 0%{?first_if:1}", 1]], "block_type": 6, "else_body": [], "else_keyword": null, "end_keyword": "endif", "expression": "ctvrty_if", "keyword": "if"}], "MacroDefinitions": [{"AP": [["! 0%{?first_if:1}", 1]], "block_type": 2, "body": "first_body", "keyword": "define", "name": "first_define", "options": null}], "metastring": "#60%0 %1\n  #20%0 %1 %3\n  #61%0 %1\n    #50%0\n  #61%5\n  #51%0\n  #62%0\n #52%0 %1\n    %5\n  #62 #63%0 %1\n    #53%0\n  #63%5\n  #54%0\n  #60%5\n"}