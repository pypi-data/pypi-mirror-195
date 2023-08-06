# robotframework-implicitcontext

A simple robotframework resource for using implicit context in BDD tests.

INSTALL:

    pip install robotframework-implicitcontext

IMPORT:

    Resource  ImplicitContextLibrary/ImplicitContextKeywords.resource

CREATE SOME KEYWORDS:

    A new robotalk titled "${talk_title}"
      ${a_robotalk}=  Create Robotalk  ${talk_title}  # Your Keyword
      Push Implicit Context  robotalk  ${a_robotalk}
      [Return]  ${a_robotalk}

    The ${idx_name:first|second|third|fourth|fifth|last|next-to-last} robotalk has not yet received applause
      ${a_robotalk}=  Get Implicit Context  robotalk  ${idx_name}
      Robotalk Should Not Have Applause  ${a_robotalk}  # Your Keyword

USE THE KEYWORDS:

    Given a new robotalk titled "My Talk"
    And a new robotalk titled "Another Talk"
    Then the first robotalk has not yet received applause
    And the second robotalk has not yet received applause

TK:
* Link to generated libdoc
* Link to atests
