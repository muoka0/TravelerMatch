from sqlalchemy.orm import Session
from db.queries.write import insert_destinations, insert_interests

def _load_data(path: str):
    with open(path, "r") as f:
        json_data = json.load(f)
    
    return json_data

def seed_destinations(db_session: Session, path="data/destinations.json"):
    destinations = _load_data(path)

    # we need to unpack the json to make it compatible with the insert_destinations function
    for country in destinations:
        country_name = country["country"]

        for city in country["data"]:
            destination_data = {
                "country": country_name,
                "city": city["city"],
                "climate": city["climate"],
                "budget_level": city["budget_level"]
            }

            insert_destinations(db_session, destination_data)

def seed_interests(db_session: Session, path="data/interests.json"):
    interests = _load_data(path)

    for interest in interests:
        insert_interests(db_session, interest)

def seed_destination_interests(db_session: Session, path="data/destination_interests.json"):
    destination_interests = _load_data(path)

    # build lookup map for interests
    interest_map = {
        row.name: row.id for row in db_session.query(Interest).all()
    }

    # build lookup for destinations
    destination_map = {
        (destination.country, destination.city): destination.id 
        for destination in db_session.query(Destination).all()
    }

    # build relationships
    for record in destination_interests:
        country = record["country"]
        city = record["city"]

        destination_id = destination_map[(country, city)]

        for interest_name in record["interests"]:
            interest_id = interest_map[interest_name]

            session.add(DestinationInterest(
                destination_id=destination_id,
                interest_id=interest_id
            ))
    
    session.commit()