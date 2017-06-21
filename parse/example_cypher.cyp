CREATE (n:Person {name:"bill"})-[:HATES {when:"now"}]->(m)

CREATE (n:Person {name:"Billy"})-[:FRIENDS]->(m:Person {name:"Matt"})
