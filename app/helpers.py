from app.models import Movie


def calculate_loyalty_points(reservation):
    points = len(reservation.seats.split(',')) * 10
    return points

def recommend_movies(user):
    user_ratings = {rating.movie_id: rating.rating for rating in user.ratings}
    all_movies = Movie.query.all()
    recommendations = []
    for movie in all_movies:
        if movie.id not in user_ratings:
            movie_avg_rating = movie.average_rating()
            if movie_avg_rating and movie_avg_rating >= 3.0:  # przykładowy próg oceny
                recommendations.append(movie)
    return recommendations

def recommend_movies(user):
    all_movies = Movie.query.all()
    rated_movies_ids = [rating.movie_id for rating in user.ratings]
    unrated_movies = [movie for movie in all_movies if movie.id not in rated_movies_ids]
    recommended_movies = sorted(unrated_movies, key=lambda movie: movie.average_rating(), reverse=True)
    return recommended_movies[:5]