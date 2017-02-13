import sys, os
from preprocess import process_data_file
from presenters import main
from nominees import findnominees
from award_winners import find_award_winners
from sentiment_analysis import get_sentiment

def usage_message():
    print("usage:")
    print("python nlp.py -nominees <path/to/tab/file>")
    print("python nlp.py -winner <path/to/tab/file>")
    print("python nlp.py -presenters <path/to/tab/file>")


if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) == 2:

        # if we haven't preprocessed do so
        if not(os.path.isfile('data_preprocessed.p')):
            process_data_file(args[1])

        if args[0] == "-nominees":
            print("Nominees: ", findnominees())
            exit()
        elif args[0] == "-winner":
            print("Find winners")
            find_award_winners()
            exit()
        elif args[0] == "-presenters":
            print("Presenter: ", main())
            exit()
        elif args[0] == "-sentiment":
            filter_word = args[1]
            get_sentiment(filter_word)        
            exit()

    usage_message()
