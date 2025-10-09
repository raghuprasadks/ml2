# -----------------------------------------------
# Python Program: Find-S Algorithm with User Input
# -----------------------------------------------

def find_s_algorithm(training_data):
    """
    Finds the most specific hypothesis consistent with the positive examples
    in the training data.
    """
    if not training_data:
        return "Error: No data provided."
        
    hypothesis = None 
    print("\n--- Starting Find-S Algorithm ---")
    
    for i, example in enumerate(training_data):
        attributes = list(example[:-1])
        target = example[-1].strip().upper()  # Normalize target input
        
        print(f"\nProcessing Example {i+1}: {attributes} -> {target}")

        if target == 'YES':
            if hypothesis is None:
                # Initialize H with the first positive example
                hypothesis = attributes
                print(f"  Initialized H to: {hypothesis}")
            else:
                # Generalize H to cover the new positive example
                for j in range(len(hypothesis)):
                    if hypothesis[j] != attributes[j]:
                        hypothesis[j] = '?'
                print(f"  Generalized H to: {hypothesis}")
        else:
            # Find-S ignores negative examples
            print("  Negative example: H remains unchanged.")
            
    return tuple(hypothesis)

def read_dataset_from_user():
    """Prompts the user to enter dataset instances."""
    data = []
    
    # Define the expected attributes based on the previous problem
    attributes_names = ["CGPA", "Interactiveness", "Comm. Skills", "Practical Know"]
    num_attributes = len(attributes_names)
    
    print("\n--- Enter Dataset Instances ---")
    print(f"Format: {', '.join(attributes_names)}, Job_Offer (Yes/No)")
    print("Example: >=9, Yes, Good, Good, Yes")
    print("Enter 'done' when finished.")

    while True:
        user_input = input(f"Enter instance {len(data) + 1}: ")
        if user_input.lower() == 'done':
            break

        parts = [p.strip() for p in user_input.split(',')]
        
        if len(parts) != num_attributes + 1:
            print(f"Error: Expected {num_attributes + 1} values, got {len(parts)}. Try again.")
            continue
            
        # The last part is the target (Job Offer)
        instance = tuple(parts)
        data.append(instance)

    return data

# --- Main Execution ---
user_data = read_dataset_from_user()

if user_data:
    final_hypothesis = find_s_algorithm(user_data)
    
    print("\n" + "="*50)
    print("FINAL MOST SPECIFIC HYPOTHESIS (S):")
    print(final_hypothesis)
    print("="*50)
else:
    print("Dataset is empty. Cannot run Find-S algorithm.")