import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    #directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    directory = "small"
    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    
    source = "144"
    #source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    #target = person_id_for_name(input("Name: "))
    target = "129"
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    print ("We got..", path)
    ### TODO ===
    # tratar lista de movies y organizar,
    # person 1 y perons 2, 
    # Ver porque no retorna otras persona
    # incluir movies ID en shortes-path? está memso epxloranod ids de movies?
    #
    
    if path is None:
        print("Not connected.")
    else:
        print( people[source]["name"], " and ", people[target]["name"], " have ",len (path[0]), "degrees of separation.")
        print("Length of path:", len(path[0]))
        
        moviesActorsList =([None]+path[0],[source]+path[1])
        
        print ("Now we have..", moviesActorsList)
        '''
        for i in range(len(moviesActorsList)):
            person1 = people[moviesActorsList[i][0]]["name"]  # Access the first element of each tuple
            person2 = people[moviesActorsList[i + 1][0]]["name"]  # Access the first element of the next tuple
            movie = movies[moviesActorsList[i + 1][1]]["title"]  # Access the second element of the next tuple
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

        
        '''   
        path =moviesActorsList
        print(" person1 = ", people[path[1][0]]["name"]," <")
        print(" movie = ", movies[path[0][1]]["title"]," <")
       
        for i in range(len(path[0])-1):
            person1 = people[path[1][i]]["name"]
            person2 = people[path[1][i+1]]["name"]
            movie = movies[path[0][i+1]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")
        #'''        


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # Keep track of number of states explored
    num_explored = 0
    node_start = Node(source, parent=None, action=None)
    frontier = StackFrontier()
    frontier.add(node_start)
    # Initialize an empty explored set
    explored = set()

    # Keep looping until solution found
    while True:

        # If nothing left in frontier, then no path
        if frontier.empty():
            raise Exception("no solution")

        # Choose a node from the frontier
        node = frontier.remove()
        num_explored += 1

        # If node is the goal, then we have a solution
        if node.state == target:
            actions = []
            cells = []
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            solution = (actions, cells)
            return solution

        # Mark node as explored
        explored.add(node.state)

        # Add neighbors to frontier
        for action, state in neighbors_for_person(node.state):
            if not frontier.contains_state(state) and state not in explored:
                child = Node(state=state, parent=node, action=action)
                frontier.add(child)


    # TODO    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
