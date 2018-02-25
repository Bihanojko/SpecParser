%if ! 0%{?first_if:1}
  %define first_define first_body
  %if second_if
    # first comment
  %endif
  # problem #1
  %if third_if
    # third comment
  %endif
  %if fourth_if
    # fourth comment
  %endif    
  # last comment
%endif
