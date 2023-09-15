import os

def count_exact_common_words(string1, string2):
    # Split the strings into sets of words
    words1 = set(string1.split())
    words2 = set(string2.split())

    # Find the common words by taking the intersection of the sets
    common_words = words1.intersection(words2)

    return len(common_words)

def create_absolute_path(file_name):

    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    data_dir = os.path.join(script_dir, '../data')  # Construct the path to the "data" directory
    file_path = os.path.abspath(os.path.join(data_dir, file_name))
    return file_path

def count_accuracy(file_contents,chatbot_response):
    total_word_count = len(file_contents.split(' '))
    same_word_count = count_exact_common_words(file_contents, chatbot_response)
    accuracy = same_word_count/total_word_count*100

    #print("Result: ", result[1])
    #print("\nAccuracy: {:.2f}".format(accuracy))

    return accuracy

# Example usage:



