path = 'data.csv'
num_steps = 3
template = """Report
We have made {} observations from tossing a coin: {} of them were tails and {} of
them were heads. The probabilities are {:.2f}% and {:.2f}%, respectively. Our
forecast is that in the next {} observations we will have: {} tail and {} heads.
"""
output_file = 'report'
