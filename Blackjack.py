import copy
import random
import pygame

# will initialize any variables needed for the game (i.e. font)
pygame.init()

# set up of window using pygame
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)

# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
active = False

# win, loss, draw
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'Player BUSTED :(', 'Player WINS :D ', 'Dealer WINS :O', 'Tie Game']



# deal cards by selecting randomly from deck and make function for one card at a time
# function should give out card for dealer and player
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    # print(current_hand, current_deck)
    return current_hand, current_deck

# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not act:
        # screen, color, [x position, y posision, width, height], 0 width = solid box, rounded edge
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        # will give the effect of having a green 'border' around the white box
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render("Deal Hand", True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    # once game started, show hit and stand buttons and win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render("Hit Me", True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stay = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stay_text = font.render("Stay", True, 'black')
        screen.blit(stay_text, (355, 735))
        button_list.append(stay)
        history_text = smaller_font.render(f'Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(history_text, (15, 840))

    # if there is an outcome for the hand that was played, display a restart button and tell the user what happened
    if result != 0: 
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render("New Hand", True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        # x * i will shift the following cards to the right of the screen by x
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        # red 'border'
        screen.blit(font.render(player[i], True,'black'), (75 + (70 * i), 465 + (5 * i)))
        screen.blit(font.render(player[i], True,'black'), (75 + (70 * i), 635 + (5 * i)))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

    # if player hasnt finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        # if we are past that first card or the dealer is revealing their cards then we can show the cards
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + (70 * i), 165 + (5 * i)))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + (70 * i), 335 + (5 * i)))
        # card that we need to hide
        else:
            screen.blit(font.render('???', True, 'black'),(75 + (70 * i), 165 + (5 * i)))
            screen.blit(font.render('???', True, 'black'),(75 + (70 * i), 335 + (5 * i)))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

# pass in player/dealer hand to get best possible score
# calculates hand score, check how many aces we have. A's have either score of 1 or 11
def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2-9, just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10 and face cards, add 10
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif hand[i] == 'A':
            hand_score += 11
            # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        # for as many aces as we have, if our hand score is still over 21, lets subtract 10 changing value from 11 to 1.
        # if hand_score is less than 21 we dont want to reduce any more aces
        for i in range(1, aces_count):
            if hand_score > 21: 
                hand_score -= 10
    return hand_score

#draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'white'), (350, 400))
    # we want to see the dealer score
    if reveal_dealer: 
        screen.blit(font.render(f'Score[{dealer}]', True, 'white'), (350, 100))

# check endgame conditions
def check_endgame(hand_act, deal_score, play_score, result, totals, add): 
    # check end game scenarios if player has stood, busted, or blackjacked and hand is not active 
    # result 1: player bust, 2: win, 3: loss, 4: push
    if not hand_act and deal_score >= 17:
        # busted
        if play_score > 21: 
            result = 1

        # player has outscored the dealer and has not busted
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        
        # lose just by comparison, nobody busted
        elif play_score < deal_score <= 21: 
            result = 3
        
        # tie
        else: 
            result = 4
        
        if add: 
            if result == 1 or result == 3: 
                # totals[1] = losses
                totals[1] += 1
            elif result == 2: 
                # totals[0] = wins
                totals[0] += 1
            else: 
                # totals[2] = draw
                totals[2] += 1
            add = False
    return result, totals, add

# main game loop
run = True
while run:
    # run game at frame rate and fill screen with background color
    timer.tick(fps)
    screen.fill('black')
    # initial deal to player and dealer
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        # print(my_hand, dealer_hand)
        initial_deal = False
    # once game is activated and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer: 
            dealer_score = calculate_score(dealer_hand)
            # while the dealer has less than 17 points, they need to keep drawing cards
            if dealer_score < 17: 
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)

    # event handling: if quit pressed then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            # if we haven't started the game yet
            if not active:
                # first button passing back in the list is deal hand button
                if buttons[0].collidepoint(event.pos):
                    active = True
                    # initial deal is the only time that two cards would come in at the same time
                    initial_deal = True
                    # this is code that we want to change every time - reset code
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else: 
                # prevents you from being able to hit if you've busted
                # hand_acitve = player actively going
                # if we click on the hit me button AND we have a score less than 21 AND it is our turn
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    
                # clicking on stay button. we want to be done with the game
                # dealer will be set to reveal score
                # we will end our turn
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3: 
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    # if player busts automatically end turn - automatic stay
    if hand_active and player_score >= 21: 
        hand_active = False 
        reveal_dealer = True
    
    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    # command that makes sure that everthing that we wrote to get drawn to the screen is flipped on to the screen to be drawn
    pygame.display.flip()
pygame.quit()
