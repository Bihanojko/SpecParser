{"block_list": [{"block_type": 6, "content": [{"AP": [["! 0%{?first_if:1}", 1]], "block_type": 2, "body": "first_body", "keyword": "define", "name": "first_define", "options": null}, {"AP": [["! 0%{?first_if:1}", 1]], "block_type": 6, "content": [{"AP": [["! 0%{?first_if:1}", 1], ["second_if", 1]], "block_type": 2, "body": "second_body", "keyword": "define", "name": "second_define", "options": "(o:)"}], "else_body": [{"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0]], "block_type": 2, "body": "scond_else_body", "keyword": "define", "name": "second_else", "options": null}, {"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0]], "block_type": 6, "content": [{"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0], ["third_if", 1]], "block_type": 2, "body": "third_body", "keyword": "define", "name": "third_if", "options": null}], "else_body": [{"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0], ["third_if", 0]], "block_type": 5, "content": "# third else comment"}], "else_keyword": "else", "end_keyword": "endif", "expression": "third_if", "keyword": "if"}, {"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0]], "block_type": 5, "content": "# inter comment"}, {"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0]], "block_type": 6, "content": [{"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0], ["fourth_if", 1]], "block_type": 5, "content": "# fourth if comment"}, {"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0], ["fourth_if", 1]], "block_type": 6, "content": [{"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0], ["fourth_if", 1], ["fifth_if", 1]], "block_type": 5, "content": "# fifth if comment"}], "else_body": [], "else_keyword": null, "end_keyword": "endif", "expression": "fifth_if", "keyword": "if"}], "else_body": [{"AP": [["! 0%{?first_if:1}", 1], ["second_if", 0], ["fourth_if", 0]], "block_type": 5, "content": "# fourth else comment"}], "else_keyword": "else", "end_keyword": "endif", "expression": "fourth_if", "keyword": "if"}], "else_keyword": "else", "end_keyword": "endif", "expression": "second_if", "keyword": "if"}], "else_body": [{"AP": [["! 0%{?first_if:1}", 0]], "block_type": 2, "body": "go build -ldflags \"${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\\\n')\" -a -v -x %{?**};", "keyword": "define", "name": "secondelse", "options": "(o:)"}], "else_keyword": "else", "end_keyword": "endif", "expression": "! 0%{?first_if:1}", "keyword": "if"}], "metastring": "#%0 %1\n  %3\n  %5\n#%0 %1 %3\n  #%0 %1\n    %3\n    %5\n\n#%0 %1%2 %3\n  #%0 %1 %3\n    #%0 %1\n      %3\n      %5\n    #%0 %1 %3\n    #%0\n    #%0\n    #%0 %1\n      %3\n      %5\n  #%0\n      #%0 %1\n        %5\n    #%0\n      #%0\n    #%0 %1%2 %3 \n"}
