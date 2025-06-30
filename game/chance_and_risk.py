chances = [
    ["You found deals on cheap components you gain $100", "mn-100"],
    ["Your equipment is working better than expected - you move up 1 square", "mv-1"],
    ["You won the mini Lotto - you gain $150", "mn-150"],
    ["Your Twitter post went viral - you roll the dice again", "rl-ag"],
    ["The customer paid the invoice in advance - you gain $120", "mn-120"],
    [
        "You have been invited to a prestigious partnership - move to any field in front",
        "mv-any",
    ],
    [
        "You have successfully optimized code - you gain $80 and move forward 1 field",
        "mn-80-mv-1",
    ],
    ["Your startup gained popularity - you gain $200", "mn-200"],
]
risks = [
    ["Power surge burnt out some equipment - you pay $150", "mn-_150"],
    ["Internet outage - you lose 1 turn", "lt-1"],
    ["Internal server error - you're going back 1 square", "mv-_1"],
    ["You lost your documentation - you pay $100", "mn-_100"],
    ["The customer has withdrawn from the contract - you pay $120", "mn-_120"],
    [
        "You sued yourself and lost rights to the software - you go back 3 squares",
        "mv-_3",
    ],
    ["The backup system worked - you avoid the start, you do nothing", "anything"],
    [
        "The mistake cost you time but you learned something new - you go back 2 spaces but gain $60",
        "mv-_2-mn-60",
    ],
    [
        "Programmer resigned but left documentation - lose turn but you gain $50",
        "lt-1-mn-50",
    ],
    ["Investor backed out - you lose your turn, but you gain $80", "lt-1-mn-80"],
    [
        "your computer has been infected - you lose a random part of your computer",
        "rm-any",
    ],
]
