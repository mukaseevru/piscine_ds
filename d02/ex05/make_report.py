from config import *
from analytics import Research


def main():
    research = Research(path)
    heads, tails = research.analytics.counts(research.data)
    heads_probability, tails_probability = research.analytics.fractions([heads, tails])
    predict_random = research.analytics.predict_random(num_steps)
    heads_predict, tails_predict = tuple(sum(elem) for elem in zip(*predict_random))
    text = template.format(len(research.data), heads, tails, heads_probability, tails_probability,
                           num_steps, heads_predict, tails_predict)
    research.analytics.save_file(text, output_file)


if __name__ == '__main__':
    main()
