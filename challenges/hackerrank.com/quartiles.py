import random

def calculate_quartiles(arr):
    marr = sorted(arr)
    median, rem = divmod(len(marr), 2)
    if rem:
        lower = int((median-1)/2)
        q1 = marr[lower] if median % 2 else float(sum(marr[lower:lower+2]) / 2)
        q2 = marr[median]
        q3 = marr[-lower-1] if median % 2 else float(sum(marr[median+lower+1:median+lower+3]) / 2)
    else:
        lower = int((median-1)/2)
        q1 = marr[lower] if median % 2 else float(sum(marr[lower:lower+2]) / 2)
        q2 = float(sum(marr[median-1:median+1]) / 2)
        q3 = marr[-lower-1] if median % 2 else float(sum(marr[median+lower:median+lower+2]) / 2)
    print(rem,lower,marr)
    return {'Q1': q1, 'Q2': q2, 'Q3': q3}
    
# Generate five random datasets with varying sizes
datasets = []
for i in range(1,24):
  #size = random.choice([4, 6, 8, 10, 12])
  #data = list(range(1, size + 1))  # Generate elements in ascending order from 1
  data = list(range(1, i))
  datasets.append(data)

# Print results for each dataset
for i, data in enumerate(datasets):
  quartiles = calculate_quartiles(data)
  if quartiles is None:
    print(f"Dataset {i+1} ({len(data)} elements): Not enough data to calculate quartiles.")
  else:
    print(f"Dataset {i+1} ({len(data)} elements):")
    print(f"\tQ1: {quartiles['Q1']}")
    print(f"\tQ2 (Median): {quartiles['Q2']}")
    print(f"\tQ3: {quartiles['Q3']}")
  print()
