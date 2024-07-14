:- dynamic male/1.
:- dynamic female/1.
:- dynamic grandfather_of/2.
:- dynamic grandmother_of/2.
:- dynamic father_of/2.
:- dynamic mother_of/2.
:- dynamic parent_of/2.
:- dynamic son_of/2.
:- dynamic daughter_of/2.
:- dynamic child_of/2.
:- dynamic sibling_of/2.
:- dynamic siblings/2.
:- dynamic sister_of/2.
:- dynamic brother_of/2.
:- dynamic aunt_of/2.
:- dynamic uncle_of/2.


father_of(X,Y):-
    male(X),
    parent_of(X,Y),
    X \= Y,
    \+(
        child_of(X, Y);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        siblings(X,Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).

mother_of(X,Y):-
    female(X),
    parent_of(X,Y),
    X \= Y,
    \+(
        child_of(X, Y);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        siblings(X,Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).


daughter_of(X,Y):-
    female(X),
    parent_of(Y,X),
    X \= Y,
    \+(
        child_of(Y, X);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        siblings(X,Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).

son_of(X,Y):-
    male(X),
    parent_of(Y,X),
    X \= Y,
   \+(
        child_of(Y, X);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        siblings(X,Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).

child_of(X,Y):-
   parent_of(Y,X),
    X \= Y.


grandfather_of(X,Y):-
    male(X),
    parent_of(X,Z),
    parent_of(Z,Y),
    X \= Y,
    \+(
        child_of(X, Z);
        child_of(Z, Y);
        siblings(X,Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).

grandmother_of(X,Y):-
    female(X),
    parent_of(X,Z),
    parent_of(Z,Y),
    X \= Y,
    \+(
        child_of(X, Z);
        child_of(Z, Y);
        siblings(X,Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).

grandparent_of(X,Y):-
    parent_of(X,Z),
    parent_of(Z,Y),
    X \= Y.


siblings(X, Y) :-
    ((sibling_of(X, Y), X \= Y);
    (parent_of(Z, X), parent_of(Z, Y), X \= Y)),
    \+(
        child_of(X, Y);
        child_of(Y, X);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).

sister_of(X,Y):-
    female(X), X \= Y,
    (
        (parent_of(F, Y), parent_of(F, X), F \= Y, F \= X) ;
        siblings(X,Y)
    ),
    \+(
        child_of(X, Y);
        child_of(Y, X);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).

brother_of(X,Y):-
    male(X), X \= Y,
    (
        (parent_of(F, Y), parent_of(F, X), F \= Y, F \= X) ;
        siblings(X,Y)
    ),
    \+(
        child_of(X, Y);
        child_of(Y, X);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        aunt_or_uncle_of(X,Y);
        aunt_or_uncle_of(Y,X)
    ).


aunt_of(X,Y):-
    female(X),
    parent_of(Z,Y),
    sister_of(X, Z),
    X \= Y,
    \+(
        child_of(X, Y);
        child_of(Y, X);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        siblings(X,Y)
    ).

uncle_of(X,Y):-
    male(X),
    parent_of(Z,Y),
    brother_of(X, Z),
    X \= Y,
    \+(
        child_of(X, Y);
        child_of(Y, X);
        grandparent_of(Y, X);
        grandparent_of(X, Y);
        siblings(X,Y)
    ).

aunt_or_uncle_of(X,Y):-
    parent_of(Z,Y),
    siblings(X, Z).

relatives(X,Y):-
    X \= Y,
    parent_of(X,Y);
    parent_of(Y,X);
    siblings(X,Y);

    aunt_of(X,Y);
    aunt_of(Y,X);
    (aunt_of(Z,X), aunt_of(Z,Y));

    uncle_of(X,Y);
    uncle_of(Y,X);
    (uncle_of(Z,X), uncle_of(Z,Y));
    aunt_or_uncle_of(X, Y);
    aunt_or_uncle_of(Y, X);

    grandmother_of(X,Y);
    grandmother_of(Y,X);
    (grandmother_of(Z,X), grandmother_of(Z,Y));
    grandparent_of(Y, X);
    grandparent_of(X, Y);

    grandfather_of(X,Y);
    grandfather_of(Y,X);
    (grandfather_of(Z,X), grandfather_of(Z,Y)).
