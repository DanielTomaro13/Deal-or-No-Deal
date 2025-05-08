import random
import numpy as np

# --- Setup ---
case_values = [
    0.05, 0.1, 0.50, 1, 5, 10, 25, 50, 75, 100, 250, 500,
    750, 1000, 2500, 5000, 7500, 10000, 20000,
    30000, 40000, 50000, 60000, 70000, 80000, 90000,
    100000
]

cases = list(range(1, 27))
random.shuffle(case_values)
case_assignment = dict(zip(cases, case_values))

print("🎲 Welcome to Deal or No Deal 🎲")
print("Pick a case to keep (1–26):")
player_case = int(input("Your case number: "))

remaining_cases = cases.copy()
remaining_cases.remove(player_case)
opened_cases = {}

print(f"\n🧳 You selected case #{player_case}. Let us begin!\n")

# --- Game Loop ---
round_structure = [6, 5, 4, 3, 2, 2, 2, 1, 1]
round_number = 1
offers_history = []
game_over = False

while not game_over and len(remaining_cases) > 1 and round_number <= len(round_structure):
    cases_to_open = round_structure[round_number - 1]
    print(f"\n🔄 Round {round_number}: Please select {cases_to_open} case(s) to eliminate.\n")

    for i in range(cases_to_open):
        while True:
            print(f"🧳 Your case: #{player_case}")
            print(f"Remaining cases: {sorted(remaining_cases)}")
            case_choice_str = input(f"Select case #{i + 1} to open: ").strip()

            if not case_choice_str.isdigit():
                print("❌ Please enter a numeric value.")
                continue

            case_choice = int(case_choice_str)

            if case_choice < 1 or case_choice > 26:
                print("❌ Please choose a case between 1 and 26.")
                continue
            if case_choice == player_case:
                print("❌ You can't open your own case.")
                continue
            if case_choice not in remaining_cases:
                print("❌ This case has already been opened.")
                continue

            # Valid choice
            value = case_assignment[case_choice]
            print(f"📦 Case #{case_choice} contained ${value:,.2f}\n")
            opened_cases[case_choice] = value
            remaining_cases.remove(case_choice)
            break

    # Remaining values for banker calc
    eliminated_values = list(opened_cases.values())
    remaining_values = [v for k, v in case_assignment.items() if k not in opened_cases and k != player_case]

    # Banker offer
    expected_value = np.mean(remaining_values)
    banker_offer = round(expected_value * 0.85, 2)
    prob_higher = sum(val > banker_offer for val in remaining_values) / len(remaining_values)

    offers_history.append({
        "round": round_number,
        "offer": banker_offer,
        "expected_value": expected_value,
        "prob_higher_than_offer": prob_higher
    })

    print("📞 Banker is calling...")
    print(f"💸 Offer: ${banker_offer:,.2f}")
    print(f"📊 Expected Value: ${expected_value:,.2f}")
    print(f"📈 P(your case > offer): {prob_higher:.2%}")

    while True:
        decision = input("\nDeal or No Deal? ").strip().lower()
        if decision in ["deal", "no deal"]:
            break
        print("Please enter 'Deal' or 'No Deal'.")

    if decision == "deal":
        print(f"\n🎉 You accepted the deal: ${banker_offer:,.2f}!")
        game_over = True
        player_winnings = banker_offer
    else:
        print("🙅‍♂️ No Deal! The game continues...")
        round_number += 1

# --- Final Round ---
if not game_over:
    print("\n🏁 Final round — only your case and one other remain.")
    last_case = remaining_cases[0]
    last_case_value = case_assignment[last_case]

    print(f"\nYour case: #{player_case}")
    print(f"Remaining case: #{last_case}")

    swap = input("\nDo you want to swap your case with the remaining one? (yes/no): ").strip().lower()
    if swap == "yes":
        final_value = last_case_value
        print(f"\n🔁 You swapped! Your new case had: ${final_value:,.2f}")
    else:
        final_value = case_assignment[player_case]
        print(f"\n🎁 You kept your case. It contained: ${final_value:,.2f}")

    player_winnings = final_value

# --- Summary Report ---
print("\n" + "="*40)
print("📊 GAME SUMMARY")
print("="*40)

for offer in offers_history:
    print(f"Round {offer['round']}:")
    print(f"  - Banker's Offer: ${offer['offer']:,.2f}")
    print(f"  - Expected Value: ${offer['expected_value']:,.2f}")
    print(f"  - P(Your Case > Offer): {offer['prob_higher_than_offer']:.2%}")
    print("-" * 30)

print(f"\n🧳 Your case: #{player_case}")
print(f"💵 Your winnings: ${player_winnings:,.2f}")

max_value = max(case_values)
if player_winnings == max_value:
    print("🏆 You got the best possible outcome!")
elif player_winnings < max_value and player_winnings >= np.mean(case_values):
    print("👍 You did well!")
else:
    print("😬 You could've done better...")
