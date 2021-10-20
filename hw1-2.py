import sys

"""
authors: Nicolas Ku
         Agni Patel
"""

"""
Task 1 PART 1
Write a function read_ratings_data(f) that takes in a ratings file, and returns a dictionary. The dictionary should have movie as key, and the corresponding list of ratings as value.

For example:   movie_ratings_dict = { "The Lion King (2019)" : [6.0, 7.5, 5.1], "Titanic (1997)": [7] }
"""
def read_ratings_data(f) -> dict:
    try:
        movie_ratings = {}
        file = open(f)
        for line in file:
            movie,ratings,movie_id = line.split('|')
            if(movie.strip() in movie_ratings):
                movie_ratings[movie.strip()].append(ratings.strip())
            else:
                movie_ratings[movie.strip()] = [ratings.strip()]
        return movie_ratings
    except:
        return ("The value of the file is invalid")

"""
TASK 1 PART 2
Write a function read_movie_genre(f) that takes in a movies file and returns a dictionary. The dictionary should have a one-to-one mapping between movie and genre.  
For example   { "Toy Story (1995)" : "Adventure", "Golden Eye (1995)" : "Action" }   
"""
def read_movie_genre(f):
    try:
        movie_genres = {}
        file = open(f)
        for line in file:
            genre,movie_id,movie = line.split('|')
            movie_genres[movie.strip()] = genre.strip()
        return movie_genres
    except:
        return("The file or its content is invalid")
    
#---------------------------------------------------------------------------------    
"""
TASK 2 PART 1
Write a function create_genre_dict that takes as a parameter a movie-to-genre dictionary, of the kind created in Task 1.2.
The function should return another dictionary in which a genre is mapped to all the movies in that genre.

For example: { Adventure: [Toy Story, Jumanji, Adventures of Tom], Action: [Heat, James Bond]}
"""
def create_genre_dict(genre_dict):
    genres_movies = {}
    for movie,genre in genre_dict.items():
        if genre in genres_movies:
            genres_movies[genre].append(movie)
        else:
            genres_movies[genre] = [movie]
    return genres_movies
       
"""
TASK 2 PART 2
Write a function calculate_average_rating that takes as a parameter a ratings dictionary, of the kind created in Task 1.1. It should return a dictionary where the movie is mapped to its average rating computed from the ratings list.

For example:   {"Spider-Man (2002)": [3,2,4,5]}  ==>   {"Spider-Man (2002)": 3.5}
    3/1 = 3, 5/2 = 3.5 9/3 =3 14/4 = 3.5
"""
def calculate_average_rating(ratings_dict):
    average_ratings = {}
    for movie,ratings in ratings_dict.items():
        total_ratings = [(float(i)) for i in ratings]
        average_ratings[movie] = round(sum(total_ratings)/len(ratings),2)
    return average_ratings

#---------------------------------------------------------------------------------
"""
TASK 3 PART 1 
Write a function get_popular_movies that takes as parameters a dictionary of movie-to-average rating ( as created in Task 2.2), and an integer n (default should be 10). The function should return a dictionary ( movie:average rating, same structure as input dictionary) of top n movies based on the average ratings. (If there are fewer movies than n, it should all return all movies in order of top average ratings.)
"""
def get_popular_movies(movie_dict, n = 10):
    top_movies = {}
    if len(movie_dict) <= n:
        top_movies = dict(sorted(movie_dict.items(),key=lambda movie: 
                            movie[1],reverse=True))
        return top_movies
    i = 0
    for movie,rating in sorted(movie_dict.items(),key=lambda movie: 
                               movie[1],reverse=True):
        if i < n:  
            top_movies[movie] = rating
            i+=1
    return top_movies        
"""
TASK 3 PART 2
Write a function filter_movies that takes as parameters a dictionary of movie-to-average rating (same as for the popularity based function above), and a threshold rating with default value of 3. The function should filter movies based on the threshold rating, and return a dictionary with same structure as the input. For example, if the threshold rating is 3.5, the returned dictionary should have only those movies from the input whose average rating is equal to or greater than 3.5.
"""
def filter_movies(movie_dict, threshold = 3):
    filtered_movies = {}
    for movie,rating in movie_dict.items():
        if(rating >= threshold):
            filtered_movies[movie] = rating
        else:
            continue
    return filtered_movies   

"""
TASK 3 PART 3

Write a function get_popular_in_genre that, given a genre, a genre-to-movies dictionary (as created in Task 2.1), a dictionary of movie:average rating (as created in Task 2.2), and an integer n (default 5), returns the top n most popular movies in that genre based on the average ratings. The return value should be a dictionary of movie-to-average rating of movies that make the cut. Genre categories will be from those in the movie:genre dictionary created in Task 1.2. Your code should handle the case when there are fewer than n movies in the data, as in Task 3.1 above.
"""
def get_popular_in_genre(genre,genre_movies, avg_dict, n = 5):
    popular_genre = {}
    temp_movies = []
    for dict_gen,movies in genre_movies.items():
        if(genre == dict_gen):
            temp_movies = movies
        else:
            continue
    #forget about the top n, just find all movies in temp_movies
    if len(temp_movies) <= n:
        for movie,avg in avg_dict.items():
            if(movie in temp_movies):
                popular_genre[movie] = avg
        return dict(sorted(popular_genre.items(),key=lambda movie: 
                            movie[1],reverse=True))
    i = 0
    for movie,rating in sorted(avg_dict.items(),key=lambda movie: 
                               movie[1],reverse=True):
        if i < n and movie in temp_movies:  
            popular_genre[movie] = rating
            i+=1
    return popular_genre

"""
TASK 3 PART 4

One important analysis for the content platforms is to determine ratings by genre.

Write a function get_genre_rating that takes the same parameters as get_popular_in_genre above, except for n, and returns the average rating of the movies in the given genre.
so gets the average of all the movies ratings. we have a map of the movie->avg, so we take every avg in that list and calculate it
"""
def get_genre_rating(genre,genre_movies, avg_dict):
    genre_rate = 0
    count = 0
    temp_movies = []
    for dict_gen, movies in genre_movies.items():
        if(genre == dict_gen):
            temp_movies = movies
    for movie,avg in avg_dict.items():
        if movie in temp_movies:
            count+=1
            genre_rate += float(avg)
    if count == 0:
        return 0.0
    return (genre_rate/count)
    
"""
TASK 3 PART 5

Write a function genre_popularity that takes as parameters a genre-to-movies dictionary (as created in Task 2.1), a movie-to-average rating dictionary (as created in Task 2.2), and n (default 5), and returns the top-n rated genres as a dictionary of genre:average rating. Hint: Use the above get_genre_rating function as a helper.

use get_genre_rating to get rating for genre, so genre-> num(avg)
"""
def genre_popularity(genre_movies,avg_dict,n=5):
    top_n_genres = {}
    genre_list = {}
    for genre,_ in genre_movies.items():
        genre_list[genre] = (get_genre_rating(genre,genre_movies,avg_dict))
    #uses genre as the movie label but performs the same function
    top_n_genres = dict(get_popular_movies(genre_list,n))
    return top_n_genres
    
#-------------------------------------------------------------------------
"""
TASK 4 PART 1

Read the ratings file to return a user-to-movies dictionary that maps user ID to the associated movies and the corresponding ratings. Write a function named read_user_ratings for this, with the ratings file as the parameter.

For example: { u1: [ (m1, r1), (m2, r2) ], u2: [ (m3, r3), (m8, r8) ] }
where ui is user ID, mi is movie, ri is corresponding rating.
"""
def read_user_ratings(file):
    f = open(file)
    user_movies = {}
    for line in f:
        movie,ratings,u_id = line.split('|')
        if(int(u_id) in user_movies):
            user_movies[int(u_id)].append((movie,ratings))
        else:
            user_movies[int(u_id)] = [(movie,ratings)]
    #does not have to be sorted but easier to debug every user is in dict
    user_movies = dict(sorted(user_movies.items(), key=lambda uid:uid[0]))
    return user_movies

"""
TASK 4 PART 2
Write a function get_user_genre that takes as parameters a user id, the user-to-movies dictionary (as created in Task 4.1 above), and the movie-to-genre dictionary (as created in Task 1.2), and returns the top genre that the user likes based on the user's ratings.

Here, the top genre for the user will be determined by taking the average rating of the movies genre-wise that the user has rated
"""
def get_user_genre(uid,user_movies,movie_genre):
    #get all the movies the user likes
    #get genre_rating
    genre_rating = {}
    if(uid in user_movies.keys()):
        movie_rating = dict(user_movies[uid])
        #print(movie_rating)
        #print(movie_genre)
        genres_movies = create_genre_dict(movie_genre)
        #print(genres_movies)
        for genre,movie in genres_movies.items():
            genre_rating[genre] = get_genre_rating(genre,genres_movies,movie_rating)
        #print(genre_rating)
    else:
        return
    return max(genre_rating, key = genre_rating.get)


"""
TASK 4 PART 3
Recommend 3 most popular (highest average rating) movies from the user's top genre that the user has not yet rated. Write a function recommend_movies for this, that takes a parameters a user id, the user-to-movies dictionary (as created in Task 4.1 above), the movie-to-genre dictionary (as created in Task 1.2), and the movie-to-average rating dictionary (as created in Task 2.2). The function should return a dictionary of movie-to-average rating. (Return all if fewer than 3 movies make the cut.)
"""
def recommend_movies(uid,user_movies,movie_genre,movie_avg):
    top_genre = get_user_genre(uid,user_movies,movie_genre)
    gender_movies = create_genre_dict(movie_genre)
    #Adventure for ex, user 5 has only seen Toy Story so its top category
    #recommend jumanji,tom and huck
    count = 0
    current_pop = dict(get_popular_in_genre(top_genre,gender_movies,movie_avg))
    for movie,_ in list(current_pop.items()):
        if movie in dict(user_movies[uid]).keys():
            current_pop.pop(movie,'None')  
    if(len(current_pop) > 3):
        while len(current_pop) !=3 :
            current_pop.popitem()
  
    return current_pop
   

#----------------------------------------------------------------------------

def main():
    args = len(sys.argv)
    #The if statement will change once we add more methods since 
    #we will need 3 arguments and the file name could be anything. 

    ratings_dict = read_ratings_data('movieRatingSample.txt')
    movie_genre = read_movie_genre('genreMovieSample.txt')
    avg_movie = calculate_average_rating(ratings_dict)
    
    if(args == 2 and sys.argv[1] == 'movieRatingSample.txt'):
        f = sys.argv[1]
        ratings_dict = read_ratings_data(f)
#         print(ratings_dict)
#         print()
        average_movies = calculate_average_rating(ratings_dict)
        print(average_movies)
        print()
        print(avg_movie)
#         print(filter_movies(average_movies))
    elif(args == 2 and sys.argv[1] == 'genreMovieSample.txt'):
        f = sys.argv[1]
        genre_dict = read_movie_genre(f)
        #print(read_movie_genre(f))
#         print()
        print(create_genre_dict(genre_dict))
    elif(args == 2 and sys.argv[1] == 'get_popular_movies'):
#         print(avg_movie)
#         print()
        #print(filter_movies(avg_movie,4.0))
#         genre_to_movie = create_genre_dict(movie_genre)
        avg_movie = calculate_average_rating(ratings_dict)
#         print(avg_movie)
        genre_movie = create_genre_dict(movie_genre)
#         print(genre_movie)
#         print()
#         print(get_genre_rating('Adventure',genre_movie,avg_movie))
        print(genre_popularity(genre_movie,avg_movie,3))
    elif(args == 2 and sys.argv[1] == 'genre_popularity'):
        print(genre_popularity(genre_dict, avg_dict,2))
    elif(args == 3 and sys.argv[1] == 'read_user_ratings'):
        file = sys.argv[2]
        user = 3
        user_movies = read_user_ratings(file)
        #print(user_movies)
        movie_to_genre = read_movie_genre('genreMovieSample.txt')
        
        
        #print(get_user_genre(user,user_movies,movie_to_genre))
        print(recommend_movies(user,user_movies,movie_to_genre,avg_movie))
        
        #print(read_user_ratings(file))
        
    else:
        print("Wrong number of args or wrong file")
         
    
    

