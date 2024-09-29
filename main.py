import pandas as pd
import pd_explain
import warnings
from fedex_generator.Measures.ExceptionalityMeasure import ExceptionalityMeasure
warnings.filterwarnings("ignore")
adults = pd.read_csv('adult.csv')

print(type(adults))

filtered_over40 = adults.where(adults['age'] > 40)
exp_adults = pd_explain.to_explainable(adults)
measure = ExceptionalityMeasure()

measure.calc_influence(utils.max_key(scores), top_k=top_k, figs_in_row=figs_in_row,
                                         show_scores=show_scores, title=title)
filtered_over40.explain()
filtered_over40.operation.explain()
print("nothing")
filtered_over40.explain(attributes=['age'])

