# rmpdataanalysis.py
# Functions to analyze RateMyProfessors data.
# For CS 1400, written by CS1400 course staff.
# Functions implementations by [your name here]

"""
read a file and return a list of data lines as a string

:param filename: str filename
:return list of strings
"""
def get_lines_from_file(filename):
    lines = []
    with open(filename, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    # Skip header if file has at least one line
    if len(all_lines) <= 1:
        return []
    # Return the remaining lines (keep newline characters consistent with starter examples)
    return all_lines[1:]

"""
filter a list for a specific gender

:param lines
:param target_gender
:return list of lists
"""
def get_reviews_for_gender(lines, target_gender):
    results = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        # split into at most 3 parts (in case the comment contains commas)
        parts = s.split(',', 2)
        # If we somehow don't get 3 parts, skip the line
        if len(parts) != 3:
            continue
        rating_str, gender_str, comment = parts
        gender_str = gender_str.strip()
        if gender_str == target_gender:
            results.append([rating_str.strip(), gender_str, comment.strip()])
    return results

"""
convert a score into one of 3 categories (< 2.5 is low, 1-2.5 is medium, and 2-3.5 is high)
:param score: numeric rating
:return: integer categoy 0, 1, 2
"""
def categorize_reviews(score):
    try:
        f = float(score)
    except Exception:
        f = 3.0
    if f < 2.5:
        return 0
    if 2.5 <= f <= 3.5:
        return 1
    return 2

"""
calculate teh percentage of reviews in 'reviews' that fall into given target_rating_category

:param reviews: list of lists
:param target_rating_category: int 0, 1, or 2
:return: rounded integer percentage of reviews in that category
"""
def calculate_rating_stats(reviews, target_rating_category):
    if not reviews:
        return 0
    count = 0
    total = 0
    for r in reviews:
        # Expect r[0] to be rating
        if len(r) == 0:
            continue
        total += 1
        if categorize_reviews(r[0]) == target_rating_category:
            count += 1
    if total == 0:
        return 0
    percent = (count / total) * 100
    return round(percent)


"""
add observations of 'word' with the given review 'score' to map the data. 

:param word_data: dict mapping str->list of three ints
:param word: str single token
:param score: numeric or numeric-string rating
:return: None
 """
def add_data_for_word(word_data, word, score):
    category = categorize_reviews(score)
    if word not in word_data:
        word_data[word] = [0, 0, 0]
    word_data[word][category] += 1

"""
Build a dictionary mapping words from a list of reviews for a single gender

:param review_data: list of [rating, gender, comment]
:return: dictionary word_data
"""
def format_to_dict(review_data):
    word_data = {}
    for review in review_data:
        if len(review) < 3:
            continue
        rating = review[0]
        comment = review[2]
        # split on whitespace to get tokens (comments are already lowercased/cleaned per dataset)
        words = comment.split()
        for w in words:
            if w == '':
                continue
            add_data_for_word(word_data, w, rating)
    return word_data

"""
return a list of words in word_dict with target_string as a substring

:param word_dict
:param target_string
:param list of matching words
"""
def search_words(word_dict, target_string):
    matches = []
    if target_string is None:
        return matches
    for word in word_dict.keys():
        if target_string in word:
            matches.append(word)
    return matches


def main():
    # Interpretation note:
    # To get the true numbers for the full dataset, uncomment the line that reads full-data.txt
    # and run this program. Compare the printed percentages for rating categories (0=low,1=med,2=high)
    # between genders. If you see a consistent multi-point difference in the same category
    # (e.g., men have substantially more "high" reviews than women), that suggests a possible
    # difference worth investigating further.
    #
    # (I left the above as a guidance comment rather than hard-coded percentages because
    #  the percentages should be computed by running the program on full-data.txt locally.)

    # Read the lines
    reviews = get_lines_from_file('small-data.txt')
    print("small-data lines:", reviews)  # examine the result
    # reviews = get_lines_from_file('full-data.txt') # uncomment this when you are ready to try the full set of reviews.

    # Get reviews for genders
    women_reviews = get_reviews_for_gender(reviews, 'W')
    print("women_reviews:", women_reviews)  # examine the result to see if it looks correct
    men_reviews = get_reviews_for_gender(reviews, 'M')
    print("men_reviews:", men_reviews)  # examine the result to see if it looks correct

    # analysis of rating stats per gender
    genders = ['W', 'M']
    rating_categories = [0, 1, 2]
    for gender in genders:
        for rating_category in rating_categories:
            data = get_reviews_for_gender(reviews, gender)
            rating = calculate_rating_stats(data, rating_category)
            print(str(rating) + '% of the reviews for', gender, 'are in rating category', rating_category,
                  '(0 = low, 1 = med, 2 = high)')

    # Format to dictionary
    women_dict = format_to_dict(women_reviews)
    print("women_dict:", women_dict)  # examine the dict to see if it looks correct
    men_dict = format_to_dict(men_reviews)
    print("men_dict:", men_dict)  # examine the dict to see if it looks correct

    # Ask the user for a word and rating category
    word = input('What word would you like to search? ')
    category = int(input('For which rating category (0 = low, 1 = med, 2 = high)? '))

    women_count_for_word = women_dict.get(word, [0, 0, 0])[category]
    men_count_for_word = men_dict.get(word, [0, 0, 0])[category]

    print("This word appears in women's reviews", women_count_for_word, "time(s) for this rating category.")
    print("This word appears in men's reviews", men_count_for_word, "time(s) for this rating category.")


if __name__ == '__main__':
    main()
