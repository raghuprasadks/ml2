# -----------------------------------------------------
# Python Program: Candidate Elimination Algorithm
# -----------------------------------------------------

# Global definition for the maximum hypothesis length 
# (Based on your previous problem: 4 features + 1 target)
NUM_FEATURES = 4 

def is_consistent(h, x_attributes):
    """Checks if hypothesis h is consistent with the example's attributes."""
    for i in range(len(h)):
        # If hypothesis has a specific value that doesn't match the example, it's inconsistent.
        if h[i] != '?' and h[i] != x_attributes[i]:
            return False
    return True

def is_more_general_than(h1, h2):
    """Checks if hypothesis h1 is more general than h2 (h1 covers h2)."""
    # h1 is more general if for every attribute, h1's value is either '?' or matches h2's value.
    for i in range(len(h1)):
        # If h1 is specific (not '?') and h1 doesn't match h2, h1 is NOT more general than h2.
        if h1[i] != '?' and h1[i] != h2[i]:
            return False
    return True

def get_minimal_generalizations(h, x):
    """Generates a minimal generalization of h that covers x."""
    new_h = list(h)
    for i in range(len(new_h)):
        if new_h[i] == '∅':
            new_h[i] = x[i]
        elif new_h[i] != '?' and new_h[i] != x[i]:
            new_h[i] = '?'
    return tuple(new_h)

def get_minimal_specializations(g, x, DOMAIN):
    """Generates a set of minimal specializations of g that exclude x."""
    specializations = set()
    
    for i in range(len(g)):
        if g[i] == '?':
            # Specialize by restricting the '?' to a value in the domain 
            # that is NOT the value in the negative example x.
            for val in DOMAIN[i]:
                if val != x[i]:
                    g_specialize = list(g)
                    g_specialize[i] = val
                    specializations.add(tuple(g_specialize))
                    
    return specializations


def candidate_elimination(training_data, DOMAIN):
    """
    Applies the Candidate Elimination Algorithm.
    """
    # Initialize S and G
    S = {('∅',) * NUM_FEATURES} # Most Specific: Requires exact match on nothing
    G = {('?',) * NUM_FEATURES} # Most General: Covers everything

    print(f"\nH0: S = {S} | G = {G}")

    for i, example in enumerate(training_data):
        attributes = example[:-1]
        target = example[-1].strip().upper()
        
        print(f"\n--- Processing Example {i+1}: {attributes} -> {target} ---")

        if target == 'YES':
            # Case 1: Positive Example
            
            # 1. Eliminate hypotheses in G inconsistent with the positive example
            G = {g for g in G if is_consistent(g, attributes)}
            
            # 2. Generalize S to cover the positive example (and prune non-maximally specific)
            S_new = set()
            for s in S:
                if not is_consistent(s, attributes):
                    # If s is inconsistent, generalize it
                    s_generalized = get_minimal_generalizations(s, attributes)
                    
                    # Ensure the new s is still more specific than some g in G
                    if any(is_more_general_than(g, s_generalized) for g in G):
                         S_new.add(s_generalized)
                else:
                    S_new.add(s) # Keep consistent S hypotheses

            # Prune S: Remove hypotheses that are more general than another hypothesis in S_new
            S_final = set()
            for h_i in S_new:
                if not any(is_more_general_than(h_j, h_i) for h_j in S_new if h_i != h_j):
                    S_final.add(h_i)
            S = S_final
            

        else: # target == 'NO' (Negative Example)
            # 1. Eliminate hypotheses in S inconsistent with the negative example
            S = {s for s in S if not is_consistent(s, attributes)}

            # 2. Specialize G to exclude the negative example (and prune non-maximally general)
            G_new = set()
            for g in G:
                if is_consistent(g, attributes):
                    # If g is inconsistent (predicts 'Yes' for a 'No' example), specialize it
                    specializations = get_minimal_specializations(g, attributes, DOMAIN)
                    for g_specialize in specializations:
                        # Ensure the specialization is more general than some s in S
                        if any(is_more_general_than(g_specialize, s) for s in S):
                            G_new.add(g_specialize)
                else:
                    G_new.add(g) # Keep consistent G hypotheses

            # Prune G: Remove hypotheses that are less general than another hypothesis in G_new
            G_final = set()
            for h_i in G_new:
                if not any(is_more_general_than(h_i, h_j) for h_j in G_new if h_i != h_j):
                    G_final.add(h_i)
            G = G_final
            
        print(f"H{i+1}: S = {sorted(list(S))} | G = {sorted(list(G))}")
        
    return S, G

def read_dataset_from_user():
    """Prompts the user to enter attribute domains and dataset instances."""
    
    attributes_names = ["CGPA", "Interactiveness", "Comm. Skills", "Practical Know"]
    
    # 1. Define the DOMAIN based on user's known data structure
    DOMAIN = [
        {'>=9', '<9'},            # CGPA
        {'Yes', 'No'},            # Interactiveness
        {'Good', 'Moderate'},     # Communication Skills
        {'Good', 'Average'}       # Practical Knowledge
    ]

    print("\n--- Enter Dataset Instances (4 Features + Target) ---")
    print(f"Expected Features: {', '.join(attributes_names)}")
    print("Example: >=9, Yes, Good, Good, Yes")
    print("Enter 'done' when finished.")

    data = []
    while True:
        user_input = input(f"Enter instance {len(data) + 1}: ")
        if user_input.lower() == 'done':
            break

        parts = [p.strip() for p in user_input.split(',')]
        
        if len(parts) != NUM_FEATURES + 1:
            print(f"Error: Expected {NUM_FEATURES + 1} values, got {len(parts)}. Please re-enter.")
            continue
            
        data.append(tuple(parts))

    return data, DOMAIN

# --- Main Execution ---
user_data, user_domain = read_dataset_from_user()

if user_data:
    S_final, G_final = candidate_elimination(user_data, user_domain)
    
    print("\n" + "="*70)
    print("FINAL VERSION SPACE BOUNDARIES")
    print("="*70)
    print(f"Most Specific Hypothesis Set (S): {sorted(list(S_final))}")
    print(f"Most General Hypothesis Set (G):  {sorted(list(G_final))}")
    print("="*70)
    
    if S_final == G_final and len(S_final) == 1:
        print("\nCONVERGED: The Version Space contains a single consistent hypothesis.")
        print(f"The unique hypothesis is: {list(S_final)[0]}")
    elif len(S_final) > 0 and len(G_final) > 0:
        print("\nVersion Space Found: Multiple hypotheses exist between S and G.")
    else:
        print("\nVersion Space is Empty: The dataset is inconsistent.")
else:
    print("Dataset is empty. Cannot run the Candidate Elimination algorithm.")