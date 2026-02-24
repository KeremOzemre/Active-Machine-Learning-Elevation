import src.retriever as retriever

def test_retriever():
    result = retriever.request_elevation_area((54, 8), (58, 15), 10)
    print(result)

def get_location():
    result = retriever.request_location(55.776345, 12.615981) # nederst til højre
    print(result)
    result = retriever.request_location(55.820256, 12.505247) # øverst til venstre
    print(result)

    # (55.776345, 12.505247), (55.820256, 12.615981)

def save_data():
    start = (54.963728, 14.688672) # (55.776345, 12.505247)
    end = (55.327825, 15.181072) # (55.820256, 12.615981)
    samples = retriever._BATCH_SIZE * 2000
    retriever.save_data_file(start, end, samples)

if __name__ == '__main__':
    save_data()